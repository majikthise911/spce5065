"""SPCE 5065 HW1 -- Socratic walkthrough figures (dark theme).

Generates four high-impact learning figures:
  walkthrough_fig1_thread.png        -- Newton's gravitation fanning into the problems
  walkthrough_fig2_v_and_T.png       -- velocity & period vs altitude (2-panel)
  walkthrough_fig3_irradiance.png    -- irradiance vs day-of-year + per-planet log (2-panel)
  walkthrough_fig4_hidden_mass.png   -- "weigh a hidden body" schematic tying Q7 & Q8

Run:  python walkthrough_figs.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Ellipse
import numpy as np

# --- dark theme palette ---
BG = "#0D1117"
TXT = "#E6EDF3"
GREEN = "#3FB950"
RED = "#F85149"
BLUE = "#58A6FF"
PURPLE = "#D2A8FF"
ORANGE = "#FFA657"
GRID = "#30363D"

FIG_DIR = Path(__file__).parent

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "savefig.facecolor": BG,
    "text.color": TXT,
    "axes.labelcolor": TXT,
    "axes.edgecolor": GRID,
    "xtick.color": TXT,
    "ytick.color": TXT,
    "axes.titlecolor": TXT,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "grid.color": GRID,
})

# --- physics constants (mirror the solution script) ---
MU_EARTH = 398600.5
R_E = 6378.0
S_E = 1366.1
E_EARTH = 0.016710


def orbital_velocity(h):
    return np.sqrt(MU_EARTH / (R_E + h))


def orbital_period(h):
    return 2.0 * np.pi * np.sqrt((R_E + h) ** 3 / MU_EARTH)


def earth_sun_distance_by_day(doy, e=E_EARTH, day_perihelion=3.0):
    M = 2 * np.pi * (doy - day_perihelion) / 365.25
    E = M.copy().astype(float)
    for _ in range(50):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return 1.0 * (1 - e * np.cos(E))


# ==========================================================================
# Figure 1 -- the thread: Newton's gravitation fanning into the problems
# ==========================================================================
def fig_thread():
    fig, ax = plt.subplots(figsize=(9.5, 6.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # central root box
    root = FancyBboxPatch((3.4, 8.1), 3.2, 1.1, boxstyle="round,pad=0.1",
                          fc="#161B22", ec=PURPLE, lw=2)
    ax.add_patch(root)
    ax.text(5.0, 8.85, "Newton's law of gravitation", ha="center",
            va="center", fontsize=11, fontweight="bold", color=PURPLE)
    ax.text(5.0, 8.4, r"$F = G\,M m / r^2$", ha="center", va="center",
            fontsize=10, color=TXT)

    # two trunks
    ax.text(2.7, 6.95, "set gravity = centripetal pull",
            ha="center", fontsize=8.5, color=BLUE, style="italic")
    ax.text(7.3, 6.95, "invert a known orbit law for the central mass",
            ha="center", fontsize=8.5, color=ORANGE, style="italic")

    leaves = [
        # x, y, color, title, subtitle
        (1.6, 5.3, BLUE, "Q2  v & T", "circular orbit\nvs altitude"),
        (3.7, 5.3, BLUE, "Q6  S(r)", "inverse-square\nirradiance"),
        (6.3, 5.3, ORANGE, "Q7  Kepler III", "Saturn mass\nfrom Titan"),
        (8.4, 5.3, ORANGE, "Q8  vis-viva", "asteroid mass\nfrom one state"),
    ]
    for x, y, col, title, sub in leaves:
        box = FancyBboxPatch((x - 0.95, y - 0.7), 1.9, 1.4,
                             boxstyle="round,pad=0.08", fc="#161B22",
                             ec=col, lw=1.8)
        ax.add_patch(box)
        ax.text(x, y + 0.35, title, ha="center", va="center",
                fontsize=9.5, fontweight="bold", color=col)
        ax.text(x, y - 0.25, sub, ha="center", va="center",
                fontsize=7.8, color=TXT)
        # arrow from root
        ax.add_patch(FancyArrowPatch((5.0, 8.05), (x, y + 0.75),
                     arrowstyle="-|>", mutation_scale=12,
                     color=GRID, lw=1.3, connectionstyle="arc3,rad=0.05"))

    # conceptual band at the bottom
    band = FancyBboxPatch((0.6, 1.7), 8.8, 2.0, boxstyle="round,pad=0.1",
                          fc="#10161D", ec=GREEN, lw=1.5)
    ax.add_patch(band)
    ax.text(5.0, 3.35, "Conceptual half -- the same environment, in words",
            ha="center", fontsize=9.5, fontweight="bold", color=GREEN)
    concepts = [
        ("Q1", "GEO charging\nanomaly (Galaxy 15)"),
        ("Q3", "800 km lifetime\nvs solar cycle"),
        ("Q4", "350 km optical-EO\nhazards"),
        ("Q5", "geomagnetic drift\n& reversals"),
    ]
    cx = [1.8, 3.85, 6.0, 8.1]
    for (q, txt), x in zip(concepts, cx):
        ax.text(x, 2.55, q, ha="center", fontsize=9, fontweight="bold",
                color=GREEN)
        ax.text(x, 2.1, txt, ha="center", fontsize=7.5, color=TXT)

    ax.text(5.0, 0.85,
            "One inverse-square force sets every orbit number; one space "
            "environment drives every anomaly.",
            ha="center", fontsize=8.6, style="italic", color="#9DA7B3")
    ax.set_title("The thread: one law of gravity fans out into eight problems",
                 fontsize=12.5, fontweight="bold", pad=14)
    fig.savefig(FIG_DIR / "walkthrough_fig1_thread.png", dpi=200,
                bbox_inches="tight")
    plt.close(fig)


# ==========================================================================
# Figure 2 -- velocity & period vs altitude (2-panel)
# ==========================================================================
def fig_v_and_T():
    h = np.linspace(0, 36000, 700)
    v = orbital_velocity(h)
    T = orbital_period(h) / 60.0

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))

    marks = [(400, "LEO"), (800, "800 km"), (20200, "GPS"), (35786, "GEO")]
    # staggered label offsets (dx, dy, ha) to keep the low-altitude
    # cluster (LEO + 800 km) from colliding
    v_off = {400: (40, 34, "left"), 800: (60, -30, "left"),
             20200: (12, 16, "left"), 35786: (-12, 18, "right")}
    T_off = {400: (50, -34, "left"), 800: (60, 14, "left"),
             20200: (-14, 14, "right"), 35786: (-14, 14, "right")}

    ax1.plot(h, v, color=BLUE, lw=2.2)
    for hm, lab in marks:
        dx, dy, ha = v_off[hm]
        ax1.plot(hm, orbital_velocity(hm), "o", color=PURPLE, ms=6)
        ax1.annotate(f"{lab}\n{orbital_velocity(hm):.2f} km/s",
                     xy=(hm, orbital_velocity(hm)), xytext=(dx, dy),
                     textcoords="offset points", fontsize=8, color=TXT,
                     ha=ha,
                     arrowprops=dict(arrowstyle="->", color=GRID))
    ax1.set_xlabel("Altitude  h  (km)")
    ax1.set_ylabel("Circular velocity  v  (km/s)")
    ax1.set_title(r"$v=\sqrt{\mu/(R_E+h)}$  -- falls as $1/\sqrt{r}$",
                  fontsize=10.5)
    ax1.grid(True, alpha=0.3)

    ax2.plot(h, T, color=ORANGE, lw=2.2)
    for hm, lab in marks:
        dx, dy, ha = T_off[hm]
        ax2.plot(hm, orbital_period(hm) / 60, "o", color=PURPLE, ms=6)
        ax2.annotate(f"{lab}\n{orbital_period(hm)/60:.0f} min",
                     xy=(hm, orbital_period(hm) / 60), xytext=(dx, dy),
                     textcoords="offset points", fontsize=8, color=TXT,
                     ha=ha,
                     arrowprops=dict(arrowstyle="->", color=GRID))
    ax2.set_xlabel("Altitude  h  (km)")
    ax2.set_ylabel("Orbital period  T  (min)")
    ax2.set_title(r"$T=2\pi\sqrt{(R_E+h)^3/\mu}$  -- climbs as $r^{3/2}$",
                  fontsize=10.5)
    ax2.grid(True, alpha=0.3)

    fig.suptitle("Q2: Higher = slower but takes longer "
                 "(velocity sags gently, period explodes)",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(FIG_DIR / "walkthrough_fig2_v_and_T.png", dpi=200)
    plt.close(fig)


# ==========================================================================
# Figure 3 -- irradiance vs day-of-year + per-planet log (2-panel)
# ==========================================================================
def fig_irradiance():
    planets = {
        "Mercury": (0.38710, 0.20563),
        "Venus": (0.72333, 0.00677),
        "Earth": (1.00000, 0.01671),
        "Mars": (1.52371, 0.09339),
        "Jupiter": (5.20289, 0.04839),
        "Saturn": (9.53707, 0.05386),
        "Uranus": (19.18914, 0.04726),
        "Neptune": (30.06992, 0.00859),
    }

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.9))

    # --- left: irradiance vs day of year ---
    doy = np.arange(1, 366)
    r_au = earth_sun_distance_by_day(doy)
    S = S_E * (1.0 / r_au) ** 2
    ax1.plot(doy, S, color=ORANGE, lw=2.2)
    i_max, i_min = int(np.argmax(S)), int(np.argmin(S))
    ax1.plot(doy[i_max], S[i_max], "o", color=RED, ms=7)
    ax1.plot(doy[i_min], S[i_min], "o", color=BLUE, ms=7)
    ax1.annotate(f"closest (~Jan {doy[i_max]})\n{S[i_max]:.0f} W/m$^2$",
                 xy=(doy[i_max], S[i_max]), xytext=(28, -4),
                 textcoords="offset points", fontsize=8, color=TXT,
                 arrowprops=dict(arrowstyle="->", color=GRID))
    ax1.annotate(f"farthest (~Jul {doy[i_min]-181})\n{S[i_min]:.0f} W/m$^2$",
                 xy=(doy[i_min], S[i_min]), xytext=(-20, 16),
                 textcoords="offset points", fontsize=8, color=TXT,
                 arrowprops=dict(arrowstyle="->", color=GRID))
    ax1.axhline(S_E, color=GREEN, ls="--", lw=1.2)
    ax1.text(120, S_E + 1.5, r"$S_e=1366.1$ W/m$^2$ (mean)", fontsize=8,
             color=GREEN)
    ax1.set_xlabel("Day of year")
    ax1.set_ylabel("Irradiance at Earth  S  (W/m$^2$)")
    ax1.set_title("Q6c: A 3.4% annual breathing\n(closest in Jan, not summer)",
                  fontsize=10)
    ax1.grid(True, alpha=0.3)

    # --- right: per-planet log ---
    names = list(planets.keys())
    a = np.array([planets[n][0] for n in names])
    e = np.array([planets[n][1] for n in names])
    s_avg = S_E / a ** 2
    s_max = S_E / (a * (1 - e)) ** 2
    s_min = S_E / (a * (1 + e)) ** 2
    x = np.arange(len(names))
    yerr = np.vstack([s_avg - s_min, s_max - s_avg])
    ax2.errorbar(x, s_avg, yerr=yerr, fmt="o", color=PURPLE,
                 ecolor=RED, elinewidth=1.6, capsize=5, ms=7,
                 label="mean (bar = min..max)")
    ax2.set_yscale("log")
    ax2.set_xticks(x)
    ax2.set_xticklabels(names, rotation=30, ha="right", fontsize=8.5)
    for xi, s in zip(x, s_avg):
        ax2.annotate(f"{s:.1f}", xy=(xi, s), xytext=(9, 2),
                     textcoords="offset points", fontsize=7.5, va="center",
                     color=TXT)
    ax2.set_ylabel("Irradiance  S  (W/m$^2$, log)")
    ax2.set_title("Q6d: Mercury to Neptune ~ 4 orders of magnitude\n"
                  "(Mercury widest bar, Venus near-flat)", fontsize=10)
    ax2.grid(True, which="both", alpha=0.25)
    ax2.legend(fontsize=8, facecolor="#161B22", edgecolor=GRID,
               labelcolor=TXT)

    fig.suptitle("Q6: Inverse-square geometry sets brightness everywhere",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(FIG_DIR / "walkthrough_fig3_irradiance.png", dpi=200)
    plt.close(fig)


# ==========================================================================
# Figure 4 -- "weigh a hidden body" schematic (Q7 Kepler III & Q8 vis-viva)
# ==========================================================================
def fig_hidden_mass():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.0))
    for ax in (ax1, ax2):
        ax.set_aspect("equal")
        ax.axis("off")

    # --- left panel: Q7 Kepler III (period of a full orbit) ---
    ax1.set_xlim(-1.4, 1.4)
    ax1.set_ylim(-1.5, 1.55)
    a_e = 1.0
    ell = Ellipse((0, 0), 2 * a_e, 2 * 0.92, fill=False, ec=ORANGE, lw=1.8)
    ax1.add_patch(ell)
    central = Circle((0.0, 0.0), 0.18, fc=PURPLE, ec="none")
    ax1.add_patch(central)
    ax1.text(0, -0.02, "Saturn\n(unknown M)", ha="center", va="center",
             fontsize=8, color=BG, fontweight="bold")
    moon = Circle((a_e, 0.0), 0.07, fc=BLUE, ec="none")
    ax1.add_patch(moon)
    ax1.text(a_e + 0.02, 0.2, "Titan", ha="center", fontsize=8, color=BLUE)
    # period arrow around
    ax1.add_patch(FancyArrowPatch((0.0, 0.92), (-0.55, 0.74),
                  connectionstyle="arc3,rad=0.4", arrowstyle="-|>",
                  mutation_scale=13, color=GREEN, lw=1.6))
    ax1.text(0.0, 1.18, "measure ONE full lap (period T)\n"
             "and the loop size a",
             ha="center", fontsize=8.5, color=GREEN)
    ax1.text(0, -1.32, r"$M = \dfrac{4\pi^2 a^3}{G\,T^2}$",
             ha="center", fontsize=12, color=ORANGE)
    ax1.set_title("Q7 -- Kepler III: time a full orbit",
                  fontsize=10.5, fontweight="bold")

    # --- right panel: Q8 vis-viva (one snapshot: r and v) ---
    ax2.set_xlim(-1.4, 1.7)
    ax2.set_ylim(-1.5, 1.55)
    ell2 = Ellipse((0.35, 0), 2 * 1.0, 2 * 0.7, fill=False, ec=ORANGE,
                   lw=1.8)
    ax2.add_patch(ell2)
    ast = Circle((0.0, 0.0), 0.13, fc=PURPLE, ec="none")
    ax2.add_patch(ast)
    ax2.text(0.0, -0.32, "asteroid\n(unknown M)", ha="center", va="top",
             fontsize=8, color=PURPLE)
    # spacecraft at r
    sc = (1.25, 0.42)
    ax2.add_patch(Circle(sc, 0.05, fc=BLUE, ec="none"))
    # r vector
    ax2.add_patch(FancyArrowPatch((0.0, 0.0), sc, arrowstyle="-|>",
                  mutation_scale=12, color=BLUE, lw=1.5))
    ax2.text(0.62, 0.32, "r = 1500 km", fontsize=8.5, color=BLUE,
             rotation=18)
    # v vector (tangent-ish)
    ax2.add_patch(FancyArrowPatch(sc, (sc[0] - 0.15, sc[1] + 0.55),
                  arrowstyle="-|>", mutation_scale=12, color=GREEN, lw=1.6))
    ax2.text(sc[0] + 0.04, sc[1] + 0.45, "v = 10 m/s", fontsize=8.5,
             color=GREEN)
    ax2.text(0.35, 1.2, "measure ONE snapshot:\ndistance r and speed v",
             ha="center", fontsize=8.5, color=GREEN)
    ax2.text(0.35, -1.32, r"$M = \dfrac{v^2}{G\,(2/r - 1/a)}$",
             ha="center", fontsize=12, color=ORANGE)
    ax2.set_title("Q8 -- vis-viva: one position + speed",
                  fontsize=10.5, fontweight="bold")

    fig.suptitle("Weighing a body you can't put on a scale: "
                 "let its captive do the work",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(FIG_DIR / "walkthrough_fig4_hidden_mass.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    fig_thread()
    fig_v_and_T()
    fig_irradiance()
    fig_hidden_mass()
    print("Walkthrough figures written to:", FIG_DIR)
