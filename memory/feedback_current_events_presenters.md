---
name: feedback_current_events_presenters
description: How to identify WHICH current-events talks belong to a given SPCE 5065 homework Problem 1 (use the week's own lesson deck, not the next week's transcript)
metadata:
  node_type: memory
  type: feedback
---

SPCE 5065 Problem 1 is always "for each of the current events presentations this week: (a) summarize (b) something learned (c) one question." Getting the right set of talks is the whole battle, and an earlier run got it wrong.

**The rule: the talks given during week N's live lecture are written up in homework N.** The authoritative source for WHO presented is **week N's own lesson deck**, which dedicates one slide per presenter carrying the literal text "Homework problem 1a / 1b / 1c" (or "HW PROBLEM 1") next to the presenter's name. Those names are real, not placeholders.

- wk04 deck `Lesson 4 Plasma Part 1.pptx` slides 3-5: Jacob Lerner, Dervens Marsielle, Miranda Robinson  ->  **HW4**
- wk05 deck `SPCE 5065 Week 5 - MMOD_1.pptx` slides 2-4: Trent Douglas, Ron Smetek, Claire Wadman  ->  **HW5**
- The wk05 lecture transcript confirms it: the homework walked through at the end of that session is introduced as "This'll be homework five."

**Where the CONTENT lives:** the same week's `*Transcript.vtt` (the lecture recording opens with the talks), plus any presenter PDFs dropped into that week's `course_material/`. For wk05 both Smetek's and Wadman's decks were sitting right there as PDFs, which is far better source material than the transcript alone.

**The trap that caused the error:** a week's transcript may be missing from the repo (wk04 has none). Do NOT resolve that by reaching into the adjacent week's transcript and using whatever talks you find, because those belong to a different homework. If the content for the correct presenters is unavailable, scaffold the section and flag it to the user.

**Why:** during the HW5 pipeline the grader caught Problem 1 covering the wrong week entirely (it had the wk06 vacuum talks: Kennedy, Danko, Malden). Chasing that down revealed the stored HW4 guidance had the same class of error baked in, and that `wk04/hw/Clayton_spce_5065_hw4_submission.md` very likely writes up HW5's presenters. Related: [[project_hw4_anchor]], [[project_hw5_anchor]].

**How to apply:** before drafting Problem 1, open week N's lesson deck and read the presenter names off the "Homework problem 1" slides. Only then go looking for content, preferring presenter PDFs in that week's `course_material/` over the transcript.
