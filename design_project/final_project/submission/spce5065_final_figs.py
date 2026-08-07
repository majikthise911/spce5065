"""SPCE 5065 Design Project, Final Report: MESA analysis and figures.

MESA (Mission Extension and Servicing Asset), a GEO servicing tug. This script
computes every number quoted in the final report and writes Figures 0 through
12 plus 16 and 17 to ./figures/. Figures 13 to 15 are the STK captures and are
built by the scripts in ./stk/.

It is a superset of the Milestone 2 script (spce5065_ms2_figs.py): the
Milestone 1 and 2 analyses are carried forward unchanged, and the new work for
the final report is the system budget closure (mass, power, delta-v,
propellant, cost), the transient thermal simulation, and the micrometeoroid and
orbital debris assessment.

Outputs:

  fig0_mesa_concept.png        Cover art: the servicer docking with a client.
  fig1_conops.png              Concept of operations: one servicing cycle and
                               the five-year manifest (Section 2).
  fig2_orbit_regimes.png       Scaled orbit-regime diagram (Section 3).
  fig3_drag_lifetime.png       Drag-decay lifetime vs altitude (Section 3).
  fig4_mesa_configuration.png  Sized configuration and mass properties (Sec 7).
  fig5_budgets.png             Mass and power budgets closing to 2,000 kg and
                               to the end-of-life array output (Section 7).
  fig6_deltav_propellant.png   Delta-v allocation and servicing capacity vs
                               propellant load (Section 7).
  fig7_thermal_balance.png     Equilibrium temperature vs radiator area (Sec 8).
  fig8_disturbance_torques.png The four disturbance torques vs altitude (Sec 11).
  fig9_momentum.png            Secular momentum build-up and dumps (Section 11).
  fig10_orbit_propagation.png  3D GEO orbit over one sidereal day plus the
                               ground track (Section 12).
  fig11_power_profile.png      Array power over one day at equinox (Section 12).
  fig12_thermal_transient.png  Lumped-capacitance temperature through eclipse,
                               bus vs an outboard zone (Section 12).
  fig16_mmod.png               Meteoroid flux and impact probability (Sec 13).
  fig17_risk_matrix.png        Risk matrix before and after mitigation (Sec 13).

Sources for the models:
  Drag decay a-dot and the thermosphere density fit       Homework 2
  Gravity gradient, SRP, magnetic, aerodynamic torques     SMAD Ch. 11 Table 11.10
  Wheel sizing (H = 0.707 T_D [P/4], M = 4 I theta / t^2)  SMAD Ch. 11 Table 11.7
  Wheel mass and power lookup                              Lesson 7 Part 2 slide 11
  Equilibrium temperature energy balance                   Pisacane Ch. 12
  RHA categories (krad(Si) limits)                         Pisacane Table 9.9
  Grun sporadic meteoroid flux, shielding, focusing        Lesson 12 slides 4 to 6
  Whipple bumper and wall sizing                           Pisacane Eqs. 11.27 to 11.31

Run: python3 spce5065_final_figs.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

FIG_DIR = Path(__file__).parent / "figures"

# ---------------------------------------------------------------------------
# Physical constants (SI)
# ---------------------------------------------------------------------------
MU = 3.986004418e14        # m^3/s^2    Earth gravitational parameter
R_E_M = 6378.137e3         # m          Earth equatorial radius
R_E_KM = 6378.137          # km
SIGMA = 5.670374419e-8     # W/m^2/K^4  Stefan-Boltzmann
C_LIGHT = 2.99792458e8     # m/s
G0 = 9.80665               # m/s^2
S_SOLAR = 1361.0           # W/m^2      solar constant at 1 AU (Section 4.1)
M_EARTH_MAG = 7.96e15      # tesla*m^3  Earth magnetic moment (SMAD Table 11.10)
Q_EARTH_IR = 237.0         # W/m^2      Earth IR emission at the surface
ALBEDO = 0.30              # -          Earth Bond albedo

H_GEO = 35786.0e3          # m          GEO altitude
R_GEO = R_E_M + H_GEO      # m          GEO radius, 42,164 km
T_GEO = 86164.0            # s          sidereal day (GEO period)
H_GRAVEYARD = 300.0e3      # m          graveyard offset above GEO

H_REENTRY = 150.0          # km         reentry altitude for the decay integral

# ---------------------------------------------------------------------------
# MESA vehicle definition (Section 7). Mass from Milestone 1; geometry sized in
# Milestone 2 and frozen here.
# ---------------------------------------------------------------------------
M_WET = 2000.0             # kg   wet mass
M_PROP = 600.0             # kg   total propellant load
M_DRY = M_WET - M_PROP     # kg
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
CD = 2.2                   # -    drag coefficient
RHO_GEO = 1.0e-15          # kg/m^3 neutral density at GEO
A_RAM_LEO = 15.0           # m^2  ram area used for the LEO drag contrast

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
    """Free-flyer principal moments (Ix, Iy, Iz) about the MESA cm, kg*m^2."""
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
# Orbit and drag decay (Milestone 1, Homework 2 model)
# ---------------------------------------------------------------------------
def rho_hw2(h_km):
    """Homework 2 thermosphere fit: rho = 1.020e7 * h^-7.172 (kg/m^3, h in km)."""
    return 1.020e7 * np.power(h_km, -7.172)


def drag_lifetime_days(h0_km: float, n: int = 6000) -> float:
    """Decay time from h0 down to 150 km using a-dot = -rho (Cd A/m) sqrt(mu a)."""
    bc_inv = CD * A_RAM_LEO / M_WET
    a0 = R_E_M + h0_km * 1000.0
    af = R_E_M + H_REENTRY * 1000.0
    a = np.linspace(a0, af, n)
    h_km = a / 1000.0 - R_E_KM
    adot = -rho_hw2(h_km) * bc_inv * np.sqrt(MU * a)
    return float(np.trapezoid(1.0 / np.abs(adot), -a)) / 86400.0


def hohmann_dv(r1: float, r2: float):
    """Two-burn transfer between circular coplanar orbits, m/s."""
    a_t = 0.5 * (r1 + r2)
    dv1 = abs(np.sqrt(MU / r1) * (np.sqrt(r2 / a_t) - 1.0))
    dv2 = abs(np.sqrt(MU / r2) * (1.0 - np.sqrt(r1 / a_t)))
    return dv1, dv2, dv1 + dv2


def relocation_dv(drift_deg_per_day: float) -> float:
    """Delta-v to start and stop a GEO longitude drift, m/s.

    A drift rate of lambda_dot deg/day needs a semi-major axis offset
    da/a = lambda_dot / (1.5 * 360), and each of the two burns costs
    dv = (V/2)(da/a).
    """
    v_geo = np.sqrt(MU / R_GEO)
    da_over_a = drift_deg_per_day / (1.5 * 360.0)
    return 2.0 * 0.5 * v_geo * da_over_a


def prop_mass(m0: float, dv: float, isp: float) -> float:
    """Propellant burned for a delta-v starting from mass m0, kg."""
    return m0 * (1.0 - np.exp(-dv / (isp * G0)))


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


# --- transient thermal (new for the final report) --------------------------
CP_AL = 900.0              # J/(kg*K)  aluminium-dominated specific heat
M_BUS_THERMAL = M_DRY      # kg        dry mass taken as the bus thermal lump

# Outboard propellant line and latch-valve zone: small mass, no internal
# dissipation, thermally isolated from the bus. This is the zone the heaters
# actually exist for, because hydrazine freezes at 2 C.
M_ZONE = 6.0               # kg
A_ZONE = 0.50              # m^2   radiating area
EPS_ZONE = 0.20            # -     effective emittance through the blanket
ALPHA_ZONE = 0.14          # -     Ag/FEP blanket outer layer
A_ZONE_PROJ = 0.25         # m^2   sun-projected area
Q_ZONE_INT = 0.0           # W     no dissipating box on this zone
P_ZONE_HEATER = 40.0       # W     heater string on this zone
T_ZONE_SETPOINT = 278.0    # K     thermostat set point (+5 C), above the 2 C
                           #       hydrazine freezing point
T_HYDRAZINE_FREEZE = 275.1  # K    2 C


def transient_temperature(t_s, t0, c_th, q_sun_fn, q_int, eps_a, heater=None,
                          setpoint=None):
    """Integrate C dT/dt = Q_in(t) - sigma*eps*A*T^4 with forward Euler.

    heater/setpoint model a thermostat: full heater power below the set point,
    nothing above it.
    """
    temps = np.empty_like(t_s)
    t = t0
    for k, tt in enumerate(t_s):
        temps[k] = t
        if k == len(t_s) - 1:
            break
        dt = t_s[k + 1] - tt
        q_h = 0.0
        if heater is not None and setpoint is not None and t < setpoint:
            q_h = heater
        q_in = q_sun_fn(tt) + q_int + q_h
        t += dt * (q_in - SIGMA * eps_a * t**4) / c_th
    return temps


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
    """One-day array power at equinox, with the eclipse and the cold-cell spike."""
    t = np.linspace(0.0, T_GEO, n)
    ecl = eclipse_duration()
    t_exit = T_GEO / 2.0 + ecl / 2.0
    in_eclipse = np.abs(t - T_GEO / 2.0) <= ecl / 2.0

    dt = np.clip(t - t_exit, 0.0, None)
    t_cell = np.where(t > t_exit,
                      T_CELL_HOT + (T_CELL_COLD - T_CELL_HOT) * np.exp(-dt / TAU_CELL),
                      T_CELL_HOT)
    temp_gain = 1.0 + K_TEMP * (T_CELL_HOT - t_cell)

    p_bol = np.where(in_eclipse, 0.0, array_power(True) * temp_gain)
    p_eol = np.where(in_eclipse, 0.0, array_power(False, years) * temp_gain)

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

# Battery sizing
DOD = 0.60                 # -        allowed depth of discharge, GEO Li-ion
ETA_LINE = 0.90            # -        discharge path efficiency
E_DENS_CELL = 150.0        # W*h/kg   Li-ion cell specific energy
PACK_OVERHEAD = 1.5        # -        cells to installed battery mass


# ---------------------------------------------------------------------------
# Mass, propulsion and cost budgets (new for the final report)
# ---------------------------------------------------------------------------
MASS_BUDGET = [
    ("Structure and mechanisms", 300.0),
    ("Docking mechanism and robotic arm", 180.0),
    ("ADACS (wheels, sensors, RPO)", 157.0),
    ("Propulsion, dry", 165.0),
    ("Power (arrays, battery, PCU, harness)", 268.0),
    ("Thermal control", 65.0),
    ("C&DH and avionics (incl. shielding)", 75.0),
    ("Communications", 40.0),
]

COST_BUDGET = [
    ("Docking mechanism and robotic arm", 15.0),
    ("ADACS and RPO sensor suite", 18.0),
    ("Avionics, C&DH, comms (category R parts)", 12.0),
    ("Bus structure and mechanisms", 12.0),
    ("Power subsystem", 10.0),
    ("Integration, test and TVAC campaign", 9.0),
    ("Propulsion", 8.0),
    ("Program management and systems engineering", 7.0),
    ("Thermal control", 4.0),
    ("Program reserve", 5.0),
]

# Propulsion
ISP_EP = 1600.0            # s     xenon Hall thruster
THRUST_EP = 0.040          # N     at the 600 W operating point
ISP_MONO = 220.0           # s     hydrazine monopropellant
M_XENON = 520.0            # kg    tank load, electric propulsion
M_HYDRAZINE = M_PROP - M_XENON   # kg  tank load, monopropellant

DV_SK_PER_YR = 50.0        # m/s/yr  north-south plus east-west stationkeeping
DV_RPO_PER_CLIENT = 8.0    # m/s     approach, backout, contingency abort
N_CLIENTS_BASELINE = 6     # servicing cycles in the five-year contract
MATED_FRACTION = 0.8       # -       fraction of the mission spent mated
DOCK_ARM = 0.9             # m       thruster moment arm for momentum dumps


# ---------------------------------------------------------------------------
# Micrometeoroids and debris (Lesson 12; Pisacane Ch. 11)
# ---------------------------------------------------------------------------
R_A_KM = R_E_KM + 100.0    # km    top of the shielding atmosphere
RHO_METEOROID = 2.5        # g/cm^3
V_METEOROID = 20.0         # km/s  mean sporadic impact speed at Earth
# Bus exterior plus both faces of both wings, computed rather than assumed.
A_MESA_MMOD = (2 * (BUS_X * BUS_Y) + 2 * (BUS_X * BUS_Z) + 2 * (BUS_Y * BUS_Z)
               + 2 * A_ARRAY)     # m^2


def sphere_mass_g(d_cm):
    """Mass of a spherical particle of diameter d_cm, grams."""
    return (4.0 * np.pi / 3.0) * (np.asarray(d_cm, float) / 2.0) ** 3 * RHO_METEOROID


def grun_flux_interplanetary(m_g):
    """Unshielded cumulative sporadic flux F_spo(m), particles/m^2/yr.

    Lesson 12 slide 4 (Pisacane Eq. 11.2). The slide misprints the third term
    as F2; it is F3.
    """
    m = np.asarray(m_g, dtype=float)
    f1 = (2.2e3 * m ** 0.306 + 15.0) ** (-4.38)
    f2 = 1.3e-9 * (m + 1.0e11 * m ** 2 + 1.0e27 * m ** 4) ** (-0.36)
    f3 = 1.3e-16 * (m + 1.0e6 * m ** 2) ** (-0.85)
    return 3.15576e7 * (f1 + f2 + f3)


def shielding_factor(r_km: float, branch: str = "random") -> float:
    """Earth-shielding factor, sin(theta) = R_a/r (Lesson 12 slide 5)."""
    cos_t = float(np.sqrt(1.0 - (R_A_KM / r_km) ** 2))
    if branch == "nadir":
        return cos_t
    return 0.5 * (1.0 + cos_t)


def focusing_factor(r_km: float) -> float:
    """Gravitational focusing factor G = 1 + R_a/r (Lesson 12 slide 6)."""
    return 1.0 + R_A_KM / r_km


def flux_at_orbit(m_g, h_km: float, branch: str = "random"):
    """F_sp(m, r) = F_spo(m) * chi(r) * G(r), particles/m^2/yr."""
    r = R_E_KM + h_km
    return (grun_flux_interplanetary(m_g)
            * shielding_factor(r, branch) * focusing_factor(r))


def whipple_thickness(s_cm, d_cm, rho_p, v_kms, sigma_ksi, rho_b, rho_w,
                      theta_deg=0.0):
    """Bumper and rear-wall thickness, cm (Pisacane Eqs. 11.27 to 11.31)."""
    s = np.asarray(s_cm, dtype=float)
    m_p = (4.0 * np.pi / 3.0) * (d_cm / 2.0) ** 3 * rho_p
    c_b = np.where(s / d_cm < 30.0, 0.25, 0.20)
    t_b = c_b * d_cm * rho_p / rho_b
    k = np.where(s / d_cm < 15.0, (s / d_cm / 15.0) ** (-0.185), 1.0)
    t_w = (0.79 * k * d_cm ** 0.5 * m_p ** (1.0 / 3.0)
           * (rho_p * rho_b) ** (1.0 / 6.0) / rho_w
           * s ** (-0.75) * (sigma_ksi / 70.0) ** (-0.5)
           * v_kms * np.cos(np.radians(theta_deg)))
    return t_b, t_w


# Risk register: (label, likelihood before, consequence before, likelihood
# after, consequence after). Scales run 1 (low) to 5 (high).
RISKS = [
    ("R1 ESD at capture", 4, 5, 2, 3),
    ("R2 SEP during RPO", 3, 4, 2, 2),
    ("R3 Deep-dielectric arc", 3, 4, 2, 2),
    ("R4 Client tumbling", 3, 5, 2, 3),
    ("R5 RPO optics contamination", 4, 4, 2, 2),
    ("R6 MMOD on array", 3, 2, 3, 1),
    ("R7 Cold welding in mechanism", 2, 5, 1, 3),
    ("R8 Wheel saturation", 4, 2, 1, 2),
    ("R9 TID above assumption", 2, 4, 1, 2),
    ("R10 Heater string failure", 2, 4, 1, 2),
]


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
def _caption(fig, text, y=0.005):
    fig.text(0.5, y, text, ha="center", va="bottom", fontsize=8.5, style="italic")


def fig_concept() -> None:
    """Cover art: MESA approaching a client comsat."""
    fig, ax = plt.subplots(figsize=(9.0, 5.2))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")
    ax.set_facecolor("#0B1020")
    fig.patch.set_facecolor("#0B1020")

    gold = "#C9A227"
    body = "#D8DCE3"
    arr = "#2E5E8C"

    ax.add_patch(mpatches.FancyBboxPatch((3.0, 3.4), 2.4, 2.2,
                 boxstyle="round,pad=0.05", fc=body, ec="0.3", lw=1.2))
    ax.text(4.2, 4.5, "MESA\nservicer", ha="center", va="center",
            fontsize=9, weight="bold", color="#111")
    for dy in (2.35, -2.35):
        ax.add_patch(mpatches.Rectangle((3.6, 4.5 + dy - 0.55), 1.2, 1.1,
                     fc=arr, ec="0.25"))
        ax.plot([4.2, 4.2], [4.5, 4.5 + dy], color="0.5", lw=1)
    for dy in (-0.6, 0.0, 0.6):
        ax.add_patch(mpatches.Polygon([[3.0, 4.5 + dy - 0.12], [3.0, 4.5 + dy + 0.12],
                     [2.6, 4.5 + dy]], closed=True, fc="#E67E22", ec="0.3"))
    ax.add_patch(mpatches.Rectangle((5.4, 4.35), 1.4, 0.3, fc="#7F8C8D", ec="0.3"))
    ax.plot([5.4, 6.4, 7.2], [3.9, 3.5, 3.9], color="#95A5A6", lw=3,
            solid_capstyle="round")
    ax.add_patch(mpatches.Circle((6.9, 4.5), 0.18, fc="#111", ec=gold, lw=1.5))

    ax.add_patch(mpatches.FancyBboxPatch((9.6, 3.7), 1.8, 1.6,
                 boxstyle="round,pad=0.05", fc="#B7BCC4", ec="0.3", lw=1.1))
    ax.text(10.5, 4.5, "client\ncomsat", ha="center", va="center",
            fontsize=8.5, color="#111")
    ax.add_patch(mpatches.Rectangle((8.4, 4.0), 1.1, 1.0, fc=arr, ec="0.25"))
    ax.add_patch(mpatches.Rectangle((11.4, 4.0), 1.1, 1.0, fc=arr, ec="0.25"))

    ax.annotate("", xy=(9.4, 4.5), xytext=(7.4, 4.5),
                arrowprops=dict(arrowstyle="-|>", color=gold, lw=2))
    ax.text(8.4, 4.95, "rendezvous\n& dock", ha="center", va="bottom",
            fontsize=8, color=gold, style="italic")

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

    ax.set_title("MESA: GEO Mission Extension and Servicing Asset",
                 fontsize=12, color="#E6EDF3", pad=10)
    fig.savefig(FIG_DIR / "fig0_mesa_concept.png", dpi=150, facecolor="#0B1020")
    plt.close(fig)


def fig_conops() -> None:
    """Concept of operations: one servicing cycle, and the five-year manifest."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.4, 6.4),
                                   gridspec_kw={"height_ratios": [1.25, 1.0]})

    # --- (A) one servicing cycle -------------------------------------------
    phases = [
        ("Drift to\nclient slot", 25, "#2E5E8C"),
        ("Far-field\ninspection", 6, "#2E7D8C"),
        ("RPO\napproach", 3, "#27AE60"),
        ("Capture\nand dock", 1, "#C9A227"),
        ("Mated ops: stationkeeping, refuel, checkout", 200, "#C0392B"),
        ("Tow to\ngraveyard", 5, "#8E6FC7"),
        ("Undock and\ndepart", 2, "#7F8C8D"),
    ]
    total_days = sum(p[1] for p in phases)
    x = 0.0
    ax1.set_xlim(-26, total_days + 6)
    ax1.set_ylim(-2.3, 2.7)
    narrow = 0
    for name, dur, color in phases:
        ax1.add_patch(mpatches.FancyBboxPatch((x + 0.6, -0.30), dur - 1.2, 0.60,
                      boxstyle="round,pad=0.02", fc=color, ec="0.25", lw=0.8))
        label = f"{name} ({dur} d)".replace("\n", " ")
        if dur >= 100:
            ax1.text(x + dur / 2.0, 0.0, label, ha="center", va="center",
                     fontsize=7.6, color="white", weight="bold")
        else:
            # Short phases get an external label on a leader line, staggered so
            # the four of them do not pile up on each other.
            y = 0.72 + 0.38 * (narrow % 4)
            ax1.annotate(label, xy=(x + dur / 2.0, 0.30),
                         xytext=(x + dur / 2.0 - 26 + 14 * (narrow % 2), y),
                         fontsize=7.4, ha="left", va="center",
                         arrowprops=dict(arrowstyle="-", color="0.55", lw=0.8))
            narrow += 1
        x += dur
    ax1.annotate("space-weather hold gate:\nno capture inside an SEP or "
                 "substorm warning window",
                 xy=(33.5, -0.30), xytext=(96, -1.35), fontsize=7.8,
                 bbox=dict(boxstyle="round,pad=0.3", fc="#FDF3E7", ec="#E67E22"),
                 arrowprops=dict(arrowstyle="->", color="#E67E22"))
    ax1.annotate("plasma contactor on,\npotentials equalized\nbefore contact",
                 xy=(34.2, -0.30), xytext=(4, -1.95), fontsize=7.8, va="bottom",
                 bbox=dict(boxstyle="round,pad=0.3", fc="#EAF2FA", ec="#2E5E8C"),
                 arrowprops=dict(arrowstyle="->", color="#2E5E8C"))
    ax1.set_yticks([])
    ax1.set_xlabel("Days from start of a servicing cycle", fontsize=9)
    ax1.set_title(f"(A) One MESA servicing cycle, {total_days} days",
                  fontsize=10.5)
    for s in ("top", "right", "left"):
        ax1.spines[s].set_visible(False)

    # --- (B) five-year manifest --------------------------------------------
    ax2.set_xlim(0, 60)
    ax2.set_ylim(0.2, 7.0)
    starts = [2, 10, 18, 26, 34, 42]
    for k, s0 in enumerate(starts):
        y = 6 - k
        ax2.add_patch(mpatches.Rectangle((s0, y - 0.28), 8.0, 0.56,
                      fc="#C0392B", ec="0.3", alpha=0.85))
        ax2.add_patch(mpatches.Rectangle((s0 - 1.6, y - 0.28), 1.6, 0.56,
                      fc="#2E5E8C", ec="0.3", alpha=0.85))
        ax2.text(s0 + 4.0, y, f"Client {k+1}: mated service", ha="center",
                 va="center", fontsize=7.6, color="white")
    ax2.axvline(60, color="#27AE60", lw=1.6, ls="--")
    ax2.text(59.2, 6.6, "five-year contract boundary", ha="right", fontsize=8,
             color="#1E7B45")
    ax2.text(0.6, 0.7, "blue: transit and rendezvous     red: mated service",
             fontsize=7.8, color="0.35")
    ax2.set_xticks(np.arange(0, 61, 12))
    ax2.set_xlabel("Months from operational handover", fontsize=9)
    ax2.set_yticks([])
    ax2.set_title("(B) Baseline manifest: six client servicing cycles in five years",
                  fontsize=10.5)
    for s in ("top", "right", "left"):
        ax2.spines[s].set_visible(False)

    _caption(fig, "Figure 1: MESA concept of operations. Capture is the short, "
             "irreversible step in a long cycle, which is why the design gates it "
             "on space weather and equalizes potential first.")
    fig.subplots_adjust(bottom=0.13, hspace=0.55, top=0.94)
    fig.savefig(FIG_DIR / "fig1_conops.png", dpi=150)
    plt.close(fig)


