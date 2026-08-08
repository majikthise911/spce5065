---
name: project_final_exam_anchor
description: SPCE 5065 Final Exam (Summer 2026) run through the pipeline; self-graded 95, with the thermal and albedo judgment calls worth reusing
metadata:
  type: project
---

Final exam (`final_exam/SPCE 5065 Final Summer 2026.pdf`, 12 pages, 100 pts + 5 bonus) run through the full `prompts/0_master_workflow_prompt.md` pipeline on 8 Aug 2026. Self-graded **95/100 on the first pass**, no revision cycles. Files in `final_exam/`: `Clayton_spce_5065_final_submission.md`, `spce_5065_final_solution.py`, `spce_5065_final_walkthrough.md`, `figures/` (4 submission + 3 walkthrough figures, `figures/walkthrough_figs.py`).

**Structure** (template for future 5065 finals): P1 T/F x10, P2 MC x5, P3 GEO 215 THz sensor, P4 solar-cycle flux table, P5 bond energy to wavelength, P6 plasma frequency at 1000 km, P7 CubeSat hazard ranking, P8 K-band excess range, P9 thermal design (15 pts, the big one), P10 MMOD survivability, P11 bonus derivation.

**Judgment calls that were right and are worth reusing:**

- **Albedo flux 465 W/m^2, not 0.37 x 1367 = 506.** Lesson 6 slide 30 states 465 directly for Earth; slide 31's geometric-albedo rule is for *other planets* (that is why HW6, which covered nine bodies, used 506, see [[project_hw6_anchor]]). Using 465 lands P9's sunlit case at **15.26 C** against a 15 C battery ceiling, which is far too well-designed to be coincidence. Rule: for an Earth-only thermal problem use 465; for other planets use geometric albedo x local solar flux. Always report the sensitivity (506 gives 16.5 C, same conclusion).
- **P9 has no passive solution, and proving that is the answer.** Solving the two bounds shows the four changeable sides would need eps = 0.879 for the hot case (max available is black paint at 0.874) and that the two *fixed* black faces alone already exceed the eps*A allowed for a 0 C eclipse. So heaters are mandatory and the coating choice cannot fix both ends. Recommendation: louvers (eps 0.05 to 0.8) + 304 W heaters, 16.8 kg, **$420,000**, giving 19.5 C sun / 0.0 C eclipse. MLI is cheaper ($220K) and a trap (96 C in sun).
- **P4 trapped protons are the only row that runs anti-correlated** (higher at solar min): GCRs feed them via CRAND and are suppressed at solar max, while the puffed-up thermosphere increases the loss rate. Electrons, GCRs, and SPEs all follow the obvious direction.
- **P3 is an atmosphere question wearing a plasma costume.** 215 THz = 1.394 um, which sits at the bottom of the 1.35 to 1.45 um H2O band, while the worst ionospheric cutoff anywhere is 19 MHz (F2 peak, day/solar max), 1.1e7 times lower. Verdict: not effective; move to the 1.55 to 1.75 um window.
- **Run the drag number before ranking hazards.** The first P7 draft ranked drag #1 at 550 km; integrating `dR/dt = -(rho/BC)sqrt(mu R)` with a 3U BC of 61 kg/m^2 gives only **40 km lost over 5 years**, so the ranking was corrected to radiation > neutral > plasma. The exam1 memory's "-459 km over 5 yr at 550 km" figure does not reproduce with the `rho = 1.02e7 * alt_km^-7.172` fit; trust a fresh integration.

**Other headline numbers:** P5 lambda_max = hc/1.67 eV = 742.4 nm, 55% of a 5900 K solar spectrum (53 to 56% across 5778 to 6000 K). P6 f_p = 0.9 to 2.6 MHz at 1000 km. P8 worst case = lowest band edge (18 GHz) with TEC 1e18: 12.44 cm / 0.415 ns vertical, x3 for a horizon-grazing slant. P11 bonus: `Rdot = 2*Vdot*sqrt(R^3/mu) = 2*Vdot/n`, verified by substituting a drag deceleration and recovering `-(rho/BC)sqrt(mu R)` exactly.

**Two T/F items worth remembering:** REM = RAD x RBE with **RBE 5 to 7 in the belts** (Lesson 7 slide 21), so (e) is FALSE; and the MMOD damage table puts **1 mm at "serious damage"** (Lesson 5 MMOD_1 slide 21), so (j) is FALSE.

**Process notes:** the `.pptx` decks were mined with python-pptx for text and LibreOffice (`soffice --headless --convert-to pdf`) for the slides whose content is embedded images (the thermal equations, the planet albedo table). The exam's own charts were read by rendering the PDF with `pdftoppm -r 300` and cropping. Applies [[feedback_exam_allowed_resources]] (only lessons, Tribble, SMAD, Canvas; zero external URLs), [[feedback_no_em_dashes]], [[feedback_no_professor_mentions]], [[feedback_conciseness]]. Related: [[project_exam1_anchor]], [[project_hw6_anchor]].
