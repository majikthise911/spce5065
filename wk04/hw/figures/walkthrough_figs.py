"""Dark-theme walkthrough figures for SPCE 5065 HW4 (the plasma environment).

Generates three figures used in spce_5065_hw4_walkthrough.md:
  walkthrough_fig1_debye_vs_density.png       (P2)
  walkthrough_fig2_delay_range_vs_freq.png    (P3)
  walkthrough_fig3_charging_current_balance.png (P5/P8)

Color scheme (dark theme):
  background #0D1117, text #E6EDF3,
  green #3FB950 positive, red #F85149 negative,
  blue #58A6FF neutral, purple #D2A8FF results, orange #FFA657 thresholds.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

# --- constants ---
E_CHG = 1.602176634e-19
K_B = 1.380649e-23
EPS0 = 8.8541878128e-12
M_E = 9.1093837015e-31
M_P = 1.67262192369e-27
C_LIGHT = 2.99792458e8

BG = "#0D1117"
FG = "#E6EDF3"
GREEN = "#3FB950"
RED = "#F85149"
BLUE = "#58A6FF"
PURPLE = "#D2A8FF"
ORANGE = "#FFA657"

FIG_DIR = Path(__file__).parent


def _style():
    plt.rcParams.update({
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "savefig.facecolor": BG,
        "text.color": FG,
        "axes.labelcolor": FG,
        "axes.edgecolor": FG,
        "xtick.color": FG,
        "ytick.color": FG,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "axes.titlecolor": FG,
        "grid.color": "#30363D",
    })


def debye_length(Te, ne):
    return np.sqrt(EPS0 * K_B * Te / (ne * E_CHG**2))


def excess_range(tec, f):
    return 40.31 * tec / f**2


def time_delay(tec, f):
    return 40.31 * tec / (C_LIGHT * f**2)


def mean_speed(T, m):
    return np.sqrt(8.0 * K_B * T / (np.pi * m))


def floating_potential(T):
    ratio = mean_speed(T, M_E) / mean_speed(T, M_P)
    root = brentq(lambda x: ratio * np.exp(x) - (1.0 - x), -10.0, 0.0)
    return root, root * K_B * T / E_CHG


def fig1_debye():
    _style()
    ne = np.logspace(10, 13, 400)
    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    for Te, color, name in [(1500.0, BLUE, "$T_e$ = 1500 K (300 km)"),
                            (5000.0, ORANGE, "$T_e$ = 5000 K (1000 km)")]:
        ax.loglog(ne, debye_length(Te, ne) * 1e3, color=color, lw=2.2,
                  label=name)
    pts = [("(a) 300 km", 1500.0, 5.0e12, (14, 20)),
           ("(b) 1000 km", 5000.0, 1.0e11, (-4, -46))]
    for label, Te, n0, dxy in pts:
        lam = debye_length(Te, n0) * 1e3
        ax.plot(n0, lam, "o", color=PURPLE, ms=9, zorder=5,
                markeredgecolor=FG)
        ax.annotate(f"{label}\n$n_e$ = {n0:.0e} m$^{{-3}}$\n"
                    f"$\\lambda_D$ = {lam:.2f} mm",
                    xy=(n0, lam), xytext=dxy, textcoords="offset points",
                    fontsize=8.5, color=FG,
                    bbox=dict(boxstyle="round,pad=0.35", fc="#161B22",
                              ec=PURPLE, alpha=0.95),
                    arrowprops=dict(arrowstyle="->", color=FG))
    ax.set_xlabel("Electron number density  $n_e$  (m$^{-3}$)")
    ax.set_ylabel("Debye length  $\\lambda_D$  (mm)")
    ax.set_title("P2: Debye length vs density  (denser plasma = shorter "
                 "shielding distance)")
    ax.grid(True, which="both", alpha=0.4)
    ax.legend(fontsize=9, facecolor="#161B22", edgecolor="#30363D",
              labelcolor=FG)
    fig.text(0.5, 0.015,
             "The hotter 1000 km plasma is also ~50x thinner; density wins, "
             "so shielding reaches ~13x farther.",
             ha="center", va="bottom", fontsize=8.5, style="italic",
             color=FG)
    fig.subplots_adjust(bottom=0.19)
    out = FIG_DIR / "walkthrough_fig1_debye_vs_density.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print("wrote", out)


def fig2_delay_range():
    _style()
    tec = 1.0e18
    f = np.logspace(np.log10(30e6), np.log10(3e9), 500)
    dR = excess_range(tec, f)
    fig, ax1 = plt.subplots(figsize=(7.4, 4.8))
    ax1.loglog(f / 1e6, dR, color=BLUE, lw=2.4, label="excess range $\\Delta R$")
    ax1.set_xlabel("Transmission frequency  $f$  (MHz)")
    ax1.set_ylabel("Excess range  $\\Delta R$  (m)", color=BLUE)
    ax1.tick_params(axis="y", labelcolor=BLUE)
    ax1.grid(True, which="both", alpha=0.4)

    ax2 = ax1.twinx()
    ax2.set_yscale("log")
    ax2.set_ylabel("Group delay  $\\Delta t$  ($\\mu$s)", color=ORANGE)
    lo, hi = ax1.get_ylim()
    ax2.set_ylim(lo / C_LIGHT * 1e6, hi / C_LIGHT * 1e6)
    ax2.tick_params(axis="y", labelcolor=ORANGE)
    for spine in ax2.spines.values():
        spine.set_color(FG)

    for fmark, name, dxy in [(150.0, "150 MHz", (18, 12)),
                             (1600.0, "1.6 GHz", (-30, -60))]:
        Rm = excess_range(tec, fmark * 1e6)
        tm = time_delay(tec, fmark * 1e6)
        ax1.plot(fmark, Rm, "o", color=PURPLE, ms=9, zorder=5,
                 markeredgecolor=FG)
        ax1.annotate(f"{name}\n$\\Delta R$ = {Rm:,.0f} m\n"
                     f"$\\Delta t$ = {tm*1e6:.3f} $\\mu$s",
                     xy=(fmark, Rm), xytext=dxy, textcoords="offset points",
                     fontsize=8.5, color=FG,
                     bbox=dict(boxstyle="round,pad=0.35", fc="#161B22",
                               ec=PURPLE, alpha=0.95),
                     arrowprops=dict(arrowstyle="->", color=FG))
    ax1.set_title("P3: Ionospheric excess range and delay vs frequency  "
                  "(TEC = $10^{18}$ e/m$^2$)")
    fig.text(0.5, 0.015,
             "Both scale as $1/f^2$; going from 150 MHz to 1.6 GHz shrinks "
             "delay and range by ~114x.",
             ha="center", va="bottom", fontsize=8.5, style="italic",
             color=FG)
    fig.subplots_adjust(bottom=0.19, right=0.85)
    out = FIG_DIR / "walkthrough_fig2_delay_range_vs_freq.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print("wrote", out)


def fig3_charging():
    _style()
    T = 1.0e7
    n = 1.0e6
    v_e = mean_speed(T, M_E)
    v_i = mean_speed(T, M_P)
    J_eo = 0.25 * E_CHG * n * v_e
    J_io = 0.25 * E_CHG * n * v_i
    kT_e = K_B * T / E_CHG

    V = np.linspace(-4000.0, 0.0, 500)
    J_e = J_eo * np.exp(V / kT_e)
    J_i = J_io * (1.0 - V / kT_e)

    _, Vf = floating_potential(T)
    Jf = J_io * (1.0 - Vf / kT_e)

    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    ax.plot(V, J_e * 1e9, color=RED, lw=2.4,
            label="electron current $I_e$ (repelled, exponential)")
    ax.plot(V, J_i * 1e9, color=BLUE, lw=2.4,
            label="ion current $I_i$ (attracted, linear)")
    ax.plot(Vf, Jf * 1e9, "o", color=PURPLE, ms=11, zorder=6,
            markeredgecolor=FG)
    ax.annotate(f"balance  $I_e = I_i$\n$V_f$ = {Vf:,.0f} V  "
                f"($\\approx -2.16$ kV)",
                xy=(Vf, Jf * 1e9), xytext=(55, 45),
                textcoords="offset points", fontsize=9, color=FG,
                bbox=dict(boxstyle="round,pad=0.35", fc="#161B22",
                          ec=PURPLE, alpha=0.95),
                arrowprops=dict(arrowstyle="->", color=FG))
    ax.axvline(Vf, color=GREEN, ls="--", lw=1.4, alpha=0.8)
    ax.set_xlabel("Spacecraft potential  $V$  (volts)")
    ax.set_ylabel("Current density per collecting area  (nA/m$^2$)")
    ax.set_title("P5 / P8: GEO current balance  ($T = 10^7$ K),  floating "
                 "potential where $I_e = I_i$")
    ax.grid(True, alpha=0.4)
    ax.legend(loc="upper left", fontsize=8.5, facecolor="#161B22",
              edgecolor="#30363D", labelcolor=FG)
    fig.text(0.5, 0.015,
             "Fast electrons drive the sphere negative until the exponential "
             "$I_e$ falls to meet the gentle line $I_i$.",
             ha="center", va="bottom", fontsize=8.5, style="italic",
             color=FG)
    fig.subplots_adjust(bottom=0.19)
    out = FIG_DIR / "walkthrough_fig3_charging_current_balance.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    fig1_debye()
    fig2_delay_range()
    fig3_charging()
