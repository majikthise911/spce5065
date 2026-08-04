# Milestone 2 session log

Running log of work on the Milestone 2 STK task. Newest entry at the top. Companion to
`HANDOFF.md`, which holds the task definition and does not change; this file records what
was actually done, so a future session does not repeat it.

---

## 3 Aug 2026, MILESTONE 2 COMPLETE

Section 12.3 written, docx rebuilt, full verification chain passing. Nothing is outstanding.

| Check | Result |
|:---|:---|
| `spce5065_ms2_figs.py` | exit 0 |
| Citations ascend 1..18 by first appearance | pass, no orphans either direction |
| `word/media/` image count | **12** (was 9, plus Figures 9 to 11) |
| Em dashes and en dashes | 0 |
| Instructor mentions | 0 |
| Equations / tables / figures | 1..13, 1..8, 1..11, all sequential |

**Two numbering traps hit while wiring this in, both worth remembering:**

1. **`\tag` in pandoc's texmath must follow a braced group.** `... \cdot G_s\tag{13}` fails to
   convert and silently degrades to raw TeX in the docx; `... \cdot G_{s}\tag{13}` works. All
   the pre-existing tagged equations happened to end in `}` already, which is why this never
   surfaced before. Grep the pandoc output for "Could not convert TeX math" after any edit
   that adds an equation.
2. **Do not cite a new source in the Revision Log.** That section sits near the top of the
   document, so a first appearance there makes the new reference number sort second and breaks
   AIAA ordering for everything after it. Section 12.3 names STK in prose there instead, and
   [18] first appears in Section 12.3 where it belongs.

New content: Section 12.3 "STK scenario verification" with Figures 9 to 11, Eq. (13), Table 8
of cross-checks, and reference [18]. Revision Log item 1 rewritten so it credits the STK
scenario rather than matplotlib, with Figure 2 retained as the reproducible 3D view.

