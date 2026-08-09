"""Figures for the SPCE 5065 HW7 Socratic walkthrough (dark theme).

Run from anywhere:  python3 figures/walkthrough_figs.py
Writes walkthrough_fig1..5 into this directory.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import spce_5065_hw7_solution as hw  # noqa: E402

OUT = Path(__file__).resolve().parent

BG = "#0D1117"
FG = "#E6EDF3"
GREEN = "#3FB950"
RED = "#F85149"
BLUE = "#58A6FF"
PURPLE = "#D2A8FF"
ORANGE = "#FFA657"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": FG, "axes.labelcolor": FG, "axes.edgecolor": "#30363D",
    "xtick.color": FG, "ytick.color": FG, "grid.color": "#21262D",
    "font.family": "sans-serif", "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "axes.titlecolor": FG,
})


def save(fig, name: str) -> None:
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


# ---------------------------------------------------------------- fig 1
def fig1_dose_ladder() -> None:
    """Where the mission dose sits on the ladder of known human exposures."""
    md = hw.mission_dose(hw.SHIELD_BASELINE)
    items = [
        ("Transcontinental flight, 1 yr", 0.004, BLUE),
        ("Chest x-ray", 0.01, BLUE),
        ("Sea level, 1 yr", 0.1, BLUE),
        ("Colorado Springs, 1 yr", 0.2, BLUE),
        ("ISS, 80 days", 4.0, GREEN),
        ("Shuttle, 80 days", 8.71, GREEN),
        ("Skylab, 84 days", 17.85, GREEN),
        ("NASA career limit", 60.0, ORANGE),
        ("Radiation sickness onset", 100.0, RED),
        ("Mars mission, this design", md["total_rem"], PURPLE),
        ("50% mortality", 340.0, RED),
    ]
    items.sort(key=lambda t: t[1])
    names = [i[0] for i in items]
    vals = [i[1] for i in items]
    cols = [i[2] for i in items]

    fig, ax = plt.subplots(figsize=(9.5, 6.0))
    y = np.arange(len(items))
    ax.set_axisbelow(True)
    ax.hlines(y, 1e-3, vals, color=cols, lw=3.0, alpha=0.75)
    ax.scatter(vals, y, s=110, c=cols, zorder=3, edgecolors="#30363D")
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=9.5)
    ax.set_xscale("log")
    ax.set_xlim(1e-3, 3e3)
    ax.set_ylim(-0.7, len(items) - 0.3)
    ax.set_xlabel("Dose equivalent (REM, log scale)")
    ax.set_title("Problem 2: where 472 REM actually sits", fontsize=13, pad=14)
    ax.axvline(60.0, color=ORANGE, ls="--", lw=1.6)
    ax.grid(axis="x", which="major", alpha=0.35)
    for yi, v in zip(y, vals):
        ax.annotate(f"{v:g}", xy=(v, yi), xytext=(11, 0), textcoords="offset points",
                    va="center", fontsize=8.5, color=FG)
    ax.annotate("60 REM\ncareer limit", xy=(60, 1.0), xytext=(-10, 0),
                textcoords="offset points", ha="right", va="center",
                color=ORANGE, fontsize=9)
    fig.text(0.5, -0.02, "Figure W1: The mission budget is not 'a bit over the limit'. "
                         "It is between radiation sickness and 50% mortality.",
             ha="center", fontsize=9, style="italic", color=FG)
    save(fig, "walkthrough_fig1_dose_ladder.png")


# ---------------------------------------------------------------- fig 2
def fig2_belt_product() -> None:
    """Dose = rate x dwell time, drawn as the product of two bar sets."""
    rows = [r for r in hw.van_allen_pass()["rows"] if r["width"] > 0]
    names = [r["color"] for r in rows]
    rate = [r["rate"] for r in rows]
    time = [r["time_s"] for r in rows]
    dose = [r["dose_rad"] for r in rows]

    fig, axes = plt.subplots(1, 3, figsize=(11.5, 4.2))
    for ax, vals, title, col, unit in (
        (axes[0], rate, "Dose rate", BLUE, "rad/s"),
        (axes[1], time, "Dwell time", GREEN, "s"),
        (axes[2], dose, "Dose = rate x time", PURPLE, "rad"),
    ):
        b = ax.bar(names, vals, color=col, edgecolor="#30363D")
        ax.set_title(title, fontsize=11)
        ax.set_ylabel(unit)
        ax.grid(axis="y", alpha=0.3)
        ax.tick_params(axis="x", labelrotation=20)
        for r, v in zip(b, vals):
            ax.annotate(f"{v:.4g}", xy=(r.get_x() + r.get_width() / 2, v),
                        xytext=(0, 4), textcoords="offset points",
                        ha="center", fontsize=8, color=FG)
        ax.set_ylim(0, max(vals) * 1.22)

    axes[2].annotate("orange wins on rate,\nyellow nearly ties on time",
                     xy=(0.5, 0.86), xycoords="axes fraction", ha="center",
                     fontsize=9, color=ORANGE)
    fig.suptitle("Problem 2: the belt dose is a product, and both factors matter",
                 fontsize=13, y=1.02)
    fig.tight_layout()
    fig.text(0.5, -0.05, "Figure W2: The blue band is the widest by far and contributes "
                         "almost nothing, because its rate is 100x lower.",
             ha="center", fontsize=9, style="italic", color=FG)
    save(fig, "walkthrough_fig2_belt_product.png")


# ---------------------------------------------------------------- fig 3
def fig3_waterfall() -> None:
    """Cascade of the four dose line items building to the mission total."""
    md = hw.mission_dose(hw.SHIELD_BASELINE)
    labels = ["Van Allen\nbelts x2", "GCR\ncruise", "SCR 50%\ncruise",
              "Mars\nsurface", "TOTAL"]
    vals = [md["belt_rem"], md["gcr_rem"], md["scr_rem"], md["surf_rem"]]
    cols = [RED, RED, ORANGE, GREEN]

    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    bottom = 0.0
    for i, (v, c) in enumerate(zip(vals, cols)):
        ax.bar(i, v, bottom=bottom, color=c, edgecolor="#30363D", width=0.62)
        ax.annotate(f"{v:.0f} REM\n({100*v/sum(vals):.0f}%)",
                    xy=(i, bottom + v / 2), ha="center", va="center",
                    fontsize=9.5, color=BG, weight="bold")
        if i < len(vals) - 1:
            ax.plot([i + 0.31, i + 1 - 0.31], [bottom + v, bottom + v],
                    color="#8B949E", ls=":", lw=1.2)
        bottom += v
    ax.bar(len(vals), bottom, color=PURPLE, edgecolor="#30363D", width=0.62)
    ax.annotate(f"{bottom:.0f} REM", xy=(len(vals), bottom / 2), ha="center",
                va="center", fontsize=11, color=BG, weight="bold")

    ax.axhline(60.0, color=ORANGE, ls="--", lw=1.8)
    ax.annotate("60 REM career limit", xy=(-0.42, 60), xytext=(0, 8),
                textcoords="offset points", ha="left", color=ORANGE, fontsize=9.5)
    ax.set_ylim(0, bottom * 1.10)
    ax.set_xlim(-0.6, len(vals) + 0.6)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=9.5)
    ax.set_ylabel("Dose equivalent (REM)")
    ax.set_title("Problem 2: the dose budget, stacked", fontsize=13, pad=12)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.text(0.5, -0.03, "Figure W3: 72% of the budget is the belts plus GCR, and neither "
                         "responds much to a thicker wall.",
             ha="center", fontsize=9, style="italic", color=FG)
    save(fig, "walkthrough_fig3_dose_waterfall.png")


# ---------------------------------------------------------------- fig 4
def fig4_hvl_ladder() -> None:
    """The halving ladder, with the two answers marked as tiny fractions of one HVL."""
    x = np.linspace(0, 80, 500)
    frac = hw.attenuation(x)

    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    ax.plot(x, frac * 100, color=BLUE, lw=2.6)
    for n in range(1, 5):
        xv = n * hw.HVL_LUCITE
        ax.plot([xv, xv], [0, 100 * 0.5 ** n], color="#30363D", ls=":", lw=1.2)
        ax.plot([0, xv], [100 * 0.5 ** n] * 2, color="#30363D", ls=":", lw=1.2)
        ax.annotate(f"{n} HVL\n{100*0.5**n:.2f}%", xy=(xv, 100 * 0.5 ** n),
                    xytext=(6, 10), textcoords="offset points",
                    fontsize=8.5, color="#8B949E")
    for xi, col, lab in ((1.0, GREEN, "1 cm"), (10.0, PURPLE, "10 cm")):
        f = float(hw.attenuation(xi)[0]) * 100
        ax.plot([xi], [f], "o", ms=9, color=col)
        ax.annotate(f"{lab}: {f:.2f}% left\n({xi/hw.HVL_LUCITE:.2f} HVL)",
                    xy=(xi, f), xytext=(34, 6 if xi == 1 else -34),
                    textcoords="offset points", fontsize=10, color=col,
                    arrowprops=dict(arrowstyle="->", color=col, lw=1.4))
    ax.set_xlabel("Lucite thickness (cm)")
    ax.set_ylabel("Flux density remaining (%)")
    ax.set_title("Problem 3: one half-value layer is 20 cm, so 10 cm is half a halving",
                 fontsize=12.5, pad=12)
    ax.set_xlim(0, 80)
    ax.set_ylim(0, 104)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.text(0.5, -0.02, "Figure W4: Attenuation is exponential, so thickness buys "
                         "halvings, not fixed percentages.",
             ha="center", fontsize=9, style="italic", color=FG)
    save(fig, "walkthrough_fig4_hvl_ladder.png")


# ---------------------------------------------------------------- fig 5
def fig5_torque_scaling() -> None:
    """All four torques vs orbit radius, showing exactly where the ranking flips."""
    dt = hw.disturbance_torques()
    r_leo = hw.R_E * 1000.0 + hw.H_LEO
    r = np.linspace(6600e3, 46000e3, 800)

    gg = dt["LEO"]["gravity_gradient"] * (r_leo / r) ** 3
    mag = dt["LEO"]["magnetic"] * (r_leo / r) ** 3
    srp = np.full_like(r, dt["LEO"]["solar"])
    h_km = r / 1000.0 - hw.R_E
    rho = hw.rho_powerlaw(h_km)
    v = np.sqrt(hw.MU_E / r)
    arm = abs(hw.srp_torque()["arm"])
    aero = 0.5 * rho * hw.CD * hw.A_TOTAL * v ** 2 * arm

    fig, ax = plt.subplots(figsize=(10.0, 5.8))
    ax.semilogy(r / 1e3, gg, color=RED, lw=2.4, label="Gravity gradient  ($R^{-3}$)")
    ax.semilogy(r / 1e3, aero, color=GREEN, lw=2.4, label="Aerodynamic  (steep)")
    ax.semilogy(r / 1e3, srp, color=PURPLE, lw=2.4, label="Solar radiation  (flat)")
    ax.semilogy(r / 1e3, mag, color=BLUE, lw=2.4, label="Magnetic  ($R^{-3}$)")

    r_cross = r_leo * (dt["LEO"]["gravity_gradient"] / dt["LEO"]["solar"]) ** (1 / 3)
    ax.axvline(r_cross / 1e3, color=ORANGE, ls="--", lw=1.6)
    ax.annotate(f"SRP overtakes gravity gradient\nat r = {r_cross/1e3:,.0f} km "
                f"({r_cross/1e3 - hw.R_E:,.0f} km altitude)",
                xy=(r_cross / 1e3, 2e-4), xytext=(18, 0), textcoords="offset points",
                fontsize=9.5, color=ORANGE)
    for rv, lab in ((r_leo / 1e3, "LEO\n550 km"), (hw.R_GEO / 1e3, "GEO")):
        ax.axvline(rv, color="#8B949E", ls=":", lw=1.2)
        ax.annotate(lab, xy=(rv, 3e-12), xytext=(4, 0), textcoords="offset points",
                    fontsize=9, color="#8B949E")
    ax.set_xlabel("Orbit radius (km)")
    ax.set_ylabel("Disturbance torque on the Starlink bus (N$\\cdot$m)")
    ax.set_title("Problem 5: three torques fall off with altitude, one does not",
                 fontsize=13, pad=12)
    ax.set_ylim(1e-13, 1e-2)
    ax.grid(which="both", alpha=0.3)
    ax.legend(loc="upper right", facecolor="#161B22", edgecolor="#30363D",
              labelcolor=FG, fontsize=9.5)
    fig.tight_layout()
    fig.text(0.5, -0.02, "Figure W5: The aerodynamic curve uses the course power-law fit, "
                         "which is only valid in the thermosphere; treat it as "
                         "illustrative above about 1000 km.",
             ha="center", fontsize=9, style="italic", color=FG)
    save(fig, "walkthrough_fig5_torque_scaling.png")


if __name__ == "__main__":
    fig1_dose_ladder()
    fig2_belt_product()
    fig3_waterfall()
    fig4_hvl_ladder()
    fig5_torque_scaling()
