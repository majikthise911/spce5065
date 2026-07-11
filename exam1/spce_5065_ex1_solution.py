"""SPCE 5065 -- Midterm, Problem 6 solution.

The neutral-environment quantitative problem: atomic-oxygen erosion and
atmospheric drag on a Starlink-class satellite.

  P6a  Max AO erosion depth of a 300 um Mylar RAM cover over 5 yr at 550 km
       (high solar activity, n_O = 1e8 atoms/cm^3). Problem or not?
  P6b  Altitude decay over 5 yr with no station-keeping, using the given
       decay-rate model and density fit (evaluated at 350 km / R=6728 km).
  P6c  With a 50 um cover and a 150 km deorbit altitude, is drag or erosion
       the bigger concern?

Outputs:
  - Console tables reproducing every boxed number in the submission
  - figures/fig1_erosion_vs_time.png   (P6a/P6c)
  - figures/fig2_altitude_decay.png    (P6b/P6c)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------
MU = 3.986e14                 # m^3/s^2   Earth GM
R_E = 6378.0e3               # m         Earth radius (exam uses R_E = 6378 km)
YEAR_S = 365.25 * 86400.0     # s/yr
T_MISSION = 5.0 * YEAR_S      # s         5-year mission

# Mylar (PET) atomic-oxygen reaction efficiency. Tribble, "The Space
# Environment," neutral-environment chapter. Kapton-H reference is
# 3.0e-24 cm^3/atom; Mylar is slightly higher.
RE_MYLAR = 3.4e-24            # cm^3/atom
RE_KAPTON = 3.0e-24          # cm^3/atom (robustness check)

FIG_DIR = Path(__file__).parent / "figures"


# --------------------------------------------------------------------------
# P6a -- atomic-oxygen erosion
# --------------------------------------------------------------------------
def orbital_velocity(alt_m: float) -> float:
    """Circular orbital (RAM) velocity, m/s.  v = sqrt(mu / (R_E + h))."""
    return np.sqrt(MU / (R_E + alt_m))


def erosion_depth_um(reaction_eff_cm3: float, n_cm3: float,
                     v_ms: float, t_s: float) -> float:
    """AO erosion depth (um).  depth = Re * fluence,  fluence = n * v * t.

    n in atoms/cm^3, v converted to cm/s, so fluence is atoms/cm^2 and
    Re*fluence is cm; convert to um.
    """
    v_cms = v_ms * 100.0
    fluence = n_cm3 * v_cms * t_s          # atoms/cm^2
    depth_cm = reaction_eff_cm3 * fluence  # cm
    return depth_cm * 1.0e4                 # um


def p6a() -> dict:
    print("=" * 70)
    print("P6a -- AO erosion of a 300 um Mylar RAM cover at 550 km, high activity")
    print("=" * 70)
    alt = 550.0e3
    n_o = 1.0e8                             # atoms/cm^3 (given)
    v = orbital_velocity(alt)
    v_cms = v * 100.0
    fluence = n_o * v_cms * T_MISSION
    depth = erosion_depth_um(RE_MYLAR, n_o, v, T_MISSION)
    depth_k = erosion_depth_um(RE_KAPTON, n_o, v, T_MISSION)
    t_penetrate = 300.0 / depth * 5.0       # yr to erode 300 um
    print(f"  RAM velocity  v          = {v:.1f} m/s  ({v/1000:.3f} km/s)")
    print(f"  AO fluence  F = n*v*t    = {fluence:.3e} atoms/cm^2")
    print(f"  Erosion depth (Mylar 3.4e-24)  = {depth:.1f} um")
    print(f"  Erosion depth (Kapton 3.0e-24) = {depth_k:.1f} um  (robustness)")
    print(f"  Cover thickness          = 300 um")
    print(f"  -> {'PROBLEM: cover fully eroded' if depth > 300 else 'OK'} "
          f"(penetrates at t = {t_penetrate:.2f} yr)")
    return {"v": v, "fluence": fluence, "depth": depth,
            "depth_k": depth_k, "t_penetrate": t_penetrate}


# --------------------------------------------------------------------------
# P6b -- altitude decay
# --------------------------------------------------------------------------
def density_model(alt_km: float) -> float:
    """Given exam density fit, rho = 1.02e7 * x^(-7.172) kg/m^3, x = alt in km."""
    return 1.02e7 * alt_km ** (-7.172)


def decay_rate(alt_km: float, R_m: float, bc: float) -> float:
    """dR/dt = -(rho / BC) * sqrt(mu * R),  m/s (given exam model)."""
    rho = density_model(alt_km)
    return -(rho / bc) * np.sqrt(MU * R_m)


def p6b() -> dict:
    print("=" * 70)
    print("P6b -- 5-year altitude decay, no station-keeping")
    print("=" * 70)
    bc = 103.0                              # kg/m^2 (given; in the typical 25-200 band)
    alt_avg = 350.0                         # km, given for the density calc
    R_avg = 6728.0e3                        # m, given
    rho = density_model(alt_avg)
    dRdt = decay_rate(alt_avg, R_avg, bc)
    decay_5yr = dRdt * T_MISSION            # m
    print(f"  BC                        = {bc:.0f} kg/m^2")
    print(f"  rho(350 km)               = {rho:.3e} kg/m^3")
    print(f"  dR/dt                     = {dRdt*1000:.4f} mm/s "
          f"= {dRdt*86400/1000:.4f} km/day")
    print(f"  5-yr decay (constant rate) = {decay_5yr/1000:.1f} km")
    print(f"  -> from 550 km start, ends near {550 + decay_5yr/1000:.0f} km "
          f"(i.e. reenters within 5 yr)")
    return {"bc": bc, "rho": rho, "dRdt": dRdt, "decay_5yr_km": decay_5yr / 1000}


# --------------------------------------------------------------------------
# P6c -- drag vs erosion for a 50 um cover
# --------------------------------------------------------------------------
def p6c(a: dict, b: dict) -> dict:
    print("=" * 70)
    print("P6c -- 50 um cover, 150 km deorbit: drag or erosion first?")
    print("=" * 70)
    # erosion time for 50 um at the 550 km rate from P6a
    rate_um_per_yr = a["depth"] / 5.0
    t_erode_50 = 50.0 / rate_um_per_yr
    # drag: reuse the P6b constant-rate estimate (same method the exam sanctions)
    # time to fall the 400 km from 550 km down to the 150 km deorbit altitude
    rate_km_per_yr = abs(b["dRdt"]) * YEAR_S / 1000.0
    t_deorbit = (550.0 - 150.0) / rate_km_per_yr
    print(f"  Erosion rate (550 km)      = {rate_um_per_yr:.1f} um/yr")
    print(f"  Time to erode 50 um cover  = {t_erode_50:.2f} yr")
    print(f"  Drag rate (P6b estimate)   = {rate_km_per_yr:.1f} km/yr")
    print(f"  Time to drag down to 150 km = {t_deorbit:.2f} yr")
    print(f"  -> {'EROSION' if t_erode_50 < t_deorbit else 'DRAG'} is the "
          f"bigger concern (happens first)")
    return {"t_erode_50": t_erode_50, "t_deorbit": t_deorbit,
            "rate_um_per_yr": rate_um_per_yr, "rate_km_per_yr": rate_km_per_yr}


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
def _caption(fig, text: str) -> None:
    fig.text(0.5, 0.01, text, ha="center", va="bottom", fontsize=9, style="italic")


def fig_erosion(a: dict, c: dict) -> None:
    t = np.linspace(0, 5, 200)
    depth = a["depth"] / 5.0 * t                    # linear at fixed 550 km rate
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.plot(t, depth, color="#1f4e79", lw=2, label="cumulative erosion (RAM, high activity)")
    ax.axhline(300, color="#c00000", ls="--", lw=1.4)
    ax.axhline(50, color="#bf8f00", ls="--", lw=1.4)
    ax.axvline(a["t_penetrate"], color="#c00000", ls=":", lw=1)
    ax.axvline(c["t_erode_50"], color="#bf8f00", ls=":", lw=1)
    ax.annotate(f"300 um cover breached\nat {a['t_penetrate']:.1f} yr",
                xy=(a["t_penetrate"], 300), xytext=(-150, -20),
                textcoords="offset points", fontsize=8,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6"),
                arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.annotate(f"50 um cover breached\nat {c['t_erode_50']:.1f} yr",
                xy=(c["t_erode_50"], 50), xytext=(20, 60),
                textcoords="offset points", fontsize=8,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6"),
                arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.set_xlabel("Time on orbit (years)")
    ax.set_ylabel("Cumulative AO erosion depth (um)")
    ax.set_title("P6a/P6c: Mylar erosion vs. cover thickness (550 km, high activity)")
    ax.set_xlim(0, 5)
    ax.set_ylim(0, max(420, a["depth"] * 1.03))
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, loc="upper left")
    fig.subplots_adjust(bottom=0.18)
    _caption(fig, "Figure 1: Cumulative atomic-oxygen erosion depth; dashed lines "
             "are the 300 um and 50 um cover thicknesses.")
    fig.savefig(FIG_DIR / "fig1_erosion_vs_time.png", dpi=150)
    plt.close(fig)


def fig_decay(b: dict, c: dict) -> None:
    # constant-rate estimate line from P6b, extended until it reaches 150 km
    t_end = c["t_deorbit"] * 1.05
    t_lin = np.linspace(0, t_end, 200)
    alt_lin = 550 + b["dRdt"] * (t_lin * YEAR_S) / 1000.0
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.plot(t_lin, alt_lin, color="#385723", lw=2,
            label=f"P6b constant-rate decay ({b['decay_5yr_km']:.0f} km/5 yr)")
    ax.axhline(150, color="#c00000", ls=":", lw=1.2)
    ax.text(0.15, 160, "150 km deorbit", fontsize=8, color="#c00000")
    ax.plot(c["t_deorbit"], 150, "o", color="#c00000", ms=6)
    ax.annotate(f"reaches 150 km\nat {c['t_deorbit']:.1f} yr",
                xy=(c["t_deorbit"], 150), xytext=(-120, 30),
                textcoords="offset points", fontsize=8,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6"),
                arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.axvline(c["t_erode_50"], color="#bf8f00", ls="--", lw=1.4)
    ax.annotate(f"50 um cover eroded through\nat {c['t_erode_50']:.1f} yr (erosion wins)",
                xy=(c["t_erode_50"], 480), xytext=(40, -4),
                textcoords="offset points", fontsize=8,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#bf8f00"),
                arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.set_xlabel("Time on orbit (years)")
    ax.set_ylabel("Altitude (km)")
    ax.set_title("P6b/P6c: Altitude decay from 550 km, no station-keeping")
    ax.set_xlim(0, t_end)
    ax.set_ylim(100, 560)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, loc="upper right")
    fig.subplots_adjust(bottom=0.18)
    _caption(fig, "Figure 2: Constant-rate orbital decay to the 150 km deorbit "
             "altitude; erosion breaches the 50 um cover long before drag deorbits it.")
    fig.savefig(FIG_DIR / "fig2_altitude_decay.png", dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------
def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    FIG_DIR.mkdir(exist_ok=True)
    a = p6a()
    print()
    b = p6b()
    print()
    c = p6c(a, b)
    fig_erosion(a, c)
    fig_decay(b, c)
    print("\nFigures written to:", FIG_DIR)


if __name__ == "__main__":
    main()
