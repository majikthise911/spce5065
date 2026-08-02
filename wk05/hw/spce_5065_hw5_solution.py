"""SPCE 5065 -- Homework 5 solution.

Micrometeoroids and orbital debris (MMOD). Covers the quantitative problems:

  P2  Kinetic energy vs particle diameter at ISS altitude (log-log) + satellite KE
  P3  1-g debris vs bowling-ball PE equivalence; 20 km/s micrometeoroid case
  P5  Grun sporadic-meteoroid flux (Lesson 12 slide 4) for ISS/GPS/GEO,
      shielding + gravitational focusing, Poisson time-between-impacts
  P9  Whipple shield bumper/wall thickness vs standoff (Pisacane Eqs. 11.27-11.31)

Outputs:
  - Console tables reproducing every boxed number in the submission
  - figures/fig1_ke_vs_diameter.png      (P2a/b)
  - figures/fig2_flux_vs_mass.png        (P5a)
  - figures/fig3_whipple_thickness.png   (P9)

Conceptual/research problems (P1, P4, P6, P7, P8) are answered in the
submission document; they need no code.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------
MU_EARTH = 398600.5      # km^3/s^2
R_E = 6378.0             # km
G0 = 9.81                # m/s^2  (surface gravity, P3)
H_ATM = 100.0            # km     (top of atmosphere per HW5 clarification)
R_A = R_E + H_ATM        # km     (radius to top of atmosphere)

H_ISS = 400.0            # km   ISS altitude assumption
H_GPS = 20200.0          # km   GPS (semi-synchronous)
H_GEO = 35786.0          # km   GEO

RHO_PARTICLE = 1.0       # g/cm^3 (given, P2 and P5 mass<->diameter conversion)

FIG_DIR = Path(__file__).parent / "figures"


def v_circ_kms(h_km: float) -> float:
    """Circular orbital velocity (km/s), v = sqrt(mu/(R_E+h))."""
    return np.sqrt(MU_EARTH / (R_E + h_km))


def sphere_mass_g(d_cm: float | np.ndarray, rho: float = RHO_PARTICLE):
    """Mass (g) of a sphere of diameter d (cm), m = (pi/6) rho d^3."""
    return (np.pi / 6.0) * rho * np.asarray(d_cm, dtype=float) ** 3


# --------------------------------------------------------------------------
# P2 -- kinetic energy vs diameter at ISS altitude
# --------------------------------------------------------------------------
def p2_results() -> None:
    print("=" * 70)
    print("P2 -- kinetic energy of orbiting objects at ISS altitude")
    print("=" * 70)
    v = v_circ_kms(H_ISS) * 1000.0                      # m/s
    print(f"  v_circ(400 km) = {v/1000:.4f} km/s")
    for d in [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]:      # cm
        m_kg = sphere_mass_g(d) * 1e-3
        ke = 0.5 * m_kg * v ** 2
        print(f"  d = {d:9.3f} cm   m = {m_kg:.3e} kg   KE = {ke:.3e} J")
    print("  -- satellites, same orbit --")
    for M in [5.0, 50.0, 100.0]:
        ke = 0.5 * M * v ** 2
        d_eq = (6.0 * M * 1e3 / (np.pi * RHO_PARTICLE)) ** (1.0 / 3.0)
        print(f"  M = {M:5.0f} kg   KE = {ke:.3e} J "
              f"(= {ke/4.184e6:.1f} kg TNT)   same-KE particle d = {d_eq:.1f} cm")


# --------------------------------------------------------------------------
# P3 -- debris KE vs a falling bowling ball
# --------------------------------------------------------------------------
def p3_results() -> None:
    print("=" * 70)
    print("P3 -- 1-g debris vs 2-kg bowling ball from 100 m")
    print("=" * 70)
    m_ball, h = 2.0, 100.0
    m_d = 1.0e-3                                        # kg
    E_pe = m_ball * G0 * h
    v_impact = np.sqrt(2.0 * E_pe / m_d)
    print(f"  (a) PE = mgh = {E_pe:.1f} J  ->  v = sqrt(2E/m) = "
          f"{v_impact:.1f} m/s = {v_impact/1000:.2f} km/s")
    v_mm = 20.0e3
    E_mm = 0.5 * m_d * v_mm ** 2
    h_eq = E_mm / (m_ball * G0)
    print(f"  (b) KE(20 km/s) = {E_mm:.3e} J   equivalent drop height = "
          f"{h_eq:.0f} m = {h_eq/1000:.2f} km")
    print(f"  (c) ratio = {E_mm/E_pe:.1f}x  (= (20/{v_impact/1000:.2f})^2)")


# --------------------------------------------------------------------------
# P5 -- Grun sporadic meteoroid flux (Lesson 12 slide 4, corrected F3 term)
# --------------------------------------------------------------------------
def grun_flux_interplanetary(m_g: np.ndarray | float):
    """Unshielded cumulative sporadic flux F_spo(m), particles/m^2/yr.

    Lesson 12 slide 4 (= Pisacane Eq. 11.2, corrected: third term is F3):
      F_spo = 3.15576e7 * [F1 + F2 + F3],  m in grams.
    """
    m = np.asarray(m_g, dtype=float)
    f1 = (2.2e3 * m ** 0.306 + 15.0) ** (-4.38)
    f2 = 1.3e-9 * (m + 1.0e11 * m ** 2 + 1.0e27 * m ** 4) ** (-0.36)
    f3 = 1.3e-16 * (m + 1.0e6 * m ** 2) ** (-0.85)
    return 3.15576e7 * (f1 + f2 + f3)


def shielding_factor(r_km: float, branch: str = "nadir") -> float:
    """Earth-shielding factor, sin(theta) = R_a/r (Lesson 12 slide 5).

    branch="nadir"  -> chi_3 = cos(theta)         (Pisacane Eq. 11.5, surface
                                                   normal pointing at Earth;
                                                   the Earth-orbiter case used
                                                   in this course)
    branch="random" -> chi_2 = (1 + cos(theta))/2 (Pisacane Eq. 11.4, surface
                                                   normal randomly oriented)
    """
    cos_t = float(np.sqrt(1.0 - (R_A / r_km) ** 2))
    if branch == "random":
        return 0.5 * (1.0 + cos_t)
    return cos_t


def focusing_factor(r_km: float) -> float:
    """Gravitational focusing factor G = 1 + R_a/r (Lesson 12 slide 6)."""
    return 1.0 + R_A / r_km


def flux_at_orbit(m_g, h_km: float, branch: str = "nadir"):
    """F_sp(m, r) = F_spo(m) * chi(r) * G(r), particles/m^2/yr."""
    r = R_E + h_km
    return (grun_flux_interplanetary(m_g)
            * shielding_factor(r, branch) * focusing_factor(r))


def p5_results() -> None:
    print("=" * 70)
    print("P5 -- micrometeoroid flux and time between impacts (A = 10 m^2)")
    print("=" * 70)
    orbits = [("ISS", H_ISS), ("GPS", H_GPS), ("GEO", H_GEO)]
    for name, h in orbits:
        r = R_E + h
        c3, c2, g = (shielding_factor(r, "nadir"),
                     shielding_factor(r, "random"), focusing_factor(r))
        print(f"  {name}: r = {r:7.0f} km  sin(th) = {R_A/r:.4f}  G = {g:.4f} | "
              f"nadir chi3 = {c3:.4f} (chi*G = {c3*g:.4f})  | "
              f"random chi2 = {c2:.4f} (chi*G = {c2*g:.4f})")

    A = 10.0                       # m^2
    P_TH = 1.0e-4                  # 0.01 %
    for branch in ("nadir", "random"):
        print(f"\n  --- shielding branch: {branch} ---")
        print(f"  {'size':>7} {'mass (g)':>11} | " +
              " | ".join(f"{n}: F, t(P=.01%), 1/(FA)" for n, _ in orbits))
        for d_cm in [0.1, 1.0, 10.0]:
            m = float(sphere_mass_g(d_cm))
            row = [f"  {d_cm:5.1f}cm {m:11.4e} |"]
            for name, h in orbits:
                F = float(flux_at_orbit(m, h, branch))
                lam = F * A                               # events/yr
                t_p = -np.log(1.0 - P_TH) / lam           # yr to reach 0.01 %
                row.append(f" {F:9.3e} {t_p:9.3e} {1.0/lam:9.3e} |")
            print("".join(row))

        print("    probability of >=1 impact in a 10-yr mission:")
        for d_cm in [0.1, 1.0, 10.0]:
            m = float(sphere_mass_g(d_cm))
            probs = [
                f"{name} {100*(1-np.exp(-flux_at_orbit(m, h, branch)*A*10.0)):.4g}%"
                for name, h in orbits]
            print(f"      d = {d_cm:4.1f} cm : " + ",  ".join(probs))


# --------------------------------------------------------------------------
# P9 -- Whipple shield sizing (Pisacane Eqs. 11.27-11.31, Christiansen 2003)
# --------------------------------------------------------------------------
def whipple_thickness(S_cm, d_cm: float, rho_p: float, V_kms: float,
                      sigma_ksi: float, rho_b: float, rho_w: float,
                      theta_deg: float = 0.0):
    """Bumper and wall thickness (cm) vs standoff S (cm), V >= 7 km/s.

    t_b = c_b d rho_p/rho_b                                   (Eq. 11.27)
    t_w = c_w d^1/2 m_p^1/3 (rho_p rho_b)^1/6 / rho_w
          * S^-3/4 (sigma/70)^-1/2 V cos(theta)               (Eq. 11.28)
    c_b = 0.25 (S/d < 30) or 0.20 (S/d >= 30)                 (Eq. 11.29)
    c_w = 0.79 k;  k = (S/d/15)^-0.185 for S/d < 15 else 1    (Eqs. 11.30-31)
    Units: cm, g, g/cm^3, km/s, ksi; theta from surface normal (<= 65 deg).
    """
    S = np.asarray(S_cm, dtype=float)
    m_p = (4.0 * np.pi / 3.0) * (d_cm / 2.0) ** 3 * rho_p     # g
    c_b = np.where(S / d_cm < 30.0, 0.25, 0.20)
    t_b = c_b * d_cm * rho_p / rho_b
    k = np.where(S / d_cm < 15.0, (S / d_cm / 15.0) ** (-0.185), 1.0)
    t_w = (0.79 * k * d_cm ** 0.5 * m_p ** (1.0 / 3.0)
           * (rho_p * rho_b) ** (1.0 / 6.0) / rho_w
           * S ** (-0.75) * (sigma_ksi / 70.0) ** (-0.5)
           * V_kms * np.cos(np.radians(theta_deg)))
    return t_b, t_w


# HW9 inputs: meteoroid rho_p = 1.6, d = 1 cm, V = 80 km/s, Al 7075-T6
RHO_AL7075 = 2.81        # g/cm^3 (Al 7075-T6)
SIGMA_7075 = 65.0        # ksi (given)


def p9_results() -> None:
    print("=" * 70)
    print("P9 -- Whipple shield sizing, Al 7075-T6, d=1 cm, 1.6 g/cm^3, 80 km/s")
    print("=" * 70)
    for S in [1.0, 5.0, 10.0, 15.0, 20.0, 30.0]:
        t_b, t_w = whipple_thickness(S, 1.0, 1.6, 80.0,
                                     SIGMA_7075, RHO_AL7075, RHO_AL7075)
        k = (S / 1.0 / 15.0) ** (-0.185) if S / 1.0 < 15.0 else 1.0
        print(f"  S = {S:5.1f} cm   S/d = {S:4.0f}   k = {k:.4f}   "
              f"t_b = {float(t_b):.4f} cm   t_w = {float(t_w):.3f} cm")

    # Verification against the published worked example (Example 11.2: d = 1 cm
    # Al at 2.7 g/cm^3, Al 6061-T6 at 35 ksi, V = 10 km/s), which gives
    # t_b = 0.25 cm.
    t_b_ck, _ = whipple_thickness(10.0, 1.0, 2.7, 10.0, 35.0, 2.7, 2.7)
    print(f"  [check vs Example 11.2] t_b = {float(t_b_ck):.2f} cm "
          f"(published value 0.25 cm)")


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
def _caption(fig, text: str) -> None:
    fig.text(0.5, 0.01, text, ha="center", va="bottom",
             fontsize=9, style="italic")


def fig1_ke_vs_diameter() -> None:
    v = v_circ_kms(H_ISS) * 1000.0                       # m/s
    d = np.logspace(-3, 2, 400)                          # cm: 10 um to 1 m
    ke = 0.5 * sphere_mass_g(d) * 1e-3 * v ** 2
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    ax.loglog(d, ke, color="#1f4e79", lw=2,
              label=r"1 g/cm$^3$ sphere at $v_{circ}$ = 7.67 km/s")
    # Satellite KE levels go in the legend rather than as inline text: the
    # 50 kg and 100 kg lines sit within a factor of 2, so stacked labels collide.
    sat_style = [("5 kg small sat", 5.0, "#c00000"),
                 ("50 kg medium sat", 50.0, "#bf8f00"),
                 ("100 kg large sat", 100.0, "#385723")]
    for lab, M, color in sat_style:
        ke_sat = 0.5 * M * v ** 2
        ax.axhline(ke_sat, color=color, ls="--", lw=1.3,
                   label=f"{lab}: {ke_sat:.2e} J")
    for d_mark, note, off in [(0.01, "100 um", (10, -14)),
                              (0.1, "1 mm", (10, -14)),
                              (1.0, "1 cm", (10, -14)),
                              (10.0, "10 cm", (-4, -30))]:
        ke_m = 0.5 * float(sphere_mass_g(d_mark)) * 1e-3 * v ** 2
        ax.plot(d_mark, ke_m, "o", color="#c00000", ms=5)
        ax.annotate(f"{note}\n{ke_m:.2e} J", xy=(d_mark, ke_m), xytext=off,
                    textcoords="offset points", fontsize=7.5,
                    bbox=dict(boxstyle="round,pad=0.25", fc="white",
                              ec="0.6", alpha=0.9))
    ax.set_xlabel("Particle diameter  d  (cm)")
    ax.set_ylabel("Kinetic energy  (J)")
    ax.set_title("P2: Kinetic energy vs particle diameter at ISS altitude")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8, loc="lower right", framealpha=0.95)
    fig.subplots_adjust(bottom=0.16)
    _caption(fig, "Figure 1: KE of a 1 g/cm$^3$ sphere in a 400 km circular "
             "orbit vs diameter (log-log), with 5/50/100 kg satellite KE.")
    fig.savefig(FIG_DIR / "fig1_ke_vs_diameter.png", dpi=150)
    plt.close(fig)


def fig2_flux_vs_mass() -> None:
    m = np.logspace(-5, 1, 400)                          # g
    # Two panels: the flux itself spans 9 decades, which visually collapses the
    # ~10% orbit-to-orbit spread. The lower panel plots the geometry correction
    # chi*G alone, which is what actually differs between orbits.
    fig, (ax, ax2) = plt.subplots(
        2, 1, figsize=(7.2, 6.4), sharex=True,
        gridspec_kw=dict(height_ratios=[3, 1.15], hspace=0.12))
    styles = [("ISS (400 km)", H_ISS, "#1f4e79", "-"),
              ("GPS (20,200 km)", H_GPS, "#c00000", "--"),
              ("GEO (35,786 km)", H_GEO, "#385723", "-.")]
    for lab, h, color, ls in styles:
        ax.loglog(m, flux_at_orbit(m, h), color=color, ls=ls, lw=2, label=lab)
    # ISS is the only orbit where the shielding-branch choice matters; show the
    # random-orientation case so the sensitivity is visible on the plot.
    ax.loglog(m, flux_at_orbit(m, H_ISS, "random"), color="#00b0f0",
              ls=(0, (1, 3)), lw=1.6,
              label=r"ISS, random orientation ($\chi_2$)")

    # Lower panel: net geometry factor chi*G, flat in mass, one line per case.
    for lab, h, color, ls in styles:
        r = R_E + h
        val = shielding_factor(r) * focusing_factor(r)
        ax2.semilogx(m, np.full_like(m, val), color=color, ls=ls, lw=2)
        ax2.annotate(f"{val:.3f}", xy=(m[-1], val), xytext=(6, -3),
                     textcoords="offset points", fontsize=7.5, color=color)
    r_iss = R_E + H_ISS
    val2 = shielding_factor(r_iss, "random") * focusing_factor(r_iss)
    ax2.semilogx(m, np.full_like(m, val2), color="#00b0f0",
                 ls=(0, (1, 3)), lw=1.8)
    ax2.annotate(f"{val2:.3f}", xy=(m[-1], val2), xytext=(6, -3),
                 textcoords="offset points", fontsize=7.5, color="#00b0f0")
    ax2.axhline(1.0, color="0.6", lw=0.9)
    ax2.set_ylim(0.45, 1.45)
    ax2.set_ylabel(r"net $\chi G$", fontsize=9)
    ax2.set_xlabel("Micrometeoroid mass  m  (g)")
    ax2.grid(True, which="both", alpha=0.3)
    # Mark the part (b) sizes; labels ride at the top of the axes so they
    # never sit on top of the flux curves.
    for d_cm in [0.1, 1.0]:
        m_mark = float(sphere_mass_g(d_cm))
        ax.axvline(m_mark, color="0.55", ls=":", lw=1)
        ax.annotate(f"{d_cm:g} cm dia.\n({m_mark:.3g} g)",
                    xy=(m_mark, 0.97), xycoords=("data", "axes fraction"),
                    xytext=(5, 0), textcoords="offset points",
                    fontsize=7.5, color="0.30", va="top",
                    bbox=dict(boxstyle="round,pad=0.25", fc="white",
                              ec="0.75", alpha=0.9))
    ax.set_ylabel(r"Cumulative flux  $F_{sp}(>m)$  (particles m$^{-2}$ yr$^{-1}$)")
    ax.set_title("P5a: Sporadic micrometeoroid flux at ISS, GPS, and GEO")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    fig.subplots_adjust(bottom=0.19, top=0.94)
    _caption(fig, "Figure 2: Top, Grun cumulative flux (Lesson 12 slide 4) with Earth shielding and\n"
             "gravitational focusing. Bottom, the net geometry factor alone, where the orbits separate:\n"
             "only the nadir-facing ISS case departs from the others.")
    fig.savefig(FIG_DIR / "fig2_flux_vs_mass.png", dpi=150)
    plt.close(fig)


def fig3_whipple_thickness() -> None:
    S = np.linspace(1.0, 30.0, 300)
    t_b, t_w = whipple_thickness(S, 1.0, 1.6, 80.0,
                                 SIGMA_7075, RHO_AL7075, RHO_AL7075)
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    # Log y: the wall spans 2 to 47 cm while the bumper sits near 0.13 cm, so a
    # linear axis flattens the bumper onto the x-axis.
    ax.semilogy(S, t_w, color="#1f4e79", lw=2, label=r"wall $t_w$")
    ax.semilogy(S, t_b, color="#c00000", lw=2, ls="--", label=r"bumper $t_b$")
    for S_mark, off in [(1.0, (26, -12)), (10.0, (14, 12)), (30.0, (-14, 16))]:
        _, t_w_m = whipple_thickness(S_mark, 1.0, 1.6, 80.0,
                                     SIGMA_7075, RHO_AL7075, RHO_AL7075)
        ax.plot(S_mark, float(t_w_m), "o", color="#1f4e79", ms=5)
        ax.annotate(f"S={S_mark:.0f} cm: {float(t_w_m):.2f} cm",
                    xy=(S_mark, float(t_w_m)), xytext=off,
                    textcoords="offset points", fontsize=8,
                    ha="right" if S_mark == 30.0 else "left",
                    bbox=dict(boxstyle="round,pad=0.25", fc="white",
                              ec="0.6", alpha=0.9),
                    arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.annotate(r"$c_b$ steps 0.25$\rightarrow$0.20 at $S/d$ = 30",
                xy=(30.0, 0.114), xytext=(-16, 34),
                textcoords="offset points", fontsize=7.5, ha="right",
                color="#c00000",
                bbox=dict(boxstyle="round,pad=0.25", fc="white",
                          ec="#c00000", alpha=0.9),
                arrowprops=dict(arrowstyle="->", color="#c00000"))
    ax.set_xlabel("Standoff distance  S  (cm)")
    ax.set_ylabel("Thickness  (cm, log scale)")
    ax.set_title("P9: Whipple shield sizing, 1 cm / 1.6 g/cm$^3$ meteoroid "
                 "at 80 km/s, Al 7075-T6")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9)
    fig.subplots_adjust(bottom=0.16)
    _caption(fig, "Figure 3: Bumper and rear-wall thickness vs standoff "
             "(Pisacane Eqs. 11.27-11.31); the wall thins as $S^{-3/4}$.")
    fig.savefig(FIG_DIR / "fig3_whipple_thickness.png", dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------
def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    FIG_DIR.mkdir(exist_ok=True)
    p2_results()
    print()
    p3_results()
    print()
    p5_results()
    print()
    p9_results()

    fig1_ke_vs_diameter()
    fig2_flux_vs_mass()
    fig3_whipple_thickness()
    print("\nFigures written to:", FIG_DIR)


if __name__ == "__main__":
    main()
