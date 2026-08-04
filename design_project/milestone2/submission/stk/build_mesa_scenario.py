"""
Build the MESA scenario in STK 13 for SPCE 5065 Milestone 2.

Every value here comes from the report, so the scenario and the written analysis
agree. See STK_MESA_scenario_guide.md for the GUI equivalent of each step.

Environment (already set up on this machine):
    STK 13.1.0 (2026R1) at C:\\Program Files\\AGI\\STK_ODTK 13
    venv at <repo>\\.venv with agi_stk13 installed from
    C:\\Program Files\\AGI\\STK_ODTK 13\\bin\\AgPythonAPI\\agi_stk13-13.1.0-py3-none-any.whl

    <repo>\\.venv\\Scripts\\python.exe build_mesa_scenario.py

Connect syntax below was read from the installed Connect Command Library
(Help\\STK\\SubSystems\\connectCmds\\Content), not guessed:
    cmd_SetState.htm, cmd_SetLifetime.htm, cmd_Lifetime.htm, cmd_VOSnapFrame.htm

KNOWN LIMITATION, verified against the local help:
    The Solar Panel tool has NO Connect command and no object model interface.
    Its only entry point is the GUI (Satellite menu, Solar Panel...). It works by
    animating the scenario and pixel-counting the illuminated panel area, so it is
    inherently tied to the 3D window. Figure 10 therefore has to be captured from
    the GUI. Everything else here is scripted.
"""

import os
import sys
import time

# ---------------------------------------------------------------------------
# MESA parameter card. Do not change these without changing the report.
# ---------------------------------------------------------------------------

SCENARIO_NAME = "MESA_MS2"
EPOCH_START = "20 Mar 2027 00:00:00.000"   # vernal equinox, worst-case eclipse
EPOCH_STOP = "21 Mar 2027 00:00:00.000"    # exactly one day
STEP_SEC = 60

SMA_M = 42164137.0        # semi-major axis, meters. Report Eq. (1)
ECC = 0.0
INC_DEG = 0.0
ARG_PERIGEE_DEG = 0.0
RAAN_DEG = 0.0
# Places the subsatellite point at 105 deg W at epoch (report Section 6).
# The 255.0 deg in the original guide was wrong: it puts MESA at 78.05 deg E,
# almost exactly half an orbit away. Verified against STK's LLA State data
# provider, which reports -105.0000 deg with this value.
TRUE_ANOMALY_DEG = 71.9539

SUBSAT_LON_DEG = -105.0    # 105 deg W, report Section 6

WET_MASS_KG = 2000.0      # Table 3
ARRAY_AREA_M2 = 10.24     # Table 3, two wings
DRAG_AREA_M2 = 16.54      # Table 3, illuminated area
CD = 2.2                  # Section 7
CR = 1.0

# Lockheed Martin A2100, a GEO communications bus with two deployed wings. This
# is a good analogue for MESA (a GEO servicing tug built on a comsat bus) and,
# unlike Space/anik_f1.glb, it SHIPS WITH a working AGI_stk_metadata
# solarPanelGroups block, so the Solar Panel tool's group list is populated.
#
# anik_f1.glb has no solarPanelGroups at all, which is why that group box came up
# empty. Stock a2100.glb declares:
#     "solarPanelGroups": [{"efficiency": 14, "name": "a2100"}]
# so the group appears as "a2100" at 14% efficiency.
#
# Using the stock file rather than a modified copy avoids having to install a
# model into Program Files. The efficiency difference from MESA's 24.3% is
# recorded honestly in the report rather than being papered over; see the note in
# GUI_STEPS_fig10_fig11.md about what the Solar Panel figure can and cannot prove.
#
# Use the RELATIVE form here: absolute paths silently fail to load.
MODEL_FILE = "Space/a2100.glb"

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_3D = os.path.join(OUT_DIR, "fig9_stk_3d.png")
LIFETIME_TXT = os.path.join(OUT_DIR, "lifetime_result.txt")