def fig_orbit_regimes() -> None:
    fig, ax = plt.subplots(figsize=(7.4, 7.4))
    ax.set_aspect("equal")
    regimes = [
        (R_E_KM + 400, "LEO  (400 km)", "#3B82C4", ":"),
        (R_E_KM + 20200, "MEO  (20,200 km)", "#8E6FC7", "--"),
        (R_E_KM + 35786, "GEO  (35,786 km)", "#C0392B", "-"),
        (R_E_KM + 36086, "GEO graveyard (+300 km)", "#7F8C8D", (0, (2, 3))),
    ]
    for r, label, color, ls in regimes:
        ax.add_patch(plt.Circle((0, 0), r, fill=False, ec=color, lw=2, ls=ls,
                                label=label))
    ax.add_patch(plt.Circle((0, 0), R_E_KM, fc="#2E5E8C", ec="#1B3A57", lw=1.2))
    ax.text(0, 0, "Earth", ha="center", va="center", color="white",
            fontsize=10, weight="bold")
    r_geo = R_E_KM + 35786
    ax.plot(r_geo, 0, marker="s", ms=11, color="#C0392B", zorder=5)
    ax.annotate("MESA tug\n(parked at GEO)", xy=(r_geo, 0), xytext=(14, 20),
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
    lim = (R_E_KM + 35786) * 1.18
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim * 1.02)
    ax.set_xlabel("km")
    ax.set_ylabel("km")
    ax.set_title("Orbit regimes to scale: MESA services at GEO", fontsize=12)
    ax.grid(True, alpha=0.2)
    ax.legend(loc="upper left", fontsize=8.5, framealpha=0.92,
              title="Orbital regime")
    _caption(fig, "Figure 2: Equatorial view to scale. The tug operates in the "
             "GEO belt (35,786 km), moving clients to and from the graveyard.")
    fig.subplots_adjust(bottom=0.10)
    fig.savefig(FIG_DIR / "fig2_orbit_regimes.png", dpi=150)
    plt.close(fig)


