"""SPCE 5065 -- Homework 2 walkthrough figures (dark-theme learning aids).

These are NEW figures built specifically for the Socratic walkthrough, in
addition to the submission figures. They use a dark GitHub-style theme so the
learning resource reads cleanly on screen.

Figures produced:
  walkthrough_fig1_decay_runaway.png   -- altitude-vs-time decay, runaway tail
  walkthrough_fig2_lifetime_explosion.png -- lifetime vs start altitude (log)
  walkthrough_fig3_kapton_threshold.png -- Kapton erosion vs 50 um threshold

All captions avoid em dashes and en dashes by user rule.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad, solve_ivp

# --------------------------------------------------------------------------
# Physics constants (mirrors spce_5065_hw2_solution.py)
# --------------------------------------------------------------------------
MU = 3.986004418e14          # m^3/s^2
R_E = 6378.137e3             # m
YEAR_S = 365.25 * 86400.0    # s
M_SAT = 100.0                # kg
A_SAT = 1.0                  # m^2
CD = 2.2
BC = CD * A_SAT / M_SAT      # m^2/kg
E_KAPTON = 3.0e-24           # cm^3/atom

FIG_DIR = Path(__file__).parent

# --------------------------------------------------------------------------
# Dark theme palette
# --------------------------------------------------------------------------
BG = "#0D1117"
FG = "#E6EDF3"
GREEN = "#3FB950"
RED = "#F85149"
PURPLE = "#D2A8FF"
ORANGE = "#FFA657"
BLUE = "#58A6FF"
GRID = "#30363D"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "savefig.facecolor": BG,
    "text.color": FG,
    "axes.labelcolor": FG,
    "axes.edgecolor": GRID,
    "xtick.color": FG,
    "ytick.color": FG,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "axes.titlecolor": FG,
})


# --------------------------------------------------------------------------
# Physics helpers
# --------------------------------------------------------------------------
def rho(h_km):
    return 1.020e7 * np.asarray(h_km, dtype=float) ** (-7.172)


def v_circ(h_km):
    return np.sqrt(MU / (R_E + h_km * 1.0e3))


def _life_integrand(a):
    h_km = (a - R_E) / 1.0e3
    return 1.0 / (rho(h_km) * BC * np.sqrt(MU * a))


def lifetime(h0_km, hf_km=150.0):
    a0 = R_E + h0_km * 1.0e3
    af = R_E + hf_km * 1.0e3
    val, _ = quad(_life_integrand, af, a0, limit=400)
    return val


def decay_profile(h0_km, hf_km=150.0):
    a0 = R_E + h0_km * 1.0e3
    af = R_E + hf_km * 1.0e3

    def dadt(_t, a):
        h_km = (a[0] - R_E) / 1.0e3
        return [-rho(h_km) * BC * np.sqrt(MU * a[0])]

    def hit_floor(_t, a):
        return a[0] - af
    hit_floor.terminal = True
    hit_floor.direction = -1

    t_span = (0.0, 5.0 * lifetime(h0_km, hf_km))
    sol = solve_ivp(dadt, t_span, [a0], events=hit_floor, max_step=3600.0,
                    rtol=1e-9, atol=1.0)
    return sol.t / 86400.0, (sol.y[0] - R_E) / 1.0e3


def style_ax(ax):
    ax.grid(True, color=GRID, alpha=0.5, lw=0.6)
    for s in ax.spines.values():
        s.set_color(GRID)


def caption(fig, text):
    fig.text(0.5, 0.015, text, ha="center", va="bottom", fontsize=8,
             style="italic", color="#9DA7B3", wrap=True)


# --------------------------------------------------------------------------
# Figure 1: decay history with the runaway tail
# --------------------------------------------------------------------------
def fig1_decay_runaway():
    t_days, h_km = decay_profile(400.0, 150.0)
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    ax.plot(t_days, h_km, color=BLUE, lw=2.4)

    # shade the runaway tail (last ~12 days)
    t_end = t_days[-1]
    tail_mask = t_days >= (t_end - 12.0)
    ax.fill_between(t_days[tail_mask], 150, h_km[tail_mask],
                    color=RED, alpha=0.18)

    ax.axhline(150.0, color=ORANGE, ls="--", lw=1.4)
    ax.text(8, 156, "deorbit floor (150 km)", color=ORANGE, fontsize=9)

    # annotate the long quiet plateau
    ax.annotate("loafs near 400 km\nfor most of its life\n(air is thin up here)",
                xy=(120, 388), xytext=(70, 250),
                textcoords="data", fontsize=8.5, color=FG, ha="left",
                arrowprops=dict(arrowstyle="->", color="#9DA7B3"))

    # annotate the runaway tail
    ax.annotate("runaway tail:\ndensity climbs fast,\ndrag explodes",
                xy=(t_end - 6, 230), xytext=(t_end - 95, 120),
                textcoords="data", fontsize=8.5, color=RED, ha="left",
                arrowprops=dict(arrowstyle="->", color=RED))

    ax.annotate(f"reentry at {t_end:.0f} days", xy=(t_end, 150),
                xytext=(t_end - 70, 175), textcoords="data", fontsize=9,
                color=PURPLE,
                arrowprops=dict(arrowstyle="->", color=PURPLE))

    ax.set_xlabel("Time since release at 400 km  (days)")
    ax.set_ylabel("Altitude  h  (km)")
    ax.set_title("Why a single average density fails: the decay is back-loaded",
                 fontsize=11, color=FG)
    ax.set_ylim(120, 410)
    style_ax(ax)
    fig.subplots_adjust(bottom=0.18, top=0.91)
    caption(fig, "Walkthrough Fig 1: most of the 223.7 day life is spent high "
                 "and slow; the last weeks collapse as density runs away.")
    fig.savefig(FIG_DIR / "walkthrough_fig1_decay_runaway.png", dpi=200)
    plt.close(fig)


# --------------------------------------------------------------------------
# Figure 2: lifetime explosion vs starting altitude
# --------------------------------------------------------------------------
def fig2_lifetime_explosion():
    starts = [200, 250, 300, 350, 400, 450, 500]
    days = [lifetime(float(h)) / 86400.0 for h in starts]

    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    colors = [RED, RED, ORANGE, ORANGE, PURPLE, GREEN, GREEN]
    bars = ax.bar([str(s) for s in starts], days, color=colors, width=0.62)
    ax.set_yscale("log")

    for b, d in zip(bars, days):
        label = f"{d:.1f} d" if d >= 1 else f"{d:.2f} d"
        ax.annotate(label, xy=(b.get_x() + b.get_width() / 2, d),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", fontsize=8.5, color=FG)

    # highlight the P1 case
    ax.annotate("P1 case\n(matches Problem 1)",
                xy=(4, days[4]), xytext=(1.6, 600),
                textcoords="data", fontsize=8.5, color=PURPLE, ha="left",
                arrowprops=dict(arrowstyle="->", color=PURPLE))

    ax.text(0.02, 0.95,
            r"density follows $h^{-7.172}$, so 300 extra km" "\n"
            "buys roughly 2000x more life",
            transform=ax.transAxes, fontsize=9, color=ORANGE, va="top")

    ax.set_xlabel("Starting altitude  (km)")
    ax.set_ylabel("Lifetime to 150 km  (days, log scale)")
    ax.set_title("Lifetime explodes with starting altitude",
                 fontsize=11, color=FG)
    style_ax(ax)
    ax.set_ylim(0.4, 4000)
    fig.subplots_adjust(bottom=0.18, top=0.91)
    caption(fig, "Walkthrough Fig 2: drag lifetime on a log axis. Under a day "
                 "at 200 km, almost four years at 500 km.")
    fig.savefig(FIG_DIR / "walkthrough_fig2_lifetime_explosion.png", dpi=200)
    plt.close(fig)


# --------------------------------------------------------------------------
# Figure 3: Kapton erosion vs the 50 um threshold
# --------------------------------------------------------------------------
def fig3_kapton_threshold():
    v_cms = v_circ(450.0) * 100.0
    cases = [("low\n(6e6)", 6e6), ("medium\n(2e7)", 2e7), ("high\n(1e8)", 1e8)]
    depths = []
    for _, n in cases:
        fluence = n * v_cms * YEAR_S
        depths.append(E_KAPTON * fluence * 1.0e4)  # micron/yr

    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    colors = [GREEN, ORANGE, RED]
    bars = ax.bar([c[0] for c in cases], depths, color=colors, width=0.6)

    ax.axhline(50.0, color=PURPLE, ls="--", lw=1.5)
    ax.text(2.46, 52, "50 um reference\npanel thickness", color=PURPLE,
            fontsize=8.5, ha="right", va="bottom")

    for b, d in zip(bars, depths):
        verdict = "survives" if d < 50 else "eaten through"
        vcol = GREEN if d < 50 else RED
        ax.annotate(f"{d:.1f} um", xy=(b.get_x() + b.get_width() / 2, d),
                    xytext=(0, 14), textcoords="offset points",
                    ha="center", fontsize=10, color=FG, weight="bold")
        ax.annotate(verdict, xy=(b.get_x() + b.get_width() / 2, d),
                    xytext=(0, 2), textcoords="offset points",
                    ha="center", fontsize=8, color=vcol)

    ax.set_xlabel("Solar activity (atomic-oxygen number density, atoms/cm$^3$)")
    ax.set_ylabel("Kapton erosion depth  (um / year)")
    ax.set_title("Bare Kapton on a ram face: survives quiet years, eaten in active ones",
                 fontsize=10.5, color=FG)
    style_ax(ax)
    ax.set_ylim(0, 82)
    fig.subplots_adjust(bottom=0.18, top=0.91)
    caption(fig, "Walkthrough Fig 3: one-year Kapton erosion at 450 km against "
                 "the 50 um yardstick. High activity removes a full thickness.")
    fig.savefig(FIG_DIR / "walkthrough_fig3_kapton_threshold.png", dpi=200)
    plt.close(fig)


def main():
    fig1_decay_runaway()
    fig2_lifetime_explosion()
    fig3_kapton_threshold()
    print("Walkthrough figures written to:", FIG_DIR)


if __name__ == "__main__":
    main()
