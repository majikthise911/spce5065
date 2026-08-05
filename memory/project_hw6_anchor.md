---
name: project_hw6_anchor
description: SPCE 5065 HW6 (vacuum environment) pipeline result plus the thermal-balance and outgassing conventions worth reusing
metadata:
  node_type: memory
  type: project
---

HW6 (wk06, vacuum environment: solar UV, thermal control, outgassing, contamination) run through the full pipeline, self-graded **96/100** on the first pass, no revision cycles. Files in `wk06/hw/`: `Clayton_spce_5065_hw6_submission.md`, `spce_5065_hw6_solution.py`, `spce_5065_hw6_walkthrough.md`, `figures/walkthrough_figs.py`.

**Two assignment-sheet corrections that matter:**
- `wk06/hw/Homework 6-1.pdf` is stale. The current version is `wk07/hw/Homework 6-3.pdf` (+ `.md`), and `wk06/hw/message.txt` carries the fix: **heaters are 0.025 kg/W, not kg/m^2** (Problem 5). The Lesson 6 deck slides 44-47 still print the wrong unit.
- Problem 8's "10 m x 10 cm" specimen is a typo for 10 cm x 10 cm, but it does not change the answer: the result is a rate per unit area, so scaling one dimension scales mass and area together.

**Conventions verified against Lesson 6 Part 1 and the wk6 lecture:**
- **Thermal balance (slides 28-30):** `Q_solar = alpha*A*S`, `Q_albedo = alpha*A*sin^2(rho)*(a_geo*S)`, `Q_IR = alpha*A*sin^2(rho)*F_IR`, `sin(rho) = R_p/(R_p+h)`, out = `eps*sigma*A_total*T^4`. **One face in per source, all six faces out.** The course writes the IR term with alpha, not eps; flag the Kirchhoff objection but keep alpha, and verify the answer set does not change (for HW6 it does not).
- **Planetary albedo/IR table is slide 31**, and albedo flux = geometric albedo x local solar flux (so Earth is 0.37*1367 = 506, not the 465 quoted on slide 30).
- **When absorptivity is not given, use alpha = eps** (Kirchhoff). This is the course's explicit instruction and the entire HW6 P5 design rests on it for MLI (alpha = 0.05).
- **Outgassing:** a torr-liter is a pressure-volume, i.e. energy. `1 torr-L/(cm^2 s) = 1333.22 W/m^2`, so `1 W/m^2 = 7.50e-4 torr-L/(cm^2 s)` (this IS what P6a asks you to "show"). Molecules: `N_dot = Q_dot/(kT)` (Pisacane Eq. 10.1). Cross-check against Pisacane Table 10.2 (296 K factor) and Table 10.3 (Kapton foil at 1e-4 W/m^2).

**Headline results:** lambda_max = 0.357 um for a 3.47 eV C-C bond; 1.13e16 bond-breaking photons/cm^2/s (3.3% of the solar total); Planck runs 41% high in that band because the real Sun's UV is line-blanketed. Baseline Eris probe images **Venus, Earth, Mars only**; outer planets miss the -35 C limit by ~1 C because 750 W of internal heat sets a -36.3 C floor. The $15K budget is **0.60 kg**, which kills louvers (2.3 kg) outright; the winning design is MLI on the sun and nadir faces plus white paint on the other four, and it gets all nine bodies inside limits at exactly $15,000.

**Process notes:** Problem 1 presenters came from the wk06 deck slides 3-6 as [[feedback_current_events_presenters]] requires (Garrett Kennedy, Jordan Clayton, Nick Dankel, Paige Mauldin), and one of them is Jordan himself, so that write-up is first-person about his own talk. Problem 9 references were verified by web search before citing (ASETS-II OHP flight experiment). Related: [[project_hw5_anchor]], [[feedback_references]], [[feedback_conciseness]].
