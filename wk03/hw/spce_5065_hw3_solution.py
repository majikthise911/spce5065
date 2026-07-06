"""SPCE 5065 -- Homework 3 figure generator (bioastronautics / human factors).

HW3 is a conceptual assignment, so this script does no physics; it just builds
the three support figures referenced in the submission:

  fig1  Habitable volume per crew member vs. mission duration (Q4)
        Celentano-style tolerable / performance / optimal bands with my
        recommended Mars-phase volumes marked.
  fig2  SHELL human-factors model schematic (first used in Q6, reused in Q9)
  fig3  Weighted trade-study scores for the eight mass-allocation options (Q8)

Figures are numbered by first appearance in the submission.

Run: python spce_5065_hw3_solution.py  -> writes PNGs to ./figures/
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

FIG_DIR = Path(__file__).parent / "figures"


def _caption(fig, text: str) -> None:
    fig.text(0.5, 0.005, text, ha="center", va="bottom", fontsize=8.5,
             style="italic")


# --------------------------------------------------------------------------
# Fig 1 -- Habitable volume vs mission duration (Q4)
# --------------------------------------------------------------------------
def fig_habitable_volume() -> None:
    # Celentano-style asymptotic curves: volume/person rises with duration and
    # levels off. Values anchored to lecture (tolerable ~5, optimal ~17 m^3)
    # and the NASA HIDH long-duration optimal (~19-20 m^3).
    d = np.linspace(0, 700, 400)                     # mission days
    tol = 5.0 * (1 - np.exp(-d / 40.0)) + 1.0        # tolerable band -> ~5-6
    perf = 10.0 * (1 - np.exp(-d / 60.0)) + 1.5      # performance band -> ~10
    opt = 19.0 * (1 - np.exp(-d / 80.0)) + 2.0       # optimal band -> ~19

    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    ax.plot(d, tol, color="#c0392b", lw=2, label="Tolerable (survivable)")
    ax.plot(d, perf, color="#e67e22", lw=2, label="Performance")
    ax.plot(d, opt, color="#27ae60", lw=2, label="Optimal")
    ax.fill_between(d, opt, perf, color="#27ae60", alpha=0.06)

    # my three Mars-phase recommendations
    recs = [("Outbound\ntransit", 210, 20.0, (14, -30)),
            ("Surface", 500, 25.0, (12, 12)),
            ("Return\ntransit", 210, 22.0, (-58, 24))]
    for lab, day, vol, off in recs:
        ax.plot(day, vol, "o", color="#2c3e50", ms=7, zorder=5)
        ax.annotate(f"{lab}\n{vol:.0f} m$^3$/person",
                    xy=(day, vol), xytext=off, textcoords="offset points",
                    fontsize=8, ha="center",
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6",
                              alpha=0.95),
                    arrowprops=dict(arrowstyle="->", color="0.5"))

    ax.set_xlabel("Mission phase duration (days)")
    ax.set_ylabel("Habitable volume per crew member (m$^3$)")
    ax.set_title("Q4: Recommended habitable volume vs. mission duration")
    ax.set_xlim(0, 700)
    ax.set_ylim(0, 28)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right", fontsize=8)
    fig.subplots_adjust(bottom=0.17)
    _caption(fig, "Figure 1: Habitability bands (Celentano-style) level off with "
             "duration; my Mars-phase picks sit at/above the optimal asymptote.")
    fig.savefig(FIG_DIR / "fig1_habitable_volume.png", dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------
# Fig 2 -- Trade-study weighted scores (Q8)
# --------------------------------------------------------------------------
def fig_trade_study() -> None:
    # criteria weights
    w = np.array([0.30, 0.20, 0.20, 0.15, 0.15])   # survival, physio, psych, red-cover, mass-eff
    options = {
        "Radiation shielding":       [5, 1, 2, 5, 2],
        "Exercise equipment":        [3, 5, 4, 3, 4],
        "Food variety":              [2, 2, 5, 3, 4],
        "Medical equipment":         [5, 2, 2, 5, 3],
        "Private crew quarters":     [2, 1, 5, 4, 3],
        "Water reserves":            [3, 1, 1, 2, 2],
        "Artificial-gravity demo":   [2, 3, 1, 2, 1],
        "Additional science eqpt.":  [1, 1, 2, 1, 2],
    }
    names = list(options.keys())
    scores = np.array([np.dot(w, options[n]) for n in names])
    order = np.argsort(scores)                     # ascending for barh
    names_s = [names[i] for i in order]
    scores_s = scores[order]
    # top 3 (highest three) get highlighted
    top3_cut = np.sort(scores)[-3]
    colors = ["#27ae60" if s >= top3_cut else "#7f8c8d" for s in scores_s]

    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    ax.barh(names_s, scores_s, color=colors, edgecolor="0.3")
    for y, s in enumerate(scores_s):
        ax.text(s + 0.03, y, f"{s:.2f}", va="center", fontsize=8.5)
    ax.set_xlabel("Weighted trade-study score (1 = poor, 5 = excellent)")
    ax.set_title("Q8: Weighted scores, 1,500 kg Mars crew-health allocation")
    ax.set_xlim(0, 4.3)
    ax.grid(True, axis="x", alpha=0.3)
    green = mpatches.Patch(color="#27ae60", label="Selected (top 3)")
    grey = mpatches.Patch(color="#7f8c8d", label="Not selected")
    ax.legend(handles=[green, grey], loc="lower right", fontsize=8)
    fig.subplots_adjust(left=0.30, bottom=0.15)
    _caption(fig, "Figure 3: Weighted scores rank exercise, medical, and "
             "radiation shielding as the top three; food variety just misses.")
    fig.savefig(FIG_DIR / "fig3_trade_study.png", dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------
# Fig 3 -- SHELL model schematic (Q6 / Q9)
# --------------------------------------------------------------------------
def fig_shell_model() -> None:
    fig, ax = plt.subplots(figsize=(7.0, 5.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    blocks = {
        "S\nSoftware\n(procedures,\nchecklists, rules)": (5, 8.0, "#5dade2"),
        "H\nHardware\n(vehicle, suits,\ntools, ECLSS)":   (2.0, 5, "#f5b041"),
        "E\nEnvironment\n(microgravity,\nradiation, workload)": (8.0, 5, "#58d68d"),
        "L\nLiveware-Liveware\n(crew, ground,\nfamily)":  (5, 2.0, "#bb8fce"),
    }
    for label, (x, y, c) in blocks.items():
        ax.add_patch(mpatches.FancyBboxPatch(
            (x - 1.35, y - 1.0), 2.7, 2.0, boxstyle="round,pad=0.05",
            fc=c, ec="0.25", lw=1.3))
        ax.text(x, y, label, ha="center", va="center", fontsize=8.5)
    # connectors first (behind the circle) so nothing stabs the center text;
    # each runs from the circle edge (r=1.15) to the box edge, in the gap.
    r = 1.15
    for (bx, by) in [(5, 8.0), (5, 2.0)]:            # vertical: box half-height 1.0
        edge = by - 1.0 if by > 5 else by + 1.0
        y0 = 5 + r if by > 5 else 5 - r
        ax.annotate("", xy=(bx, edge), xytext=(bx, y0),
                    arrowprops=dict(arrowstyle="<->", color="0.45", lw=1.4))
    for (bx, by) in [(2.0, 5), (8.0, 5)]:            # horizontal: box half-width 1.35
        edge = bx + 1.35 if bx < 5 else bx - 1.35
        x0 = 5 - r if bx < 5 else 5 + r
        ax.annotate("", xy=(edge, by), xytext=(x0, by),
                    arrowprops=dict(arrowstyle="<->", color="0.45", lw=1.4))
    # central Liveware on top of the connectors
    ax.add_patch(mpatches.Circle((5, 5), r, fc="#ec7063", ec="0.2", lw=1.5,
                                 zorder=6))
    ax.text(5, 5, "L\nLiveware\n(the human)", ha="center", va="center",
            fontsize=8.5, weight="bold", zorder=7)
    ax.set_title("SHELL model: the human at center, mishaps at the interfaces",
                 fontsize=10)
    _caption(fig, "Figure 2: In SHELL, failures live at the interfaces "
             "between the human and S, H, E, and other Liveware.")
    fig.subplots_adjust(bottom=0.08, top=0.90)
    fig.savefig(FIG_DIR / "fig2_shell_model.png", dpi=150)
    plt.close(fig)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    FIG_DIR.mkdir(exist_ok=True)
    fig_habitable_volume()      # Figure 1 (Q4)
    fig_shell_model()           # Figure 2 (Q6 / Q9)
    fig_trade_study()           # Figure 3 (Q8)
    print("Figures written to:", FIG_DIR)


if __name__ == "__main__":
    main()
