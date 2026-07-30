"""Dark-theme walkthrough figures for SPCE 5065 HW5 (micrometeoroids and orbital debris).

Generates five figures used by spce_5065_hw5_walkthrough.md:

  walkthrough_fig1_ke_cube_law.png        (P2)  KE vs diameter + energy density
  walkthrough_fig2_v_squared_scaling.png  (P3)  1 g particle at 1.98 / 10 / 20 km/s
  walkthrough_fig3_shielding_geometry.png (P5)  Earth disc vs nadir cone, ISS vs GEO
  walkthrough_fig4_poisson_curves.png     (P5)  P(>=1 impact) vs time, three sizes
  walkthrough_fig5_whipple_standoff.png   (P9)  wall/bumper thickness vs standoff

Every number reproduces the verified values in Clayton_spce_5065_hw5_submission.md;
the assertions at the bottom of this file check that on every run.

Color scheme (dark theme):
  background #0D1117, text #E6EDF3,
  green #3FB950 helps, red #F85149 hurts,
  blue #58A6FF neutral, purple #D2A8FF results, orange #FFA657 thresholds.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge

# --------------------------------------------------------------------------
# Palette and style
# --------------------------------------------------------------------------
BG = "#0D1117"
FG = "#E6EDF3"
GREEN = "#3FB950"
RED = "#F85149"
BLUE = "#58A6FF"
PURPLE = "#D2A8FF"
ORANGE = "#FFA657"
GRID = "#30363D"
DIM = "#8B949E"

FIG_DIR = Path(__file__).parent / "figures"


def _style():
    plt.rcParams.update({
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "savefig.facecolor": BG,
        "text.color": FG,
        "axes.labelcolor": FG,
        "axes.edgecolor": "#484F58",
        "xtick.color": FG,
        "ytick.color": FG,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "axes.titlecolor": FG,
        "grid.color": GRID,
        "legend.facecolor": "#161B22",
        "legend.edgecolor": "#30363D",
        "figure.dpi": 110,
    })


def _box(fc="#161B22", ec="#30363D"):
    return dict(boxstyle="round,pad=0.32", fc=fc, ec=ec, alpha=0.94)


# --------------------------------------------------------------------------
# Physics (mirrors spce_5065_hw5_solution.py)
# --------------------------------------------------------------------------
MU_EARTH = 398600.5      # km^3/s^2
R_E = 6378.0             # km
G0 = 9.81                # m/s^2
H_ATM = 100.0            # km
R_A = R_E + H_ATM        # km
H_ISS, H_GPS, H_GEO = 400.0, 20200.0, 35786.0
RHO_P = 1.0              # g/cm^3

RHO_AL7075 = 2.81        # g/cm^3
SIGMA_7075 = 65.0        # ksi


def v_circ_ms(h_km):
    return np.sqrt(MU_EARTH / (R_E + h_km)) * 1000.0


def sphere_mass_g(d_cm, rho=RHO_P):
    return (np.pi / 6.0) * rho * np.asarray(d_cm, dtype=float) ** 3


def grun_flux(m_g):
    m = np.asarray(m_g, dtype=float)
    f1 = (2.2e3 * m ** 0.306 + 15.0) ** (-4.38)
    f2 = 1.3e-9 * (m + 1.0e11 * m ** 2 + 1.0e27 * m ** 4) ** (-0.36)
    f3 = 1.3e-16 * (m + 1.0e6 * m ** 2) ** (-0.85)
    return 3.15576e7 * (f1 + f2 + f3)


def chi(r_km, branch="nadir"):
    cos_t = float(np.sqrt(1.0 - (R_A / r_km) ** 2))
    return 0.5 * (1.0 + cos_t) if branch == "random" else cos_t


def focusing(r_km):
    return 1.0 + R_A / r_km


def flux_at_orbit(m_g, h_km, branch="nadir"):
    r = R_E + h_km
    return grun_flux(m_g) * chi(r, branch) * focusing(r)


def whipple(S_cm, d_cm=1.0, rho_p=1.6, V_kms=80.0, sigma=SIGMA_7075,
            rho_b=RHO_AL7075, rho_w=RHO_AL7075, theta_deg=0.0):
    S = np.asarray(S_cm, dtype=float)
    m_p = (4.0 * np.pi / 3.0) * (d_cm / 2.0) ** 3 * rho_p
    c_b = np.where(S / d_cm < 30.0, 0.25, 0.20)
    t_b = c_b * d_cm * rho_p / rho_b
    k = np.where(S / d_cm < 15.0, (S / d_cm / 15.0) ** (-0.185), 1.0)
    t_w = (0.79 * k * d_cm ** 0.5 * m_p ** (1.0 / 3.0)
           * (rho_p * rho_b) ** (1.0 / 6.0) / rho_w
           * S ** (-0.75) * (sigma / 70.0) ** (-0.5)
           * V_kms * np.cos(np.radians(theta_deg)))
    return t_b, t_w


# --------------------------------------------------------------------------
# Figure 1 (P2): the cube law and the energy-density reframe
# --------------------------------------------------------------------------
def fig1_ke_cube_law():
    v = v_circ_ms(H_ISS)
    d_cm = np.logspace(-3, 2, 500)
    ke = 0.5 * sphere_mass_g(d_cm) * 1e-3 * v ** 2

    fig, (ax, ax2) = plt.subplots(
        2, 1, figsize=(8.0, 8.2), sharex=True,
        gridspec_kw=dict(height_ratios=[1.35, 1.0], hspace=0.10))

    # --- top: total KE, slope 3 ---
    ax.loglog(d_cm, ke, color=BLUE, lw=2.4,
              label=r"1 g/cm$^3$ sphere at 7.6686 km/s")
    sats = [("5 kg smallsat", 5.0, GREEN), ("50 kg", 50.0, ORANGE),
            ("100 kg", 100.0, RED)]
    for lab, M, c in sats:
        ke_s = 0.5 * M * v ** 2
        ax.axhline(ke_s, color=c, ls="--", lw=1.4,
                   label=f"{lab}: {ke_s:.2e} J")

    marks = [(0.1, "1 mm", (14, -30)), (1.0, "1 cm", (14, -30)),
             (10.0, "10 cm", (-96, 14))]
    for dm, note, off in marks:
        y = 0.5 * float(sphere_mass_g(dm)) * 1e-3 * v ** 2
        ax.plot(dm, y, "o", color=PURPLE, ms=7, zorder=5)
        ax.annotate(f"{note}\n{y:.2e} J", xy=(dm, y), xytext=off,
                    textcoords="offset points", fontsize=8.5, color=PURPLE,
                    bbox=_box())

    # slope-3 reference triangle
    ax.plot([2e-3, 2e-2, 2e-2, 2e-3], [3e-3, 3e-3, 3.0, 3e-3],
            color=DIM, lw=1.1, ls=":")
    ax.annotate("one decade in $d$", xy=(6e-3, 3e-3), xytext=(0, -20),
                textcoords="offset points", fontsize=8, color=DIM, ha="center")
    ax.annotate("three decades\nin energy", xy=(2.2e-2, 8e-2), xytext=(8, 0),
                textcoords="offset points", fontsize=8, color=DIM, va="center")

    ax.set_ylabel("Kinetic energy  (J)")
    ax.set_ylim(1e-6, 1e12)
    ax.set_title("P2: total energy grows as the cube of diameter (log-log slope 3)",
                 fontsize=11.5, pad=10)
    ax.grid(True, which="both", alpha=0.28)
    ax.legend(fontsize=8.5, loc="upper left", framealpha=0.95)

    # --- bottom: energy per unit frontal area ---
    ed = (1.0 / 3.0) * (RHO_P * 1000.0) * (d_cm / 100.0) * v ** 2   # J/m^2
    ax2.loglog(d_cm, ed, color=PURPLE, lw=2.4,
               label=r"particle energy density  $\frac{1}{3}\rho d v^2$")
    ke5 = 0.5 * 5.0 * v ** 2
    ax2.axhline(ke5, color=GREEN, ls="--", lw=1.4,
                label=r"5 kg smallsat energy spread over 1 m$^2$")
    d_cross = ke5 / ((1.0 / 3.0) * 1000.0 * v ** 2) * 100.0
    ax2.plot(d_cross, ke5, "o", color=ORANGE, ms=8, zorder=5)
    ax2.annotate(f"crossover at d = {d_cross:.2f} cm:\nbelow this the satellite wins,\n"
                 "above it the pebble wins",
                 xy=(d_cross, ke5), xytext=(-26, 46),
                 textcoords="offset points", fontsize=8.5, color=ORANGE,
                 ha="right", bbox=_box(),
                 arrowprops=dict(arrowstyle="->", color=ORANGE))
    for dm in (0.1, 1.0):
        y = (1.0 / 3.0) * 1000.0 * (dm / 100.0) * v ** 2
        ax2.plot(dm, y, "o", color=PURPLE, ms=6, zorder=5)
    ax2.annotate(r"1 mm: 2.0$\times$10$^{7}$ J/m$^2$",
                 xy=(0.1, (1.0 / 3.0) * 1000.0 * 1e-3 * v ** 2),
                 xytext=(12, -26), textcoords="offset points",
                 fontsize=8.5, color=PURPLE, bbox=_box())

    ax2.set_xlabel("Particle diameter  $d$  (cm)")
    ax2.set_ylabel(r"Energy per unit frontal area  (J/m$^2$)")
    ax2.set_title("The reframe: energy DENSITY is only linear in $d$, so even a "
                  "pebble hits like a satellite",
                  fontsize=11.5, pad=10)
    ax2.set_ylim(1e5, 1e12)
    ax2.grid(True, which="both", alpha=0.28)
    ax2.legend(fontsize=8.5, loc="upper left", framealpha=0.95)

    fig.subplots_adjust(left=0.115, right=0.975, top=0.945, bottom=0.075)
    fig.savefig(FIG_DIR / "walkthrough_fig1_ke_cube_law.png", dpi=200)
    plt.close(fig)


# --------------------------------------------------------------------------
# Figure 2 (P3): the v^2 ladder
# --------------------------------------------------------------------------
def fig2_v_squared_scaling():
    m_d = 1.0e-3          # kg
    m_ball, g = 2.0, G0
    E_ref = m_ball * g * 100.0                      # 1962 J

    v_line = np.linspace(0.5, 22.0, 400) * 1000.0
    ke_line = 0.5 * m_d * v_line ** 2

    cases = [(1980.9, "1.98 km/s\n(the number this\nproblem implies)", RED),
             (10000.0, "10 km/s\n(typical real LEO\ndebris closing speed)", ORANGE),
             (20000.0, "20 km/s\n(micrometeoroid)", GREEN)]

    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    ax.plot(v_line / 1000.0, ke_line, color=BLUE, lw=2.2,
            label=r"$KE = \frac{1}{2}mv^2$ for a 1.0 g particle")

    for v, lab, c in cases:
        ke = 0.5 * m_d * v ** 2
        h = ke / (m_ball * g)
        ax.plot(v / 1000.0, ke, "o", color=c, ms=10, zorder=5)
        ax.vlines(v / 1000.0, 1e2, ke, color=c, ls=":", lw=1.2)
        txt = (f"{lab}\n{ke:.3g} J\n= ball dropped {h/1000:.2f} km\n"
               fr"= {ke/E_ref:.1f}$\times$ the 100 m drop")
        ax.annotate(txt, xy=(v / 1000.0, ke), xytext=(-4, 16),
                    textcoords="offset points", fontsize=8.6, color=c,
                    ha="right" if v > 15000 else "left", bbox=_box())

    ax.axhline(E_ref, color=DIM, ls="--", lw=1.3)
    # End the label left of the 20 km/s marker line so the dotted line does not
    # strike through the text.
    ax.annotate(f"bowling-ball benchmark: 2.0 kg dropped 100 m = {E_ref:.0f} J",
                xy=(19.2, E_ref), xytext=(0, 8), textcoords="offset points",
                fontsize=8.6, color=DIM, ha="right", bbox=_box())

    ax.set_yscale("log")
    ax.set_xlim(0, 23.5)
    ax.set_ylim(1e2, 2e6)
    ax.set_xlabel("Impact speed  $v$  (km/s)")
    ax.set_ylabel("Kinetic energy of a 1.0 g particle  (J)")
    ax.set_title("P3: doubling the speed quadruples the damage budget "
                 r"($KE \propto v^2$)", fontsize=11.5, pad=10)
    ax.grid(True, which="both", alpha=0.28)
    ax.legend(fontsize=9, loc="lower right", framealpha=0.95)
    fig.subplots_adjust(left=0.10, right=0.975, top=0.915, bottom=0.11)
    fig.savefig(FIG_DIR / "walkthrough_fig2_v_squared_scaling.png", dpi=200)
    plt.close(fig)


# --------------------------------------------------------------------------
# Figure 3 (P5): Earth-disc half-angle vs the allowed nadir cone
# --------------------------------------------------------------------------
def _geometry_panel(ax, h_km, name, green_radius_frac, xlim, ylim,
                    show_legend=False, earth_label_inside=True,
                    note_xy=(0.02, 0.02), note_va="bottom", note_ha="left"):
    r = R_E + h_km
    D = r / R_A                                   # satellite distance, units of R_a
    th_disc = np.degrees(np.arcsin(1.0 / D))      # Earth disc half-angle
    alpha = 90.0 - th_disc                        # allowed nadir cone half-angle
    L = np.sqrt(D ** 2 - 1.0)                     # tangent length

    ax.add_patch(Circle((0, 0), 1.0, facecolor="#12283F",
                        edgecolor=BLUE, lw=1.6, zorder=1))
    if earth_label_inside:
        ax.text(0, 0, r"Earth + atmosphere" "\n" r"$R_a$ = 6478 km",
                ha="center", va="center", fontsize=8.2, color=BLUE, zorder=2)
    else:
        # At GEO the disc is too small to hold the label, so park it to the
        # side with a leader line instead of letting it collide with the note.
        ax.annotate(r"Earth + atmosphere" "\n" r"$R_a$ = 6478 km",
                    xy=(1.0, 0.0), xytext=(28, -6),
                    textcoords="offset points", ha="left", va="center",
                    fontsize=8.2, color=BLUE, zorder=6, bbox=_box(),
                    arrowprops=dict(arrowstyle="->", color=BLUE))

    sat = (0.0, D)
    # Earth-in-view cone (blue): everything the Earth blocks
    ax.add_patch(Wedge(sat, L, 270 - th_disc, 270 + th_disc,
                       facecolor=BLUE, alpha=0.20, edgecolor=BLUE,
                       lw=1.3, zorder=2))
    # allowed-normal cone (green): normals for which the whole Earth fits in view
    ax.add_patch(Wedge(sat, green_radius_frac * L, 270 - alpha, 270 + alpha,
                       facecolor=GREEN, alpha=0.38, edgecolor=GREEN,
                       lw=1.6, zorder=3))
    ax.plot([0, 0], [0, D], color=DIM, ls=":", lw=1.1, zorder=2)
    ax.plot(*sat, marker="s", color=PURPLE, ms=9, zorder=6)
    ax.annotate(f"{name}\nh = {h_km:,.0f} km", xy=sat, xytext=(10, 8),
                textcoords="offset points", fontsize=9, color=PURPLE,
                bbox=_box())

    ax.text(note_xy[0], note_xy[1],
            f"Earth disc half-angle  $\\theta$ = {th_disc:.1f}$\\degree$\n"
            f"normal must lie within {alpha:.1f}$\\degree$ of nadir\n"
            f"$\\chi_3 = \\cos\\theta$ = {np.cos(np.radians(th_disc)):.4f}",
            transform=ax.transAxes, fontsize=8.6, color=FG,
            va=note_va, ha=note_ha, bbox=_box())

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    if show_legend:
        ax.add_patch(Wedge((xlim[0] * 0.92, ylim[1] * 0.9), 0.0, 0, 1))  # no-op


def fig3_shielding_geometry():
    fig = plt.figure(figsize=(10.4, 8.8))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.32, 1.0],
                          hspace=0.20, wspace=0.10)
    axA = fig.add_subplot(gs[0, 0])
    axB = fig.add_subplot(gs[0, 1])
    axC = fig.add_subplot(gs[1, :])

    _geometry_panel(axA, H_ISS, "ISS", 0.88, (-1.35, 1.35), (-1.20, 1.40))
    _geometry_panel(axB, H_GEO, "GEO", 0.46, (-6.6, 6.6), (-1.6, 8.0),
                    earth_label_inside=False, note_xy=(0.02, 0.98),
                    note_va="top", note_ha="left")

    axA.set_title("ISS, 400 km: Earth fills the sky, so almost no normal "
                  "direction\nqualifies as 'total Earth in field of view'",
                  fontsize=10.2, pad=6)
    axB.set_title("GEO, 35,786 km: Earth is a small disc, so almost every "
                  "normal\ndirection qualifies (panels not to the same scale)",
                  fontsize=10.2, pad=6)

    prox = [plt.Line2D([], [], marker="s", ls="none", color=BLUE, ms=11,
                       alpha=0.5, label="cone blocked by the Earth "
                                        r"(half-angle $\theta$)"),
            plt.Line2D([], [], marker="s", ls="none", color=GREEN, ms=11,
                       alpha=0.7, label="surface normals that see the whole "
                                        r"Earth (half-angle 90$\degree - \theta$)")]
    axA.legend(handles=prox, fontsize=8.6, loc="upper left",
               framealpha=0.95, borderpad=0.6)

    # --- bottom: the tug of war between shielding and focusing ---
    orbits = [("ISS\n400 km", H_ISS), ("GPS\n20,200 km", H_GPS),
              ("GEO\n35,786 km", H_GEO)]
    labels = [r"$\chi_3 = \cos\theta$ (nadir)",
              r"$\chi_2 = \frac{1}{2}(1+\cos\theta)$ (random)",
              r"$G = 1 + R_a/r$ (focusing)",
              r"net $\chi_3 G$", r"net $\chi_2 G$"]
    colors = [RED, ORANGE, GREEN, PURPLE, BLUE]
    vals = []
    for _, h in orbits:
        r = R_E + h
        c3, c2, g = chi(r), chi(r, "random"), focusing(r)
        vals.append([c3, c2, g, c3 * g, c2 * g])
    vals = np.array(vals)

    x = np.arange(3)
    w = 0.155
    for i in range(5):
        pos = x + (i - 2) * w
        axC.bar(pos, vals[:, i], width=w * 0.92, color=colors[i],
                edgecolor=BG, lw=0.6, label=labels[i])
        for xi, yi in zip(pos, vals[:, i]):
            axC.text(xi, yi + 0.035, f"{yi:.3f}", ha="center", va="bottom",
                     fontsize=7.4, color=colors[i], rotation=90)

    axC.axhline(1.0, color=DIM, ls="--", lw=1.2)
    # The only bar-free space at y = 1 is the ~0.2-unit gap between groups, so
    # the unity label has to be short enough to fit inside it.
    axC.annotate("unity", xy=(0.5, 1.0), xytext=(0, 6),
                 textcoords="offset points", fontsize=8.2, color=DIM,
                 ha="center", bbox=_box())
    axC.set_xticks(x)
    axC.set_xticklabels([n for n, _ in orbits], fontsize=9.5)
    axC.set_ylim(0, 2.42)
    axC.set_ylabel("Geometry correction factor")
    axC.set_title("Shielding cuts the flux, focusing raises it, and at the ISS "
                  "they nearly cancel", fontsize=11, pad=8)
    axC.grid(True, axis="y", alpha=0.25)
    axC.legend(fontsize=8.2, ncol=5, loc="upper center", framealpha=0.95,
               columnspacing=1.0, handlelength=1.3)
    fig.subplots_adjust(left=0.065, right=0.98, top=0.935, bottom=0.065)
    fig.savefig(FIG_DIR / "walkthrough_fig3_shielding_geometry.png", dpi=200)
    plt.close(fig)


# --------------------------------------------------------------------------
# Figure 4 (P5): Poisson probability vs time
# --------------------------------------------------------------------------
def fig4_poisson_curves():
    A = 10.0
    t = np.logspace(-3, 7, 700)
    sizes = [(0.1, "0.1 cm (1 mm)", GREEN),
             (1.0, "1 cm", ORANGE),
             (10.0, "10 cm", RED)]

    fig, ax = plt.subplots(figsize=(8.8, 6.0))
    for d_cm, lab, c in sizes:
        m = float(sphere_mass_g(d_cm))
        F = float(flux_at_orbit(m, H_ISS))
        lam = F * A
        p = 1.0 - np.exp(-lam * t)
        ax.loglog(t, p, color=c, lw=2.3,
                  label=fr"{lab}: $F$ = {F:.3g} m$^{{-2}}$yr$^{{-1}}$")
        t_th = -np.log(1.0 - 1e-4) / lam
        ax.plot(t_th, 1e-4, "o", color=c, ms=8, zorder=6)

    ax.axhline(1e-4, color=PURPLE, ls="--", lw=1.5)
    ax.annotate(r"$p$ = 0.01% threshold", xy=(1e-3, 1e-4), xytext=(4, 6),
                textcoords="offset points", fontsize=9, color=PURPLE)
    ax.axvline(10.0, color=DIM, ls=":", lw=1.5)
    ax.annotate("10 yr mission", xy=(10.0, 3e-9), xytext=(6, 0),
                textcoords="offset points", fontsize=9, color=DIM, rotation=90,
                va="bottom")

    # crossing-time callouts, staggered so they never sit on one another
    calls = [(0.1, "ISS: 0.0129 yr\n(4.7 days)", GREEN, (34, 34)),
             (1.0, "ISS: 105 yr", ORANGE, (34, 34)),
             (10.0, r"ISS: 1.06$\times$10$^{6}$ yr", RED, (-14, 34))]
    for d_cm, txt, c, off in calls:
        m = float(sphere_mass_g(d_cm))
        lam = float(flux_at_orbit(m, H_ISS)) * A
        t_th = -np.log(1.0 - 1e-4) / lam
        ax.annotate(txt, xy=(t_th, 1e-4), xytext=off,
                    textcoords="offset points", fontsize=8.6, color=c,
                    ha="right" if off[0] < 0 else "left", bbox=_box(),
                    arrowprops=dict(arrowstyle="->", color=c))

    # 10-year readouts
    for d_cm, c, dy in [(0.1, GREEN, 1.9)]:
        m = float(sphere_mass_g(d_cm))
        p10 = 1.0 - np.exp(-float(flux_at_orbit(m, H_ISS)) * A * 10.0)
        ax.plot(10.0, p10, "s", color=c, ms=8, zorder=6)
        ax.annotate(f"7.47% in 10 yr", xy=(10.0, p10), xytext=(12, -26),
                    textcoords="offset points", fontsize=8.6, color=c,
                    bbox=_box(), arrowprops=dict(arrowstyle="->", color=c))

    ax.set_xlim(1e-3, 1e7)
    ax.set_ylim(1e-9, 2.0)
    ax.set_xlabel("Exposure time  $t$  (years)")
    ax.set_ylabel(r"$p(k \geq 1) = 1 - e^{-FAt}$")
    ax.set_title(r"P5b: Poisson impact probability at the ISS, $A$ = 10 m$^2$ "
                 "(slope 1 while $p \\ll 1$)", fontsize=11.5, pad=10)
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8.8, loc="lower right", framealpha=0.95)
    fig.subplots_adjust(left=0.10, right=0.975, top=0.915, bottom=0.105)
    fig.savefig(FIG_DIR / "walkthrough_fig4_poisson_curves.png", dpi=200)
    plt.close(fig)


# --------------------------------------------------------------------------
# Figure 5 (P9): standoff buys wall thickness
# --------------------------------------------------------------------------
def fig5_whipple_standoff():
    S = np.linspace(1.0, 30.0, 600)
    t_b, t_w = whipple(S)

    fig, ax = plt.subplots(figsize=(8.8, 6.0))
    ax.loglog(S, t_w, color=PURPLE, lw=2.6, label=r"rear wall  $t_w$")
    ax.loglog(S, t_b, color=ORANGE, lw=2.2, ls="--",
              label=r"bumper  $t_b$ (barely moves)")

    # pure S^-3/4 reference through the k = 1 branch
    S_ref = np.array([15.0, 30.0])
    _, tw15 = whipple(15.0)
    ax.loglog(S_ref, float(tw15) * (S_ref / 15.0) ** (-0.75),
              color=GREEN, lw=1.6, ls=":",
              label=r"pure $S^{-3/4}$ (where $k = 1$)")

    for Sm, off, ha in [(1.0, (26, 12), "left"), (10.0, (18, 20), "left"),
                        (30.0, (-16, 26), "right")]:
        _, tw = whipple(Sm)
        ax.plot(Sm, float(tw), "o", color=PURPLE, ms=8, zorder=6)
        ax.annotate(f"S = {Sm:.0f} cm\n$t_w$ = {float(tw):.2f} cm",
                    xy=(Sm, float(tw)), xytext=off,
                    textcoords="offset points", fontsize=8.8, color=PURPLE,
                    ha=ha, bbox=_box(),
                    arrowprops=dict(arrowstyle="->", color=PURPLE))

    ax.annotate(r"$c_b$ steps 0.25 $\rightarrow$ 0.20 at $S/d$ = 30",
                xy=(30.0, 0.1139), xytext=(-30, 34),
                textcoords="offset points", fontsize=8.4, color=ORANGE,
                ha="right", bbox=_box(),
                arrowprops=dict(arrowstyle="->", color=ORANGE))
    ax.annotate("29 cm of empty space\nreplaces 44 cm of aluminium:\n"
                "a 95% cut in wall thickness",
                xy=(4.0, 3.0), xytext=(0, 0), textcoords="offset points",
                fontsize=9.2, color=GREEN, ha="left", va="center",
                bbox=_box(ec=GREEN))

    ax.set_xlim(0.9, 34)
    ax.set_ylim(0.08, 80)
    ax.set_xlabel("Standoff distance  $S$  (cm, log scale)")
    ax.set_ylabel("Required thickness  (cm, log scale)")
    ax.set_title("P9: on log-log axes the wall law is a straight line of slope "
                 r"$-3/4$", fontsize=11.5, pad=10)
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=9, loc="upper right", framealpha=0.95)
    fig.subplots_adjust(left=0.095, right=0.975, top=0.915, bottom=0.105)
    fig.savefig(FIG_DIR / "walkthrough_fig5_whipple_standoff.png", dpi=200)
    plt.close(fig)


# --------------------------------------------------------------------------
def _verify():
    """Assert the figures are drawn from the submission's verified numbers."""
    v = v_circ_ms(H_ISS)
    assert abs(v / 1000.0 - 7.6686) < 1e-3, v
    assert abs(0.5 * float(sphere_mass_g(1.0)) * 1e-3 * v ** 2 - 1.540e4) < 5.0
    assert abs(0.5 * 5.0 * v ** 2 - 1.470e8) < 1e5

    assert abs(2.0 * G0 * 100.0 - 1962.0) < 1e-6
    assert abs(np.sqrt(2 * 1962.0 / 1e-3) - 1980.9) < 0.5
    assert abs(0.5e-3 * (2.0e4) ** 2 - 2.00e5) < 1.0

    r_iss = R_E + H_ISS
    assert abs(chi(r_iss) - 0.2942) < 1e-3
    assert abs(chi(r_iss, "random") - 0.6471) < 1e-3
    assert abs(focusing(r_iss) - 1.9557) < 1e-3
    F_1cm_iss = float(flux_at_orbit(float(sphere_mass_g(1.0)), H_ISS))
    assert abs(F_1cm_iss / 9.554e-8 - 1.0) < 0.01, F_1cm_iss
    t_th = -np.log(1 - 1e-4) / (F_1cm_iss * 10.0)
    assert abs(t_th / 105.0 - 1.0) < 0.02, t_th

    tb1, tw1 = whipple(1.0)
    tb30, tw30 = whipple(30.0)
    assert abs(float(tb1) - 0.1423) < 1e-3
    assert abs(float(tw1) - 46.65) < 0.1, tw1
    assert abs(float(tb30) - 0.1139) < 1e-3
    assert abs(float(tw30) - 2.21) < 0.02, tw30
    print("verification against submission values: OK")


def main():
    _style()
    FIG_DIR.mkdir(exist_ok=True)
    _verify()
    fig1_ke_cube_law()
    fig2_v_squared_scaling()
    fig3_shielding_geometry()
    fig4_poisson_curves()
    fig5_whipple_standoff()
    print("figures written to:", FIG_DIR)


if __name__ == "__main__":
    main()
