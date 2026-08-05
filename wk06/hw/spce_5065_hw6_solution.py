"""SPCE 5065 -- Homework 6 solution.

Vacuum environment: solar UV photon flux, spacecraft thermal balance,
outgassing, and cleanroom classification.

  Q2  UV photons energetic enough to break a C-C bond (linear fit to Fig. 1.4)
  Q3  Same count from Planck's law, plus total solar photon output
  Q4  Equilibrium temperature of the Eris probe at every planet + Pluto
  Q5  $15K thermal control design trade
  Q6  Neoprene outgassing rate: Torr-L/(cm^2 s) -> W/m^2 -> molecules/(cm^2 s)
  Q7  ISO 14644-1 cleanroom particle concentration curves
  Q8  Kapton outgassing rate from an ASTM E-595 TML

Outputs:
  - Console tables reproducing every boxed number in the submission
  - figures/fig1_solar_spectrum_fit.png     (Q2b)
  - figures/fig2_planck_vs_measured.png     (Q3a)
  - figures/fig3_equilibrium_temps.png      (Q4a)
  - figures/fig4_thermal_design.png         (Q5)
  - figures/fig5_iso_cleanroom.png          (Q7)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------------------------------
# Physical constants
# --------------------------------------------------------------------------
H_PLANCK = 6.626e-34            # J*s   (value given on the homework sheet)
C_LIGHT = 2.998e8               # m/s
K_B = 1.380649e-23              # J/K
SIGMA_SB = 5.67e-8              # W/(m^2 K^4)   Stefan-Boltzmann (Lesson 6)
EV_J = 1.602176634e-19          # J per eV
N_A = 6.02214076e23             # 1/mol
HC = H_PLANCK * C_LIGHT         # J*m
AU_M = 1.495979e11              # m
R_SUN = 6.957e8                 # m
L_SUN = 3.828e26                # W      (given)
T_SUN = 5772.0                  # K      effective photosphere temperature
S_EARTH = 1367.0                # W/m^2  solar flux at 1 AU (Lesson 6)
TORR_PA = 133.322               # Pa per Torr

FIG_DIR = Path(__file__).parent / "figures"

# Tribble Fig. 1.4 read off by eye: (wavelength um, irradiance W/cm^2/um)
FIG14 = np.array([
    [0.20, 0.0050], [0.25, 0.0180], [0.30, 0.0480], [0.35, 0.0980],
    [0.40, 0.1400], [0.45, 0.1800], [0.50, 0.2050], [0.55, 0.1950],
    [0.60, 0.1800], [0.70, 0.1450], [0.80, 0.1150], [0.90, 0.0950],
    [1.00, 0.0750], [1.20, 0.0480], [1.40, 0.0320], [1.60, 0.0220],
    [1.80, 0.0160], [2.00, 0.0120], [2.50, 0.0065], [3.00, 0.0038],
    [3.50, 0.0022], [4.00, 0.0014],
])


# --------------------------------------------------------------------------
# Q2 -- bond-breaking photons from a linear fit to the measured spectrum
# --------------------------------------------------------------------------
def lambda_max_for_bond(bond_eV: float) -> float:
    """Longest wavelength (m) whose photon still carries the bond energy."""
    return HC / (bond_eV * EV_J)


def linear_fit_band(lam_lo_um: float, lam_hi_um: float):
    """Least-squares line through the Fig. 1.4 points inside the waveband.

    Returns (slope, intercept) for S(lam) in W/cm^2/um with lam in um.
    """
    lam = FIG14[:, 0]
    s = FIG14[:, 1]
    # include an interpolated endpoint exactly at the band edge
    s_hi = np.interp(lam_hi_um, lam, s)
    mask = (lam >= lam_lo_um) & (lam <= lam_hi_um)
    x = np.append(lam[mask], lam_hi_um)
    y = np.append(s[mask], s_hi)
    slope, intercept = np.polyfit(x, y, 1)
    return slope, intercept


def photons_from_line(slope: float, intercept: float,
                      lam_lo_um: float, lam_hi_um: float) -> float:
    """N = (1/hc) * int S(lam) * lam dlam  ->  photons/(cm^2 s).

    S in W/cm^2/um, lam in um, so the integral carries units W*um/cm^2 and
    needs a 1e-6 factor to put the wavelength into metres for hc.
    """
    def anti(x):                       # integral of (m*lam + b)*lam dlam
        return slope * x ** 3 / 3.0 + intercept * x ** 2 / 2.0
    integral_um = anti(lam_hi_um) - anti(lam_lo_um)     # W*um/cm^2
    return integral_um * 1e-6 / HC                      # photons/(cm^2 s)


def q2() -> dict:
    print("=" * 74)
    print("Q2 -- UV photons capable of breaking a single C-C bond")
    print("=" * 74)
    bond_eV = 3.47
    lam_max = lambda_max_for_bond(bond_eV)
    lam_max_um = lam_max * 1e6
    print(f"  (a) E_bond = {bond_eV} eV = {bond_eV*EV_J:.4e} J")
    print(f"      lam_max = hc/E = {HC:.5e} / {bond_eV*EV_J:.4e} "
          f"= {lam_max:.4e} m = {lam_max_um:.4f} um")

    lam_lo = 0.20                       # um, where Fig. 1.4 lifts off zero
    slope, intercept = linear_fit_band(lam_lo, lam_max_um)
    lam_0 = -intercept / slope          # where the fitted line crosses zero
    lam_lo_eff = max(lam_lo, lam_0)     # never integrate a negative irradiance
    print(f"  (b) linear fit over {lam_lo}-{lam_max_um:.3f} um:")
    print(f"      S(lam) = {slope:.4f}*lam {intercept:+.5f}  W/cm^2/um")
    print(f"      crosses zero at {lam_0:.4f} um, so integrate "
          f"{lam_lo_eff:.4f} to {lam_max_um:.4f} um")
    print(f"      S({lam_max_um:.3f}) = {slope*lam_max_um+intercept:.5f} "
          f"W/cm^2/um")

    # energy in the band, straight line vs trapezoid on the digitized curve
    e_line = (slope / 2 * (lam_max_um ** 2 - lam_lo_eff ** 2)
              + intercept * (lam_max_um - lam_lo_eff))       # W/cm^2
    lam_d = np.linspace(lam_lo, lam_max_um, 400)
    e_curve = np.trapezoid(np.interp(lam_d, FIG14[:, 0], FIG14[:, 1]), lam_d)
    print(f"      band irradiance: line {e_line*1e4:6.2f} W/m^2  vs "
          f"digitized curve {e_curve*1e4:6.2f} W/m^2")

    n_band = photons_from_line(slope, intercept, lam_lo_eff, lam_max_um)
    print(f"  (c) N = (1/hc) int S*lam dlam = {n_band:.4e} photons/(cm^2 s)")
    print(f"                                = {n_band*1e4:.4e} photons/(m^2 s)")

    # (d) blackbody-style total photon output using the peak-wavelength energy
    lam_peak = 2.897771e-3 / T_SUN                          # Wien, m
    e_avg = HC / lam_peak
    n_dot_sun = L_SUN / e_avg
    area_sphere = 4 * np.pi * AU_M ** 2
    n_total_d = n_dot_sun / area_sphere                      # photons/(m^2 s)
    pct = 100 * n_band * 1e4 / n_total_d
    print(f"  (d.i)  lam_peak (Wien, T={T_SUN:.0f} K) = {lam_peak*1e6:.4f} um")
    print(f"         E_avg = hc/lam_peak = {e_avg:.4e} J = {e_avg/EV_J:.3f} eV")
    print(f"  (d.ii) N_sun = L/E_avg = {L_SUN:.4e}/{e_avg:.4e} "
          f"= {n_dot_sun:.4e} photons/s")
    print(f"  (d.iii) /(4*pi*r^2 = {area_sphere:.4e} m^2) "
          f"= {n_total_d:.4e} photons/(m^2 s)")
    print(f"          = {n_total_d/1e4:.4e} photons/(cm^2 s)")
    print(f"          bond-breaking fraction = {pct:.2f} %")

    # cross-check: total photon flux implied by the solar constant
    print(f"  [check] S_earth/E_avg = {S_EARTH/e_avg:.4e} photons/(m^2 s) "
          f"({100*(S_EARTH/e_avg)/n_total_d:.1f}% of the luminosity route)")
    return dict(lam_max_um=lam_max_um, slope=slope, intercept=intercept,
                n_band=n_band, n_total_d=n_total_d / 1e4, pct=pct,
                e_avg_eV=e_avg / EV_J, lam_lo=lam_lo_eff)


# --------------------------------------------------------------------------
# Q3 -- Planck's law
# --------------------------------------------------------------------------
def planck_irradiance_at_earth(lam_m: np.ndarray, T: float = T_SUN) -> np.ndarray:
    """Spectral irradiance at 1 AU (W/m^2/m) from a blackbody photosphere.

    E_lam = pi * B_lam(T) * (R_sun / d)^2
    """
    b_lam = (2 * H_PLANCK * C_LIGHT ** 2 / lam_m ** 5
             / (np.exp(HC / (lam_m * K_B * T)) - 1.0))
    return np.pi * b_lam * (R_SUN / AU_M) ** 2


def q3(q2res: dict) -> dict:
    print("=" * 74)
    print("Q3 -- same count from Planck's law")
    print("=" * 74)
    lam_max_um = q2res["lam_max_um"]

    # (a) shape check against Fig. 1.4
    lam = np.linspace(0.05e-6, 6.0e-6, 20000)
    e_lam = planck_irradiance_at_earth(lam)
    e_lam_fig = e_lam * 1e-6 * 1e-4                # W/m^2/m -> W/cm^2/um
    i_pk = int(np.argmax(e_lam_fig))
    total_flux = np.trapezoid(e_lam, lam)
    print(f"  (a) Planck peak {e_lam_fig[i_pk]:.4f} W/cm^2/um at "
          f"{lam[i_pk]*1e6:.4f} um   (Fig. 1.4 reads ~0.21 at ~0.50 um)")
    print(f"      integrated irradiance = {total_flux:.1f} W/m^2 "
          f"(solar constant 1367 W/m^2)")
    for t_alt in (6000.0,):
        e_alt = planck_irradiance_at_earth(lam, t_alt)
        pk = np.max(e_alt) * 1e-6 * 1e-4
        print(f"      [sensitivity] T = {t_alt:.0f} K matches the figure peak "
              f"({pk:.3f} W/cm^2/um) but integrates to "
              f"{np.trapezoid(e_alt, lam):.0f} W/m^2")

    # (b) photons in the bond-breaking band
    lam_b = np.linspace(1e-8, lam_max_um * 1e-6, 20000)
    n_band = np.trapezoid(planck_irradiance_at_earth(lam_b) * lam_b / HC, lam_b)
    n_band_cm = n_band / 1e4
    print(f"  (b) N(<{lam_max_um:.3f} um) = {n_band:.4e} photons/(m^2 s) "
          f"= {n_band_cm:.4e} photons/(cm^2 s)")

    lam_b2 = np.linspace(q2res["lam_lo"] * 1e-6, lam_max_um * 1e-6, 20000)
    n_b2 = np.trapezoid(planck_irradiance_at_earth(lam_b2) * lam_b2 / HC, lam_b2)
    print(f"      [check] starting the integral at {q2res['lam_lo']:.4f} um "
          f"instead of 0 changes it by {100*(n_b2-n_band)/n_band:+.2f}%")

    # (c) agreement with the Q2 linear-fit answer
    ratio = n_band_cm / q2res["n_band"]
    print(f"  (c) Planck / linear-fit = {ratio:.2f}x  "
          f"({q2res['n_band']:.3e} vs {n_band_cm:.3e} photons/(cm^2 s))")

    # (d) total photon flux from the same blackbody
    n_tot = np.trapezoid(e_lam * lam / HC, lam)
    n_tot_cm = n_tot / 1e4
    pct_band = 100 * n_band / n_tot
    e_mean = total_flux / n_tot
    print(f"  (d) N_total = {n_tot:.4e} photons/(m^2 s) "
          f"= {n_tot_cm:.4e} photons/(cm^2 s)")
    print(f"      mean photon energy = {e_mean:.4e} J = {e_mean/EV_J:.3f} eV "
          f"(= {e_mean/(K_B*T_SUN):.3f} kT)")
    print(f"      band is {pct_band:.2f} % of the blackbody photon total")

    # (e) versus the Q2(d) average-photon-energy estimate
    print(f"  (e) Q2(d) total {q2res['n_total_d']:.4e} vs Planck "
          f"{n_tot_cm:.4e} photons/(cm^2 s) -> "
          f"{n_tot_cm/q2res['n_total_d']:.2f}x")
    return dict(n_band=n_band_cm, n_tot=n_tot_cm, ratio=ratio,
                pct_band=pct_band, e_mean_eV=e_mean / EV_J,
                total_flux=total_flux, peak=e_lam_fig[i_pk],
                lam_peak_um=lam[i_pk] * 1e6)


# --------------------------------------------------------------------------
# Q4 / Q5 -- probe thermal balance
# --------------------------------------------------------------------------
#   name: (mean distance AU, radius km, geometric albedo, IR flux W/m^2)
PLANETS = {
    "Mercury": (0.387,  2439.7, 0.12, 4150.0),
    "Venus":   (0.723,  6051.8, 0.80,  153.0),
    "Earth":   (1.000,  6378.0, 0.37,  237.0),
    "Mars":    (1.524,  3389.5, 0.29,  162.0),
    "Jupiter": (5.203, 69911.0, 0.34,   13.5),
    "Saturn":  (9.537, 58232.0, 0.34,    4.6),
    "Uranus": (19.189, 25362.0, 0.34,    0.63),
    "Neptune": (30.070, 24622.0, 0.28,   0.52),
    "Pluto":  (39.482,  1188.3, 0.47,    0.5),
}

ALT_KM = 1000.0          # assumed circular parking orbit at every body
Q_INT = 750.0            # W, internal dissipation
A_FACE = 1.0             # m^2 per face
T_LO, T_HI = -35.0, 35.0  # deg C camera limits


def sin2_rho(radius_km: float, alt_km: float = ALT_KM) -> float:
    """sin^2(rho), rho = asin(R / (R + h))  -- Lesson 6 view-factor term."""
    return (radius_km / (radius_km + alt_km)) ** 2


def heat_loads(name: str, alpha_sun: float, alpha_nadir: float,
               perihelion_au: float | None = None) -> dict:
    """Absorbed external loads (W) on the sun face and the nadir face."""
    d_au, r_km, albedo, ir_flux = PLANETS[name]
    if perihelion_au is not None:
        d_au = perihelion_au
    s_flux = S_EARTH / d_au ** 2
    f = sin2_rho(r_km)
    q_solar = alpha_sun * A_FACE * s_flux
    q_albedo = alpha_nadir * A_FACE * f * (albedo * s_flux)
    q_ir = alpha_nadir * A_FACE * f * ir_flux
    return dict(s_flux=s_flux, sin2=f, q_solar=q_solar,
                q_albedo=q_albedo, q_ir=q_ir)


def t_equilibrium(q_in: float, eps_area: float) -> float:
    """Solve Q = eps*sigma*A*T^4 for T (K).  eps_area = sum(eps_i * A_i)."""
    return (q_in / (SIGMA_SB * eps_area)) ** 0.25


def q4() -> dict:
    print("=" * 74)
    print("Q4 -- equilibrium temperature of the baseline probe")
    print("=" * 74)
    alpha, eps = 0.3, 0.7
    eps_area = eps * 6 * A_FACE
    print(f"  alpha = {alpha}, eps = {eps}, 6 x 1 m^2 cube, Q_int = {Q_INT} W, "
          f"h = {ALT_KM:.0f} km")
    print(f"  {'Planet':9s} {'S(W/m2)':>9s} {'sin^2 rho':>9s} {'Qsol':>8s} "
          f"{'Qalb':>7s} {'Qir':>8s} {'T_sun(C)':>9s} {'T_ecl(C)':>9s} {'':>6s}")
    out = {}
    for name in PLANETS:
        h = heat_loads(name, alpha, alpha)
        q_hot = h["q_solar"] + h["q_albedo"] + h["q_ir"] + Q_INT
        q_cold = h["q_ir"] + Q_INT
        t_hot = t_equilibrium(q_hot, eps_area) - 273.15
        t_cold = t_equilibrium(q_cold, eps_area) - 273.15
        ok = "OK" if (T_LO <= t_cold and t_hot <= T_HI) else "NO"
        out[name] = (t_hot, t_cold, ok)
        print(f"  {name:9s} {h['s_flux']:9.2f} {h['sin2']:9.4f} "
              f"{h['q_solar']:8.1f} {h['q_albedo']:7.1f} {h['q_ir']:8.1f} "
              f"{t_hot:9.1f} {t_cold:9.1f} {ok:>6s}")

    hp = heat_loads("Mercury", alpha, alpha, perihelion_au=0.3075)
    t_p = t_equilibrium(hp["q_solar"] + hp["q_albedo"] + hp["q_ir"] + Q_INT,
                        eps_area) - 273.15
    print(f"  [sensitivity] Mercury at perihelion (0.3075 AU): "
          f"T_sun = {t_p:.1f} C")
    t_deep = t_equilibrium(Q_INT, eps_area) - 273.15
    print(f"  [floor] internal heat alone: T = {t_deep:.1f} C "
          f"(the outer-planet asymptote)")

    # altitude sensitivity at the marginal planet
    print("  [sensitivity] Venus sunlit case vs assumed orbit altitude:")
    d_au, r_km, albedo, ir_flux = PLANETS["Venus"]
    s_flux = S_EARTH / d_au ** 2
    for h in (300.0, 1000.0, 5000.0):
        f = (r_km / (r_km + h)) ** 2
        q = (alpha * s_flux + alpha * f * albedo * s_flux + alpha * f * ir_flux
             + Q_INT)
        print(f"      h = {h:6.0f} km: sin^2 rho = {f:.4f}, Q = {q:7.1f} W, "
              f"T = {t_equilibrium(q, eps_area)-273.15:5.1f} C")

    # Kirchhoff sensitivity: weight the planetary IR term by eps, not alpha
    print("  [sensitivity] IR term weighted by eps = 0.7 instead of alpha:")
    keep = []
    for name in PLANETS:
        h = heat_loads(name, alpha, alpha)
        q_ir_eps = h["q_ir"] * eps / alpha
        t_hot = t_equilibrium(h["q_solar"] + h["q_albedo"] + q_ir_eps + Q_INT,
                              eps_area) - 273.15
        t_cold = t_equilibrium(q_ir_eps + Q_INT, eps_area) - 273.15
        ok = T_LO <= t_cold and t_hot <= T_HI
        if ok:
            keep.append(name)
        print(f"      {name:9s} T_sun = {t_hot:7.1f} C   "
              f"T_ecl = {t_cold:7.1f} C   {'OK' if ok else 'NO'}")
    print(f"      imageable set: {', '.join(keep)} (unchanged)")
    return out


def q5() -> dict:
    print("=" * 74)
    print("Q5 -- $15K thermal control design")
    print("=" * 74)
    budget, cost_per_kg = 15_000.0, 25_000.0
    print(f"  budget {budget:,.0f} USD at {cost_per_kg:,.0f} USD/kg "
          f"-> {budget/cost_per_kg:.2f} kg of mass to spend")

    # --- option costs
    mli_cost = 2 * 0.3 * cost_per_kg
    louver_cost = 1 * (2.1 + 0.2) * cost_per_kg
    print(f"  MLI on 2 faces : 2 m^2 x 0.3 kg/m^2 = 0.60 kg = ${mli_cost:,.0f}")
    print(f"  louvers, 1 m^2 : (2.1 + 0.2) kg     = 2.30 kg = ${louver_cost:,.0f}"
          f"  ({louver_cost/budget:.1f}x budget)")

    # heater-only option: size for the deep-space cold case
    eps_area_base = 0.7 * 6
    q_need = SIGMA_SB * eps_area_base * (T_LO + 273.15) ** 4
    heater_w = q_need - Q_INT
    heater_cost = 0.025 * heater_w * cost_per_kg
    print(f"  heaters only   : need {heater_w:.1f} W to hold {T_LO:.0f} C "
          f"-> {0.025*heater_w:.2f} kg = ${heater_cost:,.0f} "
          f"(and Mercury still runs hot)")

    # --- selected design: MLI on sun + nadir faces, white paint elsewhere
    a_mli, e_mli = 0.05, 0.05
    e_white = 0.85
    eps_area = 4 * e_white * A_FACE + 2 * e_mli * A_FACE
    print(f"\n  selected: MLI (alpha=eps={e_mli}) on the sun and nadir faces, "
          f"white paint (eps={e_white}) on the other four")
    print(f"  sum(eps*A) = 4({e_white}) + 2({e_mli}) = {eps_area:.2f} m^2  "
          f"(baseline was {eps_area_base:.2f})")
    print(f"  {'Planet':9s} {'Qsol':>8s} {'Qalb':>7s} {'Qir':>8s} "
          f"{'T_sun(C)':>9s} {'T_ecl(C)':>9s} {'':>6s}")
    out = {}
    for name in PLANETS:
        h = heat_loads(name, a_mli, a_mli)
        q_hot = h["q_solar"] + h["q_albedo"] + h["q_ir"] + Q_INT
        t_hot = t_equilibrium(q_hot, eps_area) - 273.15
        t_cold = t_equilibrium(h["q_ir"] + Q_INT, eps_area) - 273.15
        ok = "OK" if (T_LO <= t_cold and t_hot <= T_HI) else "NO"
        out[name] = (t_hot, t_cold, ok)
        print(f"  {name:9s} {h['q_solar']:8.1f} {h['q_albedo']:7.1f} "
              f"{h['q_ir']:8.1f} {t_hot:9.1f} {t_cold:9.1f} {ok:>6s}")

    hp = heat_loads("Mercury", a_mli, a_mli, perihelion_au=0.3075)
    t_p = t_equilibrium(hp["q_solar"] + hp["q_albedo"] + hp["q_ir"] + Q_INT,
                        eps_area) - 273.15
    print(f"  [sensitivity] Mercury at perihelion: T_sun = {t_p:.1f} C")

    # the half-price variant that fails that sensitivity case
    eps_area_cheap = 0.05 + 0.85 + 4 * 0.7
    hc_ = heat_loads("Mercury", a_mli, 0.252, perihelion_au=0.3075)
    t_cheap = t_equilibrium(hc_["q_solar"] + hc_["q_albedo"] + hc_["q_ir"]
                            + Q_INT, eps_area_cheap) - 273.15
    print(f"  [rejected] 1 m^2 MLI variant ($7,500): Mercury perihelion "
          f"T_sun = {t_cheap:.1f} C")
    print(f"  cost: ${mli_cost:,.0f} of ${budget:,.0f} "
          f"({100*mli_cost/budget:.0f}% of budget), paint is mass-negligible")
    return out


# --------------------------------------------------------------------------
# Q6 / Q8 -- outgassing
# --------------------------------------------------------------------------
def q6() -> None:
    print("=" * 74)
    print("Q6 -- Neoprene outgassing")
    print("=" * 74)
    # (a) 1 Torr*L/(cm^2 s) in W/m^2
    j_per_torr_l = TORR_PA * 1e-3                     # J per Torr*litre
    w_per_m2 = j_per_torr_l / 1e-4                    # spread over 1 cm^2
    print(f"  (a) 1 Torr*L = {TORR_PA} Pa x 1e-3 m^3 = {j_per_torr_l:.6f} J")
    print(f"      1 Torr*L/(cm^2 s) = {j_per_torr_l:.6f} J / (1e-4 m^2 s) "
          f"= {w_per_m2:.2f} W/m^2")
    print(f"      inverting: 1 W/m^2 = {1/w_per_m2:.4e} Torr*L/(cm^2 s)")
    rate_torr = 1e-5
    rate_w = rate_torr * w_per_m2
    print(f"      so {rate_torr:.0e} Torr*L/(cm^2 s) = {rate_w:.4e} W/m^2")

    # (b) molecules per unit area per second
    T = 298.0
    n_dot = rate_w / (K_B * T)                        # molecules/(m^2 s)
    print(f"  (b) N = Q/(kT) = {rate_w:.4e}/({K_B:.6e} x {T:.0f}) "
          f"= {n_dot:.4e} molecules/(m^2 s)")
    print(f"      = {n_dot/1e4:.4e} molecules/(cm^2 s)")
    n_296 = rate_w * 2.4470e20
    print(f"  [check] Pisacane Table 10.2 factor at 296 K: "
          f"{n_296/1e4:.4e} molecules/(cm^2 s) "
          f"({100*(n_296-n_dot)/n_dot:+.1f}%)")


def q8() -> None:
    print("=" * 74)
    print("Q8 -- Kapton outgassing rate from an ASTM E-595 TML")
    print("=" * 74)
    side_cm = 10.0
    area_cm2 = side_cm * side_cm
    thick_cm = 0.001 * 2.54
    rho = 1.5                                  # g/cm^3
    tml = 0.005
    molar = 15.0                               # g/mol
    duration_s = 24 * 3600.0
    T = 298.0

    volume = area_cm2 * thick_cm
    mass = rho * volume
    dm = tml * mass
    print(f"  specimen {side_cm:.0f} x {side_cm:.0f} cm, t = {thick_cm:.5f} cm")
    print(f"  V = {volume:.4f} cm^3, m = {mass:.4f} g, "
          f"dm = 0.5% = {dm:.6f} g in {duration_s:.0f} s")

    moles = dm / molar
    # PV = nRT with R in Torr*L/(mol K)
    R_torr = 62.363577                         # L*Torr/(mol*K)
    pv = moles * R_torr * T                    # Torr*L
    q_torr = pv / (area_cm2 * duration_s)
    print(f"  n = {moles:.4e} mol -> PV = nRT = {pv:.4f} Torr*L")
    print(f"  Q = PV/(A t) = {q_torr:.4e} Torr*L/(cm^2 s)")

    w_per_m2 = TORR_PA * 1e-3 / 1e-4
    q_w = q_torr * w_per_m2
    print(f"    = {q_w:.4e} W/m^2   (Pisacane Table 10.3 lists Kapton foil "
          f"at 1e-4 W/m^2)")

    # equivalent route straight through Pisacane Eq. (10.2)
    m_dot = dm * 1e-3 / (area_cm2 * 1e-4 * duration_s)      # kg/(m^2 s)
    q_alt = m_dot * K_B * T * N_A * 1e3 / (molar)           # W/m^2
    print(f"  [check] Eq. 10.2 route: m_dot = {m_dot:.4e} kg/(m^2 s) -> "
          f"Q = {q_alt:.4e} W/m^2")
    q_hot = q_torr * 398.15 / T
    print(f"  [sensitivity] referenced to the 125 C test temperature: "
          f"{q_hot:.4e} Torr*L/(cm^2 s)")


# --------------------------------------------------------------------------
# Q7 -- cleanroom classes
# --------------------------------------------------------------------------
def iso_concentration(iso_class: float, d_um: np.ndarray) -> np.ndarray:
    """C_n = 10^N * (0.1/D)^2.08  particles per m^3  (ISO 14644-1)."""
    return 10.0 ** iso_class * (0.1 / d_um) ** 2.08


def q7() -> None:
    print("=" * 74)
    print("Q7 -- ISO 14644-1 cleanroom limits")
    print("=" * 74)
    checks = [(5, 0.5, 3520), (7, 0.5, 352000), (3, 0.2, 237), (1, 0.1, 10)]
    for n, d, book in checks:
        val = iso_concentration(n, np.array([d]))[0]
        print(f"  ISO {n}, D = {d} um: {val:10.1f} /m^3   "
              f"(tabulated {book:,})")


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
def _caption(fig, text: str) -> None:
    fig.text(0.5, 0.012, text, ha="center", va="bottom",
             fontsize=9, style="italic", wrap=True)


def fig_solar_fit(q2res: dict) -> None:
    slope, intercept = q2res["slope"], q2res["intercept"]
    lam_max = q2res["lam_max_um"]
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.plot(FIG14[:, 0], FIG14[:, 1], "o-", color="#1f4e79", ms=4, lw=1.6,
            label="Fig. 1.4 solar spectrum (read off the figure)")
    x = np.linspace(0.19, 0.42, 100)
    ax.plot(x, slope * x + intercept, "--", color="#c00000", lw=2,
            label=fr"linear fit $S={slope:.3f}\lambda{intercept:+.3f}$")
    band = np.linspace(q2res["lam_lo"], lam_max, 60)
    ax.fill_between(band, 0, slope * band + intercept, color="#c00000",
                    alpha=0.18)
    ax.axvline(lam_max, color="0.35", ls=":", lw=1.4)
    ax.annotate(fr"$\lambda_{{max}}={lam_max:.3f}\ \mu$m" "\nC-C bond cutoff",
                xy=(lam_max, 0.055), xytext=(42, -12),
                textcoords="offset points", fontsize=8.5,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6"),
                arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.set_xlim(0, 1.6)
    ax.set_ylim(0, 0.235)
    ax.set_xlabel(r"Wavelength  $\lambda$  ($\mu$m)")
    ax.set_ylabel(r"Irradiance  $S(\lambda)$  (W cm$^{-2}$ $\mu$m$^{-1}$)")
    ax.set_title("Q2b: straight-line fit to the solar spectrum over the "
                 "bond-breaking band")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8.5, loc="upper right")
    fig.subplots_adjust(bottom=0.19)
    _caption(fig, "Figure 1: Solar irradiance at 1 AU with the linear "
                  r"approximation used over 0.20 to 0.357 $\mu$m (shaded).")
    fig.savefig(FIG_DIR / "fig1_solar_spectrum_fit.png", dpi=150)
    plt.close(fig)


def fig_planck(q2res: dict) -> None:
    lam = np.linspace(0.1e-6, 3.0e-6, 2000)
    e_fig = planck_irradiance_at_earth(lam) * 1e-6 * 1e-4
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.plot(lam * 1e6, e_fig, color="#c00000", lw=2,
            label=fr"Planck, $T={T_SUN:.0f}$ K, scaled by $(R_\odot/d)^2$")
    ax.plot(FIG14[:, 0], FIG14[:, 1], "o", color="#1f4e79", ms=4.5,
            label="Fig. 1.4 measured spectrum")
    ax.axvline(q2res["lam_max_um"], color="0.35", ls=":", lw=1.4)
    ax.annotate("blackbody runs high in the UV\n(no line blanketing)",
                xy=(0.30, 0.082), xytext=(38, 46),
                textcoords="offset points", fontsize=8.5,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6"),
                arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.set_xlim(0, 3.0)
    ax.set_ylim(0, 0.235)
    ax.set_xlabel(r"Wavelength  $\lambda$  ($\mu$m)")
    ax.set_ylabel(r"Irradiance  $S(\lambda)$  (W cm$^{-2}$ $\mu$m$^{-1}$)")
    ax.set_title("Q3a: Planck blackbody vs. the measured solar spectrum")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8.5)
    fig.subplots_adjust(bottom=0.19)
    _caption(fig, "Figure 2: A 5772 K blackbody reproduces the peak but "
                  "overshoots the ultraviolet, which is where the "
                  "bond-breaking photons live.")
    fig.savefig(FIG_DIR / "fig2_planck_vs_measured.png", dpi=150)
    plt.close(fig)


def _temp_plot(res: dict, title: str, caption: str, fname: str) -> None:
    names = list(res.keys())
    x = np.arange(len(names))
    t_hot = np.array([res[n][0] for n in names])
    t_cold = np.array([res[n][1] for n in names])
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ax.axhspan(T_LO, T_HI, color="#70ad47", alpha=0.16,
               label=f"camera limits ({T_LO:.0f} to {T_HI:.0f} $^\\circ$C)")
    ax.plot(x, t_hot, "o-", color="#c00000", lw=1.8, ms=7, label="sunlit face")
    ax.plot(x, t_cold, "s--", color="#1f4e79", lw=1.8, ms=6, label="eclipse")
    for xi, th, tc in zip(x, t_hot, t_cold):
        ax.annotate(f"{th:.0f}", xy=(xi, th), xytext=(0, 9),
                    textcoords="offset points", fontsize=7.5, ha="center",
                    color="#c00000")
        ax.annotate(f"{tc:.0f}", xy=(xi, tc), xytext=(0, -14),
                    textcoords="offset points", fontsize=7.5, ha="center",
                    color="#1f4e79")
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=25, ha="right")
    ax.set_ylabel(r"Equilibrium temperature ($^\circ$C)")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8.5, loc="upper right")
    fig.subplots_adjust(bottom=0.28)
    _caption(fig, caption)
    fig.savefig(FIG_DIR / fname, dpi=150)
    plt.close(fig)


def fig_iso() -> None:
    d = np.logspace(np.log10(0.1), np.log10(10.0), 300)
    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    cmap = plt.get_cmap("viridis")
    for n in range(1, 10):
        ax.loglog(d, iso_concentration(n, d), lw=1.8,
                  color=cmap((n - 1) / 8.0), label=f"ISO {n}")
    ax.set_xlabel(r"Particle size  $D$  ($\mu$m)")
    ax.set_ylabel(r"Maximum concentration  $C_n$  (particles/m$^3$)")
    ax.set_title("Q7: ISO 14644-1 cleanroom particle concentration limits")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8, ncol=3, loc="upper right")
    ax.set_ylim(1e-2, 1e9)
    fig.subplots_adjust(bottom=0.19)
    _caption(fig, r"Figure 5: $C_n = 10^N(0.1/D)^{2.08}$ for ISO classes 1 "
                  "through 9; every class is the same $-2.08$ slope, shifted "
                  "one decade per class.")
    fig.savefig(FIG_DIR / "fig5_iso_cleanroom.png", dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------
def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    FIG_DIR.mkdir(exist_ok=True)

    q2res = q2()
    print()
    q3res = q3(q2res)
    print()
    base = q4()
    print()
    design = q5()
    print()
    q6()
    print()
    q7()
    print()
    q8()

    fig_solar_fit(q2res)
    fig_planck(q2res)
    _temp_plot(base,
               "Q4a: baseline probe equilibrium temperature by destination",
               "Figure 3: Baseline probe (alpha = 0.3, eps = 0.7, 750 W "
               "internal). Only Venus, Earth and Mars sit inside the "
               "high-resolution camera limits in both cases.",
               "fig3_equilibrium_temps.png")
    _temp_plot(design,
               "Q5: probe temperature with the $15K thermal control design",
               "Figure 4: With MLI on the sun and nadir faces and white paint "
               "elsewhere, every destination from Mercury to Pluto falls "
               "inside the camera limits.",
               "fig4_thermal_design.png")
    fig_iso()
    print("\nFigures written to:", FIG_DIR)


if __name__ == "__main__":
    main()
