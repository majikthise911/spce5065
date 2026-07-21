"""Generate original figures for the vacuum-environment / cold-welding deck.

All figures render on the deck's dark surface (#1a1a19) with a single blue
accent (#3987e5), so magnitude reads by length/position, not by hue.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

OUT = "/Volumes/Marvin SSD/Projects/spce5065/presentation/figures"

SURFACE = "#1a1a19"
INK = "#ffffff"
INK2 = "#c3c2b7"
MUTED = "#898781"
GRID = "#2c2c2a"
AXIS = "#383835"
BLUE = "#3987e5"
BLUE_L = "#86b6ef"
AMBER = "#fab219"

plt.rcParams.update({
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "text.color": INK,
    "axes.labelcolor": INK2,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "axes.edgecolor": AXIS,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 13,
})


def fig_pressure():
    # Approximate atmospheric pressure vs altitude (illustrative).
    alt = np.array([0, 10, 20, 30, 50, 80, 100, 150, 200, 300, 400, 500])   # km
    p_torr = np.array([760, 199, 41.5, 9.0, 0.60, 8e-3, 2.4e-4,
                       3.6e-6, 6e-7, 6e-8, 1.2e-8, 3e-9])                    # Torr

    fig, ax = plt.subplots(figsize=(10, 5.6))
    ax.semilogy(alt, p_torr, "-", color=BLUE, lw=2.4, zorder=3)
    ax.semilogy(alt, p_torr, "o", color=BLUE, ms=6,
                markeredgecolor=SURFACE, markeredgewidth=1.5, zorder=4)

    # Ultra-high-vacuum band where oxide films cannot re-form.
    ax.axhspan(1e-9, 1e-6, color=BLUE, alpha=0.10, zorder=0)
    ax.text(250, 3e-8, "Ultra-high vacuum\nno oxygen to re-grow oxide films",
            color=BLUE_L, fontsize=12, ha="center", va="center", zorder=5)

    # ISS marker.
    ax.annotate("ISS  (~400 km)", xy=(400, 1.2e-8), xytext=(330, 5e-6),
                color=AMBER, fontsize=12,
                arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.4))
    ax.annotate("Sea level", xy=(0, 760), xytext=(35, 300),
                color=INK2, fontsize=12,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.2))

    ax.set_xlabel("Altitude (km)")
    ax.set_ylabel("Pressure (Torr)")
    ax.set_title("Pressure falls ~13 orders of magnitude from the ground to LEO",
                 color=INK, fontsize=15, pad=12, loc="left")
    ax.set_xlim(-10, 510)
    ax.set_ylim(1e-9, 3e3)
    ax.grid(True, which="major", color=GRID, lw=0.8)
    ax.grid(True, which="minor", color=GRID, lw=0.4, alpha=0.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.text(0.0, -0.16, "Illustrative values from a standard-atmosphere profile.",
            transform=ax.transAxes, color=MUTED, fontsize=10)
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig1_pressure_vs_altitude.png", dpi=200)
    plt.close(fig)


def fig_schematic():
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.4))

    def metal(ax, y0, label, ytext):
        ax.add_patch(Rectangle((0.12, y0), 0.76, 0.24, facecolor="#6f7683",
                                edgecolor=INK2, lw=1.2))
        ax.text(0.5, y0 + 0.12, label, ha="center", va="center",
                color="#0b0b0b", fontsize=12, fontweight="bold")

    # Panel A: on the ground, protected by an oxide + adsorbed-gas film.
    axA = axes[0]
    metal(axA, 0.60, "Metal part A", None)
    metal(axA, 0.16, "Metal part B", None)
    axA.add_patch(Rectangle((0.12, 0.52), 0.76, 0.08, facecolor=AMBER,
                            edgecolor="none", alpha=0.85, hatch="////"))
    axA.text(0.5, 0.56, "oxide + adsorbed gas layer",
             ha="center", va="center", color="#0b0b0b", fontsize=10.5,
             fontweight="bold")
    axA.text(0.5, 0.95, "On the ground", ha="center", color=INK, fontsize=14,
             fontweight="bold")
    axA.text(0.5, 0.04, "Film keeps the metals apart, no bonding",
             ha="center", color=INK2, fontsize=11.5)

    # Panel B: in vacuum, fretting ruptures the film, clean metal bonds.
    axB = axes[1]
    metal(axB, 0.60, "Metal part A", None)
    metal(axB, 0.36, "Metal part B", None)
    # bond zone
    for x in np.linspace(0.22, 0.78, 6):
        axB.add_patch(FancyArrowPatch((x, 0.615), (x, 0.585),
                      arrowstyle="-", color=BLUE, lw=2.2))
    axB.text(0.5, 0.60, "clean metal, metallic bonds",
             ha="center", va="center", color=BLUE_L, fontsize=10.5,
             fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.25", fc=SURFACE, ec=BLUE, lw=1))
    axB.annotate("", xy=(0.10, 0.48), xytext=(0.02, 0.48),
                 arrowprops=dict(arrowstyle="->", color=AMBER, lw=2))
    axB.annotate("", xy=(0.90, 0.48), xytext=(0.98, 0.48),
                 arrowprops=dict(arrowstyle="->", color=AMBER, lw=2))
    axB.text(0.5, 0.95, "In vacuum + fretting", ha="center", color=INK,
             fontsize=14, fontweight="bold")
    axB.text(0.5, 0.20, "Film ruptured, bare metal exposed\nthe parts fuse into one crystal",
             ha="center", color=INK2, fontsize=11.5)

    for ax in axes:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
    fig.suptitle("Why metals cold-weld in space", color=INK, fontsize=16,
                 fontweight="bold", x=0.5, y=1.02)
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig2_coldweld_schematic.png", dpi=200,
                bbox_inches="tight")
    plt.close(fig)


def fig_pairs():
    pairs = ["Stainless 440C\nvs. Ti-6Al-4V",
             "Ti-6Al-4V\nvs. itself",
             "Stainless 440C\nvs. itself"]
    force = [10.0, 6.0, 3.0]
    y = np.arange(len(pairs))[::-1]

    fig, ax = plt.subplots(figsize=(10, 5.2))
    bars = ax.barh(y, force, height=0.55, color=BLUE, edgecolor=SURFACE, lw=1.5)
    for yi, f in zip(y, force):
        ax.text(f + 0.2, yi, f"{f:.0f} N", va="center", ha="left",
                color=INK, fontsize=13, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(pairs, color=INK2, fontsize=12)
    ax.set_xlabel("Measured fretting adhesion force (N)")
    ax.set_xlim(0, 12)
    ax.set_title("Even dissimilar metals adhere once the surface film is breached",
                 color=INK, fontsize=15, pad=12, loc="left")
    ax.grid(True, axis="x", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.text(0.0, -0.17, "Representative ESA/ESTL fretting-test values (STM-279).",
            transform=ax.transAxes, color=MUTED, fontsize=10)
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig3_material_pairs.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    fig_pressure()
    fig_schematic()
    fig_pairs()
    print("figures written to", OUT)
