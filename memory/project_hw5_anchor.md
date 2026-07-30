---
name: project_hw5_anchor
description: SPCE 5065 HW5 (MMOD) pipeline result, the corrected Grun flux/shielding conventions, and the Whipple textbook inconsistency
metadata:
  node_type: memory
  type: project
---

HW5 (wk05, micrometeoroids and orbital debris) run through the full pipeline, self-graded **97/100** after three revision passes (86 -> 93 -> 94 -> 97). Submission `wk05/hw/Clayton_spce_5065_hw5_submission.md`, script `spce_5065_hw5_solution.py`, walkthrough `spce_5065_hw5_walkthrough.md` plus `spce_5065_hw5_walkthrough_figures.py`.

**Physics conventions worth reusing (all verified against the decks and Pisacane Chap. 11):**

- **Grun sporadic flux, Lesson 12 slide 4.** `F_spo = 3.15576e7 * [F1 + F2 + F3]`, m in grams, result per m^2 per year. **The slide misprints the third term as F2**; it is F3 (Pisacane Eq. 11.2). Instructor clarification for this HW says explicitly to use the Lesson 12 slide 4 / Pisacane version because Tribble's is wrong.
- **Earth shielding has three branches** (Pisacane Eqs. 11.3-11.5) with `sin(theta) = R_a/r`, `R_a = R_E + 100 km = 6478 km` per the clarification: chi_1 = 1, chi_2 = (1+cos theta)/2 (random orientation), chi_3 = cos theta. **The course directs chi_3 = cos theta for Earth orbiters** (Lesson 12 slide 5, and the wk05 video near line 5660). Carrying chi_2 as a sensitivity case is what earned credit, because the branch changes the ISS answer by 2.2x.
- **Counterintuitive geometry worth remembering:** "total Earth in field of view" is HARDEST to satisfy in LEO. Earth disc half-angle is 72.9 deg at ISS (normal must be within 17.1 deg of nadir) vs 8.8 deg at GEO (normal may be 81.2 deg off nadir). An earlier draft argued this backwards and lost points.
- **Gravitational focusing** `G = 1 + R_a/r` peaks in LEO too and nearly cancels the shielding, so **net micrometeoroid flux is close to orbit-independent** (net chi*G: ISS 0.575 nadir / 1.266 random, GPS 1.206, GEO 1.140). That is the headline result and it is the opposite of man-made debris behaviour.
- **Poisson:** `p = 1 - exp(-F*A*t)`. For small p, the time to reach probability p is just p times the mean time between impacts, so the 0.01% waiting time is 1e-4 * (1/FA). Report both columns, since the question wording admits either reading.
- **Whipple (Pisacane Eqs. 11.27-11.31, book pp. 341-342 = PDF pp. 23-24).** Units are cm, g, g/cm^3, km/s, and **ksi** with no conversion. `t_b = c_b*d*rho_p/rho_b`, `t_w = c_w*d^0.5*m_p^(1/3)*(rho_p*rho_b)^(1/6)/rho_w * S^-0.75 * (sigma/70)^-0.5 * V*cos(theta)`.

**Textbook inconsistency found (reusable on exams):** for Example 11.2 the printed Eq. 11.28 gives `t_w = 1.24 cm` at S = 10 cm but Fig. 11.15 reads about 0.57 cm. The figure is reproduced by using `(sigma/70)^+1/2` with k = 1, so equation and figure disagree by exactly `2k`. Keep the printed equation: `t_w ~ sigma^-1/2` (a stronger wall can be thinner) is physically right, and the figure's implied `+1/2` is backwards. Checking an exponent's SIGN against physics is the cheap verification move here.

**Process lessons:** (1) Problem 1 presenters must come from the week's own lesson deck, see [[feedback_current_events_presenters]]; the first draft used the wrong week entirely and the grader caught it. (2) A grader claim is not automatically right: it asserted the 14 km/s counter-rotating figure was absent from Pisacane when it is on p. 337, so verify before "fixing". Related: [[project_hw4_anchor]], [[feedback_references]], [[feedback_conciseness]].
