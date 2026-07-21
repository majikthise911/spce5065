"""SPCE 5065 -- Homework 4 solution (the plasma environment).

Covers the quantitative parts of HW4:

  P2  Debye length in the ionosphere at 300 km and 1000 km
  P3  Ionospheric group delay and excess range at 150 MHz and 1.6 GHz (TEC = 1e18)
  P5  Spacecraft charging of a spherical GEO satellite in a 1e7 K plasma:
        mean speeds, GEO orbital speed, current-balance solve for the
        floating (zero-net-current) potential
  P8  Same floating-potential calc, stated standalone at synchronous altitude

Conceptual problems (P1 current events, P4 ionospheric model, P6 npn/pnp,
P7 grounding article) are answered in the submission document; they need no code.

Outputs:
  - Console tables reproducing every boxed number in the submission
  - figures/fig1_delay_range_vs_freq.png   (P3)
  - figures/fig2_charging_current_balance.png (P5/P8)
  - figures/fig3_debye_vs_density.png       (P2)

All formulas are taken from the Lesson 4 decks (Plasma Parts 1-3) and Tribble
Ch. 5 and Ch. 8. Density values for P2 are read from the course day/solar-max
plasma-density profile (Lesson 4 Part 1).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

# --------------------------------------------------------------------------
# Constants (Lesson 4 cheat sheet)
# --------------------------------------------------------------------------
E_CHG = 1.602176634e-19       # C        electron charge magnitude
K_B = 1.380649e-23            # J/K      Boltzmann constant
EPS0 = 8.8541878128e-12       # F/m      vacuum permittivity
M_E = 9.1093837015e-31        # kg       electron mass
M_P = 1.67262192369e-27       # kg       proton mass
C_LIGHT = 2.99792458e8        # m/s      vacuum speed of light
MU_EARTH = 398600.4418        # km^3/s^2 Earth gravitational parameter
R_GEO_KM = 42164.0            # km       geostationary orbital radius

FIG_DIR = Path(__file__).parent / "figures"


# --------------------------------------------------------------------------
# P2 -- Debye length
# --------------------------------------------------------------------------
def debye_length(Te: float, ne: float) -> float:
    """Debye length (m).  lambda_D = sqrt(eps0 * kB * Te / (ne * e^2))."""
    return np.sqrt(EPS0 * K_B * Te / (ne * E_CHG**2))


def p2() -> None:
    print("=" * 70)
    print("P2 -- Debye length in the ionosphere")
    print("=" * 70)
    # (n_e read from the course day/solar-max plasma-density profile)
    cases = [
        ("(a) 300 km ", 1500.0, 5.0e12),
        ("(b) 1000 km", 5000.0, 1.0e11),
    ]
    for label, Te, ne in cases:
        lam = debye_length(Te, ne)
        print(f"  {label}: Te = {Te:6.0f} K, ne = {ne:.1e} m^-3  ->  "
              f"lambda_D = {lam:.3e} m = {lam*1e3:.3f} mm = {lam*100:.3f} cm")
    # Verification: the 69*sqrt(Te/ne) engineering form should agree.
    lam_eng = 69.01 * np.sqrt(1500.0 / 5.0e12)
    print(f"  [check] 69.0*sqrt(Te/ne) at 300 km = {lam_eng*1e3:.3f} mm "
          f"(matches full formula)")


# --------------------------------------------------------------------------
# P3 -- ionospheric group delay and excess range
# --------------------------------------------------------------------------
def excess_range(tec: float, f: float) -> float:
    """Excess range (m).  dR = 40.31 * TEC / f^2."""
    return 40.31 * tec / f**2


def time_delay(tec: float, f: float) -> float:
    """Group delay (s).  dt = 40.31 * TEC / (c * f^2) = dR / c."""
    return 40.31 * tec / (C_LIGHT * f**2)


def p3() -> None:
    print("=" * 70)
    print("P3 -- ionospheric time delay and excess range (TEC = 1e18 e/m^2)")
    print("=" * 70)
    tec = 1.0e18
    for f, name in [(150e6, "150 MHz"), (1.6e9, "1.6 GHz")]:
        dt = time_delay(tec, f)
        dR = excess_range(tec, f)
        print(f"  f = {name:8s}: dt = {dt*1e6:8.4f} us = {dt*1e9:8.2f} ns    "
              f"dR = {dR:8.2f} m = {dR/1e3:.4f} km")
    # Verification: dR should equal c*dt
    f = 150e6
    print(f"  [check] c*dt(150 MHz) = {C_LIGHT*time_delay(tec, f):.2f} m "
          f"vs dR = {excess_range(tec, f):.2f} m")


# --------------------------------------------------------------------------
# P5 / P8 -- spacecraft charging
# --------------------------------------------------------------------------
def mean_speed(T: float, m: float) -> float:
    """Mean (thermal) speed (m/s).  v_mean = sqrt(8 kB T / (pi m))."""
    return np.sqrt(8.0 * K_B * T / (np.pi * m))


def geo_speed_kms() -> float:
    """Circular geostationary orbital speed (km/s).  v = sqrt(mu / r)."""
    return np.sqrt(MU_EARTH / R_GEO_KM)


def floating_potential_geo(T: float) -> tuple[float, float]:
    """Solve current balance I_e(V) = I_i(V) for V < 0 at GEO.

    Electrons repelled (V<0):  I_e = I_eo A exp(eV/kT_e)
    Ions attracted   (V<0):  I_i = I_io A [1 - eV/kT_i]
    with I_eo/I_io = v_e/v_i = sqrt(m_i/m_e) and T_e = T_i = T.

    Let x = eV/kT.  Balance:  (v_e/v_i) exp(x) = 1 - x.
    Returns (x, V_volts).
    """
    ratio = mean_speed(T, M_E) / mean_speed(T, M_P)   # v_e / v_i = sqrt(mi/me)
    f = lambda x: ratio * np.exp(x) - (1.0 - x)
    x = brentq(f, -10.0, 0.0)
    kT_over_e = K_B * T / E_CHG
    return x, x * kT_over_e


def p5_p8() -> None:
    print("=" * 70)
    print("P5 / P8 -- spacecraft charging at GEO, plasma T = 1e7 K")
    print("=" * 70)
    T = 1.0e7
    v_sc = geo_speed_kms()
    v_e = mean_speed(T, M_E)
    v_i = mean_speed(T, M_P)
    print(f"  (a) spacecraft (GEO) speed         = {v_sc:.4f} km/s")
    print(f"  (b) electron mean speed            = {v_e:.4e} m/s = "
          f"{v_e/1e3:,.0f} km/s")
    print(f"      proton   mean speed            = {v_i:.4e} m/s = "
          f"{v_i/1e3:,.0f} km/s")
    print(f"      v_e / v_i = sqrt(mi/me)        = {v_e/v_i:.3f}")
    print(f"      v_sc / v_e                     = {v_sc*1e3/v_e:.2e}  "
          f"(spacecraft speed negligible vs thermal)")

    x, V = floating_potential_geo(T)
    kT_over_e = K_B * T / E_CHG
    print(f"  (e) kB*Te/e                        = {kT_over_e:.2f} V")
    print(f"      current-balance root  x=eV/kT  = {x:.4f}  (prof approx -2.5)")
    print(f"      floating potential V           = {V:,.1f} V = {V/1e3:.3f} kV")
    # Verification: standard -2.5 kT/e result for a hot e-/proton plasma
    print(f"  [check] -2.5 * kB*Te/e             = {-2.5*kT_over_e:,.1f} V")


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
def _caption(fig, text: str) -> None:
    fig.text(0.5, 0.01, text, ha="center", va="bottom", fontsize=9,
             style="italic")


def fig_delay_range_vs_freq() -> None:
    """P3: excess range and time delay vs frequency at TEC = 1e18."""
    tec = 1.0e18
    f = np.logspace(np.log10(30e6), np.log10(3e9), 500)   # 30 MHz to 3 GHz
    dR = excess_range(tec, f)
    dt = time_delay(tec, f)

    fig, ax1 = plt.subplots(figsize=(7.2, 4.7))
    ax1.loglog(f / 1e6, dR, color="#1f4e79", lw=2, label="excess range")
    ax1.set_xlabel("Transmission frequency  f  (MHz)")
    ax1.set_ylabel("Excess range  $\\Delta R$  (m)", color="#1f4e79")
    ax1.tick_params(axis="y", labelcolor="#1f4e79")
    ax1.grid(True, which="both", alpha=0.3)

    ax2 = ax1.twinx()          # right axis: time delay = dR / c
    ax2.loglog(f / 1e6, dt * 1e6, color="#c00000", lw=0, alpha=0)  # keep scale
    ax2.set_ylabel("Group delay  $\\Delta t$  ($\\mu$s)", color="#c00000")
    ax2.set_ylim(ax1.get_ylim()[0] / C_LIGHT * 1e6,
                 ax1.get_ylim()[1] / C_LIGHT * 1e6)
    ax2.tick_params(axis="y", labelcolor="#c00000")

    for fmark, name, dxy in [(150.0, "150 MHz", (14, 18)),
                             (1600.0, "1.6 GHz", (-70, -28))]:
        Rm = excess_range(tec, fmark * 1e6)
        tm = time_delay(tec, fmark * 1e6)
        ax1.plot(fmark, Rm, "o", color="#385723", ms=6, zorder=5)
        ax1.annotate(f"{name}\n$\\Delta R$={Rm:,.0f} m\n$\\Delta t$={tm*1e6:.3f} $\\mu$s",
                     xy=(fmark, Rm), xytext=dxy, textcoords="offset points",
                     fontsize=8,
                     bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6",
                               alpha=0.95),
                     arrowprops=dict(arrowstyle="->", color="0.5"))
    ax1.set_title("P3: Ionospheric excess range and delay vs frequency "
                  "(TEC = $10^{18}$ e/m$^2$)")
    fig.subplots_adjust(bottom=0.17, right=0.86)
    _caption(fig, "Figure 1: Both fall as $1/f^2$; going from 150 MHz to "
             "1.6 GHz cuts the delay ~114x.")
    fig.savefig(FIG_DIR / "fig1_delay_range_vs_freq.png", dpi=150)
    plt.close(fig)


def fig_charging_current_balance() -> None:
    """P5/P8: electron and ion current density vs bias V, crossing = V_float."""
    T = 1.0e7
    n = 1.0e6            # m^-3, representative GEO density (cancels at crossing)
    v_e = mean_speed(T, M_E)
    v_i = mean_speed(T, M_P)
    J_eo = 0.25 * E_CHG * n * v_e      # A/m^2 reference electron flux
    J_io = 0.25 * E_CHG * n * v_i      # A/m^2 reference ion flux
    kT_e = K_B * T / E_CHG

    V = np.linspace(-4000.0, 0.0, 500)
    J_e = J_eo * np.exp(V / kT_e)          # electrons repelled (V<0)
    J_i = J_io * (1.0 - V / kT_e)          # ions attracted (V<0), linear

    _, Vf = floating_potential_geo(T)
    Jf = J_io * (1.0 - Vf / kT_e)

    fig, ax = plt.subplots(figsize=(7.2, 4.7))
    ax.plot(V, J_e * 1e9, color="#c00000", lw=2, label="electron current $I_e$")
    ax.plot(V, J_i * 1e9, color="#1f4e79", lw=2, label="ion current $I_i$")
    ax.plot(Vf, Jf * 1e9, "o", color="#385723", ms=8, zorder=5)
    ax.annotate(f"balance $I_e=I_i$\n$V_f$ = {Vf:,.0f} V",
                xy=(Vf, Jf * 1e9), xytext=(40, 40),
                textcoords="offset points", fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6"),
                arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.axvline(Vf, color="0.6", ls="--", lw=1)
    ax.set_xlabel("Spacecraft potential  V  (volts)")
    ax.set_ylabel("Current density per collecting area  (nA/m$^2$)")
    ax.set_title("P5/P8: GEO current balance ($T=10^7$ K), floating potential "
                 "where $I_e=I_i$")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", fontsize=9)
    fig.subplots_adjust(bottom=0.17)
    _caption(fig, "Figure 2: Fast electrons drive the sphere negative until "
             "$I_e$ falls to meet $I_i$.")
    fig.savefig(FIG_DIR / "fig2_charging_current_balance.png", dpi=150)
    plt.close(fig)


def fig_debye_vs_density() -> None:
    """P2: Debye length vs electron density for the two ionospheric temps."""
    ne = np.logspace(10, 13, 400)
    fig, ax = plt.subplots(figsize=(7.2, 4.7))
    for Te, color, name in [(1500.0, "#1f4e79", "$T_e$ = 1500 K"),
                            (5000.0, "#c00000", "$T_e$ = 5000 K")]:
        ax.loglog(ne, debye_length(Te, ne) * 1e3, color=color, lw=2, label=name)
    pts = [("(a) 300 km", 1500.0, 5.0e12, (12, 16)),
           ("(b) 1000 km", 5000.0, 1.0e11, (12, -30))]
    for label, Te, n0, dxy in pts:
        lam = debye_length(Te, n0) * 1e3
        ax.plot(n0, lam, "o", color="#385723", ms=7, zorder=5)
        ax.annotate(f"{label}\n$n_e$={n0:.0e} m$^{{-3}}$\n$\\lambda_D$={lam:.2f} mm",
                    xy=(n0, lam), xytext=dxy, textcoords="offset points",
                    fontsize=8,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6",
                              alpha=0.95),
                    arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.set_xlabel("Electron number density  $n_e$  (m$^{-3}$)")
    ax.set_ylabel("Debye length  $\\lambda_D$  (mm)")
    ax.set_title("P2: Debye length vs density (denser = shorter shielding "
                 "distance)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=9)
    fig.subplots_adjust(bottom=0.17)
    _caption(fig, "Figure 3: $\\lambda_D=\\sqrt{\\varepsilon_0 k_B T_e/(n_e e^2)}$; "
             "the hot, tenuous 1000 km plasma shields over ~13x the distance.")
    fig.savefig(FIG_DIR / "fig3_debye_vs_density.png", dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------
def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    FIG_DIR.mkdir(exist_ok=True)
    p2()
    print()
    p3()
    print()
    p5_p8()

    fig_delay_range_vs_freq()
    fig_charging_current_balance()
    fig_debye_vs_density()
    print("\nFigures written to:", FIG_DIR)


if __name__ == "__main__":
    main()
