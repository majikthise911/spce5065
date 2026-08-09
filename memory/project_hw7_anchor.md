---
name: project_hw7_anchor
description: SPCE 5065 HW7 (radiation environment) pipeline result, the Mars dose-budget conventions, the Starlink cp/cg frame trick, and the deck-vs-transcript presenter name correction
metadata:
  node_type: memory
  type: project
---

HW7 (wk07, radiation environment: Mars mission dose budget, gamma attenuation, SRP torque, disturbance torque ranking) run through the full pipeline, self-graded **91 -> 95 -> 98**. The 95 pass still had Problem 1 stubbed; the 98 came after Jordan supplied the wk07 lecture transcript and all four current-events writeups were completed. Files in `wk07/hw/`: `Clayton_spce_5065_hw7_submission.md`, `spce_5065_hw7_solution.py`, `spce_5065_hw7_walkthrough.md`, `figures/walkthrough_figs.py`.

**Problem 1 presenters, and a name correction worth remembering.** The wk07 deck (`Week 7 - Radiation Environment Part 1.pptx`, slides 2-5) lists **Jason Ansley, Fanita Pfau, Rachel Danover, Moyiwa Adewumi**, but the lecture transcript (`wk07/course_material/wk7_lecture_transcript.vtt`, added by Jordan after the first pipeline run) shows the fourth presenter introducing himself as **Emmanuel Adeyomi**, and the instructor names him the same way while sharing his screen. **The deck slide was stale; the transcript won.** Auto-captions do mangle names (Pfau appears as "Phel" throughout), but "Moyiwa" to "Emmanuel" is not a caption error. Lesson for [[feedback_current_events_presenters]]: the deck is authoritative for *who is scheduled*, the transcript is authoritative for *who actually presented*. Cross-check both when they exist.

Talk content, for reuse: Ansley = damage physics + Juno/JunoCam annealing recovery; Pfau = mission assurance for SpaceX's orbital AI data center (AI1: 150 kW, 72 chips, 98% sunlight; FCC "accepted for filing" for up to 1M sats at 500-2000 km is NOT radiation qualification; one constellation spanning that range cannot share one qual case; **her video cut out partway, instructor called it "three and a half presentations" and posted it to Canvas**); Danover = full single-event taxonomy (SEU/SET/SEL/SEB/SEGR) + Van Allen Probes case study (launched 30 Aug 2012, 34 krad design, 2-yr design life lasted 6, command loss timer, individually power-cyclable components, EDAC + hardware scrubbing, 0.5 mm solar panel coating); Adeyomi = materials and program trades (aluminum makes secondaries, polyethylene better vs protons, Solar Cycle 25 near peak, Artemis driving forecasting demand).

**Physics conventions worth reusing:**

- **Van Allen belt dose is a rate-times-dwell product.** Time per Earth radius at the given 25,000 km/hr is `6378/6.9444 = 918.43 s`. One crossing = 16.008 rad, round trip = 32.02 rad. The blue band is the *widest* (1.8 Re) and contributes almost nothing; orange (1.0 Re) dominates. The red row has zero path length because the Apollo track deliberately skirts the inner belt core.
- **RBE table is Lesson 7 Part 1 slide 21:** EM radiation at Earth 1, radiation belts 5 to 7, charged particles 10. The 60 REM career limit is slide 22 / NASA-STD-3001 (600 mSv).
- **The assignment's Mars map (Figure 4) is already in rem/yr**, so it does NOT get multiplied by RBE again. Easy 10x error.
- **The shield trade has no winning answer, and that IS the answer.** Digitizing HW Figure 2 gives GCR essentially flat (21 rad/yr at 0.01 g/cm^2 down to only 7 at 100) while SCR 50% falls 5 orders of magnitude over the same range. Design point 10 g/cm^2 (the knee). Mission total 472 REM = 7.9x the limit, and even 100 g/cm^2 (145 t of shielding) only reaches 262 REM. State plainly that no practical passive shield complies.
- **Bracket an alarming number from both sides.** MSL/RAD flight data (1.8 mSv/day cruise, 0.64 mSv/day surface) gives ~106 REM, and Apollo 11's measured 0.18 rad total shows the belt line is an unshielded free-space number. Both still exceed 60 REM, so the conclusion is robust. This cross-check is what earned the insight bonus.
- **Trajectory:** 2035 Burke Type 1, depart 21 Apr 2035 (C3 = 10.19 km^2/s^2), 196 d out, 539 d surface (DRA 5.0 fast-conjunction), 201 d back, 936 d total. Earth-Mars synodic period 779.9 d is what fixes the surface stay, not mission objectives.

**Problem 4 (Starlink SRP) coordinate-frame trick, the thing that makes the problem solvable:** the given "center of pressure of 6.03 m" has no stated origin. Put `x = 0` at the **outboard tip of the array**, array 0 to 10.9 m (centroid 5.45), bus 10.9 to 12.1 m using the **3.2 x 1.2 = 3.84 m^2** face (not 3.2 x 1.6). The area-weighted centroid then reproduces **6.05 m**, confirming the frame. cg = 6.250 m, arm = 0.220 m, F = 2.823e-4 N, T = 6.198e-5 N-m. Headline insight: the array holds 90% of the area AND 87% of the mass, so cp and cg nearly coincide; swapping the masses grows the arm to 4.67 m (21x).

**Problem 4b:** size on BOTH torque authority (`M_RW = T_D(1+margin)`, 100% margin -> 1.24e-4 N-m) and momentum storage (secular for a sun-pointing bus: `h = T_D * t_sunlit`, worst-case sunlit fraction `1 - arcsin(R_E/r)/pi = 0.628`, giving 0.45 N-m-s/orbit with margin). Wheel table (Lesson 7 Part 2 slide 11) puts this in small-sat class: 5 kg, 10 W per wheel.

**Problem 5 numbers** (same Starlink bus, theta = 10 deg, D = 1 A-m^2, Cd = 2.2): LEO 550 km GG 1.784e-3 > aero 1.218e-4 > SRP 6.198e-5 > mag 4.788e-5; GEO SRP 6.198e-5 > GG 7.913e-6 > mag 2.124e-7 > aero <= 8.8e-12. Total ratio ~29. **Internal check:** GG and magnetic both scale R^-3 so their LEO/GEO ratios must both equal `(42164/6928)^3 = 225.4`. SRP overtakes GG at r = 21,230 km.

**Process notes:**
- Grader pass 1 (91) flagged uncited external values. Fixed by pulling atmospheric density from the **course power law the class has used since HW2**, `rho = 1.020e7 * h^-7.172 kg/m^3` (Braeunig), giving rho(550 km) = 2.263e-13. Reuse this instead of quoting a random published density.
- **Figure numbering gotcha:** the caption is rendered onto the PNG by the script, so if the submission reorders figures, the on-image caption number must be changed in the script too, not just the markdown. Renaming the PNG to match the document number is the safe habit.
- A reusable renumber-by-first-appearance script pattern is worth rebuilding each time (parse `[n]` order in the body, remap, reorder the Sources list, error if a source is uncited or a citation has no source). It caught two out-of-order refs that would have cost points per [[feedback_references]].

Related: [[project_hw6_anchor]], [[feedback_references]], [[feedback_conciseness]], [[feedback_current_events_presenters]].
