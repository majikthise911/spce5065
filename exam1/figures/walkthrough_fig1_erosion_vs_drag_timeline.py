"""SPCE 5065 midterm walkthrough, Figure 1.

Who-wins timeline: the four competing clocks in Problem 6, drawn as horizontal
bars on a single 0-to-5-year mission axis so the reader can see at a glance
which failure mechanism arrives first. Dark theme per the walkthrough spec.

Numbers are the exact P6 outputs from spce_5065_ex1_solution.py:
  50 um cover eroded through      0.61 yr
  300 um cover eroded through     3.69 yr
  drag decays 550 -> 150 km       4.36 yr
  mission design life             5.00 yr
"""
from pathlib import Path

import matplotlib.pyplot as plt

BG = "#0D1117"
FG = "#E6EDF3"
GREEN = "#3FB950"
RED = "#F85149"
BLUE = "#58A6FF"
PURPLE = "#D2A8FF"
ORANGE = "#FFA657"
GRID = "#30363D"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "savefig.facecolor": BG,
    "text.color": FG,
    "axes.labelcolor": FG,
    "xtick.color": FG,
    "ytick.color": FG,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
})

# (label, time-to-event yr, color, is a failure that ends the part-c story)
rows = [
    ("50 um cover eroded through\n(erosion, part c)", 0.61, RED),
    ("300 um cover eroded through\n(erosion, part a)", 3.69, ORANGE),
    ("Drag decays 550 -> 150 km\n(deorbit, part b)", 4.36, BLUE),
    ("Mission design life\n(the deadline)", 5.00, GREEN),
]

fig, ax = plt.subplots(figsize=(8.2, 4.6))

ypos = list(range(len(rows)))[::-1]
for y, (label, t, color) in zip(ypos, rows):
    ax.barh(y, t, height=0.5, color=color, alpha=0.85, zorder=3)
    ax.text(t + 0.06, y, f"{t:.2f} yr", va="center", ha="left",
            color=color, fontsize=10, fontweight="bold", zorder=4)

ax.set_yticks(ypos)
ax.set_yticklabels([r[0] for r in rows], fontsize=9)

# 5-year mission window shading and deadline line
ax.axvspan(0, 5.0, color=GREEN, alpha=0.06, zorder=0)
ax.axvline(5.0, color=GREEN, ls="--", lw=1.3, zorder=2)

ax.set_xlim(0, 5.6)
ax.set_xlabel("Time on orbit (years)")
ax.set_title("Problem 6: the four competing clocks (550 km, high solar activity)",
             color=FG, fontsize=12, pad=12)
ax.grid(True, axis="x", color=GRID, alpha=0.6, zorder=1)
for spine in ax.spines.values():
    spine.set_color(GRID)

ax.annotate("erosion wins:\nthe thin cover fails first",
            xy=(0.61, ypos[0] - 0.28), xytext=(1.7, ypos[0] - 0.55),
            color=RED, fontsize=9,
            arrowprops=dict(arrowstyle="->", color=RED))

fig.tight_layout()
out = Path(__file__).parent / "walkthrough_fig1_erosion_vs_drag_timeline.png"
fig.savefig(out, dpi=200)
print("wrote", out)