**The write-up states plainly which cross-checks are independent and which are not.** The
eclipse (68.0 min umbra, 72.0 min total vs Eq. 11's 69.4 min) and the lifetime (no decay) are
genuine independent confirmations. The power agreement is labelled as consistency only, since
normalising STK's output by area and efficiency evaluates the same product Eq. (12) does.

---

## 3 Aug 2026, STK installed, scenario built, Lifetime done

**Outcome:** STK 13 is installed, licensed, and driving from Python. The scenario is built
and the Lifetime half of the graduate requirement is complete with the expected result.
Figure 9 framing and the Solar Panel figure are the open items.

### It is STK 13, not STK 12

The download was **Ansys STK Pro 2026R1, v13.1.0**. Both `HANDOFF.md` and
`STK_MESA_scenario_guide.md` were written against STK 12, so these differ:

| Thing | STK 12 assumption | Reality on this machine |
|:---|:---|:---|
| Install root | `C:\Program Files\AGI\STK 12` | `C:\Program Files\AGI\STK_ODTK 13` |
| Python package | `agi.stk12` | `agi.stk13` |
| Wheel | `agi.stk12-*.whl` | `bin\AgPythonAPI\agi_stk13-13.1.0-py3-none-any.whl` |
| App exe | `stk.exe` | `bin\AgUiApplication.exe` |

venv is at `<repo>\.venv` (added to `.gitignore`), with `agi_stk13` installed.

### License: Enterprise, not the limited free tier

`STK_DEMO_20722061.lic` is an **Ansys STK Enterprise** lease, **expiring 17 Aug 2026**.
It includes `stk_engine_runtime`, so the automation API is entitled; that answers the
handoff's open question about whether the tier exposes Connect/API. It does.

- Bound to `SERVER localhost DISK_SERIAL_NUM=fe72bfa4 1055` (C: volume serial, matches)
- Installed to `C:\Program Files\ANSYS Inc\Shared Files\Licensing\license_files\license.lic`
- Service "ANSYS, Inc. License Manager CVD" running, `lmgrd` listening on 1055

**The 17 Aug expiry matters for the Final Report**, which is cumulative and may need STK
again. Re-request a license if that work lands after the 17th.

### Install gotcha, worth knowing if this is ever redone

`install.exe` aborts with exit -1 because the bundled VC++ redist (14.50.35719) is **older**
than what is already installed (14.51.36247), so it returns `0x80070666` "cannot install a
product when a newer version is installed" and the orchestrator treats any nonzero exit as
fatal. The prerequisite is genuinely satisfied.

Fix that worked: in the extracted tree, back up
`Prerequisites\VC 2026 Redist 14.50.35719\x64\InstallCommand.txt` and point it at a compiled
no-op `.exe` that returns 0. It must be a real `.exe`; the orchestrator rejects a `.cmd`
with "install path not found" because the config declares `InstallType="EXE"`. Then:

```
install.exe --silent --licenseagree --licensemanager --licserverinfo="1055:localhost" --logpath="<dir>"
```

Documented switches came from strings inside `install.exe` itself. Install took 4m35s.

### Connect syntax, verified against the installed Help (not guessed)

Source: `C:\Program Files\AGI\STK_ODTK 13\Help\STK\SubSystems\connectCmds\Content`

- `SetState <sat> Classical TwoBody "<start>" "<stop>" <step> ICRF "<epoch>" <sma_m> <ecc> <inc> <argp> <raan> <ta>`
- `SetLifetime <sat> {DragCoeff|DragArea|SunArea|ReflectCoeff|Mass|LimitType|DurationLimit|...} <v>`
- `Lifetime <sat>` returns the result as text
- `VO * SnapFrame SetValues Format {BMP|JPEG|PNG|TIF}` then `VO * SnapFrame ToFile "<path>"`
- `VO <sat> ScaleModel <factor>`
- `VO * ViewFromTo Normal From <obj> To <obj>` and `VO * ViewFromTo Parameters Distance From <d>`

### The Solar Panel tool is GUI only, confirmed

There is **no Connect command and no object model interface** for solar panel power. The
only Connect entries are `VOSolarPanel` and `VOInitializeSolarPanelsToSun`, both
visualization. The tool works by animating the scenario and pixel-counting illuminated panel
area, so it is inherently tied to the 3D window. **Figure 10 has to be captured from the
GUI.** This resolves the handoff's open question the other way from Lifetime.

Two things from `Help\STK\Content\vo\solarpan.htm` that matter for the report:

1. STK computes `Power = Efficiency x Solar Intensity x Effective Area x Solar Irradiance`,
   with irradiance 1361.128 W/m^2 at 1 AU.
2. **Efficiency comes from the vehicle model file**, not a dialog. So an out-of-the-box model
   will not reproduce Eq. (12) unless its panel area and efficiency match MESA's.

Useful check: Eq. (12) is exactly `10.24 m^2 x 1361.128 W/m^2 x (0.30 x 0.90 x 0.90) = 3,387 W`,
so STK should agree if the model's panel area is 10.24 m^2 and efficiency is set to 24.3%.

### Lifetime result, done and matching the report

```
MESA does not decay within the 36500.0 day limit.
```

Saved to `submission/stk/lifetime_result.txt`. This is exactly what Section 7 concludes
(drag-decay timescale 10^5 to 10^6 yr at GEO), so the tool independently confirms the
analysis. Parameters used: Cd 2.2, DragArea 16.54 m^2, SunArea 10.24 m^2, Cr 1.0, mass 2000 kg,
100 year duration limit so the run terminates.

### 3D model rendering gotchas (cost a lot of time, do not repeat)

- `VO <sat> Model File "Space/anik_f1.glb"` (**relative** path) works. The **absolute** path
  form silently fails and leaves the object with no model.
- `Model IgnoreBoundRadius On` makes it worse: it culls the model by LOD so only the point
  marker draws. Leave it Off.
- STK swaps the model for a point marker beyond some range, so an Earth-framing wide shot
  shows the orbit trail and label but no spacecraft, no matter how large `ScaleModel` is.
- The model does render in an object-centred view at modest scale; scale 200 is already
  inside the antenna dish, so the usable range is roughly 10 to 60.

After setting the absolute path, model rendering stopped working for the rest of the session.
**Restart STK and rebuild from `build_mesa_scenario.py` to recover it.**

### Figure 9 final composition

Panel (a) is the MESA model (`Space/a2100.glb`) in an object-centred view at `ScaleModel 4`,
which fits the full wingspan. Panel (b) is a manual wide capture Jordan took showing the
complete GEO ring around Earth, which reads far better than the near-edge-on trail the
scripted view produced; it is kept as `fig9_stk_3d_zoomed_out.png` and composited by
`make_fig9.py`.

**Watch for model drift between figures.** An earlier panel (a) still showed `anik_f1.glb`
after the scenario had moved to `a2100.glb`, so the figure would have shown a different
vehicle than the one the Solar Panel numbers came from. Re-capture panel (a) whenever the
model changes.

### Figure 10 DONE. Solar Panel tool driven entirely from Connect

Final resolution of the empty-group problem, and the figure is generated.

**The model was the whole problem.** `Space/anik_f1.glb` has no
`AGI_stk_metadata.solarPanelGroups` block, so the group list was genuinely empty. Many stock
models do have one. Switched to **`Space/a2100.glb`**, the Lockheed Martin A2100 GEO comsat
bus, which is both a good MESA analogue and ships a working block:

```json
"AGI_stk_metadata": {"solarPanelGroups": [{"efficiency": 14, "name": "a2100"}]}
```

**Schema trap that cost an attempt.** A hand-built model copying the help page's example
(which shows a `modelNodes` array) was silently rejected and the list stayed empty. The stock
working models declare **only `name` and `efficiency`, no `modelNodes` key**. Match the stock
schema, not the help example. `make_mesa_model.py` is kept for the record but is not used by
the build; using the stock file avoids needing to install anything into Program Files.

**Two more things were needed to get real numbers:**

- `VO <sat> SolarPanel Visualization AddGroup AllGroups View On` before Compute
- `VO <sat> InitializeSolarPanelsToSun Enable Yes`, without which the arrays are not
  sun-pointed and power comes out around 0.05 W instead of 9,000 W
- `VO <sat> SolarPanel DeleteData` before recomputing, or results append

Also note STK writes both a per-group block and an "All Solar Panel Groups" block, so the
report has two rows per timestamp. `make_fig10.py` de-duplicates on timestamp.

### Figure 10 results, and what is and is not an independent check

| Quantity | Python model | STK | Verdict |
|:---|---:|---:|:---|
| Eclipse umbra at equinox | 69.4 min (Eq. 11) | **68.0 min** | agree within 2% |
| Umbra + penumbra | n/a | 72.0 min | |
| Eclipse timing | local midnight at 105 W | 06:32 to 07:43 UTC | as predicted |
| Array power BOL | 3,387 W (Eq. 12) | 3,386.9 W normalised | see caveat |

**The eclipse is the genuine independent validation.** It depends only on the orbit and the
epoch, both of which are really MESA's, and STK computed it from its own geometry.

**The power agreement is partly circular and must be reported as such.** STK's raw output is
9,085.7 W, which describes A2100's arrays at 14%, not MESA's. Backing out the implied area
gives 47.68 m^2, and rescaling to MESA's 10.24 m^2 and 24.3% reproduces 3,386.9 W. Since both
sides use `P = efficiency x intensity x area x irradiance`, that normalisation is close to
definitional. What it legitimately confirms is that STK uses the same solar constant
(1361.128 W/m^2) and the same formulation, and that Eq. (12)'s arithmetic is right. It is not
an independent confirmation of the power number. Say so plainly in Section 12.3.

### Solar Panel Groups box was empty: root cause and fix

Reported from the GUI: `Satellite, Solar Panel...` opened fine but the **Solar Panel Groups
list was completely empty**, and Compute warned "at least one Solar Panel Group should be
selected".

**Root cause.** The Solar Panel tool builds its group list solely from the glTF
`AGI_stk_metadata.solarPanelGroups` block:

```json
"AGI_stk_metadata": {
  "solarPanelGroups": [{"name": "...", "modelNodes": ["..."], "efficiency": 14.0}]
}
```

Stock `Space/anik_f1.glb` declares only `AGI_articulations` and has **no** such block, so the
list is genuinely empty. The panel geometry is present (10 nodes named
`s_panel_a_1..5 SolarPanel` / `s_panel_b_1..5 SolarPanel`), only the metadata is missing.
Documented in `Help\STK\Content\vo\glTFmodel.htm`.

**The .mdl fallback does not exist.** STK 13 ships **0 `.mdl` files** and 319 `.glb`, so
switching to an older model format is not possible from the stock library.

**Fix.** `make_mesa_model.py` copies the stock model, collects every node whose name ends in
`SolarPanel`, and registers them as one group:

- group name **`MESA_Array`**, 10 nodes
- efficiency **24.3%**, which is the report's own 0.30 x 0.90 x 0.90 chain from Section 12.1

Output `MESA_bus.glb` is installed into
`C:\Program Files\AGI\STK_ODTK 13\STKData\VO\Models\Space\` (needs elevation) and referenced
as `Space/MESA_bus.glb`. `build_mesa_scenario.py` now uses it. No physics parameter changed.

**Still open:** driving `SolarPanel Compute` from Connect returns "Data Unavailable" even with
the group registered and the Solar Panel View window open (it does open, as
`2 - Solar Panel View 2 - MESA`). Suspect STK's GPU Accelerated Analysis, which
`Help\STK\Content\vo\solarpan.htm` calls out as a known failure mode with the fix being
`Edit, Preferences, General, clear GPU Accelerated Analysis`. The **GUI path is untested and
may simply work**, since it renders on screen normally.

**Do not set `Window3D * SetRenderMethod Method PBuffer` on window 1.** It switches the main
3D window to off-screen rendering and every SnapFrame afterwards comes out solid black.
Restarting STK clears it. Only the Solar Panel View window (id 2) should get that treatment.

### TWO REAL BUGS IN THE SCENARIO, both found and fixed

Caught while answering a question about a GUI screenshot, not by the build script. Both would
have produced a wrong-but-plausible figure.

**1. The guide's true anomaly was wrong.** `STK_MESA_scenario_guide.md` says TA = 255 deg
"places the vehicle near 105 W". It does not: it puts the subsatellite point at
**78.05 deg E**, almost exactly half an orbit from the Section 6 slot. Verified with STK's
`LLA State / Fixed` data provider.

Correct value is **TA = 71.9539 deg**, which yields exactly -105.0000 deg. `build_mesa_scenario.py`
now carries this, and the guide's 255 is wrong wherever it appears.

**2. Connect `SetState` was not propagating the orbit at all.** The satellite sat at the right
42,164 km radius but its **inertial** position moved only about 8 km across a whole day, so in
the Earth-fixed frame it drifted westward at 360.99 deg/day, exactly Earth's sidereal rate.
It was a frozen point, not a geostationary satellite. `PropagatorType` came back as 7, not
Two-Body, so the command was silently not doing what it said.

Fix: build the orbit through the **object model** instead, then call `Propagate()`:

```python
sat.SetPropagatorType(AgEVePropagatorType.ePropagatorTwoBody)
prop.EphemerisInterval.SetExplicitInterval(START, STOP); prop.Step = 60.0
classical = prop.InitialState.Representation.ConvertTo(AgEOrbitStateType.eOrbitStateClassical)
classical.CoordinateSystemType = AgECoordinateSystem.eCoordinateSystemICRF
... rep.Assign(classical); prop.Propagate()
```

After the fix: inertial position sweeps +/-82,000 km (a full GEO circle) and fixed-frame
longitude holds -105.0000 deg with a spread of 0.0005 deg/day. Correct.

`build_mesa_scenario.py` now **verifies this and aborts** rather than emitting figures from a
wrong scenario:

```
subsatellite longitude : -105.0000 deg (target -105.0)
longitude spread / day : 0.0005 deg (must be ~0 for geostationary)
```

**Lesson worth carrying:** a Connect command returning `ok` does not mean it did what it says.
Check a data provider, not the acknowledgement.

### Two more API gotchas, both cost real time

- **Never chain `STKDesktop.AttachToApplication().Root`.** The application object gets
  garbage-collected and every subsequent `ExecuteCommand` fails with
  `'NoneType' object has no attribute '_getVtblEntry'`, which looks like a dead STK but is
  not. Hold the reference: `stk = STKDesktop.AttachToApplication()` then `root = stk.Root`.
- **`SaveAs` needs the object path**: `SaveAs / * "<path>"`, not `SaveAs / "<path>"`.

Restarting STK and re-running `build_mesa_scenario.py` restored model rendering, so the
absolute-path damage is not sticky.

### Figure 9 is a two-panel composite, on purpose

STK substitutes a point marker for the 3D model beyond a certain viewing range, so no single
frame can show both the spacecraft and the whole GEO orbit at readable size. Figure 9 is
therefore panel (a) the model at `ScaleModel 8` in an object-centred view, and panel (b)
Earth with the orbit trail from 55,000 km. Both are the same scenario at the same epoch.
Composed by `make_fig9.py`, which is committed next to the figure.

### Scenario packaging

There is **no VDF Connect command**, so VDF export is GUI-only. Took the handoff's documented
fallback: saved the scenario folder and zipped it to `MESA_MS2.zip` (103 KB), which contains
`MESA_MS2.sc`, the `MESA.sa` satellite, and the workbook.

### State of the deliverables

| Item | Status |
|:---|:---|
| Scenario `MESA_MS2` | built and saved: correct equinox epoch, GEO Two-Body, all parameters |
| `MESA_MS2.zip` | done, scenario packaged for submission |
| `lifetime_result.txt` | done, no decay at GEO |
| `fig9_stk_3d.png` | **done**, two-panel composite |
| `fig10_stk_power.png` | **needs GUI**, steps written in `GUI_STEPS_fig10_fig11.md` |
| `fig11_stk_lifetime.png` | **needs GUI**, result already known from the scripted run |
| Report Section 12.3 | not started, correctly blocked until STK produces the numbers |

### Open question for Section 12.3, do not paper over it

STK's Solar Panel tool takes **efficiency and panel area from the 3D model file**, and we are
using a stock Anik F1 model. Its absolute wattage will therefore not match Eq. (12)'s 3,387 W
and should not be forced to. The meaningful cross-check from Figure 10 is the **eclipse
duration**, which depends only on the orbit and epoch, both of which are genuinely MESA's.
Write the power comparison up honestly, noting the model-file dependence.

---

## 2 Aug 2026, Windows bootstrap session

**Machine:** Jordan's Windows 11 Home, x86-64. First session on this machine, picking up the
handoff written at the end of the macOS session.

**Outcome:** everything that does not require STK is done and verified. The task is blocked
on getting STK installed, which needs an authenticated Ansys/AGI login.

### Repo state

Repo was already cloned at `C:\Users\jclay\Desktop\main\code\spce5065`. No clone needed.

- Branch `main`, working tree clean
- HEAD at `c28a4ec`, "Make the handoff self-bootstrapping on Windows"
- Read `CLAUDE.md` and `./memory/MEMORY.md` per project convention

### STK is not on this machine (confirmed, do not re-check)

Checked every location in HANDOFF Section 3.2 plus a few more. All negative:

| Check | Result |
|:---|:---|
| `C:\Program Files\AGI` | absent |
| `C:\Program Files\Ansys Inc` | absent |
| `C:\Program Files (x86)\AGI` | absent |
| Uninstall registry, both HKLM hives, matching `STK\|AGI\|Ansys\|Systems Tool` | no entries |
| `winget search STK`, `Satellite Tool Kit`, `Ansys` | "No package found matching input criteria" |
| Chocolatey | not installed |
| `E:\Program Files` and `E:\Program Files (x86)` | present but no AGI/Ansys/STK (E: is an old Windows image) |
| `D:\` | empty |
| Downloads, Desktop, Documents scanned for a staged installer | nothing |

This confirms the handoff's prediction: the STK download sits behind a logged-in
Ansys/AGI session and cannot be scripted.

### Installed

- **Pandoc 3.10** via `winget install JohnMacFarlane.Pandoc`.
  Note the install path is **not** on `PATH` in this shell. Full path:
  `C:\Users\jclay\AppData\Local\Pandoc\pandoc.exe`
- Python 3.11.0, numpy 2.3.3, matplotlib 3.10.8 were already present. No venv needed yet;
  one will be needed only for the `agi.stk12` wheel after STK installs.

### Verified (HANDOFF Section 9 pipeline, proven end to end)

Ran the full verification chain so nothing is unknown when the STK figures land:

| Check | Result |
|:---|:---|
| `python spce5065_ms2_figs.py` | exit 0, clean |
| Headline numbers reproduced | array BOL 3,387 W, EOL 2,984 W, max eclipse 69.4 min, EOL margin 68.3%, TID 25 krad(Si) over 5 yr |
| Docx rebuild via pandoc 3.10 | succeeds |
| `word/media/` image count | **9**, cover image intact |
| Em dashes and en dashes in the .md | **0** |
| Mentions of professor/instructor/lecturer | **0** |

**Figure drift, handled.** Running the analysis script rewrote figures 2 and 4 through 8 with
byte-level differences (matplotlib version rendering, not a numbers change). Reverted with
`git checkout --` so the tree matches the state the report was verified against. Working tree
is clean.

**Reminder for the finish line:** after Figures 9 to 11 are added, the image count must be
**12**, not 9. That check is worth 5 rubric points and pandoc fails it silently.

### Created

- `submission/stk/` (the directory did not exist; git does not track empty directories)
- `submission/stk/build_mesa_scenario.py`, a pre-written build script carrying the full MESA
  parameter card. Steps 1 to 3 (scenario, satellite, Two-Body orbit) use well documented
  Connect syntax. Steps 4 onward, plus the snapshot command, are marked as needing
  verification against the local Connect Command Library, since guessed Connect syntax fails
  silently. Every uncertain command is flagged `optional=True` so it reports and continues
  rather than dying, and the script prints the GUI fallback for each.
- `scratchpad/uccs_it_stk_request.md`, the drafted UCCS IT email (see below)

### Decision taken

Asked Jordan how to obtain STK. He chose **both routes in parallel**: register for STK Free
immediately for speed, and send the UCCS IT request as the backstop.

Reason for running both: the free tier may not expose the Solar Panel Tool and the Lifetime
Tool, which are exactly what the graduate requirement asks for. A campus license is far more
likely to include them but is slower, and Milestone 2 is already past due. Running both costs
one extra email and loses no time.

The IT email deliberately asks two questions up front to avoid a multi-day round trip:
whether the campus tier covers Component Browser Power Sources, Solar Panel Tool, and
Lifetime Tool; and what is required if licensing depends on a network license server, given
that Windows 11 **Home** cannot join a domain.

### Blocked on

1. **Jordan:** create the free Ansys account, download the STK installer, hand over the path.
2. **Jordan:** send the UCCS IT request.

Nothing else is blocking. Once an installer path exists, the next session should read the
installer's silent-install flags (`setup.exe /?`) rather than guessing them, install, then
install the `agi.stk12` wheel from `<STK install>\bin\AgPythonAPI\` into a venv.

### First thing to check once STK opens

Per HANDOFF Section 3.4, confirm these three exist and are not greyed out, **before**
building anything:

1. Utilities, Component Browser, Power Sources
2. Satellite menu, Solar Panel Tool
3. Satellite menu, Lifetime Tool

If any is missing, the license tier does not cover it. Stop and tell Jordan immediately
rather than working around it, since that moves the whole task onto the IT route.

### Still to do (unchanged from HANDOFF)

- Build the MESA scenario, epoch 20 Mar 2027 (the equinox epoch is what makes the eclipse
  appear at all)
- Capture `fig9_stk_3d.png`, `fig10_stk_power.png`, `fig11_stk_lifetime.png`
- Export `MESA_MS2.vdf`, or a zipped scenario folder verified to open from another directory
- Add Section 12.3 to the report with the three cross-checks recorded honestly
- Update Revision Log item 1 (currently credits the 3D fix to matplotlib)
- Rebuild the docx and re-run every check in HANDOFF Section 9, with the image count at 12
