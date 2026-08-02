---
name: project_ms2_anchor
description: MESA design-project Milestone 2 anchor, the frozen vehicle configuration and headline results the final report must build on
metadata:
  node_type: memory
  type: project
---

Milestone 2 (written 2 Aug 2026, submitted late; the sheet said due 7/29) is a **cumulative** report: corrected MS1 Sections 1 to 7 plus new Sections 8 to 13. The final report is cumulative again, so it continues from this document, not from MS1.

**The MS2 rubric is not the MS1 rubric.** 100 pts: cover 5, intro 5, corrections to MS1 in cumulative format 10, TCS 10, plasma 15, radiation 15, ADACS 10, simulations 10, conclusions 5, references 5, grammar 10. Plasma and radiation are the heavyweight sections and each explicitly wants risks + mitigations + **impact on the other subsystems** (that third part is easy to forget and is worth real points).

**The MESA configuration is now frozen** (MS1 had only mass). Every later section must use these or restate them:
bus 1.8 x 1.8 x 3.5 m, wet 2,000 kg, arrays 2 x 5.12 m2 = 10.24 m2, illuminated area 16.54 m2, bus radiating area 31.68 m2, Ix/Iy/Iz = 3,279 / 2,452 / 1,893 kg m2, cp-to-cm 0.25 m, residual dipole 5 A m2, Q_int 1,200 W.

**Headline results** (all reproduced by `design_project/milestone2/submission/spce5065_ms2_figs.py`, which prints every number in the report):
- TCS: 4.9 m2 OSR radiator, T_sun = +36.3 C, T_eclipse = -13.1 C, 49.4 K swing, 260 W heaters
- Plasma: floating potential -2.16 kV (reused from HW4)
- Radiation: 25 krad(Si) over 5 yr, 2x margin, RHA category R parts (Pisacane Table 9.9)
- ADACS: SRP is 93.5% of the 3.21e-5 N m total disturbance torque; wheels sized 0.20 N m
- Power: 3,387 W BOL, 2,984 W EOL, 69.4 min equinox eclipse, power-limited life 25.6 yr

**Two design ideas that carry the report and should survive into the final:** docking, not free flight, sizes the ADACS (a 3,000 kg client raises Ix by 5.3x), and the docking interface creates a charging failure mode no conventional satellite has (two independently charged vehicles bonded through the capture latch), which is why MESA carries a plasma contactor.

**Best sources, all in-repo:** SMAD Ch. 11 disturbance-torque formulas are `wk07/course_material/SMAD Chapter 11.1.pdf` Table 11.10 (p. 27) with wheel sizing in Table 11.7; the wheel **mass and power** lookup the course actually wants is `Week 7 - Radiation Environment Part 2.pptx` slide 11, not SMAD Table 11.12 (the two disagree). Pisacane radiation Ch. 9 Tables 9.1/9.2/9.6/9.9 and thermal Ch. 12 are the citable textbook. HW6 P4 fixes the course convention for equilibrium temperature (absorb on projected area, emit from all sides, include Q_int, albedo and planetary IR).

**Why:** MS2 is the spine of the final report and re-deriving the configuration would silently change every downstream number.

**How to apply:** before the final report, run the script first and pull numbers from its console output; never retype them. Related: [[feedback_references]], [[feedback_docx_cover_image]], [[project_hw4_anchor]].
