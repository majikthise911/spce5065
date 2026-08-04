# GUI steps for Figures 10 and 11

Everything else in the STK task is scripted and done. These two figures need the GUI,
because the **Solar Panel tool has no Connect command and no object model interface**: it
works by animating the scenario and pixel-counting the illuminated panels, so it is tied to
the 3D window.

**Before you start:** STK should already be open with the `MESA_MS2` scenario loaded and
`MESA` in the Object Browser. If it is not, reopen
`submission/stk/MESA_MS2/MESA_MS2.sc`, or re-run `build_mesa_scenario.py` from the venv.

Save both screenshots into `design_project/milestone2/submission/stk/`.

---

## Figure 10, Solar Panel power over one day

1. Click **MESA** in the Object Browser to select it.
2. Menu bar: **Satellite**, then **Solar Panel...**. Two windows open, a Solar Panel View
   and a Solar Panel control window.
3. In the Solar Panel window:
   - Time interval dropdown: **Use Scenario Interval** (this is already exactly one day,
     20 Mar 2027 00:00 to 21 Mar 2027 00:00)
   - **Time Step: 60** seconds
   - Under Solar Panel Groups you should now see a group named **`MESA_Array`**.
     **Select it.** If the box is empty, see the note below.

### Why the group box was empty before, and what changed

The stock `anik_f1.glb` declares only the `AGI_articulations` glTF extension. It has **no
`AGI_stk_metadata.solarPanelGroups` block at all**, and that block is the only thing the
Solar Panel tool reads to build its group list. The panel geometry was always there, the
metadata was not, so the list was genuinely empty and no amount of clicking would populate it.
STK 13 also ships **zero `.mdl` files** (319 `.glb` and nothing else), so falling back to an
older model format was not an option.

The scenario now uses **`Space/MESA_bus.glb`**, built by `make_mesa_model.py`. It is the same
Anik F1 geometry with a solar panel group added:

```json
"AGI_stk_metadata": {
  "solarPanelGroups": [
    {"name": "MESA_Array", "modelNodes": [ ...10 panel nodes... ], "efficiency": 24.3}
  ]
}
```

The 24.3% is the report's own derating chain from Section 12.1, 0.30 cell efficiency x 0.90
packing x 0.90 temperature derate, so STK applies the same conversion factor the report does.
No orbit, epoch, mass, or area parameter was touched.

**If the group list is still empty**, the model did not load. Check
3D Graphics, Model and confirm it reads `Space/MESA_bus.glb`, then re-run
`build_mesa_scenario.py`.
4. Click **Compute**. It animates through the day; give it a moment.
5. Set **Graph** (not Report), and **Type: Power**.
6. Click **Generate...**.
7. Screenshot the resulting graph window and save as **`fig10_stk_power.png`**.

**What you should see:** a curve that sits flat through most of the day and drops to zero
for roughly **69 minutes**. That notch is the whole point of using the 20 March epoch.

**If there is no notch at all**, the epoch is wrong and the scenario is not at an equinox.
Tell me rather than screenshotting it, because it would silently contradict Eq. (11).

### One thing to expect, and not to worry about

The absolute wattage will probably **not** equal the report's 3,387 W. STK computes

```
Power = Efficiency x Solar Intensity x Effective Area x Solar Irradiance
```

and it takes **Efficiency and panel area from the 3D model file**, not from anything we set.
We are using a stock Anik F1 model, so its panels are its own, not MESA's 10.24 m² at 24.3%.

Do not try to force the numbers to agree. Just send me whatever STK reports and I will write
the comparison up honestly in Section 12.3. The **eclipse duration** is the cross-check that
is genuinely meaningful here, since it depends only on the orbit and the epoch, both of which
are MESA's. Sanity note for the record: `10.24 x 1361.128 x (0.30 x 0.90 x 0.90) = 3,387 W`,
which is exactly Eq. (12), so the report's own arithmetic is self-consistent.

---

## Figure 11, Lifetime report

1. Select **MESA** in the Object Browser.
2. Menu bar: **Satellite**, then **Lifetime...**.
3. The parameters are already set by the build script. Confirm they read:

   | Field | Value |
   |:---|---:|
   | Drag coefficient (Cd) | 2.2 |
   | Drag area | 16.54 m² |
   | Sun (SRP) area | 10.24 m² |
   | Reflection coefficient (Cr) | 1.0 |
   | Mass | 2,000 kg |

4. Click **Compute**.
5. Screenshot the result window and save as **`fig11_stk_lifetime.png`**.

**Expected result, already confirmed from the scripted run:**

```
MESA does not decay within the 36500.0 day limit.
```

That is not a tool failure. It is the correct physics at GEO and it is exactly what report
Section 7 concludes, a drag-decay timescale of 10⁵ to 10⁶ years. A tool that confirms the
analysis is a stronger result than one that just prints a number.

---

## Optional, and worth it if you have five more minutes

Re-run **Lifetime** with the same vehicle at **400 km** altitude and compare against the
298 days in Table 2. If STK lands in the same ballpark, Section 7's model is independently
validated at an altitude where drag actually matters, which is a much stronger claim than
"the tool agreed that nothing happens at GEO."

To do it: change the satellite's semi-major axis to **6,778.137 km**, recompute Lifetime,
note the number, then set it back to 42,164.137 km. Send me the number and I will add it to
Section 12.3.