def fig_orbit_3d() -> None:
    """3D inertial view of the GEO orbit plus the ground track."""
    a_km = R_GEO / 1000.0

    fig = plt.figure(figsize=(12.0, 5.6))
    axA = fig.add_subplot(1, 2, 1, projection="3d")

    u = np.linspace(0, 2 * np.pi, 90)
    v = np.linspace(0, np.pi, 45)
    xs = R_E_KM * np.outer(np.cos(u), np.sin(v))
    ys = R_E_KM * np.outer(np.sin(u), np.sin(v))
    zs = R_E_KM * np.outer(np.ones_like(u), np.cos(v))
    axA.plot_surface(xs, ys, zs, color="#2E5E8C", alpha=0.85, linewidth=0,
                     antialiased=True, shade=True, zorder=1)
    th = np.linspace(0, 2 * np.pi, 200)
    axA.plot(R_E_KM * np.cos(th), R_E_KM * np.sin(th), 0, color="#9FC0DC",
             lw=0.8, alpha=0.9)
    axA.plot([0, 0], [0, 0], [-R_E_KM * 1.9, R_E_KM * 1.9], color="0.45",
             lw=1.0, ls=":")

    axA.plot(a_km * np.cos(th), a_km * np.sin(th), 0, color="#C0392B", lw=2.2,
             label="GEO orbit (35,786 km)")
    ag = a_km + 300.0
    axA.plot(ag * np.cos(th), ag * np.sin(th), 0, color="#7F8C8D", lw=1.0,
             ls=(0, (2, 3)), label="graveyard (+300 km)")

    uh = 2.0 * np.pi * np.arange(24) / 24.0
    axA.scatter(a_km * np.cos(uh), a_km * np.sin(uh), np.zeros_like(uh),
                color="#E67E22", s=16, depthshade=False, label="MESA, hourly")
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

    _caption(fig, "Figure 10: Three-dimensional simulation of the MESA orbit over "
             "one sidereal day. The vehicle holds one longitude, but without\n"
             "north-south stationkeeping the inclination grows and the ground "
             "track opens into an analemma.", y=0.015)
    fig.subplots_adjust(bottom=0.19, wspace=0.16, left=0.02, right=0.97)
    fig.savefig(FIG_DIR / "fig10_orbit_propagation.png", dpi=150)
    plt.close(fig)


