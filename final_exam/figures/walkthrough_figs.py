"""Walkthrough figures for the SPCE 5065 final exam study guide.

Dark theme, 200 dpi, written to this directory:
  walkthrough_fig1_frequency_ladder.png   ties P3, P5, P6 and P8 to one axis
  walkthrough_fig2_thermal_waterfall.png  P9 sunlit vs eclipse energy balance
  walkthrough_fig3_solar_cycle_arrows.png P4 correlation table as a picture
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

HERE = Path(__file__).parent

BG = "#0D1117"
FG = "#E6EDF3"
GREEN = "#3FB950"
RED = "#F85149"
BLUE = "#58A6FF"
PURPLE = "#D2A8FF"
ORANGE = "#FFA657"
GREY = "#8B949E"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "savefig.facecolor": BG,
    "text.color": FG,
    "axes.labelcolor": FG,
    "axes.edgecolor": GREY,
    "xtick.color": FG,
    "ytick.color": FG,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "grid.color": "#30363D",
})


def fig1_frequency_ladder() -> None:
    """One log-frequency axis carrying every frequency the exam asks about."""
    fig, ax = plt.subplots(figsize=(12.5, 6.0))
    ax.set_xscale("log")
    ax.set_xlim(3e5, 3e15)
    ax.set_ylim(-1.35, 1.5)
    ax.axhline(0, color=GREY, lw=1.4, zorder=1)
    ax.get_yaxis().set_visible(False)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)

    # Shaded regions
    ax.axvspan(9.2e5, 2.62e6, color=RED, alpha=0.22, zorder=0)
    ax.axvspan(1.8e10, 2.65e10, color=GREEN, alpha=0.22, zorder=0)

    marks = [
        (9.2e5,  "P6: 1000 km plasma cutoff\n0.9 to 2.6 MHz\n(signals below this reflect)",
         RED,    0.95,  "left"),
        (1.91e7, "P3/P6: F2 peak cutoff\n19 MHz\n(the real gate for a ground link)",
         ORANGE, -0.95, "center"),
        (2.1e10, "P8: K-band, 18 to 26.5 GHz\nexcess range 12 cm, delay 0.42 ns",
         GREEN,  0.95,  "center"),
        (4.04e14, "P5: 1.67 eV bond threshold\n404 THz (742 nm)\nabove this, bonds break",
         PURPLE, -0.95, "right"),
        (2.15e14, "P3: the proposed sensor\n215 THz (1.394 um)\nblocked by water vapour",
         BLUE,   0.95,  "right"),
    ]
    for f, label, color, y, ha in marks:
        ax.plot([f, f], [0, y * 0.55], color=color, lw=2.0, zorder=3)
        ax.plot(f, 0, "o", color=color, ms=9, zorder=4)
        ax.text(f, y * 0.62, label, color=color, fontsize=9, ha=ha,
                va="bottom" if y > 0 else "top", linespacing=1.45)

    # Regime bar underneath
    regimes = [(3e5, 3e7, "ionosphere\nis a mirror", RED),
               (3e7, 1e12, "ionosphere is a\nsmall 1/f^2 correction", GREEN),
               (1e12, 3e15, "ionosphere irrelevant,\natmosphere takes over", BLUE)]
    for f0, f1, txt, color in regimes:
        ax.add_patch(Rectangle((f0, -1.32), f1 - f0, 0.16, color=color,
                               alpha=0.35, zorder=2))
        ax.text(np.sqrt(f0 * f1), -1.24, txt, color=FG, fontsize=8.5,
                ha="center", va="center", linespacing=1.3)

    ax.set_xlabel("Frequency (Hz), logarithmic", fontsize=11)
    ax.set_title("The whole exam on one axis: what the ionosphere does to a "
                 "signal depends only on how far above cutoff you are",
                 fontsize=12.5, pad=14)
    ax.grid(True, axis="x", which="major", alpha=0.28)
    fig.tight_layout()
    fig.savefig(HERE / "walkthrough_fig1_frequency_ladder.png", dpi=200)
    plt.close(fig)


def fig2_thermal_waterfall() -> None:
    """P9: where the heat comes from in each case, and what T it produces."""
    sigma, eps, A = 5.67e-8, 0.874, 6.0

    def temp(q):
        return (q / (eps * sigma * A))**0.25 - 273.15

    labels = ["Solar\n$\\alpha A S$", "Albedo\n$\\alpha A s^2 \\cdot 465$",
              "Earth IR\n$\\alpha A s^2 \\cdot 237$", "Internal\n100 W", "TOTAL IN"]
    sun = [1332.8, 413.6, 210.8, 100.0]
    ecl = [0.0, 0.0, 210.8, 100.0]

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.6), sharey=True)
    for ax, vals, name, tot_color in [
            (axes[0], sun, "SUNLIT", RED),
            (axes[1], ecl, "ECLIPSE", BLUE)]:
        running = 0.0
        for i, v in enumerate(vals):
            color = GREY if v == 0 else (GREEN if i < 3 else ORANGE)
            ax.bar(i, v, bottom=running, color=color, alpha=0.9, width=0.62)
            if v > 0:
                ax.text(i, running + v / 2, f"{v:.0f} W", ha="center",
                        va="center", fontsize=9.5, color=BG, fontweight="bold")
            else:
                ax.text(i, 40, "0 W", ha="center", va="center", fontsize=9.5,
                        color=GREY)
            running += v
        ax.bar(4, running, color=tot_color, alpha=0.95, width=0.62)
        ax.text(4, running / 2, f"{running:.0f} W", ha="center", va="center",
                fontsize=10.5, color=BG, fontweight="bold")
        ax.set_xticks(range(5))
        ax.set_xticklabels(labels, fontsize=8.5)
        ax.grid(True, axis="y", alpha=0.25)
        ax.set_axisbelow(True)
        T = temp(running)
        ax.set_title(f"{name}:  $T = {T:+.1f}\\ ^\\circ$C", fontsize=13,
                     color=tot_color, pad=10)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)

    axes[0].set_ylabel("Absorbed power (W)", fontsize=11)
    axes[0].set_ylim(0, 2250)
    fig.suptitle("P9: losing the Sun removes 85% of the heat input, and the "
                 "fourth root still leaves a 109 $^\\circ$C swing",
                 fontsize=12.5, y=0.985)
    fig.text(0.5, 0.015, "Battery band is 0 to 15 $^\\circ$C. The sunlit case "
             "grazes the ceiling; the eclipse case misses the floor by 93 "
             "$^\\circ$C.", ha="center", fontsize=9.5, style="italic",
             color=GREY)
    fig.tight_layout(rect=(0, 0.045, 1, 0.95))
    fig.savefig(HERE / "walkthrough_fig2_thermal_waterfall.png", dpi=200)
    plt.close(fig)


def fig3_solar_cycle_arrows() -> None:
    """P4: the correlation table drawn, with the driving mechanism named."""
    rows = [
        ("Trapped electrons", "lower", "higher",
         "storms and substorms inject them,\nand storms track solar activity"),
        ("Trapped protons", "higher", "lower",
         "source (GCR) is suppressed and the\npuffed-up thermosphere eats them"),
        ("Galactic cosmic rays", "higher", "lower",
         "the strong solar-max heliospheric\nfield deflects them away"),
        ("Solar particle events", "lower", "higher",
         "flares and CMEs cluster within a year\nor two of sunspot maximum"),
    ]
    fig, ax = plt.subplots(figsize=(12.6, 5.8))
    ax.set_xlim(0, 12)
    ax.set_ylim(-0.75, len(rows) + 1.15)
    ax.axis("off")

    ax.text(3.30, len(rows) + 0.50, "SOLAR MIN", fontsize=12,
            fontweight="bold", ha="center", color=BLUE)
    ax.text(5.55, len(rows) + 0.50, "SOLAR MAX", fontsize=12,
            fontweight="bold", ha="center", color=ORANGE)
    ax.text(7.05, len(rows) + 0.50, "Why", fontsize=12, fontweight="bold",
            ha="left", color=FG)

    for i, (name, lo, hi, why) in enumerate(rows):
        y = len(rows) - i - 0.5
        ax.text(0.05, y, name, fontsize=11, va="center", color=FG,
                fontweight="bold")
        for x, val in [(3.30, lo), (5.55, hi)]:
            up = val == "higher"
            color = RED if up else GREEN
            ax.add_patch(Rectangle((x - 0.72, y - 0.30), 1.44, 0.60,
                                   color=color, alpha=0.22, zorder=0))
            ax.add_patch(FancyArrowPatch((x - 0.46, y - (0.16 if up else -0.16)),
                                         (x - 0.46, y + (0.16 if up else -0.16)),
                                         arrowstyle="-|>", mutation_scale=15,
                                         color=color, lw=2.2))
            ax.text(x + 0.16, y, val, fontsize=10.5, va="center",
                    ha="center", color=color, fontweight="bold")
        ax.text(7.05, y, why, fontsize=9, va="center", color=GREY,
                linespacing=1.35)
        ax.plot([0.0, 11.95], [y - 0.5, y - 0.5], color="#30363D", lw=0.8)

    ax.text(0.05, -0.35, "Only the trapped protons run against solar activity. "
            "Everything else follows the obvious direction.",
            fontsize=10.5, color=PURPLE, style="italic", va="center")
    ax.set_title("P4: which way does each flux move across the solar cycle?",
                 fontsize=13, pad=16)
    fig.tight_layout()
    fig.savefig(HERE / "walkthrough_fig3_solar_cycle_arrows.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    fig1_frequency_ladder()
    fig2_thermal_waterfall()
    fig3_solar_cycle_arrows()
    print("walkthrough figures written to", HERE)
