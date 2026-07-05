"""SPCE 5065 -- Homework 2 solution.

Atmospheric drag, orbital decay/lifetime, and atomic-oxygen erosion. Covers the
quantitative parts of HW2:

  P1  Drag lifetime of a 100 kg / 1 m^2 / Cd=2.2 satellite, 400 km -> 150 km,
      using the altitude-varying thermosphere density power law (no constant R).
  P2  Drag-makeup fuel to hold the 400 km orbit for one year (Isp = 200 s).
  P3  Kapton ram-face erosion depth per year at 450 km, low/med/high AO density.
  P4a Mass of oxygen in the Apollo command module (ideal gas).
  P5  Lifetime vs. starting altitude for all start altitudes 200-500 km.
  P6b ISS Kapton ram erosion over one year, anchored to MISSE-2 PEACE fluence.

Density model (problem statement, valid >150 km, h in km, rho in kg/m^3):
  rho(h) = 1.020e7 * h^(-7.172)

Drag/decay model (Lesson 2): F_drag = -1/2 rho Cd A v^2, energy of a circular
orbit E = -m mu / (2a), dE/dt = -1/2 rho Cd A v^3, which collapses to
  da/dt = -rho (Cd A / m) sqrt(mu a)
so the lifetime is the closed integral
  t = integral_{a_f}^{a_0} da / [ rho(h) (Cd A/m) sqrt(mu a) ].
Because rho, v, and a all change as the satellite falls, this is integrated
numerically -- that is exactly what "do not assume an average R" requires.

Outputs:
  - Console tables reproducing every boxed number in the submission
  - figures/fig1_lifetime_vs_altitude.png   (P5)
  - figures/fig2_decay_profile.png          (P1)
  - figures/fig3_kapton_erosion.png         (P3)

Conceptual parts (P4b, P6a) are answered in the submission document.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad, solve_ivp

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------
MU = 3.986004418e14          # m^3/s^2   Earth gravitational parameter
R_E = 6378.137e3             # m         Earth equatorial radius
G0 = 9.80665                 # m/s^2     standard gravity (rocket equation)
R_UNIV = 8.314462618         # J/(mol*K) universal gas constant
M_O2 = 0.0319988             # kg/mol    molar mass of O2
YEAR_S = 365.25 * 86400.0    # s         one year

# Spacecraft (P1/P2/P5)
M_SAT = 100.0                # kg
A_SAT = 1.0                  # m^2
CD = 2.2                     # drag coefficient
BC = CD * A_SAT / M_SAT      # m^2/kg    inverse ballistic coeff (Cd A / m)

# Kapton atomic-oxygen erosion yield (Ch. 7 Table 7-3 ~ 3.04e-24; course 3.1e-24)
E_KAPTON = 3.0e-24           # cm^3/atom

FIG_DIR = Path(__file__).parent / "figures"


# --------------------------------------------------------------------------
# Atmosphere + orbit helpers
# --------------------------------------------------------------------------
def rho(h_km: float | np.ndarray) -> float | np.ndarray:
    """Thermosphere density (kg/m^3) from the HW power-law fit, h in km."""
    return 1.020e7 * np.asarray(h_km, dtype=float) ** (-7.172)


def v_circ(h_km: float) -> float:
    """Circular orbital speed (m/s) at altitude h (km).  v = sqrt(mu/a)."""
    return np.sqrt(MU / (R_E + h_km * 1.0e3))


# --------------------------------------------------------------------------
# P1 / P5 -- drag lifetime by numerical integration
# --------------------------------------------------------------------------
def _life_integrand(a: float) -> float:
    """dt/da = 1 / [rho (Cd A/m) sqrt(mu a)] with rho evaluated at the
    instantaneous altitude (km).  R = a is NOT frozen."""
    h_km = (a - R_E) / 1.0e3
    return 1.0 / (rho(h_km) * BC * np.sqrt(MU * a))


def lifetime(h0_km: float, hf_km: float = 150.0) -> float:
    """Orbital lifetime (s) decaying from h0 to the hf deorbit altitude."""
    a0 = R_E + h0_km * 1.0e3
    af = R_E + hf_km * 1.0e3
    val, _ = quad(_life_integrand, af, a0, limit=400)
    return val


def decay_profile(h0_km: float, hf_km: float = 150.0):
    """Integrate da/dt to get altitude vs. time for the decay-history figure."""
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
    t_days = sol.t / 86400.0
    h_km = (sol.y[0] - R_E) / 1.0e3
    return t_days, h_km


def p1_p5() -> dict:
    print("=" * 72)
    print("P1 -- drag lifetime 400 km -> 150 km (varying R, rho, v)")
    print("=" * 72)
    t1 = lifetime(400.0, 150.0)
    print(f"  rho(400 km) = {rho(400.0):.4e} kg/m^3,  v(400 km) = {v_circ(400.0):.1f} m/s")
    print(f"  Cd A/m = {BC:.4f} m^2/kg")
    print(f"  lifetime = {t1:.4e} s = {t1/86400:.2f} days = {t1/YEAR_S:.3f} yr")

    print("\n" + "=" * 72)
    print("P5 -- lifetime vs. starting altitude (200-500 km)")
    print("=" * 72)
    starts = [200, 250, 300, 350, 400, 450, 500]
    for h0 in starts:
        t = lifetime(float(h0), 150.0)
        print(f"  {h0:3d} km -> {t/86400:9.2f} days = {t/YEAR_S:7.3f} yr")
    return {"t1_days": t1 / 86400.0, "starts": starts}


# --------------------------------------------------------------------------
# P2 -- drag-makeup fuel for one year at 400 km
# --------------------------------------------------------------------------
def p2() -> dict:
    print("\n" + "=" * 72)
    print("P2 -- drag-makeup fuel, 400 km, 1 year, Isp = 200 s")
    print("=" * 72)
    h = 400.0
    v = v_circ(h)
    a_drag = 0.5 * rho(h) * v ** 2 * BC          # m/s^2 (= 1/2 rho v^2 Cd A / m)
    dv = a_drag * YEAR_S                          # m/s, drag decel held one year
    isp = 200.0
    dm = M_SAT * (1.0 - np.exp(-dv / (isp * G0)))  # rocket equation
    dm_lin = M_SAT * dv / (isp * G0)               # small-burn approximation
    print(f"  drag decel a_d = 1/2 rho v^2 (Cd A/m) = {a_drag:.4e} m/s^2")
    print(f"  delta-v over 1 yr = {dv:.2f} m/s")
    print(f"  fuel (rocket eqn) = {dm:.3f} kg   (linear approx {dm_lin:.3f} kg)")
    return {"dv": dv, "dm": dm}


# --------------------------------------------------------------------------
# P3 -- Kapton ram erosion at 450 km
# --------------------------------------------------------------------------
def p3() -> dict:
    print("\n" + "=" * 72)
    print("P3 -- Kapton ram erosion at 450 km (low/med/high AO density)")
    print("=" * 72)
    v_cms = v_circ(450.0) * 100.0                 # cm/s
    print(f"  v(450 km) = {v_circ(450.0):.1f} m/s = {v_cms:.4e} cm/s")
    cases = {"low": 6e6, "medium": 2e7, "high": 1e8}  # atoms/cm^3
    out = {}
    for label, n in cases.items():
        fluence = n * v_cms * YEAR_S              # atoms/cm^2/yr
        depth_cm = E_KAPTON * fluence
        out[label] = depth_cm * 1.0e4             # micron/yr
        print(f"  {label:6s}: n={n:.0e}  Phi={fluence:.3e} atoms/cm^2/yr  "
              f"depth={depth_cm*1e4:7.2f} um/yr")
    return out


# --------------------------------------------------------------------------
# P4a -- oxygen mass in the Apollo command module
# --------------------------------------------------------------------------
def p4a() -> dict:
    print("\n" + "=" * 72)
    print("P4a -- O2 mass in the Apollo command module")
    print("=" * 72)
    p_pa = 5.0 * 6894.757                          # 5 psia -> Pa
    vol = 5.9                                       # m^3
    temp = 21.0 + 273.15                            # K
    n_mol = p_pa * vol / (R_UNIV * temp)
    mass = n_mol * M_O2
    print(f"  P = {p_pa:.1f} Pa (5 psia), V = {vol} m^3, T = {temp:.2f} K")
    print(f"  n = {n_mol:.2f} mol,  mass O2 = {mass:.3f} kg")
    return {"mass": mass}


# --------------------------------------------------------------------------
# P6b -- ISS Kapton erosion, one year (MISSE-2 PEACE anchored)
# --------------------------------------------------------------------------
def p6b() -> dict:
    print("\n" + "=" * 72)
    print("P6b -- ISS Kapton ram erosion, 1 year")
    print("=" * 72)
    fluence_4yr = 8.43e21                           # atoms/cm^2 over 3.95 yr (MISSE-2)
    years = 3.95
    fluence_yr = fluence_4yr / years                # atoms/cm^2/yr
    depth_cm = E_KAPTON * fluence_yr
    print(f"  MISSE-2 PEACE fluence = {fluence_4yr:.3e} atoms/cm^2 over {years} yr")
    print(f"  annual fluence = {fluence_yr:.3e} atoms/cm^2/yr")
    print(f"  Kapton erosion = {depth_cm*1e4:.1f} um/yr  ({depth_cm*10:.3f} mm/yr)")
    return {"depth_um": depth_cm * 1e4}


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
def _caption(fig, text: str) -> None:
    fig.text(0.5, 0.01, text, ha="center", va="bottom", fontsize=9, style="italic")


def fig_lifetime_vs_altitude() -> None:
    h0 = np.arange(200.0, 501.0, 5.0)
    t_days = np.array([lifetime(h, 150.0) / 86400.0 for h in h0])
    fig, ax = plt.subplots(figsize=(7.2, 4.7))
    ax.semilogy(h0, t_days, color="#1f4e79", lw=2)
    for h_mark, lab, off in [(400, "P1 case: 400 km", (-4, 30)),
                             (300, "300 km", (8, -28)),
                             (500, "500 km", (-58, -6))]:
        tv = lifetime(float(h_mark), 150.0) / 86400.0
        ax.plot(h_mark, tv, "o", color="#c00000", ms=5)
        ax.annotate(f"{lab}\n{tv:.0f} days", xy=(h_mark, tv), xytext=off,
                    textcoords="offset points", fontsize=8,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6", alpha=0.9),
                    arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.set_xlabel("Starting altitude  h0  (km)")
    ax.set_ylabel("Lifetime to 150 km  (days, log scale)")
    ax.set_title("P5: Drag lifetime vs. starting altitude")
    ax.grid(True, which="both", alpha=0.3)
    fig.subplots_adjust(bottom=0.17)
    _caption(fig, "Figure 3: Orbital lifetime (deorbit at 150 km) vs. starting "
                  "altitude, 100 kg / 1 m$^2$ / C$_d$=2.2 satellite.")
    fig.savefig(FIG_DIR / "fig1_lifetime_vs_altitude.png", dpi=150)
    plt.close(fig)


def fig_decay_profile() -> None:
    t_days, h_km = decay_profile(400.0, 150.0)
    fig, ax = plt.subplots(figsize=(7.2, 4.7))
    ax.plot(t_days, h_km, color="#385723", lw=2)
    ax.axhline(150.0, color="#c00000", ls="--", lw=1)
    ax.text(5, 158, "deorbit floor (150 km)", color="#c00000", fontsize=8)
    ax.annotate(f"reentry at {t_days[-1]:.0f} days", xy=(t_days[-1], 150),
                xytext=(-120, 40), textcoords="offset points", fontsize=8,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6"),
                arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.set_xlabel("Time since 400 km  (days)")
    ax.set_ylabel("Altitude  h  (km)")
    ax.set_title("P1: Altitude decay history, 400 km -> 150 km")
    ax.grid(True, alpha=0.3)
    fig.subplots_adjust(bottom=0.16)
    _caption(fig, "Figure 1: Altitude vs. time from the integrated decay; the "
                  "drop steepens as density climbs near the end.")
    fig.savefig(FIG_DIR / "fig2_decay_profile.png", dpi=150)
    plt.close(fig)


def fig_kapton_erosion(p3_out: dict) -> None:
    labels = ["low\n(6e6)", "medium\n(2e7)", "high\n(1e8)"]
    vals = [p3_out["low"], p3_out["medium"], p3_out["high"]]
    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    bars = ax.bar(labels, vals, color=["#9dc3e6", "#2e75b6", "#1f4e79"], width=0.6)
    ax.axhline(50.0, color="#c00000", ls="--", lw=1.2)
    ax.text(-0.42, 52.0, "50 um reference panel thickness", color="#c00000",
            fontsize=8, ha="left")
    for b, v in zip(bars, vals):
        ax.annotate(f"{v:.1f} um", xy=(b.get_x() + b.get_width()/2, v),
                    xytext=(0, 4), textcoords="offset points", ha="center", fontsize=9)
    ax.set_xlabel("Solar activity (atomic-oxygen number density, atoms/cm$^3$)")
    ax.set_ylabel("Kapton erosion depth  (um / year)")
    ax.set_title("P3: Kapton ram erosion at 450 km vs. solar activity")
    ax.grid(True, axis="y", alpha=0.3)
    fig.subplots_adjust(bottom=0.18)
    _caption(fig, "Figure 2: One-year ram-face Kapton recession at 450 km for "
                  "low/medium/high atomic-oxygen density.")
    fig.savefig(FIG_DIR / "fig3_kapton_erosion.png", dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------
def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    FIG_DIR.mkdir(exist_ok=True)

    p1_p5()
    p2()
    p3_out = p3()
    p4a()
    p6b()

    fig_lifetime_vs_altitude()
    fig_decay_profile()
    fig_kapton_erosion(p3_out)
    print("\nFigures written to:", FIG_DIR)


if __name__ == "__main__":
    main()
