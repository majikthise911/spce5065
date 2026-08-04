"""
Figure 10: solar panel power over one day, from the STK Solar Panel tool.

Data source is solar_panel_power.txt, written by STK's
"VO <sat> SolarPanel Compute ... Power" command over the full scenario day at a
60 s step.

Two traces are plotted, and the distinction matters for the report:

  1. STK as computed. The Solar Panel tool derives illuminated area from the 3D
     model's geometry and efficiency from the model's AGI_stk_metadata block. The
     scenario uses the stock Space/a2100.glb (a GEO comsat bus) at its shipped
     14% efficiency, so the raw wattage describes A2100's arrays, not MESA's.

  2. Normalised to MESA. STK's own power law is
         Power = Efficiency x Solar Intensity x Effective Area x Solar Irradiance
     so scaling trace 1 by MESA's area and efficiency ratios puts it on the
     report's basis and makes it directly comparable to Eq. (12).

The eclipse is the cross-check that is independent of the model entirely: it
depends only on the orbit and the epoch, both of which are genuinely MESA's.
"""

import os
import re
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "solar_panel_power.txt")
OUT = os.path.join(HERE, "fig10_stk_power.png")

# Model basis that STK actually used
STK_EFFICIENCY = 0.14           # stock a2100.glb AGI_stk_metadata
SOLAR_IRRADIANCE = 1361.128     # W/m^2 at 1 AU, STK's value (Help vo/solarpan.htm)

# MESA basis, from the report
MESA_AREA_M2 = 10.24            # Table 3, two wings
MESA_EFFICIENCY = 0.30 * 0.90 * 0.90   # Section 12.1 -> 0.243
EQ12_BOL_W = 3387.0             # Eq. (12)
EQ11_ECLIPSE_MIN = 69.4         # Eq. (11)

ROW = re.compile(
    r"^\s*(\d{1,2} \w{3} \d{4} \d{2}:\d{2}:\d{2}\.\d+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s*$")


def load(path):
    """Parse the report. STK emits a per-group block and an 'All groups' block,
    so de-duplicate on timestamp."""
    seen = {}
    for line in open(path, errors="replace"):
        m = ROW.match(line)
        if not m:
            continue
        t = datetime.strptime(m.group(1), "%d %b %Y %H:%M:%S.%f")
        seen[t] = (float(m.group(2)), float(m.group(3)))
    times = sorted(seen)
    return times, [seen[t][0] for t in times], [seen[t][1] for t in times]


def main():
    if not os.path.exists(SRC):
        raise SystemExit("missing %s, run the Solar Panel compute first" % SRC)

    times, power, intensity = load(SRC)
    print("parsed %d unique samples, %s to %s" % (len(times), times[0], times[-1]))

    sunlit = [p for p, i in zip(power, intensity) if i > 0.999]
    stk_bol = sum(sunlit) / len(sunlit)

    # Back out the model's effective array area from STK's own power law.
    stk_area = stk_bol / (STK_EFFICIENCY * SOLAR_IRRADIANCE)
    scale = (MESA_AREA_M2 / stk_area) * (MESA_EFFICIENCY / STK_EFFICIENCY)
    mesa_power = [p * scale for p in power]
    mesa_bol = stk_bol * scale

    # Eclipse extent straight from solar intensity.
    umbra = [t for t, i in zip(times, intensity) if i <= 1e-4]
    shadow = [t for t, i in zip(times, intensity) if i < 0.999]
    umbra_min = (umbra[-1] - umbra[0]).total_seconds() / 60.0 + 1.0
    shadow_min = (shadow[-1] - shadow[0]).total_seconds() / 60.0 + 1.0

    print("STK sunlit power      : %.1f W  (a2100 arrays at %.0f%%)"
          % (stk_bol, STK_EFFICIENCY * 100))
    print("implied array area    : %.2f m^2" % stk_area)
    print("scale to MESA basis   : %.4f" % scale)
    print("normalised BOL power  : %.1f W   (Eq. 12 says %.0f W)" % (mesa_bol, EQ12_BOL_W))
    print("umbra                 : %.1f min (Eq. 11 says %.1f min)" % (umbra_min, EQ11_ECLIPSE_MIN))
    print("umbra + penumbra      : %.1f min" % shadow_min)

    fig, ax = plt.subplots(figsize=(9.5, 4.6))

    ax.plot(times, mesa_power, lw=1.8, color="#1f77b4",
            label="Normalised to MESA (%.2f m$^2$, %.1f%%)"
                  % (MESA_AREA_M2, MESA_EFFICIENCY * 100))
    ax.plot(times, power, lw=1.0, color="#aaaaaa", ls="--",
            label="STK as computed (a2100 arrays, %.0f%%)" % (STK_EFFICIENCY * 100))

    ax.axhline(EQ12_BOL_W, color="#d62728", lw=1.2, ls=":",
               label="Eq. (12) BOL, %d W" % EQ12_BOL_W)

    ax.axvspan(shadow[0], shadow[-1], color="#333333", alpha=0.12)
    ax.annotate("eclipse\numbra %.0f min\n(Eq. 11: %.1f min)" % (umbra_min, EQ11_ECLIPSE_MIN),
                xy=(umbra[len(umbra) // 2], max(mesa_power) * 0.55),
                ha="center", va="center", fontsize=9,
                bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#666666", lw=0.8))

    ax.set_xlabel("Time, 20 Mar 2027 (UTCG)")
    ax.set_ylabel("Solar array power (W)")
    ax.set_title("MESA solar array power over one day at GEO, STK Solar Panel tool")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
    ax.set_ylim(0, max(max(mesa_power), max(power)) * 1.15)
    ax.grid(alpha=0.3)
    ax.legend(loc="lower right", fontsize=8.5, framealpha=0.95)

    fig.tight_layout()
    fig.savefig(OUT, dpi=200)
    print("\nwrote %s" % OUT)


if __name__ == "__main__":
    main()
