"""SPCE 5065 Design Project MS1 -- figures and the orbital-decay numbers.

Space Tug (GEO servicing) space-environment analysis. Outputs (written to
./figures/ next to this script):

  fig0_orca_concept.png       Conceptual diagram of the ORCA servicer docking a
                              client (cover-page graphic).
  fig1_orbit_regimes.png      Scaled orbit diagram: Earth, LEO, MEO, GEO, graveyard
                              (Section 5, orbit selection).
  fig2_orbit_propagation.png  GEO orbit propagated over one sidereal day: inertial
                              motion + ground-track analemma (Section 6, visual sim).
  fig3_drag_lifetime.png      Drag-decay lifetime vs. altitude, HW2 model, GEO off
                              scale (Section 7, orbital decay estimation).

Also prints the Section 7 decay numbers and the GEO drag check.

Run: python spce5065_ms1_figs.py
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
M_TUG = 2000.0            # kg
A_TUG = 15.0              # m^2
CD = 2.2                  # -
BC_INV = CD * A_TUG / M_TUG   # m^2/kg   (Cd*A/m)


def rho_hw2(h_km):
    """HW2 thermosphere density fit: rho = 1.020e7 * h^-7.172 (kg/m^3, h in km)."""
    return 1.020e7 * np.power(h_km, -7.172)


def drag_lifetime_days(h0_km: float, n: int = 6000) -> float:
    """Decay time from h0 to H_REENTRY (HW2 a-dot model, SI units)."""
    a0 = R_E_M + h0_km * 1000.0
    af = R_E_M + H_REENTRY * 1000.0
    a = np.linspace(a0, af, n)
    h_km = a / 1000.0 - R_E
    rho_si = rho_hw2(h_km)
    adot = -rho_si * BC_INV * np.sqrt(MU * a)
    t_s = np.trapezoid(1.0 / np.abs(adot), -a)
    return t_s / 86400.0


def geo_drag_check() -> None:
    rho_geo = 1.0e-15
    a_geo = R_E_M + 35786.0 * 1000.0
    v_geo = np.sqrt(MU / a_geo) / 1000.0
    adot = rho_geo * BC_INV * np.sqrt(MU * a_geo)
    tau_yr = (a_geo / adot) / (86400.0 * 365.25)
    print(f"GEO check: rho ~ {rho_geo:.0e} kg/m^3, v = {v_geo:.3f} km/s")
    print(f"  characteristic drag-decay timescale ~ {tau_yr:.1e} yr "
          f"(~{tau_yr/5:.0e} x the 5-yr mission; drag is not the life-limiter)")


# --------------------------------------------------------------------------
# Fig 0 -- ORCA conceptual diagram (cover graphic)
# --------------------------------------------------------------------------
def fig_concept() -> None:
    fig, ax = plt.subplots(figsize=(9.0, 5.2))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")
    ax.set_facecolor("#0B1020")
    fig.patch.set_facecolor("#0B1020")

    gold = "#C9A227"
    body = "#D8DCE3"
    arr = "#2E5E8C"

    # --- ORCA servicer (left) ---
    ax.add_patch(mpatches.FancyBboxPatch((3.0, 3.4), 2.4, 2.2,
                 boxstyle="round,pad=0.05", fc=body, ec="0.3", lw=1.2))
    ax.text(4.2, 4.5, "ORCA\nservicer", ha="center", va="center",
            fontsize=9, weight="bold", color="#111")
    # solar arrays
    for dy in (2.35, -2.35):
        ax.add_patch(mpatches.Rectangle((3.6, 4.5 + dy - 0.55), 1.2, 1.1,
                     fc=arr, ec="0.25"))
        ax.plot([4.2, 4.2], [4.5, 4.5 + dy], color="0.5", lw=1)
    # thrusters (left face)
    for dy in (-0.6, 0.0, 0.6):
        ax.add_patch(mpatches.Polygon([[3.0, 4.5 + dy - 0.12], [3.0, 4.5 + dy + 0.12],
                     [2.6, 4.5 + dy]], closed=True, fc="#E67E22", ec="0.3"))
    # docking probe + robotic arm (right face, toward client)
    ax.add_patch(mpatches.Rectangle((5.4, 4.35), 1.4, 0.3, fc="#7F8C8D", ec="0.3"))
    ax.plot([5.4, 6.4, 7.2], [3.9, 3.5, 3.9], color="#95A5A6", lw=3,
            solid_capstyle="round")
    ax.add_patch(mpatches.Circle((6.9, 4.5), 0.18, fc="#111", ec=gold, lw=1.5))

    # --- client satellite (right) ---
    ax.add_patch(mpatches.FancyBboxPatch((9.6, 3.7), 1.8, 1.6,
                 boxstyle="round,pad=0.05", fc="#B7BCC4", ec="0.3", lw=1.1))
    ax.text(10.5, 4.5, "client\ncomsat", ha="center", va="center",
            fontsize=8.5, color="#111")
    ax.add_patch(mpatches.Rectangle((8.4, 4.0), 1.1, 1.0, fc=arr, ec="0.25"))
    ax.add_patch(mpatches.Rectangle((11.4, 4.0), 1.1, 1.0, fc=arr, ec="0.25"))

    # approach arrow
    ax.annotate("", xy=(9.4, 4.5), xytext=(7.4, 4.5),
                arrowprops=dict(arrowstyle="-|>", color=gold, lw=2))
    ax.text(8.4, 4.95, "rendezvous\n& dock", ha="center", va="bottom",
            fontsize=8, color=gold, style="italic")

    # labels with leader lines
    labels = [
        ("Solar arrays", (4.2, 7.0), (5.4, 6.9)),
        ("RPO sensors +\ndocking mechanism", (6.9, 4.5), (7.8, 6.4)),
        ("Robotic arm", (6.4, 3.5), (7.6, 2.3)),
        ("Station-keeping\nthrusters", (2.7, 4.5), (1.3, 6.2)),
    ]
    for text, xy, xytext in labels:
        ax.annotate(text, xy=xy, xytext=xytext, fontsize=8, color="#E6EDF3",
                    ha="center",
                    arrowprops=dict(arrowstyle="->", color="#8892A0", lw=1))

    ax.set_title("ORCA: GEO Repair and Cooperative Assist servicing tug",
                 fontsize=12, color="#E6EDF3", pad=10)
    fig.savefig(FIG_DIR / "fig0_orca_concept.png", dpi=150, facecolor="#0B1020")
    plt.close(fig)


# --------------------------------------------------------------------------
# Fig 1 -- scaled orbit-regime diagram (section 5)
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
        ax.add_patch(plt.Circle((0, 0), r, fill=False, ec=color, lw=2, ls=ls,
                                label=label))
    ax.add_patch(plt.Circle((0, 0), R_E, fc="#2E5E8C", ec="#1B3A57", lw=1.2))
    ax.text(0, 0, "Earth", ha="center", va="center", color="white",
            fontsize=10, weight="bold")
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
# Fig 2 -- propagated orbit simulation (section 6, visual simulation)
# --------------------------------------------------------------------------
def fig_orbit_propagation() -> None:
    a = R_E + 35786.0
    T = 86164.0
    n = 2.0 * np.pi / T
    slot_lon = -105.0

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(11.4, 5.4))

    axA.set_aspect("equal")
    theta = np.linspace(0, 2 * np.pi, 400)
    axA.plot(a * np.cos(theta), a * np.sin(theta), color="#C0392B", lw=1.6,
             label="GEO orbit")
    axA.add_patch(plt.Circle((0, 0), R_E, fc="#2E5E8C", ec="#1B3A57"))
    t_hr = np.arange(0, 25) * 3600.0
    u_hr = n * t_hr
    axA.plot(a * np.cos(u_hr), a * np.sin(u_hr), "o", color="#E67E22", ms=4,
             label="satellite, hourly")
    axA.plot(a, 0, "s", color="#C0392B", ms=10, zorder=5)
    axA.annotate("t = 0", xy=(a, 0), xytext=(8, 10),
                 textcoords="offset points", fontsize=8.5)
    lim = a * 1.15
    axA.set_xlim(-lim, lim)
    axA.set_ylim(-lim, lim)
    axA.set_xlabel("ECI x (km)")
    axA.set_ylabel("ECI y (km)")
    axA.set_title("(A) Inertial orbit, propagated over 1 sidereal day")
    axA.grid(True, alpha=0.2)
    axA.legend(loc="upper right", fontsize=8)

    u = np.linspace(0, 2 * np.pi, 721)
    cases = [(5.0, "#E67E22", "~6 yr drift, no N-S SK"),
             (15.0, "#C0392B", "~26.5 yr drift, no N-S SK")]
    for inc_deg, color, label in cases:
        i = np.radians(inc_deg)
        alpha = np.arctan2(np.sin(u) * np.cos(i), np.cos(u))
        dlon = np.degrees(np.unwrap(alpha - u))
        dlon = (dlon + 180) % 360 - 180
        lat = np.degrees(np.arcsin(np.sin(u) * np.sin(i)))
        axB.plot(slot_lon + dlon, lat, color=color, lw=1.8, label=label)
    # station-kept case holds a point (an inclined analemma collapses to the slot)
    axB.plot(slot_lon, 0, "o", color="#27AE60", ms=9, zorder=6,
             label="station-kept (holds the point)")
    axB.annotate("assigned slot\n(105 W)", xy=(slot_lon, 0), xytext=(12, -18),
                 textcoords="offset points", fontsize=8)
    axB.set_xlabel("Longitude (deg)")
    axB.set_ylabel("Latitude (deg)")
    axB.set_title("(B) Ground track over 1 sidereal day")
    axB.set_xlim(slot_lon - 6, slot_lon + 6)
    axB.set_ylim(-18, 18)
    axB.grid(True, alpha=0.3)
    axB.legend(loc="upper right", fontsize=7.5)

    fig.text(0.5, 0.01, "Figure 2: GEO orbit propagated over one sidereal day. "
             "The satellite holds one longitude, but without N-S station-keeping "
             "the inclination grows and the ground track opens into an analemma.",
             ha="center", va="bottom", fontsize=8.5, style="italic")
    fig.subplots_adjust(bottom=0.16, wspace=0.28)
    fig.savefig(FIG_DIR / "fig2_orbit_propagation.png", dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------
# Fig 3 -- drag lifetime vs altitude (section 7, orbital decay estimation)
# --------------------------------------------------------------------------
def fig_drag_lifetime() -> None:
    alts = np.arange(250, 1001, 25)
    life = np.array([drag_lifetime_days(h) for h in alts]) / 365.25

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
    ax.set_title("Section 7: LEO drag lifetime for the tug (HW2 model); "
                 "GEO is off-scale", fontsize=11)
    ax.grid(True, which="both", alpha=0.3)
    ax.text(0.98, 0.06, "GEO (35,786 km): drag decay ~10$^{5}$ to 10$^{6}$ yr,\n"
            "not the life-limiting mechanism",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.35", fc="#FDECEA", ec="#C0392B"))
    fig.subplots_adjust(bottom=0.14)
    fig.text(0.5, 0.005, "Figure 3: Using the HW2 neutral-density model, LEO "
             "lifetime rises steeply with altitude; at GEO drag is negligible.",
             ha="center", va="bottom", fontsize=8.5, style="italic")
    fig.savefig(FIG_DIR / "fig3_drag_lifetime.png", dpi=150)
    plt.close(fig)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    FIG_DIR.mkdir(exist_ok=True)
    print("=" * 64)
    print("MS1 Section-7 decay numbers (tug: m=2000 kg, A=15 m^2, Cd=2.2)")
    print(f"  inverse ballistic coeff Cd*A/m = {BC_INV:.5f} m^2/kg")
    print("=" * 64)
    for h in (300, 400, 500, 600, 800):
        d = drag_lifetime_days(h)
        print(f"  LEO what-if at {h:4d} km: decay to 150 km in "
              f"{d:8.1f} days = {d/365.25:6.2f} yr")
    print()
    geo_drag_check()
    fig_concept()
    fig_orbit_regimes()
    fig_orbit_propagation()
    fig_drag_lifetime()
    print("\nFigures written to:", FIG_DIR)


if __name__ == "__main__":
    main()