def fig_drag_lifetime() -> None:
    alts = np.arange(250, 1001, 25)
    life = np.array([drag_lifetime_days(h) for h in alts]) / 365.25

    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    ax.semilogy(alts, life, color="#1f4e79", lw=2)
    ax.axhline(5.0, color="#C0392B", ls="--", lw=1.3)
    ax.text(255, 6.2, "5-yr mission requirement", color="#C0392B", fontsize=8.5)
    l400 = drag_lifetime_days(400) / 365.25
    ax.plot(400, l400, "o", color="#C0392B", ms=6)
    ax.annotate(f"tug at 400 km:\n{l400*365.25:.0f} days ({l400:.2f} yr)",
                xy=(400, l400), xytext=(20, 10), textcoords="offset points",
                fontsize=8.5, bbox=dict(boxstyle="round,pad=0.3", fc="white",
                ec="0.6"), arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.set_xlabel("Starting altitude (km)")
    ax.set_ylabel("Drag-decay lifetime (years, log scale)")
    ax.set_title("Section 3: LEO drag lifetime for the tug; GEO is off-scale",
                 fontsize=11)
    ax.grid(True, which="both", alpha=0.3)
    ax.text(0.98, 0.06, "GEO (35,786 km): drag decay ~10$^{5}$ to 10$^{6}$ yr,\n"
            "not the life-limiting mechanism",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.35", fc="#FDECEA", ec="#C0392B"))
    _caption(fig, "Figure 3: With the Homework 2 neutral-density model, LEO "
             "lifetime rises steeply with altitude; at GEO drag is negligible.")
    fig.subplots_adjust(bottom=0.16)
    fig.savefig(FIG_DIR / "fig3_drag_lifetime.png", dpi=150)
    plt.close(fig)


def fig_configuration(ix, iy, iz, a_rad) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.4, 5.0))

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

    _caption(fig, "Figure 4: Sized MESA configuration and mass properties. The "
             "wheels must be sized for the mated stack, not the free flyer.")
    fig.subplots_adjust(bottom=0.16, wspace=0.24)
    fig.savefig(FIG_DIR / "fig4_mesa_configuration.png", dpi=150)
    plt.close(fig)


def fig_budgets(m_margin, load_peak, load_avg, p_bol, p_eol) -> None:
    """Mass budget closing to 2,000 kg and power budget against array output."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 5.4))

    # --- (A) mass budget ---
    items = list(MASS_BUDGET) + [("Margin", m_margin), ("Propellant", M_PROP)]
    names = [n for n, _ in items][::-1]
    vals = [v for _, v in items][::-1]
    colors = (["#8E6FC7"] + ["#27AE60"]
              + ["#2E5E8C"] * len(MASS_BUDGET))[::-1]
    colors = ["#2E5E8C"] * len(MASS_BUDGET) + ["#27AE60", "#8E6FC7"]
    colors = colors[::-1]
    ypos = np.arange(len(names))
    ax1.barh(ypos, vals, color=colors, ec="0.3", lw=0.6)
    for y, v in zip(ypos, vals):
        ax1.text(v + 12, y, f"{v:,.0f}", va="center", fontsize=8)
    ax1.set_yticks(ypos)
    ax1.set_yticklabels(names, fontsize=8.5)
    ax1.set_xlim(0, max(vals) * 1.22)
    ax1.set_xlabel("Mass (kg)")
    ax1.set_title(f"(A) Mass budget: closes at {M_WET:,.0f} kg wet "
                  f"({M_DRY:,.0f} kg dry)", fontsize=10.5)
    ax1.grid(True, axis="x", alpha=0.3)
    ax1.text(0.97, 0.62, f"margin {100*m_margin/M_DRY:.0f}%\nof dry mass",
             transform=ax1.transAxes, ha="right", va="center", fontsize=8.5,
             bbox=dict(boxstyle="round,pad=0.3", fc="#EAF7EF", ec="#27AE60"))

    # --- (B) power budget ---
    labels = [n for n, _ in POWER_LOADS]
    vals_p = [v for _, v in POWER_LOADS]
    bottom = 0.0
    palette = ["#2E5E8C", "#3B82C4", "#7FB3D5", "#27AE60", "#E67E22",
               "#C0392B", "#8E6FC7"]
    for (lab, v), c in zip(POWER_LOADS, palette):
        ax2.bar([0], [v], 0.5, bottom=bottom, color=c, ec="0.3", lw=0.5,
                label=f"{lab} ({v:.0f} W)")
        bottom += v
    ax2.bar([1], [load_avg], 0.5, color="#95A5A6", ec="0.3", lw=0.5)
    ax2.text(1, load_avg + 40, f"{load_avg:,.0f} W", ha="center", fontsize=8.5)
    ax2.text(0, bottom + 40, f"{bottom:,.0f} W", ha="center", fontsize=8.5)
    ax2.axhline(p_bol, color="#1f4e79", ls="--", lw=1.6,
                label=f"array output BOL ({p_bol:,.0f} W)")
    ax2.axhline(p_eol, color="#C0392B", ls=":", lw=1.8,
                label=f"array output EOL ({p_eol:,.0f} W)")
    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(["Peak load\n(all loads on)", "Orbit-average\nload"],
                        fontsize=9)
    ax2.set_ylabel("Power (W)")
    ax2.set_ylim(0, p_bol * 1.30)
    ax2.set_title(f"(B) Power budget: {100*(p_eol-load_peak)/load_peak:.0f}% EOL "
                  f"margin on peak load", fontsize=10.5)
    ax2.grid(True, axis="y", alpha=0.3)
    ax2.legend(loc="upper right", fontsize=6.8, framealpha=0.94)

    _caption(fig, "Figure 5: Both budgets close with margin. The array is sized "
             "by the end-of-life case, not the beginning-of-life case.")
    fig.subplots_adjust(bottom=0.15, left=0.24, wspace=0.55, right=0.97)
    fig.savefig(FIG_DIR / "fig5_budgets.png", dpi=150)
    plt.close(fig)


def fig_deltav(dv_items, prop_by_clients, n_capacity) -> None:
    """Delta-v allocation and servicing capacity versus propellant load."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 5.0))

    names = [n for n, _ in dv_items][::-1]
    vals = [v for _, v in dv_items][::-1]
    ypos = np.arange(len(names))
    ax1.barh(ypos, vals, color="#2E5E8C", ec="0.3", lw=0.6)
    for y, v in zip(ypos, vals):
        ax1.text(v + max(vals) * 0.02, y, f"{v:,.0f}", va="center", fontsize=8.5)
    ax1.set_yticks(ypos)
    ax1.set_yticklabels(names, fontsize=8.5)
    ax1.set_xlim(0, max(vals) * 1.25)
    ax1.set_xlabel("Delta-v (m/s)")
    ax1.set_title(f"(A) Five-year delta-v allocation, "
                  f"{sum(v for _, v in dv_items):,.0f} m/s total", fontsize=10.5)
    ax1.grid(True, axis="x", alpha=0.3)

    n, ep, mono = prop_by_clients
    ax2.plot(n, 100.0 * ep / M_XENON, color="#2E5E8C", lw=2.2,
             label=f"xenon, {M_XENON:.0f} kg loaded")
    ax2.plot(n, 100.0 * mono / M_HYDRAZINE, color="#C0392B", lw=2.2,
             label=f"hydrazine, {M_HYDRAZINE:.0f} kg loaded")
    ax2.axhline(100.0, color="0.35", ls="--", lw=1.6, label="tank empty")
    ax2.axvline(N_CLIENTS_BASELINE, color="#27AE60", ls=":", lw=1.8,
                label=f"baseline manifest ({N_CLIENTS_BASELINE} clients)")
    ax2.axvspan(0, n_capacity, color="#27AE60", alpha=0.08)
    ax2.plot(n_capacity, 100.0, "o", color="#C0392B", ms=8, zorder=6)
    ax2.annotate(f"capacity {n_capacity:.1f} cycles,\nset by the hydrazine tank",
                 xy=(n_capacity, 100.0), xytext=(-12, -52),
                 textcoords="offset points", fontsize=8.5, ha="right",
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6"),
                 arrowprops=dict(arrowstyle="->", color="0.5"))
    ax2.set_xlabel("Client servicing cycles completed")
    ax2.set_ylabel("Fraction of tank consumed (%)")
    ax2.set_xlim(0, n.max())
    ax2.set_ylim(0, 175)
    ax2.set_title("(B) Servicing capacity, tank by tank", fontsize=10.5)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="upper left", fontsize=8)

    _caption(fig, "Figure 6: Propellant sizes the servicing capacity, not the "
             "calendar life. The baseline manifest leaves capacity in reserve.")
    fig.subplots_adjust(bottom=0.15, left=0.20, wspace=0.42, right=0.97)
    fig.savefig(FIG_DIR / "fig6_deltav_propellant.png", dpi=150)
    plt.close(fig)


