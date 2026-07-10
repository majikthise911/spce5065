"""SPCE 5065 Design Project MS1 -- figures and the section-6 lifetime numbers.

Space Tug (GEO servicing) space-environment analysis. Two outputs:

  fig1_orbit_regimes.png   Scaled orbit diagram: Earth, LEO, MEO, GEO, and the
                           GEO graveyard, with the tug parked at GEO (section 7).
  fig2_drag_lifetime.png   Drag-decay lifetime vs starting altitude in LEO using
                           the HW2 neutral-density model, with GEO annotated as
                           effectively infinite (section 6).

Also prints the section-6 numbers: the LEO "what-if" decay lifetime for the tug's
ballistic coefficient, and a check that GEO drag decay is not life-limiting.

Run: python spce5065_ms1_figs.py  -> writes PNGs to ./figures/ and prints numbers.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

FIG_DIR = Path(__file__).parent / "figures"

# Constants (SI: meters, seconds)
MU = 3.986004418e14       # m^3/s^2   Earth gravitational parameter
R_E = 6378.137            # km        Earth equatorial radius
R_E_M = R_E * 1000.0      # m
H_REENTRY = 150.0         # km        assumed reentry altitude (HW2 convention)

# Tug (MEV-class servicing vehicle) drag properties for the LEO what-if case
M_TUG = 2000.0            # kg   representative wet mass
A_TUG = 15.0              # m^2  ram area with arrays
CD = 2.2                  # -    free-molecular drag coefficient
BC_INV = CD * A_TUG / M_TUG   # m^2/kg   (Cd*A/m), inverse ballistic coefficient


def rho_hw2(h_km: np.ndarray | float) -> np.ndarray | float:
    """HW2 thermosphere density fit: rho = 1.020e7 * h^-7.172 (kg/m^3, h in km).

    Valid in the LEO band (roughly 150 to ~1000 km). It is NOT valid at GEO; at
    GEO a standard model gives ~1e-15 kg/m^3, which we handle separately.
    """
    return 1.020e7 * np.power(h_km, -7.172)


def drag_lifetime_days(h0_km: float, n: int = 6000) -> float:
    """Time to decay from h0 to H_REENTRY using the HW2 a-dot model, in SI.

    a_dot = -rho(h) * (Cd*A/m) * sqrt(mu*a),  integrated as t = int da / |a_dot|.
    Everything in meters and seconds: mu [m^3/s^2], a [m], rho [kg/m^3],
    Cd*A/m [m^2/kg]  ->  a_dot [m/s].
    """
    a0 = R_E_M + h0_km * 1000.0
    af = R_E_M + H_REENTRY * 1000.0
    a = np.linspace(a0, af, n)          # m
    h_km = a / 1000.0 - R_E             # km, for the density fit
    rho_si = rho_hw2(h_km)              # kg/m^3
    adot = -rho_si * BC_INV * np.sqrt(MU * a)   # m/s (negative)
    integrand = 1.0 / np.abs(adot)      # s/m
    t_s = np.trapezoid(integrand, -a)   # -a increases as the sat descends
    return t_s / 86400.0


def geo_drag_check() -> None:
    """Show that GEO drag decay is not life-limiting (SI units)."""
    rho_geo = 1.0e-15                   # kg/m^3, standard GEO neutral density
    a_geo = R_E_M + 35786.0 * 1000.0    # m
    v_geo = np.sqrt(MU / a_geo) / 1000.0   # km/s
    adot = rho_geo * BC_INV * np.sqrt(MU * a_geo)   # m/s
    tau_yr = (a_geo / adot) / (86400.0 * 365.25)
    print(f"GEO check: rho ~ {rho_geo:.0e} kg/m^3, v = {v_geo:.3f} km/s")
    print(f"  characteristic drag-decay timescale ~ {tau_yr:.1e} yr "
          f"(~{tau_yr/5:.0e} x the 5-yr mission; drag is not the life-limiter)")


# --------------------------------------------------------------------------
# Fig 1 -- scaled orbit-regime diagram (section 7)
# --------------------------------------------------------------------------
def fig_orbit_regimes() -> None:
    fig, ax = plt.subplots(figsize=(7.4, 7.4))
    ax.set_aspect("equal")

    regimes = [
        (R_E + 400, "LEO  (400 km)", "#3B82C4", ":"),
        (R_E + 20200, "MEO  (20,200 km)", "#8E6FC7", "--"),
        (R_E + 35786, "GEO  (35,786 km)", "#C0392B", "-"),
        (R_E + 36086, "GEO graveyard (+300 km)", "#7F8C8D", (0, (2, 3))),
    ]
    for r, label, color, ls in regimes:
        circ = plt.Circle((0, 0), r, fill=False, ec=color, lw=2, ls=ls,
                          label=label)
        ax.add_patch(circ)

    # Earth
    ax.add_patch(plt.Circle((0, 0), R_E, fc="#2E5E8C", ec="#1B3A57", lw=1.2))
    ax.text(0, 0, "Earth", ha="center", va="center", color="white",
            fontsize=10, weight="bold")

    # tug + a client comsat on the GEO ring
    r_geo = R_E + 35786
    ax.plot(r_geo, 0, marker="s", ms=11, color="#C0392B", zorder=5)
    ax.annotate("ORCA tug\n(parked at GEO)", xy=(r_geo, 0), xytext=(14, 20),
                textcoords="offset points", fontsize=9, ha="left",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6"),
                arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.plot(r_geo * np.cos(np.radians(35)), r_geo * np.sin(np.radians(35)),
            marker="o", ms=8, color="#E67E22", zorder=5)
    ax.annotate("client comsat", xy=(r_geo * np.cos(np.radians(35)),
                r_geo * np.sin(np.radians(35))), xytext=(10, 10),
                textcoords="offset points", fontsize=8.5, ha="left",
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="0.6"),
                arrowprops=dict(arrowstyle="->", color="0.5"))

    lim = (R_E + 35786) * 1.18
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim * 1.02)
    ax.set_xlabel("km")
    ax.set_ylabel("km")
    ax.set_title("Orbit regimes to scale: ORCA services at GEO", fontsize=12)
    ax.grid(True, alpha=0.2)
    ax.legend(loc="upper left", fontsize=8.5, framealpha=0.92,
              title="Orbital regime")
    fig.text(0.5, 0.005, "Figure 1: Equatorial view to scale. The tug operates in "
             "the GEO belt (35,786 km), rescuing clients to and from the graveyard.",
             ha="center", va="bottom", fontsize=8.5, style="italic")
    fig.subplots_adjust(bottom=0.10)
    fig.savefig(FIG_DIR / "fig1_orbit_regimes.png", dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------
# Fig 2 -- drag lifetime vs altitude (section 6)
# --------------------------------------------------------------------------
def fig_drag_lifetime() -> None:
    alts = np.arange(250, 1001, 25)
    life = np.array([drag_lifetime_days(h) for h in alts]) / 365.25   # years

    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    ax.semilogy(alts, life, color="#1f4e79", lw=2)
    ax.axhline(5.0, color="#C0392B", ls="--", lw=1.3)
    ax.text(255, 6.2, "5-yr mission requirement", color="#C0392B", fontsize=8.5)

    h400 = 400
    l400 = drag_lifetime_days(h400) / 365.25
    ax.plot(h400, l400, "o", color="#C0392B", ms=6)
    ax.annotate(f"tug at 400 km:\n{l400*365.25:.0f} days ({l400:.2f} yr)",
                xy=(h400, l400), xytext=(20, 10), textcoords="offset points",
                fontsize=8.5, bbox=dict(boxstyle="round,pad=0.3", fc="white",
                ec="0.6"), arrowprops=dict(arrowstyle="->", color="0.5"))

    ax.set_xlabel("Starting altitude (km)")
    ax.set_ylabel("Drag-decay lifetime (years, log scale)")
    ax.set_title("Section 6: LEO drag lifetime for the tug (HW2 model); "
                 "GEO is off-scale", fontsize=11)
    ax.grid(True, which="both", alpha=0.3)
    ax.text(0.98, 0.06, "GEO (35,786 km): drag decay ~10$^{5}$ to 10$^{6}$ yr,\n"
            "not the life-limiting mechanism",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.35", fc="#FDECEA", ec="#C0392B"))
    fig.subplots_adjust(bottom=0.14)
    fig.text(0.5, 0.005, "Figure 2: Using the HW2 neutral-density model, LEO "
             "lifetime rises steeply with altitude; at GEO drag is negligible.",
             ha="center", va="bottom", fontsize=8.5, style="italic")
    fig.savefig(FIG_DIR / "fig2_drag_lifetime.png", dpi=150)
    plt.close(fig)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    FIG_DIR.mkdir(exist_ok=True)
    print("=" * 64)
    print("MS1 section-6 lifetime numbers (tug: m=2000 kg, A=15 m^2, Cd=2.2)")
    print(f"  inverse ballistic coeff Cd*A/m = {BC_INV:.5f} m^2/kg")
    print("=" * 64)
    for h in (300, 400, 500, 600, 800):
        d = drag_lifetime_days(h)
        print(f"  LEO what-if at {h:4d} km: decay to 150 km in "
              f"{d:8.1f} days = {d/365.25:6.2f} yr")
    print()
    geo_drag_check()
    fig_orbit_regimes()
    fig_drag_lifetime()
    print("\nFigures written to:", FIG_DIR)


if __name__ == "__main__":
    main()
