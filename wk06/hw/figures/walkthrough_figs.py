"""Figures for the SPCE 5065 HW6 Socratic walkthrough (dark theme, 200 dpi)."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent

BG = "#0D1117"
FG = "#E6EDF3"
GREEN = "#3FB950"
RED = "#F85149"
BLUE = "#58A6FF"
PURPLE = "#D2A8FF"
ORANGE = "#FFA657"

H = 6.626e-34
C = 2.998e8
HC = H * C
KB = 1.380649e-23
EV = 1.602176634e-19
T_SUN = 5772.0
R_SUN = 6.957e8
AU = 1.495979e11
SIGMA = 5.67e-8


def style(ax, title, xlabel, ylabel):
    ax.set_facecolor(BG)
    ax.set_title(title, color=FG, fontsize=12, pad=12)
    ax.set_xlabel(xlabel, color=FG)
    ax.set_ylabel(ylabel, color=FG)
    ax.tick_params(colors=FG)
    for s in ax.spines.values():
        s.set_color("#30363D")
    ax.grid(True, color="#21262D", lw=0.8)


def new_fig(size=(8, 5)):
    fig, ax = plt.subplots(figsize=size, facecolor=BG)
    return fig, ax


def planck_at_earth(lam_m, T=T_SUN):
    b = 2 * H * C ** 2 / lam_m ** 5 / (np.exp(HC / (lam_m * KB * T)) - 1.0)
    return np.pi * b * (R_SUN / AU) ** 2


# ---------------------------------------------------------------- figure 1
def fig1_bond_ladder():
    lam = np.linspace(0.15, 1.1, 600)
    e_ev = HC / (lam * 1e-6) / EV
    fig, ax = new_fig()
    ax.axvspan(0.40, 0.70, color="#1F6FEB", alpha=0.13)
    ax.text(0.55, 7.4, "visible", color=BLUE, ha="center", fontsize=9)
    ax.plot(lam, e_ev, color=BLUE, lw=2.2, label=r"$E = hc/\lambda$")

    bonds = [("O-O single", 1.52, GREEN), ("C-C single", 3.47, RED),
             ("C-C double", 6.29, PURPLE)]
    for name, e, col in bonds:
        lam_b = HC / (e * EV) * 1e6
        ax.plot([0.15, lam_b], [e, e], ls=":", color=col, lw=1.4)
        ax.plot([lam_b, lam_b], [0, e], ls=":", color=col, lw=1.4)
        ax.plot(lam_b, e, "o", color=col, ms=7)
        ax.annotate(f"{name}\n{e:.2f} eV at {lam_b:.3f} " r"$\mu$m",
                    xy=(lam_b, e), xytext=(26, 16), textcoords="offset points",
                    color=col, fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.3", fc="#161B22",
                              ec=col, alpha=0.95),
                    arrowprops=dict(arrowstyle="->", color=col))
    ax.set_xlim(0.15, 1.1)
    ax.set_ylim(0, 8.5)
    style(ax, "Photon energy sets the bond it can break",
          r"Wavelength  $\lambda$  ($\mu$m)", "Photon energy  (eV)")
    ax.legend(facecolor="#161B22", edgecolor="#30363D", labelcolor=FG,
              fontsize=9)
    fig.text(0.5, 0.015, "Shorter wavelength means a more energetic photon, "
             "so every bond has a cutoff wavelength to its left.",
             ha="center", color="#8B949E", fontsize=9, style="italic")
    fig.subplots_adjust(bottom=0.17)
    fig.savefig(OUT / "walkthrough_fig1_bond_ladder.png", dpi=200,
                facecolor=BG)
    plt.close(fig)


# ---------------------------------------------------------------- figure 2
def fig2_energy_vs_photons():
    lam = np.linspace(0.1e-6, 3.0e-6, 4000)
    s_lam = planck_at_earth(lam)                 # W/m^2/m   (energy)
    n_lam = s_lam * lam / HC                     # photons/m^2/s/m (count)
    fig, ax = new_fig()
    ax.plot(lam * 1e6, s_lam / s_lam.max(), color=ORANGE, lw=2.2,
            label="energy per wavelength  $S(\\lambda)$")
    ax.plot(lam * 1e6, n_lam / n_lam.max(), color=GREEN, lw=2.2,
            label="photons per wavelength  $S(\\lambda)\\lambda/hc$")
    lam_e = lam[int(np.argmax(s_lam))] * 1e6
    lam_n = lam[int(np.argmax(n_lam))] * 1e6
    for x, col, txt in [(lam_e, ORANGE, f"energy peak\n{lam_e:.3f} " r"$\mu$m"),
                        (lam_n, GREEN, f"photon peak\n{lam_n:.3f} " r"$\mu$m")]:
        ax.axvline(x, color=col, ls=":", lw=1.3)
    ax.annotate(f"energy peak {lam_e:.2f} " r"$\mu$m" "\n(2.47 eV photon)",
                xy=(lam_e, 1.0), xytext=(24, -58), textcoords="offset points",
                color=ORANGE, fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", fc="#161B22", ec=ORANGE),
                arrowprops=dict(arrowstyle="->", color=ORANGE))
    ax.annotate(f"photon peak {lam_n:.2f} " r"$\mu$m" "\nmean photon 1.38 eV",
                xy=(lam_n, 1.0), xytext=(96, -6), textcoords="offset points",
                color=GREEN, fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", fc="#161B22", ec=GREEN),
                arrowprops=dict(arrowstyle="->", color=GREEN))
    ax.axvspan(0.1, 0.3573, color=RED, alpha=0.18)
    ax.annotate("bond-breaking band\n2.6% of the photons",
                xy=(0.30, 0.20), xytext=(70, 30), textcoords="offset points",
                color=RED, fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", fc="#161B22", ec=RED),
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.set_xlim(0.1, 2.5)
    ax.set_ylim(0, 1.18)
    style(ax, "Where the energy peaks is not where the photons peak",
          r"Wavelength  $\lambda$  ($\mu$m)", "Normalized spectral density")
    ax.legend(facecolor="#161B22", edgecolor="#30363D", labelcolor=FG,
              fontsize=9, loc="center right")
    fig.text(0.5, 0.015, "Counting photons shifts the curve redward, so the "
             "peak-wavelength energy overstates the average photon by 1.8x.",
             ha="center", color="#8B949E", fontsize=9, style="italic")
    fig.subplots_adjust(bottom=0.17)
    fig.savefig(OUT / "walkthrough_fig2_energy_vs_photons.png", dpi=200,
                facecolor=BG)
    plt.close(fig)


# ---------------------------------------------------------------- figure 3
def fig3_heat_waterfall():
    labels = ["Solar\n0.3(1)(1367)", "Albedo\n" r"$\alpha A\sin^2\rho\,aS$",
              "Planet IR\n" r"$\alpha A\sin^2\rho\,F_{IR}$",
              "Internal\n(given)", "Total in"]
    vals = [410.1, 113.4, 53.1, 750.0]
    fig, ax = new_fig((8.6, 5))
    running = 0.0
    for i, (lab, v) in enumerate(zip(labels[:-1], vals)):
        col = ORANGE if i < 3 else BLUE
        ax.bar(i, v, bottom=running, color=col, edgecolor=col, alpha=0.9,
               width=0.62)
        ax.annotate(f"{v:.1f} W", xy=(i, running + v), xytext=(0, 7),
                    textcoords="offset points", ha="center", color=FG,
                    fontsize=9)
        running += v
    ax.bar(4, running, color=PURPLE, edgecolor=PURPLE, alpha=0.95, width=0.62)
    ax.annotate(f"{running:.1f} W", xy=(4, running), xytext=(0, 7),
                textcoords="offset points", ha="center", color=PURPLE,
                fontsize=10, weight="bold")
    ax.text(0.62, running * 0.86, "radiated off all 6 faces:\n"
            r"$T=[Q/(\epsilon\sigma A)]^{1/4} = 273.2$ K $= 0.0^\circ$C",
            color=PURPLE, fontsize=10, va="center",
            bbox=dict(boxstyle="round,pad=0.35", fc="#161B22", ec=PURPLE))
    ax.set_xticks(range(5))
    ax.set_xticklabels(labels, color=FG, fontsize=9)
    ax.set_ylim(0, running * 1.18)
    style(ax, "Problem 4 heat balance at Earth, 1000 km orbit", "",
          "Absorbed power  (W)")
    fig.text(0.5, 0.015, "Internal dissipation is 57% of the input at Earth "
             "and effectively 100% of it past Jupiter.",
             ha="center", color="#8B949E", fontsize=9, style="italic")
    fig.subplots_adjust(bottom=0.20)
    fig.savefig(OUT / "walkthrough_fig3_heat_waterfall.png", dpi=200,
                facecolor=BG)
    plt.close(fig)


# ---------------------------------------------------------------- figure 4
def fig4_emissivity_window():
    eps = np.linspace(0.30, 1.00, 400)
    eps_area = 4 * eps + 2 * 0.05
    q_hot, q_cold = 1338.3, 750.0
    t_hot = (q_hot / (SIGMA * eps_area)) ** 0.25 - 273.15
    t_cold = (q_cold / (SIGMA * eps_area)) ** 0.25 - 273.15
    fig, ax = new_fig()
    ax.axhspan(-35, 35, color=GREEN, alpha=0.12)
    ax.plot(eps, t_hot, color=RED, lw=2.4, label="Mercury, sunlit (hot case)")
    ax.plot(eps, t_cold, color=BLUE, lw=2.4, label="Pluto (cold case)")
    ax.axhline(35, color=ORANGE, ls="--", lw=1.2)
    ax.axhline(-35, color=ORANGE, ls="--", lw=1.2)
    lo, hi = 0.6295, 1.0035
    ax.axvspan(lo, min(hi, 1.0), color=PURPLE, alpha=0.16)
    ax.axvline(0.85, color=PURPLE, ls=":", lw=1.6)
    ax.annotate("white paint\n" r"$\epsilon = 0.85$",
                xy=(0.85, 5), xytext=(-96, 40), textcoords="offset points",
                color=PURPLE, fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", fc="#161B22", ec=PURPLE),
                arrowprops=dict(arrowstyle="->", color=PURPLE))
    ax.annotate("both limits met\nfor " r"$0.63 \leq \epsilon \leq 1.00$",
                xy=(0.72, -52), xytext=(-8, -30), textcoords="offset points",
                color=FG, fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", fc="#161B22", ec="#30363D"))
    ax.set_xlim(0.30, 1.00)
    ax.set_ylim(-75, 75)
    style(ax, "Problem 5: the design window in side-face emissivity",
          r"Emissivity of the four uninsulated faces  $\epsilon$",
          r"Equilibrium temperature ($^\circ$C)")
    ax.legend(facecolor="#161B22", edgecolor="#30363D", labelcolor=FG,
              fontsize=9, loc="upper right")
    fig.text(0.5, 0.015, "Both curves fall together as emissivity rises, so "
             "one knob has to satisfy the hot limit and the cold limit at once.",
             ha="center", color="#8B949E", fontsize=9, style="italic")
    fig.subplots_adjust(bottom=0.17)
    fig.savefig(OUT / "walkthrough_fig4_emissivity_window.png", dpi=200,
                facecolor=BG)
    plt.close(fig)


# ---------------------------------------------------------------- figure 5
def fig5_cost_bars():
    opts = ["Louvers\n1 m$^2$", "Radiators\n1 m$^2$", "Heaters\n16 W",
            "MLI\n2 faces", "White paint\n4 faces"]
    cost = [57500, 15000, 10000, 15000, 0]
    cols = [RED, ORANGE, BLUE, GREEN, GREEN]
    fig, ax = new_fig((8.4, 5))
    bars = ax.bar(opts, cost, color=cols, alpha=0.9, width=0.6)
    ax.axhline(15000, color=PURPLE, ls="--", lw=1.8)
    ax.annotate("$15,000 budget (0.60 kg)", xy=(4.35, 15000), xytext=(0, 10),
                textcoords="offset points", ha="right", color=PURPLE,
                fontsize=10)
    for b, c in zip(bars, cost):
        ax.annotate(f"${c:,}", xy=(b.get_x() + b.get_width() / 2, c),
                    xytext=(0, 6), textcoords="offset points", ha="center",
                    color=FG, fontsize=9)
    ax.set_ylim(0, 66000)
    style(ax, "Problem 5: what $15K actually buys at $25,000/kg", "",
          "Cost  (USD)")
    fig.text(0.5, 0.015, "Paint is free because its mass is negligible, which "
             "is the only reason the design closes.",
             ha="center", color="#8B949E", fontsize=9, style="italic")
    fig.subplots_adjust(bottom=0.19)
    fig.savefig(OUT / "walkthrough_fig5_cost_bars.png", dpi=200, facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    fig1_bond_ladder()
    fig2_energy_vs_photons()
    fig3_heat_waterfall()
    fig4_emissivity_window()
    fig5_cost_bars()
    print("walkthrough figures written to", OUT)
