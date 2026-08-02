# STK Build Guide: MESA Scenario for Milestone 2

Everything needed to build the MESA scenario in STK and capture the stills that go
into the submission. Written against STK 12. Every number below is already used in
the report, so the STK scenario and the written analysis agree.

---

## 0. Getting STK access (Apple Silicon problem)

STK desktop is Windows x86-64 only. This machine is an Apple M4 running macOS 26.2,
so STK will not install natively. Options, best first:

| Path | Effort | Notes |
|:---|:---|:---|
| **UCCS lab machine or IT-provided remote desktop** | Low | The assignment says STK is "available through UCCS IT," so this is the intended route. Ask IT for a license and whether they host it via remote desktop |
| **Any Windows PC you have access to** | Low | Install STK Free there, build the scenario, export the stills and the `.sc` file |
| **Parallels + Windows 11 ARM** | High | Windows ARM emulates x86-64, but STK leans on OpenGL 3D and will be slow or unstable. Not recommended under time pressure |
| **Ansys/AGI cloud offering** | Unknown | Ask IT whether the UCCS license covers a hosted option |

License terms and tiers change, so confirm with UCCS IT rather than trusting this table.

---

## 1. Scenario setup

Create a new scenario named `MESA_MS2`.

| Field | Value |
|:---|:---|
| Start epoch | 20 Mar 2027 00:00:00.000 UTCG |
| Stop epoch | 21 Mar 2027 00:00:00.000 UTCG |
| Duration | Exactly one day |

**Why this epoch:** it is the vernal equinox, which is the worst-case eclipse season at
GEO. The report quotes a 69.4 min eclipse, and that only shows up in the STK power plot
if the scenario runs through an equinox. Pick a date well away from it and the array
never enters shadow, which will silently contradict Section 12.

---

## 2. Insert the satellite

Insert a Satellite, name it `MESA`, propagator **Two-Body** (Astrogator is a paid module
and is not needed here).

Set the orbit with Classical (Keplerian) elements:

| Element | Value | Source |
|:---|---:|:---|
| Semi-major axis | 42,164.137 km | Report Eq. (1) |
| Eccentricity | 0.0 | circular |
| Inclination | 0.0 deg | equatorial, stationkept |
| Argument of periapsis | 0.0 deg | undefined for a circular orbit, set to zero |
| RAAN | 0.0 deg | |
| True anomaly | 255.0 deg | places the vehicle near 105 W at epoch |

If you prefer, STK's Geostationary orbit type lets you type the **subsatellite longitude
directly as -105 deg** and skips the true-anomaly step. Either is fine; the longitude is
what matters, since Section 6 uses the 105 W slot.

**Sanity check before moving on:** the ground track in the 2D window should be a
stationary dot at 105 W, not a moving line. If it moves, the semi-major axis is wrong.

---

## 3. 3D model (grad requirement bullet 1)

Right-click `MESA` → **Properties** → **3D Graphics** → **Model**.

Browse the model library and pick the closest match to the MESA configuration. Good
candidates, in order of fit:

1. Any **satellite bus with two deployed solar wings** (the MESA planform is a
   1.8 x 1.8 x 3.5 m bus with two wings totalling 10.24 m²)
2. A **GEO comsat** model, which is the right class and mass
3. The generic **Satellite** model as a fallback

Set the model scale so the vehicle is visible at GEO range. In the same panel, turn on
the orbit trail and the body axes, which makes the still far more readable.

**Capture still #1 here:** 3D view showing MESA with Earth behind it and the orbit trail.

---

## 4. Power sources (grad requirement bullet 2)

**Utilities** → **Component Browser** → **Power Sources**.

Configure to match the report's Table 7 and Section 12.1:

| Parameter | Value |
|:---|---:|
| Solar panel area | 10.24 m² |
| Cell efficiency (BOL) | 30% |
| Packing factor | 0.90 |
| Temperature derate | 0.90 |
| Efficiency after 5 yr degradation | 26.4% (30% x 0.881) |
| Beginning-of-life output | 3,387 W |
| End-of-life output | 2,984 W |
| Peak load | 1,773 W |
| Orbit-average load | 1,200 W |

---

## 5. Solar panel power over one day (grad requirement bullet 3)

Select `MESA` → **Satellite** menu → **Solar Panel Tool**.

1. Define the panel with the area and efficiency above
2. Set the sun-tracking option, since MESA uses single-axis tracking wings
3. Compute over the full one-day scenario span
4. Generate the **Solar Panel Power** graph

**Capture still #2 here:** the power-vs-time plot across one day.

**What to expect, and how to check it:** the curve should sit flat near 3.4 kW BOL and
drop to zero for about 69 minutes near local midnight. If STK's eclipse duration lands
close to the 69.4 min in Eq. (11), the Python model and STK agree and that cross-check is
worth a sentence in the report. If STK reports no eclipse at all, the epoch is not at an
equinox; go back to step 1.

---

## 6. Lifetime (grad requirement bullet 3, second half)

Select `MESA` → **Satellite** menu → **Lifetime Tool**.

| Parameter | Value | Source |
|:---|---:|:---|
| Drag area | 16.54 m² | Table 3 illuminated area |
| Drag coefficient $C_D$ | 2.2 | Section 7 |
| Mass | 2,000 kg | Table 3 |
| Reflection coefficient | 1.0 | |
| Solar flux / geomagnetic | STK defaults | |

**Expect STK to report that the orbit does not decay.** That is not a tool failure, it is
the correct physical answer and it is exactly the Section 7 conclusion: at GEO the
drag-decay timescale is on the order of $10^5$ to $10^6$ years, so a lifetime tool built
for LEO decay will report no reentry. Screenshot the result anyway and say so in the
report, because a tool that confirms the analysis is a stronger result than one that
merely produces a number.

**Optional but strong:** re-run Lifetime with the same vehicle at 400 km to show the tool
working where drag matters, and compare against the 298 days in Table 2. If STK lands in
the same ballpark, the Section 7 model is independently validated.

**Capture still #3 here:** the Lifetime report.

---

## 7. What to export

Save into `design_project/milestone2/submission/stk/`:

| File | Purpose |
|:---|:---|
| `MESA_MS2.sc` (plus its scenario folder) | The scenario file submitted alongside the report |
| `fig9_stk_3d.png` | Still #1, 3D view |
| `fig10_stk_power.png` | Still #2, power over one day |
| `fig11_stk_lifetime.png` | Still #3, Lifetime report |

STK scenarios are a folder, not a single file, so zip the whole scenario directory for
submission.

Send me those three PNGs and I will wire them into Section 12 as Figures 9 through 11,
with the text referencing the scenario file as a separately submitted artifact.

---

## 8. Cross-checks worth putting in the report

Once STK runs, these three comparisons are the real value, because they turn the STK work
from a screenshot exercise into validation of the analysis:

| Quantity | Python model | STK | Where |
|:---|---:|:---|:---|
| Eclipse duration at equinox | 69.4 min | from the power plot | Eq. (11) |
| Array power, BOL | 3,387 W | from the Solar Panel tool | Eq. (12) |
| Orbital decay at GEO | none, $10^5$ to $10^6$ yr | expect "does not decay" | Eq. (3) |

If STK disagrees with any of these by more than a few percent, tell me the numbers before
we submit and I will chase down which model is wrong rather than paper over it.
