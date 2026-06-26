"""SPCE 5065 -- Homework 1 solution.

Two-body orbital mechanics + solar irradiance geometry. Covers the quantitative
parts of HW1:

  Q2  Circular-orbit velocity and period vs. altitude (derivations + 2 graphs)
  Q6  Solar constant vs. eccentricity / day-of-year, and per-planet irradiance
  Q7  Mass of Saturn from Titan's period and semi-major axis (Kepler III)
  Q8  Mass of an asteroid from a single vis-viva state

Outputs:
  - Console tables reproducing every boxed number in the submission
  - figures/fig1_velocity_vs_altitude.png   (Q2c)
  - figures/fig2_period_vs_altitude.png      (Q2e)
  - figures/fig3_irradiance_vs_doy.png       (Q6c)
  - figures/fig4_planet_irradiance.png       (Q6d)

Conceptual problems (Q1, Q3, Q4, Q5) are answered in the submission document;
they need no code.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------
MU_EARTH = 398600.5          # km^3/s^2  (given, mu = G*M_E)
R_E = 6378.0                 # km        (given Earth radius)
G = 6.67430e-11              # N*m^2/kg^2 (CODATA 2018)
S_E = 1366.1                 # W/m^2     (given solar irradiance at 1 AU)
AU_KM = 149_597_871.0        # km        (given 1 AU)
E_EARTH = 0.016710           # Earth orbital eccentricity
DAY_S = 86400.0              # s per day

FIG_DIR = Path(__file__).parent / "figures"


# --------------------------------------------------------------------------
# Q2 -- circular-orbit velocity and period
# --------------------------------------------------------------------------
def orbital_velocity(h_km: float, mu: float = MU_EARTH, re: float = R_E) -> float:
    """Circular orbital velocity (km/s).  v = sqrt(mu / (R_E + h))   [Q2b]."""
    return np.sqrt(mu / (re + h_km))


def orbital_period(h_km: float, mu: float = MU_EARTH, re: float = R_E) -> float:
    """Circular orbital period (s).  T = 2*pi*sqrt((R_E + h)^3 / mu)   [Q2d]."""
    return 2.0 * np.pi * np.sqrt((re + h_km) ** 3 / mu)


def q2_check() -> None:
    print("=" * 70)
    print("Q2 -- velocity & period vs altitude (spot checks)")
    print("=" * 70)
    for h, label in [(0.0, "surface"), (400.0, "ISS-ish"),
                     (800.0, "Q3 orbit"), (35786.0, "GEO")]:
        v = orbital_velocity(h)
        T = orbital_period(h)
        print(f"  h = {h:8.0f} km ({label:8s}):  "
              f"v = {v:7.4f} km/s   T = {T:10.2f} s = {T/60:7.3f} min")
    # Verification: GEO period should be ~one sidereal day (86164 s)
    T_geo = orbital_period(35786.0)
    print(f"  [check] GEO period {T_geo:.1f} s vs sidereal day 86164 s  "
          f"-> {100*(T_geo-86164)/86164:+.3f}%")


# --------------------------------------------------------------------------
# Q6 -- solar irradiance
# --------------------------------------------------------------------------
def solar_constant_from_r_au(r_au: np.ndarray | float) -> np.ndarray | float:
    """Inverse-square solar constant.  S(r) = S_e * (1 AU / r)^2."""
    return S_E * (1.0 / r_au) ** 2


def radius_au_from_true_anomaly(nu_rad, a_au=1.0, e=E_EARTH):
    """Orbit equation r = a(1 - e^2) / (1 + e cos nu)."""
    return a_au * (1 - e ** 2) / (1 + e * np.cos(nu_rad))


def earth_sun_distance_by_day(doy: np.ndarray, e=E_EARTH,
                              day_perihelion: float = 3.0) -> np.ndarray:
    """Earth-Sun distance (AU) vs day-of-year, solving Kepler's equation.

    Mean anomaly measured from perihelion (~Jan 3 = DOY 3), then
    M -> E (Newton) -> r = a(1 - e cos E),  a = 1 AU.
    """
    M = 2 * np.pi * (doy - day_perihelion) / 365.25
    E = M.copy()
    for _ in range(50):                      # Newton-Raphson on E - e sinE = M
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return 1.0 * (1 - e * np.cos(E))          # AU


def q6_results() -> None:
    print("=" * 70)
    print("Q6 -- solar irradiance")
    print("=" * 70)
    # (b) Earth max/min from perihelion/aphelion: r = a(1 -/+ e)
    s_max = S_E / (1 - E_EARTH) ** 2          # perihelion
    s_min = S_E / (1 + E_EARTH) ** 2          # aphelion
    print(f"  (b) Earth perihelion S_max = {s_max:7.2f} W/m^2   "
          f"(r = 1-e = {1-E_EARTH:.4f} AU)")
    print(f"      Earth aphelion   S_min = {s_min:7.2f} W/m^2   "
          f"(r = 1+e = {1+E_EARTH:.4f} AU)")
    print(f"      mean (S_e)             = {S_E:7.2f} W/m^2")

    # (d) per-planet table:  a (AU), e
    planets = {
        "Mercury": (0.38710, 0.20563),
        "Venus":   (0.72333, 0.00677),
        "Earth":   (1.00000, 0.01671),
        "Mars":    (1.52371, 0.09339),
        "Jupiter": (5.20289, 0.04839),
        "Saturn":  (9.53707, 0.05386),
        "Uranus":  (19.18914, 0.04726),
        "Neptune": (30.06992, 0.00859),
    }
    print(f"\n  (d) Planetary solar irradiance (W/m^2):")
    print(f"      {'Planet':9s} {'a(AU)':>8s} {'e':>7s} "
          f"{'S_avg':>10s} {'S_max':>10s} {'S_min':>10s}")
    for name, (a, e) in planets.items():
        s_avg = S_E / a ** 2
        s_mx = S_E / (a * (1 - e)) ** 2
        s_mn = S_E / (a * (1 + e)) ** 2
        print(f"      {name:9s} {a:8.3f} {e:7.4f} "
              f"{s_avg:10.2f} {s_mx:10.2f} {s_mn:10.2f}")
    return planets


# --------------------------------------------------------------------------
# Q7 -- mass of Saturn from Titan
# --------------------------------------------------------------------------
def kepler_third_central_mass(period_s: float, a_m: float) -> float:
    """M = 4*pi^2 a^3 / (G T^2)  -- central mass from a satellite's orbit."""
    return 4 * np.pi ** 2 * a_m ** 3 / (G * period_s ** 2)