def main():
    from agi.stk13.stkdesktop import STKDesktop

    print("=" * 70)
    print("MESA_MS2 SCENARIO BUILD  (STK 13)")
    print("=" * 70)

    # Reuse an already-open STK if there is one, otherwise start it.
    try:
        stk = STKDesktop.AttachToApplication()
        print("\nAttached to the running STK instance.")
    except Exception:
        print("\nStarting STK...")
        stk = STKDesktop.StartApplication(visible=True, userControl=True)
    root = stk.Root

    results = {}

    def cmd(command, optional=False):
        """Run a Connect command and return its result lines."""
        try:
            res = root.ExecuteCommand(command)
            out = [res.Item(i) for i in range(res.Count)]
            print("  ok   " + command[:88])
            return out
        except Exception as exc:
            tag = "  SKIP " if optional else "  FAIL "
            print(tag + command[:88])
            print("         " + str(exc).strip().replace("\n", " ")[:180])
            if not optional:
                raise
            return None

    # -- 1. Scenario ------------------------------------------------------
    print("\n[1] Scenario")
    try:
        root.CloseScenario()
    except Exception:
        pass
    root.NewScenario(SCENARIO_NAME)
    root.CurrentScenario.SetTimePeriod(EPOCH_START, EPOCH_STOP)
    root.Rewind()
    print("  %s : %s -> %s" % (SCENARIO_NAME, EPOCH_START, EPOCH_STOP))

    # -- 2. Satellite and orbit -------------------------------------------
    #
    # Built through the object model, NOT the Connect SetState command.
    # SetState was silently producing a satellite that did not propagate: its
    # inertial position moved only 8 km across a whole day while sitting at the
    # right 42,164 km radius, so the fixed-frame longitude drifted westward at
    # Earth's sidereal rate and the vehicle was not geostationary at all.
    # The object model path below propagates correctly and is verified at the
    # end of this step.
    print("\n[2] Satellite MESA, Two-Body at GEO")
    from agi.stk13.stkobjects import (
        AgESTKObjectType, AgEVePropagatorType, AgECoordinateSystem,
        AgEClassicalSizeShape, AgEClassicalLocation, AgEOrientationAscNode,
        AgEOrbitStateType,
    )

    root.UnitPreferences.SetCurrentUnit("DistanceUnit", "km")
    sc = root.CurrentScenario

    sat = sc.Children.New(AgESTKObjectType.eSatellite, "MESA")
    sat.SetPropagatorType(AgEVePropagatorType.ePropagatorTwoBody)
    prop = sat.Propagator
    prop.EphemerisInterval.SetExplicitInterval(EPOCH_START, EPOCH_STOP)
    prop.Step = float(STEP_SEC)

    rep = prop.InitialState.Representation
    classical = rep.ConvertTo(AgEOrbitStateType.eOrbitStateClassical)
    classical.CoordinateSystemType = AgECoordinateSystem.eCoordinateSystemICRF
    classical.SizeShapeType = AgEClassicalSizeShape.eSizeShapeSemimajorAxis
    classical.SizeShape.SemiMajorAxis = SMA_M / 1000.0
    classical.SizeShape.Eccentricity = ECC
    classical.Orientation.Inclination = INC_DEG
    classical.Orientation.ArgOfPerigee = ARG_PERIGEE_DEG
    classical.Orientation.AscNodeType = AgEOrientationAscNode.eAscNodeRAAN
    classical.Orientation.AscNode.Value = RAAN_DEG
    classical.LocationType = AgEClassicalLocation.eLocationTrueAnomaly
    classical.Location.Value = TRUE_ANOMALY_DEG
    rep.Assign(classical)
    prop.Propagate()
    print("  propagated: a=%.3f km, e=%.1f, i=%.1f deg, TA=%.4f deg"
          % (SMA_M / 1000.0, ECC, INC_DEG, TRUE_ANOMALY_DEG))

    # Verify it really is geostationary at the report's slot before going on.
    lla = sat.DataProviders.Item("LLA State").Group.Item("Fixed").Exec(
        EPOCH_START, EPOCH_STOP, 14400)
    lons = lla.DataSets.GetDataSetByName("Lon").GetValues()
    spread = max(lons) - min(lons)
    print("  subsatellite longitude : %.4f deg (target %.1f)" % (lons[0], SUBSAT_LON_DEG))
    print("  longitude spread / day : %.4f deg (must be ~0 for geostationary)" % spread)
    if abs(lons[0] - SUBSAT_LON_DEG) > 0.05 or spread > 0.05:
        raise SystemExit(
            "Orbit is not geostationary at %.1f deg. Stopping rather than "
            "producing figures from a wrong scenario." % SUBSAT_LON_DEG)

    # -- 3. 3D model, grad requirement bullet 1 ---------------------------
    print("\n[3] 3D model and graphics")
    cmd('VO */Satellite/MESA Model File "%s"' % MODEL_FILE, optional=True)
    cmd('VO */Satellite/MESA OrbitDisplay Show On', optional=True)
    cmd('Graphics */Satellite/MESA Basic Show On', optional=True)

    # -- 4. Lifetime parameters (grad requirement bullet 3, second half) --
    print("\n[4] Lifetime parameters")
    cmd('SetLifetime */Satellite/MESA DragCoeff %s' % CD)
    cmd('SetLifetime */Satellite/MESA DragArea %s' % DRAG_AREA_M2)
    cmd('SetLifetime */Satellite/MESA SunArea %s' % ARRAY_AREA_M2)
    cmd('SetLifetime */Satellite/MESA ReflectCoeff %s' % CR)
    cmd('SetLifetime */Satellite/MESA Mass %s' % WET_MASS_KG)
    # Bound the run so it terminates instead of grinding: at GEO it will not decay.
    cmd('SetLifetime */Satellite/MESA LimitType Duration', optional=True)
    cmd('SetLifetime */Satellite/MESA DurationLimit 36500', optional=True)  # 100 yr

    # -- 5. Compute lifetime ----------------------------------------------
    print("\n[5] Lifetime computation (expect NO DECAY at GEO)")
    life = cmd('Lifetime */Satellite/MESA', optional=True)
    if life:
        results["lifetime"] = life
        for line in life:
            print("      > " + str(line))
        with open(LIFETIME_TXT, "w", encoding="utf-8") as fh:
            fh.write("STK 13 Lifetime tool result for MESA\n")
            fh.write("Scenario: %s, epoch %s\n" % (SCENARIO_NAME, EPOCH_START))
            fh.write("Cd=%s, DragArea=%s m2, SunArea=%s m2, Cr=%s, mass=%s kg\n\n"
                     % (CD, DRAG_AREA_M2, ARRAY_AREA_M2, CR, WET_MASS_KG))
            for line in life:
                fh.write(str(line) + "\n")
        print("      saved -> %s" % LIFETIME_TXT)

    # -- 6. 3D snapshot, Figure 9 -----------------------------------------
    # Syntax from cmd_VOSnapFrame.htm:
    #   VO * SnapFrame SetValues Format {BMP|JPEG|PNG|TIF}
    #   VO * SnapFrame SetValues AntiAlias On FXAA
    #   VO * SnapFrame ToFile "<path>"
    print("\n[6] 3D snapshot -> Figure 9")
    root.Rewind()
    time.sleep(3)  # let the 3D window finish drawing before grabbing a frame
    cmd('VO * SnapFrame SetValues Format PNG', optional=True)
    cmd('VO * SnapFrame SetValues AntiAlias On FXAA', optional=True)
    if os.path.exists(FIG_3D):
        os.remove(FIG_3D)
    cmd('VO * SnapFrame ToFile "%s"' % FIG_3D, optional=True)
    time.sleep(2)
    print("  fig9 written: %s" % os.path.exists(FIG_3D))

    # -- 7. Save -----------------------------------------------------------
    print("\n[7] Save scenario")
    # Syntax is: SaveAs <ApplicationPath> <ObjectPath> "<FilePath>".
    # The object path (*) is required; omitting it fails.
    sc_path = os.path.join(OUT_DIR, SCENARIO_NAME, SCENARIO_NAME)
    os.makedirs(os.path.dirname(sc_path), exist_ok=True)
    cmd('SaveAs / * "%s"' % sc_path, optional=True)

    print("\n" + "=" * 70)
    print("REMAINING, GUI only (the Solar Panel tool has no Connect command):")
    print("  Satellite menu -> Solar Panel..., Compute over the scenario interval,")
    print("  then Graph/Power -> Generate, and capture fig10_stk_power.png")
    print("=" * 70)


if __name__ == "__main__":
    main()
