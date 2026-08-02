"""SPCE 5065 Design Project MS2 -- subsystem design analysis and figures.

MESA (Mission Extension and Servicing Asset), a GEO servicing tug. This script
computes every number quoted in the Milestone 2 report and writes the new
figures to ./figures/ next to this script.

Outputs:

  fig4_mesa_configuration.png  Sized configuration: bus, arrays, radiators, the
                               cp-to-cm offset (Section 8, vehicle definition).
  fig5_thermal_balance.png     Equilibrium temperature vs radiator area for the
                               sun and eclipse cases (Section 8, TCS).
  fig6_disturbance_torques.png The four external disturbance torques vs altitude
                               for the MESA geometry, GEO marked (Section 11).
  fig7_power_profile.png       Array power over one day at equinox, BOL vs EOL,
                               with the eclipse dropout (Section 12, simulation).
  fig8_momentum.png            Secular momentum accumulation and wheel dump
                               cadence (Section 11 / 12).

Sources for the models:
  Gravity gradient, SRP, magnetic, aerodynamic torques  SMAD Ch. 11, Table 11.10
  Wheel sizing (H = 0.707 T_D [P/4], M = 4 I theta / t^2) SMAD Ch. 11, Table 11.7
  Wheel mass/power lookup                                Lesson 7 Part 2 slide 11
  Equilibrium temperature energy balance                 Pisacane Ch. 12
  RHA categories (krad(Si) limits)                       Pisacane Table 9.9

Run: python3 spce5065_ms2_figs.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

FIG_DIR = Path(__file__).parent / "figures"

# ---------------------------------------------------------------------------
# Physical constants (SI)
# ---------------------------------------------------------------------------
MU = 3.986004418e14        # m^3/s^2    Earth gravitational parameter
R_E_M = 6378.137e3         # m          Earth equatorial radius
SIGMA = 5.670374419e-8     # W/m^2/K^4  Stefan-Boltzmann
C_LIGHT = 2.99792458e8     # m/s
S_SOLAR = 1361.0           # W/m^2      solar constant at 1 AU (MS1 Section 2.1)
M_EARTH_MAG = 7.96e15      # tesla*m^3  Earth magnetic moment (SMAD Table 11.10)
Q_EARTH_IR = 237.0         # W/m^2      Earth IR emission at the surface
ALBEDO = 0.30              # -          Earth Bond albedo

H_GEO = 35786.0e3          # m          GEO altitude
R_GEO = R_E_M + H_GEO      # m          GEO radius, 42,164 km
T_GEO = 86164.0            # s          sidereal day (GEO period)

# ---------------------------------------------------------------------------
# MESA vehicle definition (Section 8). Mass from MS1; geometry sized here.
# ---------------------------------------------------------------------------
M_WET = 2000.0             # kg   wet mass (MS1)
M_PROP = 600.0             # kg   propellant
M_ARRAY_EACH = 60.0        # kg   per solar wing
N_WINGS = 2

BUS_X, BUS_Y, BUS_Z = 1.8, 1.8, 3.5        # m, z is the docking / nadir axis
WING_X, WING_Y = 1.6, 3.2                  # m, each wing (chord x span)
A_WING = WING_X * WING_Y                   # m^2 per wing
A_ARRAY = N_WINGS * A_WING                 # m^2 total array

M_ARRAYS = N_WINGS * M_ARRAY_EACH
M_BUS = M_WET - M_ARRAYS

CP_CM_OFFSET = 0.25        # m    center of pressure to center of mass
D_DIPOLE = 5.0             # A*m^2 residual magnetic dipole
Q_REFLECT = 0.6            # -    reflectance factor (SMAD rough-estimate value)
CD = 2.2                   # -    drag coefficient (MS1)
RHO_GEO = 1.0e-15          # kg/m^3 neutral density at GEO (MS1 Section 7)

# Optical properties
ALPHA_MLI, EPS_MLI = 0.14, 0.03    # Ag/FEP outer layer; effective blanket emittance
ALPHA_OSR, EPS_OSR = 0.14, 0.78    # optical solar reflector radiator
Q_INT = 1200.0             # W    orbit-average internal dissipation
T_SUN_TARGET = 310.0       # K    radiator sizing target in the sun case

# Power
ETA_CELL = 0.30            # -    triple-junction GaAs BOL efficiency
PACK_FACTOR = 0.90         # -    cell packing factor
TEMP_DERATE = 0.90         # -    hot-cell derate at operating temperature
DEGRADE_PER_YR = 0.025     # -    GEO array degradation per year
MISSION_YR = 5.0

# Client satellite for the mated (docked) case
M_CLIENT = 3000.0
CLIENT_X, CLIENT_Y, CLIENT_Z = 2.0, 2.0, 3.0
DOCK_STANDOFF = 3.0        # m  client cm measured from MESA cm along +z


# ---------------------------------------------------------------------------
# Mass properties
# ---------------------------------------------------------------------------
def box_inertia(m, lx, ly, lz):
    """Principal moments of a uniform rectangular box about its own centroid."""
    return (m / 12.0 * (ly**2 + lz**2),
            m / 12.0 * (lx**2 + lz**2),
            m / 12.0 * (lx**2 + ly**2))


def mesa_inertia():
    """Free-flyer principal moments (Ix, Iy, Iz) about the MESA cm, kg*m^2.

    Wings are flat plates deployed along +/- y, so each carries a parallel-axis
    term about x and z but none about its own span axis y.
    """
    ibx, iby, ibz = box_inertia(M_BUS, BUS_X, BUS_Y, BUS_Z)

    m_w = M_ARRAY_EACH
    iwx = m_w / 12.0 * WING_Y**2          # about x: span dimension
    iwy = m_w / 12.0 * WING_X**2          # about y: chord dimension
    iwz = m_w / 12.0 * (WING_X**2 + WING_Y**2)
    d = BUS_Y / 2.0 + WING_Y / 2.0        # wing centroid offset along y
    md2 = m_w * d**2

    ix = ibx + N_WINGS * (iwx + md2)
    iy = iby + N_WINGS * iwy
    iz = ibz + N_WINGS * (iwz + md2)
    return ix, iy, iz, d


def mated_inertia(ix_free):
    """Ix of the MESA + client stack about the combined cm, kg*m^2."""
    m_tot = M_WET + M_CLIENT
    z_cm = M_CLIENT * DOCK_STANDOFF / m_tot          # combined cm, from MESA cm
    icx, _, _ = box_inertia(M_CLIENT, CLIENT_X, CLIENT_Y, CLIENT_Z)
    ix_mesa = ix_free + M_WET * z_cm**2
    ix_client = icx + M_CLIENT * (DOCK_STANDOFF - z_cm)**2
    return ix_mesa + ix_client, z_cm, m_tot


# ---------------------------------------------------------------------------
# Disturbance torques (SMAD Table 11.10)
# ---------------------------------------------------------------------------
def torque_gravity_gradient(r, iz, iy, theta_deg=10.0):
    """Tg = 3*mu*|Iz - Iy|*sin(2*theta) / (2*R^3)."""
    return 3.0 * MU * abs(iz - iy) * np.sin(2.0 * np.radians(theta_deg)) / (2.0 * r**3)


def torque_srp(area, offset=CP_CM_OFFSET, incidence_deg=0.0):
    """Tsp = F*(cps - cm), F = (1/c)*Fs*As*(1 + q)*cos(i)."""
    f = (S_SOLAR / C_LIGHT) * area * (1.0 + Q_REFLECT) * np.cos(np.radians(incidence_deg))
    return f * offset, f


def torque_magnetic(r, dipole=D_DIPOLE):
    """Tm = D*B, with B = M/R^3 at the equator (SMAD Table 11.10)."""
    b = M_EARTH_MAG / r**3
    return dipole * b, b


def torque_aero(r, area, offset=CP_CM_OFFSET, rho=RHO_GEO):
    """Ta = F*(cpa - cm), F = 0.5*rho*Cd*A*V^2."""
    v = np.sqrt(MU / r)
    f = 0.5 * rho * CD * area * v**2
    return f * offset, f, v


def torque_summary(r, ix, iy, iz, area_srp, rho=RHO_GEO):
    tg = torque_gravity_gradient(r, iz, iy)
    tsp, _ = torque_srp(area_srp)
    tm, b = torque_magnetic(r)
    ta, _, _ = torque_aero(r, area_srp, rho=rho)
    return {"gravity gradient": tg, "solar radiation": tsp,
            "magnetic": tm, "aerodynamic": ta,
            "total": tg + tsp + tm + ta, "B": b}


# ---------------------------------------------------------------------------
# Thermal (Pisacane Ch. 12 energy balance)
# ---------------------------------------------------------------------------
def bus_areas():
    """Total radiating area and the sun-projected area of the bus, m^2."""
    a_total = 2 * (BUS_X * BUS_Y) + 2 * (BUS_X * BUS_Z) + 2 * (BUS_Y * BUS_Z)
    a_proj = BUS_Y * BUS_Z          # sun normal to one large face, worst case
    a_nadir = BUS_X * BUS_Y         # face toward Earth
    return a_total, a_proj, a_nadir


def effective_emitting_area(a_rad):
    """eps*A summed over the MLI blanket and the OSR radiator, m^2."""
    a_total, _, _ = bus_areas()
    return EPS_MLI * (a_total - a_rad) + EPS_OSR * a_rad


def earth_fluxes():
    """Earth IR and albedo irradiance at GEO, W/m^2 (both tiny, shown for rigor)."""
    view = (R_E_M / R_GEO) ** 2
    return Q_EARTH_IR * view, ALBEDO * S_SOLAR * view


def equilibrium_temps(a_rad):
    """Isothermal-bus equilibrium temperature in sun and in eclipse, K."""
    _, a_proj, a_nadir = bus_areas()
    q_ir, q_alb = earth_fluxes()
    eps_a = effective_emitting_area(a_rad)

    q_sun = ALPHA_MLI * S_SOLAR * a_proj
    q_earth = a_nadir * (EPS_MLI * q_ir + ALPHA_MLI * q_alb)

    t_sun = ((q_sun + q_earth + Q_INT) / (SIGMA * eps_a)) ** 0.25
    t_ecl = ((Q_INT) / (SIGMA * eps_a)) ** 0.25
    return t_sun, t_ecl, q_sun, q_earth, eps_a


def size_radiator(t_target=T_SUN_TARGET):
    """Radiator area that holds the sun-case equilibrium temperature at t_target."""
    a_total, a_proj, a_nadir = bus_areas()
    q_ir, q_alb = earth_fluxes()
    q_in = ALPHA_MLI * S_SOLAR * a_proj + a_nadir * (EPS_MLI * q_ir + ALPHA_MLI * q_alb) + Q_INT
    eps_a_needed = q_in / (SIGMA * t_target**4)
    return (eps_a_needed - EPS_MLI * a_total) / (EPS_OSR - EPS_MLI)


def heater_power(a_rad, t_hold=273.15):
    """Make-up heater power to hold t_hold through eclipse, W."""
    return max(0.0, SIGMA * effective_emitting_area(a_rad) * t_hold**4 - Q_INT)


# ---------------------------------------------------------------------------
# Power and eclipse
# ---------------------------------------------------------------------------
def eclipse_duration():
    """Maximum GEO eclipse duration at equinox, from cylindrical shadow geometry."""
    half_angle = np.arcsin(R_E_M / R_GEO)
    return (2.0 * half_angle / (2.0 * np.pi)) * T_GEO


def array_power(bol=True, years=MISSION_YR):
    """Sun-tracking array output, W."""
    p = S_SOLAR * A_ARRAY * ETA_CELL * PACK_FACTOR * TEMP_DERATE
    return p if bol else p * (1.0 - DEGRADE_PER_YR) ** years


T_CELL_HOT = 333.0         # K   steady-state cell temperature in sunlight
T_CELL_COLD = 193.0        # K   cell temperature on eclipse exit
TAU_CELL = 300.0           # s   cell thermal time constant
K_TEMP = 6.0e-4            # 1/K power temperature coefficient (triple-junction)


def power_profile(n=4000, years=MISSION_YR):
    """One-day array power at equinox.

    Models three real effects on top of the flat sun-tracking baseline: the
    eclipse dropout, the cold-cell power spike on eclipse exit (cells leave
    shadow near 193 K and decay to 333 K), and a body-fixed array for contrast.
    """
    t = np.linspace(0.0, T_GEO, n)
    ecl = eclipse_duration()
    t_exit = T_GEO / 2.0 + ecl / 2.0
    in_eclipse = np.abs(t - T_GEO / 2.0) <= ecl / 2.0

    # Cell temperature: hot everywhere except the recovery after eclipse exit.
    dt = np.clip(t - t_exit, 0.0, None)
    t_cell = np.where(t > t_exit,
                      T_CELL_HOT + (T_CELL_COLD - T_CELL_HOT) * np.exp(-dt / TAU_CELL),
                      T_CELL_HOT)
    temp_gain = 1.0 + K_TEMP * (T_CELL_HOT - t_cell)

    p_bol = np.where(in_eclipse, 0.0, array_power(True) * temp_gain)
    p_eol = np.where(in_eclipse, 0.0, array_power(False, years) * temp_gain)

    # Body-fixed (non-tracking) array for the design comparison.
    sun_angle = 2.0 * np.pi * (t / T_GEO)          # zero at local noon
    p_fixed = np.where(in_eclipse, 0.0,
                       array_power(True) * np.clip(np.cos(sun_angle), 0.0, None))
    return t, p_bol, p_eol, p_fixed, in_eclipse, ecl


POWER_LOADS = [
    ("ADACS (wheels, sensors, electronics)", 283.0),
    ("Avionics and C&DH", 150.0),
    ("Communications (TT&C)", 120.0),
    ("RPO sensors (LIDAR, cameras)", 60.0),
    ("Thermal heaters (eclipse)", 260.0),
    ("Electric stationkeeping thruster", 600.0),
    ("Robotic arm and servicing payload", 300.0),
]


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
def fig_orbit_3d():
    """Regenerate Figure 2 with a true 3D orbit view (MS1 grader asked for one).

    Panel A is a 3D inertial rendering of the GEO orbit around a shaded Earth
    with the MESA and client positions; Panel B is the ground track.
    """
    R_E_KM = R_E_M / 1000.0
    a_km = R_GEO / 1000.0

    fig = plt.figure(figsize=(12.0, 5.6))
    axA = fig.add_subplot(1, 2, 1, projection="3d")

    # Earth as a shaded sphere
    u = np.linspace(0, 2 * np.pi, 90)
    v = np.linspace(0, np.pi, 45)
    xs = R_E_KM * np.outer(np.cos(u), np.sin(v))
    ys = R_E_KM * np.outer(np.sin(u), np.sin(v))
    zs = R_E_KM * np.outer(np.ones_like(u), np.cos(v))
    axA.plot_surface(xs, ys, zs, color="#2E5E8C", alpha=0.85, linewidth=0,
                     antialiased=True, shade=True, zorder=1)
    # Equator and spin axis for orientation
    th = np.linspace(0, 2 * np.pi, 200)
    axA.plot(R_E_KM * np.cos(th), R_E_KM * np.sin(th), 0, color="#9FC0DC",
             lw=0.8, alpha=0.9)
    axA.plot([0, 0], [0, 0], [-R_E_KM * 1.9, R_E_KM * 1.9], color="0.45",
             lw=1.0, ls=":")

    # GEO orbit, equatorial
    axA.plot(a_km * np.cos(th), a_km * np.sin(th), 0, color="#C0392B", lw=2.2,
             label="GEO orbit (35,786 km)")
    # Graveyard orbit, 300 km above
    ag = a_km + 300.0
    axA.plot(ag * np.cos(th), ag * np.sin(th), 0, color="#7F8C8D", lw=1.0,
             ls=(0, (2, 3)), label="graveyard (+300 km)")

    # Hourly satellite positions over one sidereal day
    uh = 2.0 * np.pi * np.arange(24) / 24.0
    axA.scatter(a_km * np.cos(uh), a_km * np.sin(uh), np.zeros_like(uh),
                color="#E67E22", s=16, depthshade=False, label="MESA, hourly")
    # MESA and a client separated in longitude
    axA.scatter([a_km], [0], [0], color="#C0392B", s=90, marker="s",
                depthshade=False, edgecolor="k", linewidth=0.5, zorder=10)
    cl = np.radians(38.0)
    axA.scatter([a_km * np.cos(cl)], [a_km * np.sin(cl)], [0], color="#F1C40F",
                s=70, marker="o", depthshade=False, edgecolor="k",
                linewidth=0.5, zorder=10)
    axA.text(a_km * 1.04, 0, -a_km * 0.20, "MESA", fontsize=8.5, color="#C0392B")
    axA.text(a_km * np.cos(cl) * 1.02, a_km * np.sin(cl), a_km * 0.20,
             "client", fontsize=8.5, color="#B7950B")
    axA.text2D(0.02, 0.02, "Earth shown to scale", transform=axA.transAxes,
               fontsize=7, color="0.4")

    lim = a_km * 1.05
    axA.set_xlim(-lim, lim)
    axA.set_ylim(-lim, lim)
    axA.set_zlim(-lim * 0.6, lim * 0.6)
    axA.set_box_aspect((1, 1, 0.6))
    axA.set_xlabel("ECI x (km)", fontsize=8, labelpad=-2)
    axA.set_ylabel("ECI y (km)", fontsize=8, labelpad=-2)
    axA.set_zlabel("ECI z (km)", fontsize=8, labelpad=-4)
    axA.tick_params(labelsize=6.5, pad=-1)
    axA.view_init(elev=24, azim=-58)
    axA.set_title("(A) 3D inertial view, one sidereal day", fontsize=10.5, pad=0)
    axA.legend(loc="upper left", fontsize=7, framealpha=0.9,
               bbox_to_anchor=(-0.06, 0.98))
    axA.grid(False)

    # Panel B, ground track
    axB = fig.add_subplot(1, 2, 2)
    slot_lon = -105.0
    ug = np.linspace(0, 2 * np.pi, 721)
    for inc_deg, color, label in ((5.0, "#E67E22", "~6 yr drift, no N-S SK"),
                                  (15.0, "#C0392B", "~26.5 yr drift, no N-S SK")):
        i = np.radians(inc_deg)
        alpha = np.arctan2(np.sin(ug) * np.cos(i), np.cos(ug))
        dlon = np.degrees(np.unwrap(alpha - ug))
        dlon = (dlon + 180) % 360 - 180
        lat = np.degrees(np.arcsin(np.sin(ug) * np.sin(i)))
        axB.plot(slot_lon + dlon, lat, color=color, lw=1.8, label=label)
    axB.plot(slot_lon, 0, "o", color="#27AE60", ms=9, zorder=6,
             label="station-kept (holds the point)")
    axB.annotate("assigned slot\n(105 W)", xy=(slot_lon, 0), xytext=(12, -20),
                 textcoords="offset points", fontsize=8)
    axB.set_xlabel("Longitude (deg)")
    axB.set_ylabel("Latitude (deg)")
    axB.set_title("(B) Ground track over one sidereal day", fontsize=10.5)
    axB.set_xlim(slot_lon - 6, slot_lon + 6)
    axB.set_ylim(-18, 18)
    axB.grid(True, alpha=0.3)
    axB.legend(loc="upper right", fontsize=7.5)

    fig.text(0.5, 0.015, "Figure 2: Three-dimensional simulation of the MESA orbit "
             "over one sidereal day. The vehicle holds one longitude, but without\n"
             "north-south stationkeeping the inclination grows and the ground track "
             "opens into an analemma.",
             ha="center", va="bottom", fontsize=8.5, style="italic")
    fig.subplots_adjust(bottom=0.19, wspace=0.16, left=0.02, right=0.97)
    fig.savefig(FIG_DIR / "fig2_orbit_propagation.png", dpi=150)
    plt.close(fig)


def fig_configuration(ix, iy, iz, a_rad):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.4, 5.0))

    # --- (A) deployed configuration, +y / +z plane ---
    ax1.set_aspect("equal")
    ax1.add_patch(mpatches.Rectangle((-BUS_Y / 2, -BUS_Z / 2), BUS_Y, BUS_Z,
                  fc="#D8DCE3", ec="0.3", lw=1.4))
    ax1.text(0, BUS_Z / 2 - 0.42, f"bus\n{BUS_X} x {BUS_Y} x {BUS_Z} m",
             ha="center", va="center", fontsize=8)
    for sgn in (1, -1):
        y0 = sgn * BUS_Y / 2
        ax1.add_patch(mpatches.Rectangle((min(y0, y0 + sgn * WING_Y), -WING_X / 2),
                      WING_Y, WING_X, fc="#2E5E8C", ec="0.25"))
        ax1.text(sgn * (BUS_Y / 2 + WING_Y / 2), 0, "solar\nwing", ha="center",
                 va="center", fontsize=7.5, color="white")
    # radiator on the anti-sun face
    ax1.add_patch(mpatches.Rectangle((-BUS_Y / 2, -BUS_Z / 2), BUS_Y, 0.32,
                  fc="#7FB3D5", ec="0.3", hatch="///"))
    ax1.plot(0, 0, "o", color="#C0392B", ms=7, zorder=6, label="cm")
    ax1.plot(0, CP_CM_OFFSET, "^", color="#E67E22", ms=8, zorder=6, label="cp")
    ax1.annotate(f"cp to cm offset\n{CP_CM_OFFSET:.2f} m", xy=(0.05, CP_CM_OFFSET),
                 xytext=(1.7, 1.75), fontsize=7.5,
                 bbox=dict(boxstyle="round,pad=0.28", fc="white", ec="0.6"),
                 arrowprops=dict(arrowstyle="->", color="0.5"))
    ax1.annotate(f"OSR radiator\n{a_rad:.1f} m$^2$", xy=(-0.4, -BUS_Z / 2 + 0.16),
                 xytext=(-4.3, -2.3), fontsize=7.5,
                 bbox=dict(boxstyle="round,pad=0.28", fc="white", ec="0.6"),
                 arrowprops=dict(arrowstyle="->", color="0.5"))
    ax1.legend(loc="upper left", fontsize=8, framealpha=0.9)
    ax1.set_xlim(-5.2, 5.2)
    ax1.set_ylim(-3.0, 2.6)
    ax1.set_xlabel("body y (m)")
    ax1.set_ylabel("body z (m), nadir / docking axis")
    ax1.set_title("(A) MESA deployed configuration", fontsize=11)
    ax1.grid(True, alpha=0.2)

    # --- (B) inertia, free-flyer vs mated ---
    ix_m, z_cm, _ = mated_inertia(ix)
    labels = ["$I_x$", "$I_y$", "$I_z$"]
    free = [ix, iy, iz]
    xpos = np.arange(3)
    ax2.bar(xpos - 0.18, free, 0.36, color="#2E5E8C", label="free flyer")
    ax2.bar([xpos[0] + 0.18], [ix_m], 0.36, color="#C0392B",
            label="mated with 3,000 kg client")
    for x, v in zip(xpos - 0.18, free):
        ax2.text(x, v * 1.03, f"{v:,.0f}", ha="center", fontsize=8)
    ax2.text(xpos[0] + 0.18, ix_m * 1.03, f"{ix_m:,.0f}", ha="center", fontsize=8)
    ax2.set_xticks(xpos)
    ax2.set_xticklabels(labels)
    ax2.set_ylabel("moment of inertia (kg$\\cdot$m$^2$)")
    ax2.set_title(f"(B) Mass properties; docking raises $I_x$ by "
                  f"{ix_m/ix:.1f}x", fontsize=11)
    ax2.legend(fontsize=8)
    ax2.grid(True, axis="y", alpha=0.3)
    ax2.set_ylim(0, ix_m * 1.18)

    fig.text(0.5, 0.005, "Figure 4: Sized MESA configuration and mass properties. "
             "The wheels must be sized for the mated stack, not the free flyer.",
             ha="center", va="bottom", fontsize=8.5, style="italic")
    fig.subplots_adjust(bottom=0.16, wspace=0.24)
    fig.savefig(FIG_DIR / "fig4_mesa_configuration.png", dpi=150)
    plt.close(fig)


def fig_thermal(a_rad):
    areas = np.linspace(0.5, 12.0, 400)
    t_sun = np.array([equilibrium_temps(a)[0] for a in areas]) - 273.15
    t_ecl = np.array([equilibrium_temps(a)[1] for a in areas]) - 273.15
    ts, te, _, _, _ = equilibrium_temps(a_rad)

    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    ax.plot(areas, t_sun, color="#C0392B", lw=2, label="sunlit equilibrium")
    ax.plot(areas, t_ecl, color="#2E5E8C", lw=2, label="eclipse equilibrium")
    ax.axhspan(-20, 50, color="#27AE60", alpha=0.10)
    ax.text(11.8, 48, "typical electronics\nsurvival band", ha="right", va="top",
            fontsize=8, color="#1E7B45")
    ax.axvline(a_rad, color="0.35", ls="--", lw=1.2)
    for temp, color, name in ((ts - 273.15, "#C0392B", "sun"),
                              (te - 273.15, "#2E5E8C", "eclipse")):
        ax.plot(a_rad, temp, "o", color=color, ms=7, zorder=5)
        ax.annotate(f"{name}: {temp:+.1f} $^\\circ$C", xy=(a_rad, temp),
                    xytext=(16, 14) if name == "sun" else (16, -34),
                    textcoords="offset points", fontsize=8.5,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6"),
                    arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.set_ylim(-70, 160)
    ax.annotate(f"selected radiator\n{a_rad:.1f} m$^2$ OSR", xy=(a_rad, -55),
                xytext=(a_rad + 1.6, -62), fontsize=8.5,
                bbox=dict(boxstyle="round,pad=0.3", fc="#FDF3E7", ec="#E67E22"),
                arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.set_xlabel("OSR radiator area (m$^2$)")
    ax.set_ylabel("Equilibrium temperature ($^\\circ$C)")
    ax.set_title("Section 8: MESA isothermal-bus thermal balance at GEO", fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=9)
    fig.text(0.5, 0.005, "Figure 5: Sizing the radiator is a trade between the "
             "sunlit and eclipse cases; heaters close the remaining eclipse gap.",
             ha="center", va="bottom", fontsize=8.5, style="italic")
    fig.subplots_adjust(bottom=0.15)
    fig.savefig(FIG_DIR / "fig5_thermal_balance.png", dpi=150)
    plt.close(fig)


def fig_torques(ix, iy, iz, area_srp):
    alts = np.logspace(np.log10(200e3), np.log10(40000e3), 500)
    r = R_E_M + alts
    tg = torque_gravity_gradient(r, iz, iy)
    tm, _ = torque_magnetic(r)
    tsp = np.full_like(r, torque_srp(area_srp)[0])
    # Aerodynamic uses the HW2 thermosphere fit, floored at the GEO exosphere
    # value so the curve stays continuous where the LEO fit runs out of validity.
    h_km = alts / 1000.0
    rho = np.maximum(1.020e7 * np.power(h_km, -7.172), RHO_GEO)
    ta = np.array([torque_aero(ri, area_srp, rho=rhoi)[0]
                   for ri, rhoi in zip(r, rho)])

    fig, ax = plt.subplots(figsize=(7.8, 5.4))
    ax.loglog(tsp, alts / 1000.0, color="#C0392B", lw=2, label="solar radiation")
    ax.loglog(tg, alts / 1000.0, color="#27AE60", lw=2, label="gravity gradient")
    ax.loglog(tm, alts / 1000.0, color="#8E6FC7", lw=2, label="magnetic")
    ax.loglog(ta, alts / 1000.0, color="#E67E22", lw=2, label="aerodynamic")
    ax.axhline(H_GEO / 1000.0, color="#1f4e79", ls="--", lw=1.5)
    ax.text(2e-9, H_GEO / 1000.0 * 1.10, "geostationary orbit", fontsize=9,
            color="#1f4e79")

    d = torque_summary(R_GEO, ix, iy, iz, area_srp)
    for key, color in (("solar radiation", "#C0392B"), ("gravity gradient", "#27AE60"),
                       ("magnetic", "#8E6FC7"), ("aerodynamic", "#E67E22")):
        ax.plot(d[key], H_GEO / 1000.0, "o", color=color, ms=7, zorder=6)
    ax.set_xlim(1e-9, 1e-1)
    ax.set_ylim(200, 45000)
    ax.set_xlabel("Disturbance torque (N$\\cdot$m)")
    ax.set_ylabel("Altitude (km)")
    ax.set_title("Section 11: External disturbance torques on MESA", fontsize=11)
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(loc="lower left", fontsize=8.5, framealpha=0.93)
    ax.text(0.97, 0.06,
            f"At GEO: SRP = {d['solar radiation']:.2e} N$\\cdot$m dominates\n"
            f"(gravity gradient {d['solar radiation']/d['gravity gradient']:.0f}x "
            f"smaller, aero {d['solar radiation']/d['aerodynamic']:.0f}x smaller)",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8,
            bbox=dict(boxstyle="round,pad=0.35", fc="#FDECEA", ec="#C0392B"))
    fig.text(0.5, 0.005, "Figure 6: Torque magnitudes for the MESA geometry. "
             "Markers are the GEO operating point; SRP sets the ADACS design.",
             ha="center", va="bottom", fontsize=8.5, style="italic")
    fig.subplots_adjust(bottom=0.14)
    fig.savefig(FIG_DIR / "fig6_disturbance_torques.png", dpi=150)
    plt.close(fig)


def fig_power(load_avg, load_peak):
    t, p_bol, p_eol, p_fixed, in_ecl, ecl = power_profile()
    th = t / 3600.0

    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    ax.fill_between(th, 0, p_eol, color="#2E5E8C", alpha=0.13)
    ax.plot(th, p_bol, color="#2E5E8C", lw=2, label="sun-tracking, BOL")
    ax.plot(th, p_eol, color="#C0392B", lw=2, ls="--",
            label=f"sun-tracking, EOL ({MISSION_YR:.0f} yr)")
    ax.plot(th, p_fixed, color="#8E6FC7", lw=1.6, ls="-.",
            label="body-fixed array (rejected)")
    ax.axhline(load_peak, color="#E67E22", lw=1.6, ls=":",
               label=f"peak load ({load_peak:.0f} W)")
    ax.axhline(load_avg, color="#27AE60", lw=1.6, ls=":",
               label=f"orbit-average load ({load_avg:.0f} W)")

    t0 = (T_GEO / 2 - ecl / 2) / 3600.0
    t1 = (T_GEO / 2 + ecl / 2) / 3600.0
    ax.axvspan(t0, t1, color="0.25", alpha=0.22)
    ax.annotate(f"eclipse\n{ecl/60:.0f} min",
                xy=((t0 + t1) / 2, 250), xytext=((t0 + t1) / 2 - 3.6, 900),
                fontsize=8.5, ha="center",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6"),
                arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.annotate("cold-cell spike on\neclipse exit (+8%)",
                xy=(t1 + 0.05, p_bol.max()), xytext=(t1 + 2.2, p_bol.max() * 1.09),
                fontsize=8.5,
                bbox=dict(boxstyle="round,pad=0.3", fc="#FDF3E7", ec="#E67E22"),
                arrowprops=dict(arrowstyle="->", color="0.5"))

    ax.set_xlim(0, 24)
    ax.set_ylim(0, p_bol.max() * 1.26)
    ax.set_xticks(np.arange(0, 25, 3))
    ax.set_xlabel("Time (hours from local noon)")
    ax.set_ylabel("Solar array power (W)")
    ax.set_title("Section 12: MESA array power over one day at GEO (equinox)",
                 fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower left", fontsize=8, ncol=2, framealpha=0.93)
    fig.text(0.5, 0.005, "Figure 7: Single-axis tracking holds full output through "
             "the day; a body-fixed array would not, which is why the wings track.",
             ha="center", va="bottom", fontsize=8.5, style="italic")
    fig.subplots_adjust(bottom=0.15)
    fig.savefig(FIG_DIR / "fig7_power_profile.png", dpi=150)
    plt.close(fig)


def fig_momentum(t_total, h_wheel_usable, h_capacity=200.0):
    """Sawtooth: momentum ramps under secular SRP, thrusters dump it to zero."""
    dump_day = h_wheel_usable / (t_total * 86400.0)
    days = np.linspace(0, 60, 4000)
    h = np.mod(t_total * days * 86400.0, h_wheel_usable)
    # Break the line at each dump so the drop renders vertically.
    h_plot = h.copy()
    h_plot[np.diff(h, prepend=h[0]) < 0] = np.nan

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    ax.plot(days, h_plot, color="#C0392B", lw=2, label="stored wheel momentum")
    ax.axhline(h_wheel_usable, color="#1f4e79", ls="--", lw=1.5,
               label=f"dump threshold ({h_wheel_usable:.0f} N$\\cdot$m$\\cdot$s)")
    ax.axhline(h_capacity, color="#27AE60", ls="-.", lw=1.5,
               label=f"wheel capacity ({h_capacity:.0f} N$\\cdot$m$\\cdot$s)")
    ax.axhspan(h_wheel_usable, h_capacity, color="#27AE60", alpha=0.08)
    ax.text(59, (h_wheel_usable + h_capacity) / 2, "saturation margin",
            ha="right", va="center", fontsize=8.5, color="#1E7B45")
    ax.annotate(f"thruster dump every {dump_day:.1f} days\n"
                f"({t_total*86400.0:.2f} N$\\cdot$m$\\cdot$s accumulated per day)",
                xy=(dump_day, h_wheel_usable), xytext=(dump_day + 5.5, 118),
                fontsize=8.5,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6"),
                arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.set_xlim(0, 60)
    ax.set_ylim(0, h_capacity * 1.12)
    ax.set_xlabel("Days on orbit")
    ax.set_ylabel("Stored angular momentum (N$\\cdot$m$\\cdot$s)")
    ax.set_title("Section 11: Secular momentum build-up and dump cadence",
                 fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", fontsize=8.5, ncol=3, framealpha=0.93)
    fig.text(0.5, 0.005, "Figure 8: SRP torque at GEO is secular, so the wheels "
             "ramp and must be desaturated with thrusters, not magnetorquers.",
             ha="center", va="bottom", fontsize=8.5, style="italic")
    fig.subplots_adjust(bottom=0.16)
    fig.savefig(FIG_DIR / "fig8_momentum.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    FIG_DIR.mkdir(exist_ok=True)
    bar = "=" * 72

    # --- mass properties ---
    ix, iy, iz, d_wing = mesa_inertia()
    ix_mated, z_cm, m_mated = mated_inertia(ix)
    a_total, a_proj, a_nadir = bus_areas()
    area_srp = A_ARRAY + a_proj

    print(bar)
    print("MESA VEHICLE DEFINITION (Section 8)")
    print(bar)
    print(f"  wet mass                    {M_WET:8.1f} kg  "
          f"(bus {M_BUS:.0f} kg + {N_WINGS} wings x {M_ARRAY_EACH:.0f} kg)")
    print(f"  bus envelope                {BUS_X} x {BUS_Y} x {BUS_Z} m")
    print(f"  array area (total)          {A_ARRAY:8.2f} m^2  "
          f"({N_WINGS} wings x {A_WING:.2f} m^2)")
    print(f"  bus radiating area          {a_total:8.2f} m^2")
    print(f"  bus sun-projected area      {a_proj:8.2f} m^2")
    print(f"  SRP reference area          {area_srp:8.2f} m^2  (arrays + bus)")
    print(f"  wing centroid offset        {d_wing:8.2f} m")
    print(f"  Ix, Iy, Iz (free flyer)     {ix:8.1f}  {iy:8.1f}  {iz:8.1f} kg*m^2")
    print(f"  |Iz - Iy|                   {abs(iz-iy):8.1f} kg*m^2")
    print(f"  Ix mated with {M_CLIENT:.0f} kg client {ix_mated:8.1f} kg*m^2 "
          f"({ix_mated/ix:.2f}x free flyer; cm shifts {z_cm:.2f} m)")

    # --- thermal ---
    a_rad = size_radiator()
    a_rad = round(a_rad, 1)
    t_sun, t_ecl, q_sun, q_earth, eps_a = equilibrium_temps(a_rad)
    q_ir, q_alb = earth_fluxes()
    p_heat = heater_power(a_rad)

    print()
    print(bar)
    print("SECTION 8  THERMAL CONTROL (Pisacane Ch. 12 energy balance)")
    print(bar)
    print(f"  Earth IR at GEO             {q_ir:8.2f} W/m^2")
    print(f"  albedo at GEO               {q_alb:8.2f} W/m^2")
    print(f"  absorbed solar (sun case)   {q_sun:8.1f} W")
    print(f"  absorbed Earth IR + albedo  {q_earth:8.2f} W  "
          f"({100*q_earth/(q_sun+Q_INT):.2f}% of the rest, neglected in hand calcs)")
    print(f"  internal dissipation        {Q_INT:8.1f} W")
    print(f"  radiator area (sized to {T_SUN_TARGET:.0f} K)  {a_rad:8.2f} m^2 OSR")
    print(f"  effective emitting area     {eps_a:8.3f} m^2")
    print(f"  >> T_sun                    {t_sun:8.2f} K = {t_sun-273.15:+7.2f} C")
    print(f"  >> T_eclipse                {t_ecl:8.2f} K = {t_ecl-273.15:+7.2f} C")
    print(f"  temperature swing           {t_sun-t_ecl:8.2f} K")
    print(f"  heater power to hold 0 C    {p_heat:8.1f} W")

    # --- disturbance torques ---
    d = torque_summary(R_GEO, ix, iy, iz, area_srp)
    _, f_srp = torque_srp(area_srp)
    _, f_aero, v_geo = torque_aero(R_GEO, area_srp)

    print()
    print(bar)
    print("SECTION 11  DISTURBANCE TORQUES AT GEO (SMAD Table 11.10)")
    print(bar)
    print(f"  orbit radius R              {R_GEO/1e3:8.1f} km")
    print(f"  orbital velocity V          {v_geo:8.1f} m/s")
    print(f"  Earth field B at GEO        {d['B']:8.3e} T")
    print(f"  SRP force                   {f_srp:8.3e} N")
    print(f"  aerodynamic force           {f_aero:8.3e} N")
    print("  " + "-" * 58)
    for k in ("solar radiation", "gravity gradient", "magnetic", "aerodynamic"):
        print(f"  {k:24s}    {d[k]:8.3e} N*m   "
              f"({100*d[k]/d['total']:5.2f}% of total)")
    print("  " + "-" * 58)
    print(f"  {'worst-case total T_D':24s}    {d['total']:8.3e} N*m")

    # --- wheel sizing ---
    theta_slew = np.radians(30.0)
    t_slew_free, t_slew_mated = 300.0, 600.0
    m_slew_free = 4.0 * ix * theta_slew / t_slew_free**2
    m_slew_mated = 4.0 * ix_mated * theta_slew / t_slew_mated**2
    h_slew_free = ix * (2.0 * theta_slew / t_slew_free)
    h_slew_mated = ix_mated * (2.0 * theta_slew / t_slew_mated)
    h_cyclic = 0.707 * d["total"] * (T_GEO / 4.0)
    h_secular_day = d["total"] * T_GEO
    margin = 1.0
    m_required = max(m_slew_free, m_slew_mated, d["total"]) * (1.0 + margin)

    h_usable = 50.0
    n_wheels = 4
    m_wheel, p_wheel = 25.0, 100.0        # Lesson 7 Part 2 slide 11, large sats

    print()
    print(bar)
    print("SECTION 11  ACTUATOR SIZING (SMAD Table 11.7; Lesson 7 Pt 2 slide 11)")
    print(bar)
    print(f"  30 deg slew, free flyer     {m_slew_free:8.4f} N*m, "
          f"H = {h_slew_free:6.2f} N*m*s  ({t_slew_free:.0f} s)")
    print(f"  30 deg slew, mated          {m_slew_mated:8.4f} N*m, "
          f"H = {h_slew_mated:6.2f} N*m*s  ({t_slew_mated:.0f} s)")
    print(f"  cyclic H = 0.707 T_D (P/4)  {h_cyclic:8.4f} N*m*s")
    print(f"  secular H per day           {h_secular_day:8.3f} N*m*s/day")
    print(f"  >> wheel torque, margin {margin:.0f}.0   {m_required:8.4f} N*m "
          f"-> 'large sats' row (> 0.15 N*m)")
    print(f"  >> {n_wheels} wheels                 {n_wheels*m_wheel:8.1f} kg, "
          f"{n_wheels*p_wheel:.0f} W peak")
    print(f"  >> dump cadence             {h_usable/h_secular_day:8.1f} days "
          f"(at {h_usable:.0f} N*m*s usable)")

    sensors = [("2 star trackers", 10.0, 36.0), ("2 IMUs (1 active)", 10.0, 30.0),
               ("4 coarse sun sensors", 4.0, 12.0),
               ("ADACS control electronics", 8.0, 25.0),
               ("RPO LIDAR and cameras", 25.0, 60.0)]
    m_ad = n_wheels * m_wheel + sum(s[1] for s in sensors)
    p_ad = 120.0 + sum(s[2] for s in sensors)     # wheels at orbit-average draw
    print(f"  >> ADACS total              {m_ad:8.1f} kg ({100*m_ad/M_WET:.1f}% of "
          f"wet mass), {p_ad:.0f} W orbit-average")

    # --- power ---
    p_bol, p_eol = array_power(True), array_power(False)
    load_peak = sum(v for _, v in POWER_LOADS)
    load_avg = Q_INT
    ecl = eclipse_duration()
    years_to_limit = np.log(load_peak / p_bol) / np.log(1.0 - DEGRADE_PER_YR)

    print()
    print(bar)
    print("SECTION 12  POWER AND MISSION LIFE")
    print(bar)
    for name, w in POWER_LOADS:
        print(f"    {name:40s} {w:7.0f} W")
    print(f"    {'peak load':40s} {load_peak:7.0f} W")
    print(f"    {'orbit-average load':40s} {load_avg:7.0f} W")
    print(f"  array BOL output            {p_bol:8.0f} W")
    print(f"  array EOL output ({MISSION_YR:.0f} yr)     {p_eol:8.0f} W  "
          f"({100*p_eol/p_bol:.1f}% of BOL)")
    print(f"  EOL margin over peak load   {100*(p_eol-load_peak)/load_peak:8.1f}%")
    print(f"  max eclipse at equinox      {ecl/60:8.1f} min "
          f"(commonly quoted maximum is ~72 min)")
    print(f"  battery energy for eclipse  {load_peak*ecl/3600:8.0f} W*h at peak load")
    print(f"  power-limited life          {years_to_limit:8.1f} yr "
          f"(propellant-limited life from MS1 is the binding constraint)")

    # --- radiation ---
    tid_per_yr = 5.0
    tid_mission = tid_per_yr * MISSION_YR
    tid_margin = tid_mission * 2.0
    print()
    print(bar)
    print("SECTION 10  RADIATION (Pisacane Tables 9.6, 9.9)")
    print(bar)
    print(f"  assumed TID behind 100 mil Al {tid_per_yr:6.1f} krad(Si)/yr at GEO")
    print(f"  {MISSION_YR:.0f}-year mission TID         {tid_mission:8.1f} krad(Si)")
    print(f"  with 2x rad-hard margin     {tid_margin:8.1f} krad(Si)")
    print(f"  >> select RHA category R (100 krad(Si)), the next level above "
          f"{tid_margin:.0f} krad(Si)")
    print(f"  array degradation           {100*DEGRADE_PER_YR:8.1f} %/yr -> "
          f"{100*(1-(1-DEGRADE_PER_YR)**MISSION_YR):.1f}% total over {MISSION_YR:.0f} yr")

    # --- figures ---
    fig_orbit_3d()
    fig_configuration(ix, iy, iz, a_rad)
    fig_thermal(a_rad)
    fig_torques(ix, iy, iz, area_srp)
    fig_power(load_avg, load_peak)
    fig_momentum(d["total"], h_usable)
    print()
    print("Figures written to:", FIG_DIR)


if __name__ == "__main__":
    main()
