"""SPCE 5065 -- Final Exam solution script (Summer 2026).

Covers every quantitative part of the final:

  P3   GEO sensor at 215 THz: wavelength, ionospheric plasma cutoff,
       atmospheric transmittance verdict
  P5   NO bond severing: longest photon wavelength for a 1.67 eV bond and
       the fraction of the solar spectrum shorter than it
  P6   Plasma frequency range for a 1000 km orbit
  P8   Worst-case ionospheric excess range and time delay, 500 km, K-band
  P9   Isothermal cube thermal balance at 300 km (sun and eclipse),
       plus the four-side thermal-control trade study
  P11  (bonus) symbolic check that dR/dt = 2 dV/dt sqrt(R^3/mu) collapses to
       the course drag result when the applied acceleration is drag

Conceptual problems (P1 T/F, P2 multiple choice, P4 solar-cycle table,
P7 CubeSat hazards, P10 MMOD survivability) are answered in the submission.

Outputs:
  - Console tables reproducing every boxed number in the submission
  - figures/fig1_plasma_freq_vs_altitude.png   (P3, P6)
  - figures/fig2_solar_spectrum_fraction.png   (P5)
  - figures/fig3_excess_range_vs_freq.png      (P8)
  - figures/fig4_thermal_emissivity_trade.png  (P9)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
C_LIGHT = 2.99792458e8         # m/s
H_PLANCK = 6.62607015e-34      # J s
K_B = 1.380649e-23             # J/K
E_CHG = 1.602176634e-19        # C  (also J per eV)
EPS0 = 8.8541878128e-12        # F/m
M_E = 9.1093837015e-31         # kg
SIGMA_SB = 5.67e-8             # W/m^2/K^4   (course value, Lesson 6 slide 24)

R_EARTH = 6378.0               # km
SOLAR_FLUX = 1367.0            # W/m^2       (Lesson 6 slide 29)
ALBEDO_FLUX = 465.0            # W/m^2       (Lesson 6 slide 30, Earth)
ALBEDO_FLUX_ALT = 0.37 * SOLAR_FLUX   # slide 31 rule: geometric albedo * solar
IR_FLUX = 237.0                # W/m^2       (Lesson 6 slide 30, Earth)

FIG_DIR = Path(__file__).parent / "figures"


def c2k(c: float) -> float:
    return c + 273.15


def k2c(k: float) -> float:
    return k - 273.15


# ---------------------------------------------------------------------------
# Plasma frequency  (Lesson 4 Part 1)
# ---------------------------------------------------------------------------
def plasma_frequency(n_e: float) -> float:
    """Electron plasma frequency (Hz).  f_p = (1/2pi) sqrt(n e^2 / (eps0 m_e))."""
    return np.sqrt(n_e * E_CHG**2 / (EPS0 * M_E)) / (2.0 * np.pi)


# ---------------------------------------------------------------------------
# Plasma density profile (m^-3).
#
# CAUTION: these are MY OWN visual reads off the density chart printed on the
# exam (page 7), obtained by measuring marker positions against the decade
# gridlines on the log axis. They are NOT tabulated anywhere in the course
# material. One significant figure is all a scanned log plot supports:
# locating a marker to +/-10 px is already +/-7% in density, and the gridline
# positions carry their own error. Treat every number below as "about".
#
# The only reads that any answer depends on are the 1000 km row (P6) and the
# F2 peak (P3); the rest exist to shape the curves in Figure 1 and are rough.
# ---------------------------------------------------------------------------
ALT_KM = np.array([100, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
N_PROFILE = {                                      # all values approximate
    "Day - Solar Max":   [2e11, 5e11, 1e12, 5e12, 1e12, 5e11,
                          3e11, 2e11, 1e11, 1e11, 9e10],
    "Night - Solar Max": [1e10, 5e9,  2e10, 3e11, 1e11, 7e10,
                          6e10, 5e10, 4e10, 3e10, 3e10],
    "Day - Solar Min":   [8e10, 2e11, 2e11, 4e11, 1e11, 5e10,
                          4e10, 2e10, 2e10, 2e10, 1e10],
    "Night - Solar Min": [4e9,  5e9,  3e9,  7e10, 3e10, 2e10,
                          1e10, 1e10, 1e10, 1e10, 1e10],
}


def p3() -> None:
    print("=" * 74)
    print("P3 -- GEO sensor at 215 THz")
    print("=" * 74)
    f_sensor = 215e12
    lam = C_LIGHT / f_sensor
    print(f"  sensor frequency                 = {f_sensor:.3e} Hz = 215 THz")
    print(f"  wavelength lambda = c/f          = {lam:.4e} m = {lam*1e6:.3f} um")

    # Highest plasma frequency anywhere in the ionosphere (F2 peak, day/solar max)
    n_peak = 5e12
    fp_peak = plasma_frequency(n_peak)
    print(f"  F2-peak density (day/solar max)  = {n_peak:.1e} m^-3")
    print(f"  max ionospheric plasma frequency = {fp_peak/1e6:.2f} MHz")
    print(f"  ratio f_sensor / f_p,max         = {f_sensor/fp_peak:.2e}")
    # Ionospheric delay at the sensor frequency, worst-case TEC, for scale
    dR = 40.31 * 1.0e18 / f_sensor**2
    print(f"  ionospheric excess range at 215 THz (TEC=1e18) = {dR*1e9:.4f} nm "
          f"(utterly negligible)")
    print("  -> plasma is a non-issue; the 1.394 um water-vapor band is not")


# ---------------------------------------------------------------------------
# P5 -- NO bond severing
# ---------------------------------------------------------------------------
def planck_spectral(lam: float, T: float) -> float:
    """Planck spectral radiant exitance (W/m^2 per m of wavelength)."""
    return (2.0 * np.pi * H_PLANCK * C_LIGHT**2 / lam**5) / (
        np.exp(H_PLANCK * C_LIGHT / (lam * K_B * T)) - 1.0)


def p5() -> None:
    print("=" * 74)
    print("P5 -- NO bond, E_bond = 1.67 eV")
    print("=" * 74)
    E_bond_eV = 1.67
    E_bond_J = E_bond_eV * E_CHG
    lam_max = H_PLANCK * C_LIGHT / E_bond_J
    f_min = E_bond_J / H_PLANCK
    print(f"  E_bond                    = {E_bond_eV} eV = {E_bond_J:.4e} J")
    print(f"  lambda_max = hc/E         = {lam_max:.4e} m = {lam_max*1e9:.1f} nm "
          f"= {lam_max*1e6:.4f} um")
    print(f"  f_min      = E/h          = {f_min:.4e} Hz = {f_min/1e12:.1f} THz")
    print(f"  [check] hc = 1239.84 eV-nm -> {1239.84/E_bond_eV:.1f} nm")

    # Fraction of a 5900 K solar blackbody shorter than lambda_max
    T_sun = 5900.0
    tot, _ = quad(planck_spectral, 1e-9, 200e-6, args=(T_sun,), limit=400)
    below, _ = quad(planck_spectral, 1e-9, lam_max, args=(T_sun,), limit=400)
    print(f"  5900 K blackbody: fraction with lambda < lambda_max = "
          f"{below/tot*100:.1f} %")
    for T in (5778.0, 6000.0):
        t2, _ = quad(planck_spectral, 1e-9, 200e-6, args=(T,), limit=400)
        b2, _ = quad(planck_spectral, 1e-9, lam_max, args=(T,), limit=400)
        print(f"    [sensitivity] T = {T:.0f} K -> {b2/t2*100:.1f} %")


# ---------------------------------------------------------------------------
# P6 -- plasma frequency at 1000 km
# ---------------------------------------------------------------------------
def p6() -> None:
    print("=" * 74)
    print("P6 -- plasma frequency range for a 1000 km orbit")
    print("=" * 74)
    for name, prof in N_PROFILE.items():
        n = prof[-1]                      # 1000 km entry
        print(f"  {name:18s}: n_e = {n:.2e} m^-3  ->  f_p = "
              f"{plasma_frequency(n)/1e6:.2f} MHz")
    n_lo = min(p[-1] for p in N_PROFILE.values())
    n_hi = max(p[-1] for p in N_PROFILE.values())
    print(f"  RANGE at 1000 km: n_e = {n_lo:.1e} to {n_hi:.1e} m^-3")
    print(f"  RANGE at 1000 km: f_p = {plasma_frequency(n_lo)/1e6:.2f} to "
          f"{plasma_frequency(n_hi)/1e6:.2f} MHz")
    print(f"  [check] engineering form f_p = 8.98*sqrt(n_e) Hz: "
          f"{8.98*np.sqrt(n_hi)/1e6:.2f} MHz")
    # The F2 peak underneath the orbit is the real gate for a ground link
    fp_peak = plasma_frequency(5e12)
    print(f"  F2 peak below the orbit -> {fp_peak/1e6:.1f} MHz must also be "
          f"cleared for a ground link")


# ---------------------------------------------------------------------------
# P8 -- ionospheric excess range and delay, 500 km, K-band
# ---------------------------------------------------------------------------
def excess_range(tec: float, f: float) -> float:
    """Excess range (m).  dR = 40.31 * TEC / f^2   (Lesson 4 Part 3)."""
    return 40.31 * tec / f**2


def p8() -> None:
    print("=" * 74)
    print("P8 -- worst-case excess range / delay, 500 km satellite, K-band")
    print("=" * 74)
    tec = 1.0e18                      # worst-case vertical TEC, e/m^2
    obliquity = 3.0                   # slant factor at a horizon-grazing link
    for f, name in [(18.0e9, "K-band low  (18 GHz, worst case)"),
                    (26.5e9, "K-band high (26.5 GHz)")]:
        dR = excess_range(tec, f)
        dt = dR / C_LIGHT
        print(f"  {name}")
        print(f"      vertical : dR = {dR*100:7.3f} cm   dt = {dt*1e9:6.3f} ns")
        print(f"      slant x3 : dR = {dR*obliquity*100:7.3f} cm   "
              f"dt = {dt*obliquity*1e9:6.3f} ns")
    # Scale comparison: same TEC at L-band (GPS L1)
    dR_l1 = excess_range(tec, 1.57542e9)
    print(f"  [context] same TEC at GPS L1 (1.575 GHz): dR = {dR_l1:.2f} m, "
          f"dt = {dR_l1/C_LIGHT*1e9:.1f} ns")
    print(f"  [check] dR ratio L1/K-low = {dR_l1/excess_range(tec, 18e9):.1f}x "
          f"= (18/1.575)^2 = {(18/1.57542)**2:.1f}")


# ---------------------------------------------------------------------------
# P9 -- isothermal cube thermal balance at 300 km
# ---------------------------------------------------------------------------
ALPHA_BLACK = 0.975
EPS_BLACK = 0.874
A_FACE = 1.0                      # m^2 per side
Q_INT = 100.0                     # W
ALT_P9 = 300.0                    # km
COST_PER_KG = 25_000.0            # $/kg  (Lesson 6 slide 44)


def view_factor(alt_km: float) -> float:
    """sin^2(rho), rho = asin(R_E / (R_E + h))  (Lesson 6 slide 30)."""
    return (R_EARTH / (R_EARTH + alt_km))**2


def heat_in(sunlit: bool, albedo_flux: float = ALBEDO_FLUX) -> float:
    """Absorbed environmental + internal heat (W).

    One face takes the sun, one face takes albedo and Earth IR
    (Lesson 6 Eq. 11-25a/b; the course writes the IR term with alpha).
    """
    s2 = view_factor(ALT_P9)
    q_ir = ALPHA_BLACK * A_FACE * s2 * IR_FLUX
    if not sunlit:
        return q_ir + Q_INT
    q_sol = ALPHA_BLACK * A_FACE * SOLAR_FLUX
    q_alb = ALPHA_BLACK * A_FACE * s2 * albedo_flux
    return q_sol + q_alb + q_ir + Q_INT


def eps_area(eps_sides: float) -> float:
    """Effective sum(eps * A) over the cube: 2 fixed black faces + 4 changeable."""
    return 2.0 * EPS_BLACK * A_FACE + 4.0 * eps_sides * A_FACE


def T_eq(q_in: float, eps_sides: float, q_heater: float = 0.0) -> float:
    """Equilibrium temperature (K) from Q_in = eps sigma A T^4."""
    return ((q_in + q_heater) / (SIGMA_SB * eps_area(eps_sides)))**0.25


def heater_for(T_target_C: float, eps_sides: float) -> float:
    """Heater power (W) needed to hold T_target in eclipse."""
    q_out = SIGMA_SB * eps_area(eps_sides) * c2k(T_target_C)**4
    return max(0.0, q_out - heat_in(sunlit=False))


def p9() -> None:
    print("=" * 74)
    print("P9 -- 1 m cube, black paint, 300 km, 100 W internal")
    print("=" * 74)
    s2 = view_factor(ALT_P9)
    print(f"  sin(rho) = R_E/(R_E+h)    = {np.sqrt(s2):.6f}")
    print(f"  sin^2(rho)                = {s2:.6f}")
    print(f"  Q_solar  = a*A*S          = {ALPHA_BLACK*A_FACE*SOLAR_FLUX:8.2f} W")
    print(f"  Q_albedo = a*A*s2*465     = "
          f"{ALPHA_BLACK*A_FACE*s2*ALBEDO_FLUX:8.2f} W")
    print(f"  Q_IR     = a*A*s2*237     = {ALPHA_BLACK*A_FACE*s2*IR_FLUX:8.2f} W")
    print(f"  Q_int                     = {Q_INT:8.2f} W")
    q_sun = heat_in(True)
    q_ecl = heat_in(False)
    print(f"  TOTAL in, sunlit          = {q_sun:8.2f} W")
    print(f"  TOTAL in, eclipse         = {q_ecl:8.2f} W")
    print(f"  eps*A (all six black)     = {eps_area(EPS_BLACK):8.4f} m^2")

    T_sun = T_eq(q_sun, EPS_BLACK)
    T_ecl = T_eq(q_ecl, EPS_BLACK)
    print(f"\n  (a) T_sun     = {T_sun:7.2f} K = {k2c(T_sun):7.2f} C")
    print(f"      T_eclipse = {T_ecl:7.2f} K = {k2c(T_ecl):7.2f} C")

    # Sensitivity to the albedo-flux convention (slide 30 vs slide 31)
    q_sun_alt = heat_in(True, albedo_flux=ALBEDO_FLUX_ALT)
    T_sun_alt = T_eq(q_sun_alt, EPS_BLACK)
    print(f"      [sensitivity] albedo flux 0.37*1367 = {ALBEDO_FLUX_ALT:.1f} "
          f"W/m^2 -> T_sun = {k2c(T_sun_alt):.2f} C (eclipse unchanged)")

    print(f"\n  (b) battery band 0 to 15 C (SMAD Table 11.43, survival -10 to 25)")
    print(f"      sun     : {k2c(T_sun):+7.2f} C -> "
          f"{'over' if k2c(T_sun) > 15 else 'ok'} by "
          f"{k2c(T_sun)-15:+.2f} C")
    print(f"      eclipse : {k2c(T_ecl):+7.2f} C -> under by "
          f"{k2c(T_ecl)-0:+.2f} C")

    # ---- (c) trade study over the four changeable sides -------------------
    print(f"\n  (c) four-side trade (cost = ${COST_PER_KG:,.0f}/kg)")
    print(f"      {'option':34s} {'T_sun':>8s} {'T_ecl,raw':>10s} "
          f"{'heater W':>9s} {'mass kg':>8s} {'cost $':>10s}")
    options = [
        # name, eps hot, eps cold, coating mass kg/m^2, extra fixed mass kg
        ("black paint (no change)",      EPS_BLACK, EPS_BLACK, 0.00, 0.0),
        ("white paint",                  0.85,      0.85,      0.00, 0.0),
        ("radiators (eps 0.8)",          0.80,      0.80,      0.60, 0.0),
        ("MLI insulation (eps 0.05)",    0.05,      0.05,      0.30, 0.0),
        ("radiators w/ louvers",         0.80,      0.05,      2.10, 0.8),
    ]
    results = []
    for name, e_hot, e_cold, m_area, m_extra in options:
        Ts = k2c(T_eq(heat_in(True), e_hot))
        Tc_raw = k2c(T_eq(heat_in(False), e_cold))
        q_htr = heater_for(0.0, e_cold)
        mass = 4.0 * A_FACE * m_area + m_extra + q_htr * 0.025
        cost = mass * COST_PER_KG
        results.append((name, Ts, Tc_raw, q_htr, mass, cost))
        print(f"      {name:34s} {Ts:8.1f} {Tc_raw:10.1f} {q_htr:9.1f} "
              f"{mass:8.2f} {cost:10,.0f}")

    print(f"\n      recommended: radiators w/ louvers + kapton heaters")
    name, Ts, Tc_raw, q_htr, mass, cost = results[-1]
    print(f"        louvers  : 4 m^2 x 2.10 kg/m^2      = {4*2.10:6.2f} kg")
    print(f"        controllers: 4 x 0.2 kg (8 W total) = {0.8:6.2f} kg")
    print(f"        heaters  : {q_htr:.1f} W x 0.025 kg/W  = {q_htr*0.025:6.2f} kg")
    print(f"        TOTAL    : {mass:.2f} kg -> ${cost:,.0f}")
    print(f"        T_sun (louvers open, eps=0.80)          = {Ts:.1f} C")
    print(f"        T_eclipse (louvers closed + heaters on) = {0.0:.1f} C")

    # Is any purely passive eps able to satisfy the hot case?
    need_hot = heat_in(True) / (SIGMA_SB * c2k(15.0)**4)
    eps_req = (need_hot - 2.0 * EPS_BLACK) / 4.0
    # Mixed configuration: louvers on 2 of the 4 sides, black paint on the rest
    e_hot_mix = (2 * 0.80 + 2 * EPS_BLACK) / 4.0
    e_cold_mix = (2 * 0.05 + 2 * EPS_BLACK) / 4.0
    Ts_mix = k2c(T_eq(heat_in(True), e_hot_mix))
    q_mix = heater_for(0.0, e_cold_mix)
    mass_mix = 2 * 2.10 + 2 * 0.2 + q_mix * 0.025
    print(f"      {'2 louvered + 2 black sides':34s} {Ts_mix:8.1f} "
          f"{k2c(T_eq(heat_in(False), e_cold_mix)):10.1f} {q_mix:9.1f} "
          f"{mass_mix:8.2f} {mass_mix*COST_PER_KG:10,.0f}")

    print(f"\n      [check] eps on the 4 sides needed for T_sun = 15 C: "
          f"{eps_req:.3f}")
    print(f"              max available eps in the course table = "
          f"{EPS_BLACK:.3f} (black paint) -> unreachable")
    cold_cap = heat_in(False) / (SIGMA_SB * c2k(0.0)**4)
    print(f"      [check] eps*A allowed for T_ecl = 0 C without heaters: "
          f"{cold_cap:.3f} m^2")
    print(f"              the two fixed black faces alone are "
          f"{2*EPS_BLACK:.3f} m^2 -> heaters are mandatory")

    # Heater energy per orbit: does a primary-battery bus survive it?
    mu_km = 398600.4418
    a_km = R_EARTH + ALT_P9
    period_s = 2.0 * np.pi * np.sqrt(a_km**3 / mu_km)
    rho_deg = np.degrees(np.arcsin(R_EARTH / a_km))
    ecl_frac = 2.0 * rho_deg / 360.0
    ecl_s = ecl_frac * period_s
    print(f"\n      [orbit] period = {period_s/60:.1f} min, eclipse fraction = "
          f"{ecl_frac:.3f} -> {ecl_s/60:.1f} min/orbit")
    for q, tag in [(304.1, "louvers"), (1344.4, "all black")]:
        wh = q * ecl_s / 3600.0
        print(f"      [energy] {tag:9s}: {q:6.1f} W x {ecl_s/60:.1f} min = "
              f"{wh:6.1f} Wh/orbit = {wh*86400/period_s/1000:.2f} kWh/day")


# ---------------------------------------------------------------------------
# P7 -- how hard does drag actually bite a CubeSat at 550 km over 5 years?
# ---------------------------------------------------------------------------
def density_kgm3(alt_km: float) -> float:
    """Course power-law fit to the LEO density profile (kg/m^3)."""
    return 1.02e7 * alt_km**(-7.172)


def decay(alt0_km: float, bc: float, years: float, dt_days: float = 1.0):
    """Integrate dR/dt = -(rho/BC) sqrt(mu R) (Lesson 2 drag decay)."""
    mu = 3.986004418e14
    R = (R_EARTH + alt0_km) * 1e3
    dt = dt_days * 86400.0
    t = 0.0
    while t < years * 365.25 * 86400.0:
        alt = R / 1e3 - R_EARTH
        if alt <= 150.0:
            return alt, t / (365.25 * 86400.0)
        R += -(density_kgm3(alt) / bc) * np.sqrt(mu * R) * dt
        t += dt
    return R / 1e3 - R_EARTH, years


def p7() -> None:
    print("=" * 74)
    print("P7 -- 3U CubeSat drag decay from 550 km over 5 years")
    print("=" * 74)
    m, cd, area = 4.0, 2.2, 0.03      # 3U: 4 kg, Cd 2.2, 10x30 cm frontal
    bc = m / (cd * area)
    print(f"  BC = m/(Cd*A) = {m}/({cd}*{area}) = {bc:.1f} kg/m^2 "
          f"(typical range 25 to 200)")
    for label, b in [("3U CubeSat", bc), ("BC = 103 reference", 103.0)]:
        alt_end, t_end = decay(550.0, b, 5.0)
        note = f"reaches 150 km at {t_end:.2f} yr" if alt_end <= 151 else \
               f"{550.0 - alt_end:.0f} km lost in 5 yr"
        print(f"  {label:20s} BC={b:6.1f}: final alt = {alt_end:6.1f} km  ({note})")
    print(f"  [check] rho(550 km) = {density_kgm3(550.0):.3e} kg/m^3 "
          f"(typical 1e-13 to 5e-13)")


# ---------------------------------------------------------------------------
# P11 (bonus) -- numerical check of dR/dt = 2 * Vdot * sqrt(R^3/mu)
# ---------------------------------------------------------------------------
def p11() -> None:
    print("=" * 74)
    print("P11 (bonus) -- dR/dt due to an applied delta-V")
    print("=" * 74)
    mu = 3.986004418e14            # m^3/s^2
    R = (R_EARTH + 400.0) * 1e3    # m, 400 km circular
    rho = 3.0e-12                  # kg/m^3, representative 400 km density
    BC = 100.0                     # kg/m^2

    # Applied acceleration equal to drag deceleration: Vdot = -rho*v^2/(2 BC)
    v = np.sqrt(mu / R)
    Vdot = -rho * v**2 / (2.0 * BC)
    Rdot_general = 2.0 * Vdot * np.sqrt(R**3 / mu)
    Rdot_drag = -(rho / BC) * np.sqrt(mu * R)      # course drag result
    print(f"  circular speed v            = {v:.2f} m/s")
    print(f"  applied Vdot (= drag decel) = {Vdot:.4e} m/s^2")
    print(f"  Rdot = 2*Vdot*sqrt(R^3/mu)  = {Rdot_general:.6e} m/s "
          f"= {Rdot_general*86400/1e3:.4f} km/day")
    print(f"  Rdot = -(rho/BC)*sqrt(mu R) = {Rdot_drag:.6e} m/s "
          f"(course drag form)")
    print(f"  [check] relative difference = "
          f"{abs(Rdot_general-Rdot_drag)/abs(Rdot_drag):.2e}")
    print(f"  Also Rdot = 2*Vdot/n with n = sqrt(mu/R^3): "
          f"{2*Vdot/np.sqrt(mu/R**3):.6e} m/s")


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
def _caption(fig, text: str) -> None:
    fig.text(0.5, 0.012, text, ha="center", va="bottom", fontsize=8.5,
             style="italic")


def fig_plasma_freq() -> None:
    """P3/P6: plasma frequency vs altitude for the four course profiles."""
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    styles = {
        "Day - Solar Max":   ("#c00000", "-",  "s"),
        "Night - Solar Max": ("#c00000", "--", "s"),
        "Day - Solar Min":   ("#1f4e79", "-",  "o"),
        "Night - Solar Min": ("#1f4e79", "--", "o"),
    }
    for name, prof in N_PROFILE.items():
        color, ls, mk = styles[name]
        ax.plot(plasma_frequency(np.array(prof)) / 1e6, ALT_KM, color=color,
                ls=ls, marker=mk, ms=4, lw=1.6, label=name)
    ax.axhline(1000, color="0.4", lw=1.2, ls=":")
    f_lo = plasma_frequency(1e10) / 1e6
    f_hi = plasma_frequency(1e11) / 1e6
    ax.axvspan(f_lo, f_hi, color="#ffd966", alpha=0.35, zorder=0)
    ax.annotate(f"1000 km band\n{f_lo:.1f} to {f_hi:.1f} MHz",
                xy=(f_lo, 1000), xytext=(0.44, 660), textcoords="data",
                fontsize=9, ha="left", va="center",
                bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="0.6"),
                arrowprops=dict(arrowstyle="->", color="0.5"))
    fp_peak = plasma_frequency(5e12) / 1e6
    ax.annotate(f"F2 peak, day/solar max\n{fp_peak:.0f} MHz",
                xy=(fp_peak, 300), xytext=(9.0, 880), textcoords="data",
                fontsize=9, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="0.6"),
                arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.set_xscale("log")
    ax.set_xlabel("Plasma frequency  $f_p$  (MHz)")
    ax.set_ylabel("Altitude (km)")
    ax.set_ylim(0, 1160)
    ax.set_xlim(0.4, 40)
    ax.set_title("P3 / P6: Ionospheric plasma frequency vs altitude")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8.5, loc="lower right")
    fig.subplots_adjust(bottom=0.20, top=0.91)
    _caption(fig, "Figure 1: Redrawn from approximate visual reads of the exam's "
                  "density chart (1 significant figure).\nA 1000 km orbit sits "
                  "in a ~1 to 3 MHz plasma; the 215 THz sensor of Problem 3 is "
                  "~7 orders of magnitude above even the F2 peak.")
    fig.savefig(FIG_DIR / "fig1_plasma_freq_vs_altitude.png", dpi=150)
    plt.close(fig)


def fig_solar_fraction() -> None:
    """P5: 5900 K solar blackbody with the 1.67 eV cutoff shaded."""
    T = 5900.0
    lam = np.linspace(50e-9, 3.2e-6, 1200)
    E = planck_spectral(lam, T)
    E_norm = E / E.max()
    lam_cut = H_PLANCK * C_LIGHT / (1.67 * E_CHG)

    tot, _ = quad(planck_spectral, 1e-9, 200e-6, args=(T,), limit=400)
    below, _ = quad(planck_spectral, 1e-9, lam_cut, args=(T,), limit=400)
    frac = below / tot

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.plot(lam * 1e6, E_norm, color="#1f4e79", lw=2)
    ax.fill_between(lam * 1e6, 0, E_norm, where=(lam <= lam_cut),
                    color="#c00000", alpha=0.30)
    ax.axvline(lam_cut * 1e6, color="#c00000", lw=1.6, ls="--")
    ax.axvspan(0.40, 0.75, color="0.55", alpha=0.14, zorder=0)
    ax.text(0.575, 0.06, "visible", ha="center", fontsize=8.5, color="0.3")
    ax.annotate(f"$\\lambda_{{max}}$ = {lam_cut*1e9:.0f} nm\n"
                f"shaded = {frac*100:.0f}% of the solar output",
                xy=(lam_cut * 1e6, 0.52), xytext=(42, 22),
                textcoords="offset points", fontsize=9,
                bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="0.6"),
                arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.set_xlabel("Wavelength  $\\lambda$  ($\\mu$m)")
    ax.set_ylabel("Spectral irradiance (normalized)")
    ax.set_xlim(0, 3.2)
    ax.set_ylim(0, 1.08)
    ax.set_title("P5: 5900 K solar spectrum, photons able to break a 1.67 eV "
                 "N-O bond")
    ax.grid(True, alpha=0.3)
    fig.subplots_adjust(bottom=0.18)
    _caption(fig, "Figure 2: Everything shorter than 742 nm carries at least "
                  "1.67 eV, and that is a majority of the solar output.")
    fig.savefig(FIG_DIR / "fig2_solar_spectrum_fraction.png", dpi=150)
    plt.close(fig)


def fig_excess_range() -> None:
    """P8: excess range vs frequency with the comm bands marked."""
    tec = 1.0e18
    f = np.logspace(np.log10(1e8), np.log10(4e10), 600)
    dR = excess_range(tec, f)

    fig, ax1 = plt.subplots(figsize=(7.2, 4.8))
    ax1.loglog(f / 1e9, dR, color="#1f4e79", lw=2, label="vertical, TEC $=10^{18}$")
    ax1.loglog(f / 1e9, dR * 3.0, color="#c00000", lw=1.6, ls="--",
               label="slant (obliquity 3)")
    ax1.axvspan(18.0, 26.5, color="#ffd966", alpha=0.45, zorder=0)
    ax1.text(21.8, 3e3, "K-band", ha="center", fontsize=9, color="0.25")

    dR18 = excess_range(tec, 18e9)
    ax1.plot(18.0, dR18, "o", color="#385723", ms=7, zorder=5)
    ax1.annotate(f"worst case 18 GHz\n$\\Delta R$ = {dR18*100:.1f} cm\n"
                 f"$\\Delta t$ = {dR18/C_LIGHT*1e9:.2f} ns",
                 xy=(18.0, dR18), xytext=(-135, 58), textcoords="offset points",
                 fontsize=8.5,
                 bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="0.6"),
                 arrowprops=dict(arrowstyle="->", color="0.5"))
    ax1.set_xlabel("Frequency (GHz)")
    ax1.set_ylabel("Excess range  $\\Delta R$  (m)")
    ax1.set_title("P8: Ionospheric excess range vs frequency "
                  "($\\Delta R \\propto 1/f^2$)")
    ax1.grid(True, which="both", alpha=0.3)
    ax1.legend(fontsize=8.5, loc="upper right")
    fig.subplots_adjust(bottom=0.18)
    _caption(fig, "Figure 3: K-band lands at the far right of the $1/f^2$ "
                  "curve, which is exactly why the delay is sub-nanosecond.")
    fig.savefig(FIG_DIR / "fig3_excess_range_vs_freq.png", dpi=150)
    plt.close(fig)


def fig_thermal_trade() -> None:
    """P9: hot and cold equilibrium temperature vs the four-side emissivity."""
    eps = np.linspace(0.02, 0.95, 400)
    T_hot = np.array([k2c(T_eq(heat_in(True), e)) for e in eps])
    T_cold = np.array([k2c(T_eq(heat_in(False), e)) for e in eps])

    fig, ax = plt.subplots(figsize=(7.4, 5.2))
    ax.axhspan(0, 15, color="#a9d18e", alpha=0.45, zorder=0)
    ax.text(0.015, 7.5, "battery band 0 to 15 $^\\circ$C", ha="left",
            va="center", fontsize=8.5, color="0.15",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none",
                      alpha=0.75))
    ax.plot(eps, T_hot, color="#c00000", lw=2, label="sunlit")
    ax.plot(eps, T_cold, color="#1f4e79", lw=2, label="eclipse (no heaters)")

    for e, lbl, dxy in [(0.05, "MLI 0.05", (58, -14)),
                        (0.80, "louvers open 0.80", (-58, 58)),
                        (EPS_BLACK, "black paint 0.874", (-26, -78))]:
        ax.plot([e, e], [k2c(T_eq(heat_in(False), e)),
                         k2c(T_eq(heat_in(True), e))], color="0.6", lw=0.9,
                ls=":")
        ax.plot(e, k2c(T_eq(heat_in(True), e)), "o", color="#385723", ms=6,
                zorder=5)
        ax.annotate(f"{lbl}\nsun {k2c(T_eq(heat_in(True), e)):.0f} $^\\circ$C, "
                    f"ecl {k2c(T_eq(heat_in(False), e)):.0f} $^\\circ$C",
                    xy=(e, k2c(T_eq(heat_in(True), e))), xytext=dxy,
                    textcoords="offset points", fontsize=8, ha="center",
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6",
                              alpha=0.95),
                    arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.set_xlabel("Emissivity of the four changeable sides  $\\varepsilon_4$")
    ax.set_ylabel("Equilibrium temperature ($^\\circ$C)")
    ax.set_ylim(-125, 145)
    ax.set_xlim(0, 1.0)
    ax.set_title("P9: No single surface finish puts both cases in the battery "
                 "band")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9, loc="upper right")
    fig.subplots_adjust(bottom=0.20, top=0.92)
    _caption(fig, "Figure 4: The sunlit curve never drops to 15 $^\\circ$C and "
                  "the eclipse curve never climbs to 0 $^\\circ$C,\nso the fix "
                  "has to be variable emissivity plus heaters.")
    fig.savefig(FIG_DIR / "fig4_thermal_emissivity_trade.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    FIG_DIR.mkdir(exist_ok=True)
    p3(); print()
    p5(); print()
    p6(); print()
    p7(); print()
    p8(); print()
    p9(); print()
    p11()

    fig_plasma_freq()
    fig_solar_fraction()
    fig_excess_range()
    fig_thermal_trade()
    print("\nFigures written to:", FIG_DIR)


if __name__ == "__main__":
    main()