def fig_thermal_balance(a_rad) -> None:
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
    _caption(fig, "Figure 7: Sizing the radiator is a trade between the sunlit "
             "and eclipse cases; heaters close the remaining eclipse gap.")
    fig.subplots_adjust(bottom=0.15)
    fig.savefig(FIG_DIR / "fig7_thermal_balance.png", dpi=150)
    plt.close(fig)


def fig_torques(ix, iy, iz, area_srp) -> None:
    alts = np.logspace(np.log10(200e3), np.log10(40000e3), 500)
    r = R_E_M + alts
    tg = torque_gravity_gradient(r, iz, iy)
    tm, _ = torque_magnetic(r)
    tsp = np.full_like(r, torque_srp(area_srp)[0])
    h_km = alts / 1000.0
    rho = np.maximum(rho_hw2(h_km), RHO_GEO)
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
    _caption(fig, "Figure 8: Torque magnitudes for the MESA geometry. Markers are "
             "the GEO operating point; SRP sets the ADACS design.")
    fig.subplots_adjust(bottom=0.14)
    fig.savefig(FIG_DIR / "fig8_disturbance_torques.png", dpi=150)
    plt.close(fig)


def fig_momentum(t_total, h_wheel_usable, h_capacity=200.0) -> None:
    dump_day = h_wheel_usable / (t_total * 86400.0)
    days = np.linspace(0, 60, 4000)
    h = np.mod(t_total * days * 86400.0, h_wheel_usable)
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
    _caption(fig, "Figure 9: SRP torque at GEO is secular, so the wheels ramp "
             "and must be desaturated with thrusters, not magnetorquers.")
    fig.subplots_adjust(bottom=0.16)
    fig.savefig(FIG_DIR / "fig9_momentum.png", dpi=150)
    plt.close(fig)


def fig_power(load_avg, load_peak) -> None:
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
    _caption(fig, "Figure 11: Single-axis tracking holds full output through the "
             "day; a body-fixed array would not, which is why the wings track.")
    fig.subplots_adjust(bottom=0.15)
    fig.savefig(FIG_DIR / "fig11_power_profile.png", dpi=150)
    plt.close(fig)


def fig_thermal_transient(a_rad, results) -> None:
    """Lumped-capacitance temperature through one eclipse, bus vs outboard zone."""
    t_h, bus, zone_off, zone_on, ecl, t_sun_eq, t_ecl_eq = results

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 5.0), sharex=True)
    t0 = (T_GEO / 2 - ecl / 2) / 3600.0
    t1 = (T_GEO / 2 + ecl / 2) / 3600.0

    for ax in (ax1, ax2):
        ax.axvspan(t0, t1, color="0.25", alpha=0.20)
        ax.set_xlim(8, 16)
        ax.set_xlabel("Time (hours from local noon)")
        ax.grid(True, alpha=0.3)

    ax1.plot(t_h, bus - 273.15, color="#C0392B", lw=2.2, label="bus, transient")
    ax1.axhline(t_sun_eq - 273.15, color="#E67E22", ls="--", lw=1.4,
                label=f"sunlit equilibrium ({t_sun_eq-273.15:+.1f} $^\\circ$C)")
    ax1.axhline(t_ecl_eq - 273.15, color="#2E5E8C", ls=":", lw=1.6,
                label=f"eclipse equilibrium ({t_ecl_eq-273.15:+.1f} $^\\circ$C)")
    drop = bus.max() - bus.min()
    ax1.annotate(f"actual excursion {drop:.1f} K,\nnot the "
                 f"{t_sun_eq-t_ecl_eq:.0f} K steady-state bound",
                 xy=(t1, bus.min() - 273.15), xytext=(13.0, 18.0),
                 fontsize=8.5, ha="left",
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.6"),
                 arrowprops=dict(arrowstyle="->", color="0.5"))
    ax1.set_ylabel("Temperature ($^\\circ$C)")
    ax1.set_ylim(-20, 45)
    ax1.set_title(f"(A) Bus lump, {M_BUS_THERMAL:,.0f} kg: thermal mass carries it "
                  f"through", fontsize=10.5)
    ax1.legend(loc="lower left", fontsize=8)

    ax2.plot(t_h, zone_off - 273.15, color="#C0392B", lw=2.2,
             label="propellant line zone, heater off")
    ax2.plot(t_h, zone_on - 273.15, color="#27AE60", lw=2.2,
             label=f"same zone, {P_ZONE_HEATER:.0f} W heater on thermostat")
    ax2.axhline(T_HYDRAZINE_FREEZE - 273.15, color="#C0392B", ls="--", lw=1.3,
                label="hydrazine freezing point (+2 $^\\circ$C)")
    ax2.axhline(T_ZONE_SETPOINT - 273.15, color="0.35", ls=":", lw=1.2,
                label=f"thermostat set point ({T_ZONE_SETPOINT-273.15:+.0f} "
                      f"$^\\circ$C)")
    ax2.annotate(f"{zone_off.min()-273.15:+.1f} $^\\circ$C without the heater,\n"
                 f"below the freezing point",
                 xy=(12.6, zone_off.min() - 273.15), xytext=(15.7, 11.0),
                 fontsize=8.5, ha="right",
                 bbox=dict(boxstyle="round,pad=0.3", fc="#FDECEA", ec="#C0392B"),
                 arrowprops=dict(arrowstyle="->", color="0.5"))
    ax2.set_ylim(-6, 44)
    ax2.set_ylabel("Temperature ($^\\circ$C)")
    ax2.set_title(f"(B) Outboard propellant line, {M_ZONE:.0f} kg: this is what "
                  f"needs heaters", fontsize=10.5)
    ax2.legend(loc="upper left", fontsize=7.4, framealpha=0.95)

    _caption(fig, "Figure 12: Transient simulation through the equinox eclipse. "
             "The bus barely moves; the low-mass outboard zones set the heater "
             "requirement.")
    fig.subplots_adjust(bottom=0.15, wspace=0.24)
    fig.savefig(FIG_DIR / "fig12_thermal_transient.png", dpi=150)
    plt.close(fig)


