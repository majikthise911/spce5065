---
name: project_exam1_anchor
description: SPCE 5065 Midterm (Exam 1) run through the pipeline; anchor for future exams (mixed T/F + MC + essays + one quantitative problem)
metadata:
  type: project
---

Exam 1 (the Midterm) was produced through the full `prompts/0_master_workflow_prompt.md` pipeline (solution -> grade -> walkthrough), scored 95/100 on the first grading pass, then corrected. Files in `exam1/`: `Clayton_spce_5065_ex1_submission.md`, `spce_5065_ex1_solution.py`, `spce_5065_ex1_walkthrough.md`, plus `figures/`.

Structure of this exam (useful template for future 5065 exams): 7 problems, 100 pts, mostly conceptual with one quantitative problem. P1 True/False x10, P2 multiple choice x5, P3/P4/P5/P7 conceptual essays (human factors, safe-mode anomaly diagnosis, Starlink altitude tradeoff, CubeSat one-improvement), P6 the only real math (atomic-oxygen erosion + drag decay).

Two judgment calls that were right and are worth reusing:
- **Ballistic coefficient "103" reads as 103 kg/m^2, not 10^3.** The Lesson 2 neutral-environment slide states typical BC = 25 to 200 kg/m^2 (avg 109), so 103 fits and 10^3 is off-scale. This also makes the exam's "350 km average altitude / 150 km deorbit" framing cohere. General habit: sanity-check ambiguous flattened-superscript exam numbers against the course's stated typical ranges.
- **P1f "atomic oxygen is the main constituent in the heterosphere during solar min" is FALSE.** The Lesson 2 video says hydrogen dominates at solar min, atomic oxygen toward solar max. AO is still top species in the 200 to 600 km band across the cycle, but the "solar min" qualifier makes the blanket statement false. First draft had it TRUE; the grading subagent caught it via the transcript.

P6 physics (verified in the script): RAM v = 7585 m/s at 550 km; AO fluence n*v*t; Mylar reaction efficiency 3.4e-24 cm^3/atom (Kapton-H reference 3.0e-24); erosion 407 um > 300 um cover (breach ~3.7 yr); decay dR/dt = -(rho/BC)*sqrt(mu*R) with rho = 1.02e7 * (alt_km)^-7.172, gives -459 km over 5 yr (reenters); 50 um cover erodes in 0.6 yr vs drag-to-150 km in 4.4 yr, so erosion wins.

Applies [[feedback_exam_allowed_resources]] (authorized-only citations), [[feedback_no_em_dashes]], [[feedback_conciseness]], [[feedback_submission_voice]], and the conceptual patterns in [[project_hw3_conceptual_anchor]].
