---
name: project_hw4_anchor
description: SPCE 5065 HW4 (plasma environment) pipeline result + the recurring Problem-1 current-events blocker
metadata:
  node_type: memory
  type: project
---

HW4 (wk04, plasma environment) run through the full pipeline, self-graded **95/100**. Submission `wk04/hw/Clayton_spce_5065_hw4_submission.md`, script `spce_5065_hw4_solution.py`, walkthrough `spce_5065_hw4_walkthrough.md`.

**Recurring Problem 1 (current-events write-up):** SPCE 5065 Problem 1 is always a write-up of the week's live current-events presentations by classmates: (a) summarize (b) something learned (c) one question. KEY: the presentation CONTENT is in the LECTURE VIDEO TRANSCRIPT, and it may sit in the FOLLOWING week's folder, not the HW's own week. For HW4 (wk04) the three talks were in `wk05/course_material/Week 5 Video Transcript.vtt`. The Lesson-deck slide names (wk04 deck listed Lerner/Marsielle/Robinson) were placeholders and did NOT match the actual presenters. So: before scaffolding P1, grep the wkNN and wk(NN+1) `*Transcript.vtt` for "current event"/"present" and pull the real presenters and content. HW4's actual presenters + topics: Trent Douglas (rising LEO debris, ESA 2026 report: crash clock 121 days in 2018 to 2.8-5.5 days by mid-2025, Kessler threshold exceeded 500-20,000 km); Ron Smetak (China's abandoned rocket bodies: 51 bodies >650 km = 86% of global total since 2021, Guowang/Qianfan constellations, CZ-6A/Jielong explosions); Claire Wadman (MMOD design: 1-10 cm is the unshieldable/untrackable band, Whipple shields, ISS window chip). Only scaffold+flag if no transcript exists. HW3 same shape (Schreckenberg, Burns), content already supplied by the student.

**Physics anchors (all verified against the Lesson 4 decks, so reuse for exams):**
- Debye length densities came from the professor's OWN day/solar-max plasma-density profile (Lesson 4 Part 1 slide image): n_e ~ 5e12 m^-3 at 300 km, ~1e11 m^-3 at 1000 km. Read the chart, do not guess.
- Ionospheric delay: dt = 40.31*TEC/(c*f^2) s; excess range dR = 40.31*TEC/f^2 m = c*dt. Both ~1/f^2.
- GEO spacecraft charging at T=1e7 K: spacecraft speed 3.07 km/s is negligible vs thermal; electron mean speed ~20,000 km/s, proton ~459 km/s (professor's own slide numbers), ratio sqrt(mp/me)=42.85. Current balance 42.85*exp(x)=1-x with x=eV/kBT gives x=-2.50, so **V = -2.5*kBTe/e = -2.16 kV** (professor states the -2.5 coefficient explicitly on the Part 3 slide). P5 and P8 are the SAME scenario and give the SAME answer.

**Grader feedback that recurred:** the P6 silicon-mobility values were initially uncited inline (the exact HW1 sin, [[feedback_references]]); fixed by adding an inline [n]. Always do the inline-citation pass. Related: [[feedback_conciseness]], [[project_week_summaries]] (wk04 master summary was the load-bearing source).
