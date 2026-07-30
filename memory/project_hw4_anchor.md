---
name: project_hw4_anchor
description: SPCE 5065 HW4 (plasma environment) pipeline result + the recurring Problem-1 current-events blocker
metadata:
  node_type: memory
  type: project
---

HW4 (wk04, plasma environment) run through the full pipeline, self-graded **95/100**. Submission `wk04/hw/Clayton_spce_5065_hw4_submission.md`, script `spce_5065_hw4_solution.py`, walkthrough `spce_5065_hw4_walkthrough.md`.

**Recurring Problem 1 (current-events write-up):** SPCE 5065 Problem 1 is always a write-up of the week's live current-events presentations by classmates: (a) summarize (b) something learned (c) one question. See [[feedback_current_events_presenters]] for the authoritative rule on WHICH talks belong to WHICH homework.

**CORRECTION (found while doing HW5, 2026-07-29):** the guidance previously stored here was WRONG and it appears to have put the wrong presentations into the HW4 submission. It claimed the wk04 deck names (Jacob Lerner, Dervens Marsielle, Miranda Robinson) were "placeholders" and that HW4's real talks were the ones in the wk05 transcript (Trent Douglas, Ron Smetek, Claire Wadman). That is backwards. The wk04 deck (`Lesson 4 Plasma Part 1.pptx`, slides 3-5) labels those three names "Homework problem 1a / 1b / 1c" explicitly, so Lerner/Marsielle/Robinson ARE HW4's presenters. Douglas/Smetek/Wadman presented during the WEEK 5 lecture and belong to **HW5** (wk05 deck `SPCE 5065 Week 5 - MMOD_1.pptx` slides 2-4 label them "HW PROBLEM 1", and the wk05 transcript has the assignment being discussed as "This'll be homework five"). `wk04/hw/Clayton_spce_5065_hw4_submission.md` Problem 1 therefore covers the wrong week and should be revisited if it has not already been graded. No wk04 transcript exists in the repo, which is probably why the substitution happened; the correct response to missing content is to flag it, not to borrow another week's talks.

**Physics anchors (all verified against the Lesson 4 decks, so reuse for exams):**
- Debye length densities came from the professor's OWN day/solar-max plasma-density profile (Lesson 4 Part 1 slide image): n_e ~ 5e12 m^-3 at 300 km, ~1e11 m^-3 at 1000 km. Read the chart, do not guess.
- Ionospheric delay: dt = 40.31*TEC/(c*f^2) s; excess range dR = 40.31*TEC/f^2 m = c*dt. Both ~1/f^2.
- GEO spacecraft charging at T=1e7 K: spacecraft speed 3.07 km/s is negligible vs thermal; electron mean speed ~20,000 km/s, proton ~459 km/s (professor's own slide numbers), ratio sqrt(mp/me)=42.85. Current balance 42.85*exp(x)=1-x with x=eV/kBT gives x=-2.50, so **V = -2.5*kBTe/e = -2.16 kV** (professor states the -2.5 coefficient explicitly on the Part 3 slide). P5 and P8 are the SAME scenario and give the SAME answer.

**Grader feedback that recurred:** the P6 silicon-mobility values were initially uncited inline (the exact HW1 sin, [[feedback_references]]); fixed by adding an inline [n]. Always do the inline-citation pass. Related: [[feedback_conciseness]], [[project_week_summaries]] (wk04 master summary was the load-bearing source).