def q7_results() -> float:
    print("=" * 70)
    print("Q7 -- mass of Saturn from Titan")
    print("=" * 70)
    P = 14.1 * DAY_S                  # s
    a = 1_110_781_765.0              # m
    M_saturn = kepler_third_central_mass(P, a)
    M_published = 5.6834e26          # kg (NASA Saturn Fact Sheet)
    pct = 100 * (M_saturn - M_published) / M_published
    print(f"  Titan period      P = {P:.1f} s ({P/DAY_S:.1f} d)")
    print(f"  Titan SMA         a = {a:.0f} m")
    print(f"  Computed mass       = {M_saturn:.4e} kg")
    print(f"  Published mass      = {M_published:.4e} kg")
    print(f"  Percent difference  = {pct:+.2f}%")
    return M_saturn


# --------------------------------------------------------------------------
# Q8 -- mass of an asteroid from vis-viva
# --------------------------------------------------------------------------
def q8_results() -> float:
    print("=" * 70)
    print("Q8 -- mass of an asteroid (vis-viva)")
    print("=" * 70)
    a = 1.0e6            # m   (semi-major axis 1000 km)
    r = 1.5e6            # m   (range 1500 km)
    v = 10.0            # m/s
    # v^2 = mu (2/r - 1/a)  ->  mu = v^2 / (2/r - 1/a)
    mu = v ** 2 / (2 / r - 1 / a)
    M = mu / G
    print(f"  a = {a:.0f} m,  r = {r:.0f} m,  v = {v:.1f} m/s")
    print(f"  2/r - 1/a = {2/r - 1/a:.6e} 1/m")
    print(f"  mu = {mu:.4e} m^3/s^2")
    print(f"  M  = {M:.4e} kg")
    return M


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
def _caption(fig, text: str) -> None:
    fig.text(0.5, 0.01, text, ha="center", va="bottom",
             fontsize=9, style="italic")


def fig_velocity_vs_altitude() -> None:
    h = np.linspace(0, 36000, 600)
    v = orbital_velocity(h)
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.plot(h, v, color="#1f4e79", lw=2)
    for h_mark, lab in [(400, "LEO ~400 km"), (800, "800 km"),
                        (20200, "MEO/GPS"), (35786, "GEO")]:
        ax.plot(h_mark, orbital_velocity(h_mark), "o", color="#c00000", ms=5)
        ax.annotate(f"{lab}\n{orbital_velocity(h_mark):.2f} km/s",
                    xy=(h_mark, orbital_velocity(h_mark)),
                    xytext=(12, 12), textcoords="offset points", fontsize=8,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6",
                              alpha=0.9),
                    arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.set_xlabel("Altitude  h  (km)")
    ax.set_ylabel("Circular orbital velocity  v  (km/s)")
    ax.set_title("Q2c: Orbital velocity vs. altitude")
    ax.grid(True, alpha=0.3)
    fig.subplots_adjust(bottom=0.18)
    _caption(fig, "Figure 1: Circular orbital velocity "
             r"$v=\sqrt{\mu/(R_E+h)}$ vs. altitude.")
    fig.savefig(FIG_DIR / "fig1_velocity_vs_altitude.png", dpi=150)
    plt.close(fig)