def fig_mmod() -> None:
    """Meteoroid flux and cumulative impact probability at GEO."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 5.0))

    m = np.logspace(-9, 1, 400)
    ax1.loglog(m, flux_at_orbit(m, H_GEO / 1000.0), color="#C0392B", lw=2.2,
               label="MESA at GEO")
    ax1.loglog(m, flux_at_orbit(m, 400.0), color="#2E5E8C", lw=1.8, ls="--",
               label="same vehicle at 400 km")
    ax1.loglog(m, grun_flux_interplanetary(m), color="0.45", lw=1.2, ls=":",
               label="unshielded interplanetary")
    for d_cm, lab in ((0.01, "0.1 mm"), (0.1, "1 mm"), (1.0, "1 cm")):
        mm = float(sphere_mass_g(d_cm))
        ax1.axvline(mm, color="0.75", lw=0.8)
        ax1.text(mm * 1.2, 2e-9, lab, rotation=90, fontsize=7.5, color="0.45",
                 va="bottom")
    ax1.set_xlabel("Particle mass (g)")
    ax1.set_ylabel("Cumulative flux (particles/m$^2$/yr)")
    ax1.set_ylim(1e-9, 1e5)
    ax1.set_title("(A) Grun sporadic meteoroid flux", fontsize=10.5)
    ax1.grid(True, which="both", alpha=0.25)
    ax1.legend(loc="upper right", fontsize=8)

    d = np.logspace(-2.3, 0.3, 300)          # cm
    mg = sphere_mass_g(d)
    f_geo = flux_at_orbit(mg, H_GEO / 1000.0)
    p5 = 1.0 - np.exp(-f_geo * A_MESA_MMOD * MISSION_YR)
    ax2.semilogx(d * 10.0, 100.0 * p5, color="#C0392B", lw=2.2)
    offsets = {0.1: (16, -30), 1.0: (12, 34), 5.0: (34, 16)}
    for d_mm, color in ((0.1, "#27AE60"), (1.0, "#E67E22"), (5.0, "#8E6FC7")):
        pv = 100.0 * (1.0 - np.exp(-float(flux_at_orbit(sphere_mass_g(d_mm / 10.0),
                      H_GEO / 1000.0)) * A_MESA_MMOD * MISSION_YR))
        ax2.plot(d_mm, pv, "o", color=color, ms=8, zorder=5)
        txt = f"{pv:.1f}%" if pv >= 1.0 else f"{pv:.3f}%"
        ax2.annotate(f"{d_mm:g} mm: {txt}", xy=(d_mm, pv),
                     xytext=offsets[d_mm], textcoords="offset points",
                     fontsize=8.5, ha="left",
                     bbox=dict(boxstyle="round,pad=0.28", fc="white", ec="0.6"),
                     arrowprops=dict(arrowstyle="->", color="0.5"))
    ax2.set_xlabel("Particle diameter (mm)")
    ax2.set_ylabel("Probability of at least one impact (%)")
    ax2.set_title(f"(B) Five years, {A_MESA_MMOD:.0f} m$^2$ exposed area",
                  fontsize=10.5)
    ax2.set_ylim(-8, 118)
    ax2.grid(True, which="both", alpha=0.25)

    _caption(fig, "Figure 16: Sub-millimetre impacts are certain and are designed "
             "around; the mission-ending sizes are rare enough to accept.")
    fig.subplots_adjust(bottom=0.15, wspace=0.28)
    fig.savefig(FIG_DIR / "fig16_mmod.png", dpi=150)
    plt.close(fig)


def fig_risk_matrix() -> None:
    """Five-by-five risk matrix, before and after the design mitigations."""
    fig, ax = plt.subplots(figsize=(8.4, 6.4))
    for i in range(1, 6):
        for j in range(1, 6):
            score = i * j
            if score >= 15:
                c = "#F5B7B1"
            elif score >= 8:
                c = "#FAE5B7"
            else:
                c = "#CFEBD8"
            ax.add_patch(mpatches.Rectangle((j - 0.5, i - 0.5), 1, 1, fc=c,
                         ec="white", lw=1.5))

    jitter = {}
    for name, l0, c0, l1, c1 in RISKS:
        for (ll, cc, color, marker) in ((l0, c0, "#C0392B", "o"),
                                        (l1, c1, "#1E7B45", "s")):
            k = (ll, cc)
            n = jitter.get(k, 0)
            jitter[k] = n + 1
            dx = -0.34 + 0.34 * (n % 2)
            dy = 0.28 - 0.28 * (n // 2)
            ax.plot(cc + dx, ll + dy, marker, color=color, ms=6, zorder=5)
            ax.text(cc + dx + 0.06, ll + dy, name.split()[0], fontsize=7.0,
                    va="center", color=color, zorder=6)
        ax.annotate("", xy=(c1, l1), xytext=(c0, l0),
                    arrowprops=dict(arrowstyle="->", color="0.45", lw=0.9,
                                    alpha=0.55, shrinkA=6, shrinkB=6))

    ax.plot([], [], "o", color="#C0392B", label="before mitigation")
    ax.plot([], [], "s", color="#1E7B45", label="after mitigation")
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 5.5)
    ax.set_xticks(range(1, 6))
    ax.set_yticks(range(1, 6))
    ax.set_xticklabels(["1 negligible", "2 minor", "3 moderate", "4 major",
                        "5 mission loss"], fontsize=8)
    ax.set_yticklabels(["1 remote", "2 unlikely", "3 possible", "4 likely",
                        "5 near certain"], fontsize=8)
    ax.set_xlabel("Consequence")
    ax.set_ylabel("Likelihood")
    ax.set_title("Section 13: MESA risk posture before and after mitigation",
                 fontsize=11)
    ax.legend(loc="upper left", fontsize=8.5, framealpha=0.95)
    _caption(fig, "Figure 17: Every mitigation in this report moves a specific "
             "risk down and to the left. Nothing remains in the red band.")
    fig.subplots_adjust(bottom=0.13)
    fig.savefig(FIG_DIR / "fig17_risk_matrix.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    FIG_DIR.mkdir(exist_ok=True)
    bar = "=" * 74

    # --- mass properties ---
    ix, iy, iz, d_wing = mesa_inertia()
    ix_mated, z_cm, m_mated = mated_inertia(ix)
    a_total, a_proj, a_nadir = bus_areas()
    area_srp = A_ARRAY + a_proj

    print(bar)
    print("SECTION 7  MESA VEHICLE DEFINITION")
    print(bar)
    print(f"  wet mass                    {M_WET:8.1f} kg  "
          f"(bus {M_BUS:.0f} kg + {N_WINGS} wings x {M_ARRAY_EACH:.0f} kg)")
    print(f"  bus envelope                {BUS_X} x {BUS_Y} x {BUS_Z} m")
    print(f"  array area (total)          {A_ARRAY:8.2f} m^2  "
          f"({N_WINGS} wings x {A_WING:.2f} m^2)")
    print(f"  bus radiating area          {a_total:8.2f} m^2")
    print(f"  bus sun-projected area      {a_proj:8.2f} m^2")
    print(f"  SRP reference area          {area_srp:8.2f} m^2  (arrays + bus)")
    print(f"  Ix, Iy, Iz (free flyer)     {ix:8.1f}  {iy:8.1f}  {iz:8.1f} kg*m^2")
    print(f"  |Iz - Iy|                   {abs(iz-iy):8.1f} kg*m^2")
    print(f"  Ix mated with {M_CLIENT:.0f} kg client {ix_mated:8.1f} kg*m^2 "
          f"({ix_mated/ix:.2f}x free flyer; cm shifts {z_cm:.2f} m)")

    # --- orbit and decay ---
    v_geo = np.sqrt(MU / R_GEO)
    print()
    print(bar)
    print("SECTION 3  ORBIT AND DRAG DECAY")
    print(bar)
    print(f"  GEO radius / velocity       {R_GEO/1e3:8.1f} km, {v_geo:.1f} m/s")
    for h in (300.0, 400.0, 500.0, 600.0):
        dl = drag_lifetime_days(h)
        print(f"  LEO decay from {h:5.0f} km      {dl:8.1f} days ({dl/365.25:.2f} yr)")

    # --- thermal, steady state ---
    a_rad = round(size_radiator(), 1)
    t_sun, t_ecl, q_sun, q_earth, eps_a = equilibrium_temps(a_rad)
    q_ir, q_alb = earth_fluxes()
    p_heat = heater_power(a_rad)

    print()
    print(bar)
    print("SECTION 8  THERMAL CONTROL, STEADY STATE (Pisacane Ch. 12)")
    print(bar)
    print(f"  Earth IR / albedo at GEO    {q_ir:8.2f} / {q_alb:.2f} W/m^2")
    print(f"  absorbed solar (sun case)   {q_sun:8.1f} W")
    print(f"  absorbed Earth IR + albedo  {q_earth:8.2f} W  "
          f"({100*q_earth/(q_sun+Q_INT):.2f}% of the rest)")
    print(f"  radiator area (to {T_SUN_TARGET:.0f} K)     {a_rad:8.2f} m^2 OSR")
    print(f"  effective emitting area     {eps_a:8.3f} m^2")
    print(f"  >> T_sun                    {t_sun:8.2f} K = {t_sun-273.15:+7.2f} C")
    print(f"  >> T_eclipse                {t_ecl:8.2f} K = {t_ecl-273.15:+7.2f} C")
    print(f"  temperature swing           {t_sun-t_ecl:8.2f} K")
    print(f"  heater power to hold 0 C    {p_heat:8.1f} W")

    # --- thermal, transient (new) ---
    ecl = eclipse_duration()
    t_s = np.arange(0.0, T_GEO, 5.0)
    t_h = t_s / 3600.0
    in_ecl = np.abs(t_s - T_GEO / 2.0) <= ecl / 2.0

    def q_sun_bus(tt):
        return 0.0 if abs(tt - T_GEO / 2.0) <= ecl / 2.0 else q_sun

    def q_sun_zone(tt):
        return (0.0 if abs(tt - T_GEO / 2.0) <= ecl / 2.0
                else ALPHA_ZONE * S_SOLAR * A_ZONE_PROJ)

    c_bus = M_BUS_THERMAL * CP_AL
    bus = transient_temperature(t_s, t_sun, c_bus, q_sun_bus, Q_INT, eps_a)

    c_zone = M_ZONE * CP_AL
    eps_a_zone = EPS_ZONE * A_ZONE
    t_zone0 = ((ALPHA_ZONE * S_SOLAR * A_ZONE_PROJ + Q_ZONE_INT)
               / (SIGMA * eps_a_zone)) ** 0.25
    zone_off = transient_temperature(t_s, t_zone0, c_zone, q_sun_zone,
                                     Q_ZONE_INT, eps_a_zone)
    zone_on = transient_temperature(t_s, t_zone0, c_zone, q_sun_zone,
                                    Q_ZONE_INT, eps_a_zone,
                                    heater=P_ZONE_HEATER,
                                    setpoint=T_ZONE_SETPOINT)
    q_zone_hold = SIGMA * eps_a_zone * T_ZONE_SETPOINT ** 4

    print()
    print(bar)
    print("SECTION 12  THERMAL TRANSIENT THROUGH ECLIPSE (lumped capacitance)")
    print(bar)
    print(f"  bus thermal capacitance     {c_bus:8.3e} J/K "
          f"({M_BUS_THERMAL:.0f} kg at {CP_AL:.0f} J/kg/K)")
    print(f"  bus radiative conductance   {4*SIGMA*eps_a*t_sun**3:8.2f} W/K at T_sun")
    print(f"  bus time constant           {c_bus/(4*SIGMA*eps_a*t_sun**3)/3600:8.2f} h "
          f"vs a {ecl/3600:.2f} h eclipse")
    print(f"  >> bus drop through eclipse {bus.max()-bus.min():8.2f} K  "
          f"(min {bus.min()-273.15:+.1f} C, steady-state bound "
          f"{t_ecl-273.15:+.1f} C)")
    print(f"  propellant line zone        {M_ZONE:.0f} kg, eps*A = "
          f"{eps_a_zone:.3f} m^2, tau = "
          f"{c_zone/(4*SIGMA*eps_a_zone*t_zone0**3)/3600:.2f} h")
    print(f"    sunlit equilibrium        {t_zone0-273.15:+7.1f} C")
    print(f"    heater off, eclipse min   {zone_off.min()-273.15:+7.1f} C "
          f"(hydrazine freezes at +2.0 C)")
    print(f"    steady power to hold {T_ZONE_SETPOINT-273.15:+.0f} C  "
          f"{q_zone_hold:6.1f} W -> {P_ZONE_HEATER:.0f} W heater")
    print(f"    heater on, eclipse min    {zone_on.min()-273.15:+7.1f} C")

    # --- disturbance torques ---
    d = torque_summary(R_GEO, ix, iy, iz, area_srp)
    _, f_srp = torque_srp(area_srp)
    _, f_aero, _ = torque_aero(R_GEO, area_srp)

    print()
    print(bar)
    print("SECTION 11  DISTURBANCE TORQUES AT GEO (SMAD Table 11.10)")
    print(bar)
    print(f"  Earth field B at GEO        {d['B']:8.3e} T")
    print(f"  SRP force / aero force      {f_srp:8.3e} / {f_aero:.3e} N")
    for k in ("solar radiation", "gravity gradient", "magnetic", "aerodynamic"):
        print(f"  {k:24s}    {d[k]:8.3e} N*m   "
              f"({100*d[k]/d['total']:5.2f}% of total)")
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
    m_required = max(m_slew_free, m_slew_mated, d["total"]) * 2.0

    h_usable = 50.0
    n_wheels = 4
    m_wheel, p_wheel = 25.0, 100.0        # Lesson 7 Part 2 slide 11, large sats
    dump_days = h_usable / h_secular_day
    n_dumps = MISSION_YR * 365.25 / dump_days
    impulse_per_dump = 2.0 * h_usable / DOCK_ARM      # torque couple
    m_dump_prop = n_dumps * impulse_per_dump / (ISP_MONO * G0)

    print()
    print(bar)
    print("SECTION 11  ACTUATOR SIZING (SMAD Table 11.7; Lesson 7 Pt 2 slide 11)")
    print(bar)
    print(f"  30 deg slew, free flyer     {m_slew_free:8.4f} N*m, "
          f"H = {h_slew_free:6.2f} N*m*s")
    print(f"  30 deg slew, mated          {m_slew_mated:8.4f} N*m, "
          f"H = {h_slew_mated:6.2f} N*m*s")
    print(f"  cyclic H = 0.707 T_D (P/4)  {h_cyclic:8.4f} N*m*s")
    print(f"  secular H per day           {h_secular_day:8.3f} N*m*s/day")
    print(f"  >> wheel torque, 100% margin{m_required:8.4f} N*m -> large-sat row")
    print(f"  >> {n_wheels} wheels                 {n_wheels*m_wheel:8.1f} kg, "
          f"{n_wheels*p_wheel:.0f} W peak")
    print(f"  >> dump cadence             {dump_days:8.1f} days, "
          f"{n_dumps:.0f} dumps in {MISSION_YR:.0f} yr")
    print(f"  >> momentum-dump propellant {m_dump_prop:8.2f} kg hydrazine")

    sensors = [("2 star trackers", 10.0, 36.0), ("2 IMUs (1 active)", 10.0, 30.0),
               ("4 coarse sun sensors", 4.0, 12.0),
               ("ADACS control electronics", 8.0, 25.0),
               ("RPO LIDAR and cameras", 25.0, 60.0)]
    m_ad = n_wheels * m_wheel + sum(s[1] for s in sensors)
    p_ad = 120.0 + sum(s[2] for s in sensors)
    print(f"  >> ADACS total              {m_ad:8.1f} kg ({100*m_ad/M_WET:.1f}% of "
          f"wet mass), {p_ad:.0f} W orbit-average")

    # --- power ---
    p_bol, p_eol = array_power(True), array_power(False)
    load_peak = sum(v for _, v in POWER_LOADS)
    load_avg = Q_INT
    years_to_limit = np.log(load_peak / p_bol) / np.log(1.0 - DEGRADE_PER_YR)
    e_eclipse = load_peak * ecl / 3600.0
    e_battery = e_eclipse / (DOD * ETA_LINE)
    m_cells = e_battery / E_DENS_CELL
    m_battery = m_cells * PACK_OVERHEAD

    print()
    print(bar)
    print("SECTION 12  POWER, BATTERY AND MISSION LIFE")
    print(bar)
    for name, w in POWER_LOADS:
        print(f"    {name:42s} {w:7.0f} W")
    print(f"    {'peak load':42s} {load_peak:7.0f} W")
    print(f"    {'orbit-average load':42s} {load_avg:7.0f} W")
    print(f"  array BOL / EOL output      {p_bol:8.0f} / {p_eol:.0f} W  "
          f"({100*p_eol/p_bol:.1f}% of BOL)")
    print(f"  EOL margin over peak load   {100*(p_eol-load_peak)/load_peak:8.1f}%")
    print(f"  max eclipse at equinox      {ecl/60:8.1f} min")
    print(f"  eclipse energy at peak load {e_eclipse:8.0f} W*h")
    print(f"  battery capacity needed     {e_battery:8.0f} W*h at "
          f"{100*DOD:.0f}% DoD, {100*ETA_LINE:.0f}% line")
    print(f"  >> installed battery mass   {m_battery:8.1f} kg "
          f"({m_cells:.1f} kg of cells x {PACK_OVERHEAD:.1f})")
    print(f"  power-limited life          {years_to_limit:8.1f} yr")

    # --- radiation ---
    tid_per_yr = 5.0
    tid_mission = tid_per_yr * MISSION_YR
    a_avionics = 6.0 * 0.6 ** 2
    m_shield = a_avionics * 0.00254 * 2700.0
    print()
    print(bar)
    print("SECTION 10  RADIATION (Pisacane Tables 9.6, 9.9)")
    print(bar)
    print(f"  assumed TID behind 100 mil Al {tid_per_yr:6.1f} krad(Si)/yr")
    print(f"  {MISSION_YR:.0f}-year mission TID         {tid_mission:8.1f} krad(Si)")
    print(f"  with 2x rad-hard margin     {2*tid_mission:8.1f} krad(Si) "
          f"-> RHA category R (100 krad(Si))")
    print(f"  shield mass, 100 mil over a 0.6 m avionics cube: "
          f"{m_shield:.1f} kg over {a_avionics:.2f} m^2")
    print(f"  array degradation           {100*DEGRADE_PER_YR:8.1f} %/yr -> "
          f"{100*(1-(1-DEGRADE_PER_YR)**MISSION_YR):.1f}% over {MISSION_YR:.0f} yr")

    # --- mass, delta-v, propellant and cost budgets ---
    m_subsystems = sum(v for _, v in MASS_BUDGET)
    m_margin = M_DRY - m_subsystems

    dv1, dv2, dv_grave = hohmann_dv(R_GEO, R_GEO + H_GRAVEYARD)
    dv_reloc = relocation_dv(1.0)

    dv_sk_mated = DV_SK_PER_YR * MISSION_YR * MATED_FRACTION
    dv_sk_free = DV_SK_PER_YR * MISSION_YR * (1.0 - MATED_FRACTION)
    dv_tow_total = 2.0 * dv_grave * N_CLIENTS_BASELINE
    dv_reloc_total = dv_reloc * N_CLIENTS_BASELINE
    dv_rpo_total = DV_RPO_PER_CLIENT * N_CLIENTS_BASELINE

    dv_items = [
        ("Mated stationkeeping (4 yr, stack)", dv_sk_mated),
        ("Free-flight stationkeeping (1 yr)", dv_sk_free),
        (f"Graveyard tows ({N_CLIENTS_BASELINE} round trips)", dv_tow_total),
        (f"Longitude relocations ({N_CLIENTS_BASELINE})", dv_reloc_total),
        (f"RPO, approach and backout ({N_CLIENTS_BASELINE})", dv_rpo_total),
    ]
    dv_total = sum(v for _, v in dv_items)

    m_stack = M_WET + M_CLIENT
    p_sk_mated = prop_mass(m_stack, dv_sk_mated, ISP_EP)
    p_sk_free = prop_mass(M_WET, dv_sk_free, ISP_EP)
    p_tow = prop_mass(m_stack, dv_tow_total, ISP_EP)
    p_reloc = prop_mass(M_WET, dv_reloc_total, ISP_EP)
    p_rpo = prop_mass(M_WET, dv_rpo_total, ISP_MONO)
    p_ep_total = p_sk_mated + p_sk_free + p_tow + p_reloc
    p_mono_total = p_rpo + m_dump_prop

    # Per-client marginal propellant per system, used for the capacity curve.
    # The two tanks are sized separately, so capacity is set by whichever runs
    # dry first, not by the combined 600 kg.
    per_client_ep = (p_sk_mated + p_tow + p_reloc) / N_CLIENTS_BASELINE
    per_client_mono = p_rpo / N_CLIENTS_BASELINE
    n_axis = np.linspace(0, 30, 600)
    ep_curve = p_sk_free + n_axis * per_client_ep
    mono_curve = m_dump_prop + n_axis * per_client_mono
    n_cap_ep = (M_XENON - p_sk_free) / per_client_ep
    n_cap_mono = (M_HYDRAZINE - m_dump_prop) / per_client_mono
    n_capacity = min(n_cap_ep, n_cap_mono)

    duty = (m_stack * DV_SK_PER_YR / 365.25) / (THRUST_EP * 86400.0)

    print()
    print(bar)
    print("SECTION 7  MASS, DELTA-V, PROPELLANT AND COST BUDGETS")
    print(bar)
    for name, v in MASS_BUDGET:
        print(f"    {name:44s} {v:7.1f} kg")
    print(f"    {'margin':44s} {m_margin:7.1f} kg "
          f"({100*m_margin/M_DRY:.1f}% of dry)")
    print(f"    {'dry mass':44s} {M_DRY:7.1f} kg")
    print(f"    {'propellant':44s} {M_PROP:7.1f} kg")
    print(f"    {'wet mass':44s} {M_WET:7.1f} kg")
    print()
    print(f"  graveyard Hohmann (+{H_GRAVEYARD/1e3:.0f} km)  "
          f"{dv1:.2f} + {dv2:.2f} = {dv_grave:.2f} m/s each way")
    print(f"  relocation at 1 deg/day     {dv_reloc:8.2f} m/s per repositioning")
    for name, v in dv_items:
        print(f"    {name:44s} {v:7.1f} m/s")
    print(f"    {'TOTAL five-year delta-v':44s} {dv_total:7.1f} m/s")
    print()
    print(f"    {'mated stationkeeping + tows (Xe, 5,000 kg)':44s} "
          f"{p_sk_mated+p_tow:7.1f} kg")
    print(f"    {'free-flight SK + relocations (Xe, 2,000 kg)':44s} "
          f"{p_sk_free+p_reloc:7.1f} kg")
    print(f"    {'RPO approach and backout (N2H4, 2,000 kg)':44s} {p_rpo:7.1f} kg")
    print(f"    {'momentum dumping (N2H4)':44s} {m_dump_prop:7.1f} kg")
    print(f"  xenon consumed / loaded     {p_ep_total:8.1f} / {M_XENON:.0f} kg "
          f"({100*(M_XENON-p_ep_total)/M_XENON:.0f}% reserve)")
    print(f"  hydrazine consumed / loaded {p_mono_total:8.1f} / {M_HYDRAZINE:.0f} kg "
          f"({100*(M_HYDRAZINE-p_mono_total)/M_HYDRAZINE:.0f}% reserve)")
    print(f"  TOTAL propellant consumed   {p_ep_total+p_mono_total:8.1f} kg of "
          f"{M_PROP:.0f} kg loaded")
    print(f"  >> capacity, xenon-limited      {n_cap_ep:8.1f} client cycles")
    print(f"  >> capacity, hydrazine-limited  {n_cap_mono:8.1f} client cycles "
          f"<-- binding")
    print(f"  >> servicing capacity       {n_capacity:8.1f} client cycles "
          f"(baseline manifest is {N_CLIENTS_BASELINE})")
    print(f"  EP duty cycle for mated SK  {100*duty:8.1f}% of each day "
          f"({24*duty:.1f} h/day at {THRUST_EP*1000:.0f} mN)")
    print()
    cost_total = sum(v for _, v in COST_BUDGET)
    for name, v in COST_BUDGET:
        print(f"    {name:44s} ${v:6.1f}M")
    print(f"    {'TOTAL':44s} ${cost_total:6.1f}M")

    # --- MMOD ---
    r_geo_km = R_GEO / 1000.0
    chi_geo = shielding_factor(r_geo_km)
    g_geo = focusing_factor(r_geo_km)
    print()
    print(bar)
    print("SECTION 13  MICROMETEOROIDS AND DEBRIS (Lesson 12; Pisacane Ch. 11)")
    print(bar)
    print(f"  GEO: chi = {chi_geo:.4f}, G = {g_geo:.4f}, chi*G = {chi_geo*g_geo:.4f}")
    r_leo = R_E_KM + 400.0
    print(f"  400 km: chi = {shielding_factor(r_leo):.4f}, "
          f"G = {focusing_factor(r_leo):.4f}, "
          f"chi*G = {shielding_factor(r_leo)*focusing_factor(r_leo):.4f}")
    print(f"  exposed area used           {A_MESA_MMOD:8.1f} m^2")
    for d_mm in (0.1, 1.0, 5.0, 10.0):
        mg = float(sphere_mass_g(d_mm / 10.0))
        f = float(flux_at_orbit(mg, H_GEO / 1000.0))
        lam = f * A_MESA_MMOD
        p = 1.0 - np.exp(-lam * MISSION_YR)
        mtbi = np.inf if lam == 0 else 1.0 / lam
        print(f"  d = {d_mm:5.1f} mm (m = {mg:9.3e} g): F = {f:9.3e} /m^2/yr, "
              f"P(5 yr) = {100*p:8.4f}%, mean interval {mtbi:10.3e} yr")
    t_b, t_w = whipple_thickness(10.0, 0.3, RHO_METEOROID, V_METEOROID, 35.0,
                                 2.7, 2.7)
    print(f"  Whipple shield for a 0.3 cm meteoroid at {V_METEOROID:.0f} km/s, "
          f"S = 10 cm:")
    print(f"    bumper t_b = {float(t_b):.3f} cm, rear wall t_w = {float(t_w):.3f} cm")

    # --- figures ---
    fig_concept()
    fig_conops()
    fig_orbit_regimes()
    fig_drag_lifetime()
    fig_configuration(ix, iy, iz, a_rad)
    fig_budgets(m_margin, load_peak, load_avg, p_bol, p_eol)
    fig_deltav(dv_items, (n_axis, ep_curve, mono_curve), n_capacity)
    fig_thermal_balance(a_rad)
    fig_torques(ix, iy, iz, area_srp)
    fig_momentum(d["total"], h_usable)
    fig_orbit_3d()
    fig_power(load_avg, load_peak)
    fig_thermal_transient(a_rad, (t_h, bus, zone_off, zone_on, ecl,
                                    t_sun, t_ecl))
    fig_mmod()
    fig_risk_matrix()
    print()
    print("Figures written to:", FIG_DIR)


if __name__ == "__main__":
    main()
