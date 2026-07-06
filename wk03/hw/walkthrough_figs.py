"""SPCE 5065 -- HW3 walkthrough figures (dark theme, learning aids).

  walkthrough_fig1_risk_escalation.png  Roadmap R/Y/G counts across the four
                                        columns, showing Ceres pushing to red (Q5)
  walkthrough_fig2_freefall_effects.png The three free-fall effects on the body
                                        and their symptom cascades (Q2/Q3)

Run: python walkthrough_figs.py  -> writes PNGs to ./figures/
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

FIG_DIR = Path(__file__).parent / "figures"

BG = "#0D1117"
FG = "#E6EDF3"
RED = "#F85149"
YEL = "#E3B341"
GRN = "#3FB950"
GREY = "#6E7681"
BLUE = "#58A6FF"
PURP = "#D2A8FF"
ORNG = "#FFA657"


def _dark(ax, fig):
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_color("#30363D")
    ax.tick_params(colors=FG)
    ax.xaxis.label.set_color(FG)
    ax.yaxis.label.set_color(FG)
    ax.title.set_color(FG)


# --------------------------------------------------------------------------
# Fig 1 -- roadmap R/Y/G counts across the four columns (Q5)
# --------------------------------------------------------------------------
def fig_risk_escalation() -> None:
    cols = ["Mars\noperational", "Mars\nlong-term", "Ceres\noperational", "Ceres\nlong-term"]
    # counts from the completed roadmap table (Table 2 in the submission)
    green = np.array([1, 3, 0, 0])
    yellow = np.array([6, 8, 0, 3])
    red = np.array([13, 6, 20, 14])
    na = np.array([0, 3, 0, 3])

    x = np.arange(len(cols))
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    _dark(ax, fig)
    b = np.zeros(len(cols))
    for arr, c, lab in [(green, GRN, "Green (well mitigated)"),
                        (yellow, YEL, "Yellow (partial mitigation)"),
                        (red, RED, "Red (no mitigation)"),
                        (na, GREY, "N/A")]:
        ax.bar(x, arr, bottom=b, color=c, edgecolor=BG, width=0.62, label=lab)
        for xi, (v, b0) in enumerate(zip(arr, b)):
            if v > 0:
                ax.text(xi, b0 + v / 2, str(int(v)), ha="center", va="center",
                        color=BG, fontsize=9, weight="bold")
        b = b + arr

    ax.set_xticks(x)
    ax.set_xticklabels(cols, fontsize=9)
    ax.set_ylabel("Number of roadmap risk areas", fontsize=10)
    ax.set_ylim(0, 20.5)
    ax.set_title("Mars to Ceres: the ratings collapse toward red", fontsize=12)
    ax.legend(facecolor="#161B22", edgecolor="#30363D", labelcolor=FG,
              fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1.0))
    fig.text(0.5, 0.02,
             "Walkthrough Figure 1: A longer trip, more radiation, and near-zero "
             "surface gravity wipe out the greens and yellows for Ceres.",
             ha="center", va="bottom", fontsize=8.5, style="italic", color=FG)
    fig.subplots_adjust(left=0.11, right=0.72, bottom=0.17)
    fig.savefig(FIG_DIR / "walkthrough_fig1_risk_escalation.png", dpi=200,
                facecolor=BG)
    plt.close(fig)


# --------------------------------------------------------------------------
# Fig 2 -- three free-fall effects on the body (Q2 / Q3)
# --------------------------------------------------------------------------
def fig_freefall_effects() -> None:
    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    _dark(ax, fig)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # central cause
    ax.add_patch(mpatches.FancyBboxPatch((5.0, 8.0), 2.0, 1.2,
                 boxstyle="round,pad=0.08", fc=BLUE, ec="#30363D"))
    ax.text(6.0, 8.6, "Free fall\n(microgravity)", ha="center", va="center",
            color=BG, fontsize=9.5, weight="bold")

    branches = [
        (2.2, PURP, "1. Altered vestibular\nfunction",
         "Otoliths lose the\ngravity cue",
         ["Space motion sickness", "Disorientation, illusions",
          "Post-landing balance loss"]),
        (6.0, ORNG, "2. Reduced load on\nweight-bearing tissue",
         "Bones and muscles\nunload",
         ["Bone loss -> calcium dump", "Muscle atrophy",
          "Fix: exercise, vitamin D"]),
        (9.8, GRN, "3. Reduced hydrostatic\ngradient",
         "Fluid shifts\ntoward the head",
         ["'Fat face, chicken legs'", "Congestion, puffiness",
          "SANS / vision risk"]),
    ]
    for cx, color, title, mech, effects in branches:
        # arrow from center down to branch head
        ax.annotate("", xy=(cx, 6.7), xytext=(6.0, 8.0),
                    arrowprops=dict(arrowstyle="->", color=GREY, lw=1.4))
        ax.add_patch(mpatches.FancyBboxPatch((cx - 1.55, 5.5), 3.1, 1.2,
                     boxstyle="round,pad=0.06", fc=color, ec="#30363D"))
        ax.text(cx, 6.1, title, ha="center", va="center", color=BG,
                fontsize=9, weight="bold")
        ax.text(cx, 4.85, mech, ha="center", va="center", color=FG,
                fontsize=8, style="italic")
        for i, eff in enumerate(effects):
            y = 3.9 - i * 0.85
            ax.text(cx, y, "- " + eff, ha="center", va="center", color=FG,
                    fontsize=8)

    ax.set_title("The three effects of free fall on the human body",
                 fontsize=12, color=FG)
    fig.text(0.5, 0.01,
             "Walkthrough Figure 2: One cause, three physiological branches; "
             "Q2 lives in branch 1, Q3's nutrition fixes in branches 1 and 2.",
             ha="center", va="bottom", fontsize=8.5, style="italic", color=FG)
    fig.subplots_adjust(bottom=0.10, top=0.92)
    fig.savefig(FIG_DIR / "walkthrough_fig2_freefall_effects.png", dpi=200,
                facecolor=BG)
    plt.close(fig)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    FIG_DIR.mkdir(exist_ok=True)
    fig_risk_escalation()
    fig_freefall_effects()
    print("Walkthrough figures written to:", FIG_DIR)


if __name__ == "__main__":
    main()