def fig_period_vs_altitude() -> None:
    h = np.linspace(0, 36000, 600)
    T = orbital_period(h) / 60.0     # minutes
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.plot(h, T, color="#385723", lw=2)
    for h_mark, lab in [(400, "LEO"), (800, "800 km"),
                        (20200, "GPS"), (35786, "GEO")]:
        ax.plot(h_mark, orbital_period(h_mark) / 60, "o", color="#c00000", ms=5)
        ax.annotate(f"{lab}\n{orbital_period(h_mark)/60:.1f} min",
                    xy=(h_mark, orbital_period(h_mark) / 60),
                    xytext=(12, -4), textcoords="offset points", fontsize=8,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6",
                              alpha=0.9),
                    arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.set_xlabel("Altitude  h  (km)")
    ax.set_ylabel("Orbital period  T  (min)")
    ax.set_title("Q2e: Orbital period vs. altitude")
    ax.grid(True, alpha=0.3)
    fig.subplots_adjust(bottom=0.18)
    _caption(fig, "Figure 2: Circular orbital period "
             r"$T=2\pi\sqrt{(R_E+h)^3/\mu}$ vs. altitude.")
    fig.savefig(FIG_DIR / "fig2_period_vs_altitude.png", dpi=150)
    plt.close(fig)


def fig_irradiance_vs_doy() -> None:
    doy = np.arange(1, 366)
    r_au = earth_sun_distance_by_day(doy)
    S = solar_constant_from_r_au(r_au)
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.plot(doy, S, color="#bf8f00", lw=2)
    i_max, i_min = int(np.argmax(S)), int(np.argmin(S))
    ax.plot(doy[i_max], S[i_max], "o", color="#c00000", ms=5)
    ax.plot(doy[i_min], S[i_min], "o", color="#1f4e79", ms=5)
    ax.annotate(f"perihelion (~Jan {doy[i_max]})\n{S[i_max]:.1f} W/m$^2$",
                xy=(doy[i_max], S[i_max]), xytext=(20, -6),
                textcoords="offset points", fontsize=8,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6"),
                arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.annotate(f"aphelion (~Jul {doy[i_min]-181})\n{S[i_min]:.1f} W/m$^2$",
                xy=(doy[i_min], S[i_min]), xytext=(-30, 14),
                textcoords="offset points", fontsize=8,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6"),
                arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.axhline(S_E, color="0.5", ls="--", lw=1)
    ax.text(190, S_E + 1, r"$S_e=1366.1$ W/m$^2$ (1 AU)", fontsize=8, color="0.4")
    ax.set_xlabel("Day of year")
    ax.set_ylabel("Solar irradiance at Earth  S  (W/m$^2$)")
    ax.set_title("Q6c: Solar irradiance at Earth vs. day of year")
    ax.grid(True, alpha=0.3)
    fig.subplots_adjust(bottom=0.18)
    _caption(fig, "Figure 3: Top-of-atmosphere solar irradiance over a year; "
             "perihelion in early January gives the annual max.")
    fig.savefig(FIG_DIR / "fig3_irradiance_vs_doy.png", dpi=150)
    plt.close(fig)


def fig_planet_irradiance(planets: dict) -> None:
    names = list(planets.keys())
    a = np.array([planets[n][0] for n in names])
    e = np.array([planets[n][1] for n in names])
    s_avg = S_E / a ** 2
    s_max = S_E / (a * (1 - e)) ** 2
    s_min = S_E / (a * (1 + e)) ** 2
    x = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(8, 4.8))
    # asymmetric error bars from avg to max/min
    yerr = np.vstack([s_avg - s_min, s_max - s_avg])
    ax.errorbar(x, s_avg, yerr=yerr, fmt="o", color="#1f4e79",
                ecolor="#c00000", elinewidth=1.5, capsize=5, ms=7,
                label="mean (bar = min..max)")
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=30, ha="right")
    for xi, s in zip(x, s_avg):
        ax.annotate(f"{s:.1f}", xy=(xi, s), xytext=(8, 0),
                    textcoords="offset points", fontsize=7.5, va="center")
    ax.set_ylabel("Solar irradiance  S  (W/m$^2$, log scale)")
    ax.set_title("Q6d: Mean / max / min solar irradiance by planet")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    fig.subplots_adjust(bottom=0.26)
    _caption(fig, "Figure 4: Per-planet solar irradiance at semi-major axis "
             "(marker) with perihelion/aphelion spread (bars), log y-axis.")
    fig.savefig(FIG_DIR / "fig4_planet_irradiance.png", dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------
def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    FIG_DIR.mkdir(exist_ok=True)
    q2_check()
    print()
    planets = q6_results()
    print()
    q7_results()
    print()
    q8_results()

    fig_velocity_vs_altitude()
    fig_period_vs_altitude()
    fig_irradiance_vs_doy()
    fig_planet_irradiance(planets)
    print("\nFigures written to:", FIG_DIR)


if __name__ == "__main__":
    main()
