---
name: feedback_conciseness
description: SPCE 5065 submissions must match HW1's density; cap sanity checks and intuition asides, no justification paragraphs
metadata:
  node_type: memory
  type: feedback
---

Submissions tend to come out **wordier than the student wants**. The density target is the hand-tuned HW1 (`wk01/hw/Clayton_spce_5065_hw1_submission.md`, 96/100). Jordan reviewed HW2 against HW1 and had it trimmed. The concrete rules that emerged:

- **Sanity checks / verifications: one sentence, two at the very most.** HW1 model: "that μ is ~9 orders of magnitude below Earth's, which is the right ballpark for a small body." Not a paragraph.
- **Physical-intuition asides: one sentence / one clause.**
- **No labeled justification paragraphs** ("Why this is the honest way to do it..."). Fold the *why* into a clause.
- **Approach Overview: keep it, but short.** Jordan likes the Approach Overview and wants it kept, but it must be a punchy hit list and is the first thing he'll cut if the finished doc runs long. Do not let it restate the problem sections.
- **Deliverables table is optional.** HW1 omits it; include only for multi-file packages.
- **The cap is for computation/derivation prose only.** Conceptual and judgment/recommendation answers (e.g. HW2 P4b Mars-atmosphere call) stay substantive: bulleted, 4-6 technical points. Trimming filler, not gutting content.

These rules are now baked into `prompts/1_solution_prompt_v9.4.md` (Rule 15 + length exemplar + reframed Approach Overview + optional Deliverables). v9.3 is in `prompts/archive/`.

**Why:** Direct feedback after HW2. Jordan said "sometimes you can be a bit wordy and so i edited hw1 to be the way i want it," then had HW2 trimmed to match and the solution prompt updated so future first drafts land at HW1 density without a cleanup pass.

**Concrete density metric (added after HW7):** measure **words of body prose per assignment point**, not raw word count, since problem counts vary wildly between assignments. Strip the code appendix and any fenced blocks first. Benchmarks: HW1 = 33 w/pt, HW6 = 59 w/pt, HW7 after trimming = 56 w/pt. **Anything above about 60 w/pt is bloat.** Check Problem 1 separately, since current-events writeups inflate easily: HW6 runs 744 words for four talks (186 each, 74 w/pt) and that is the target shape, a dense fact-list summary plus a one-to-two-sentence "what I learned" plus a one-sentence question. HW7's first draft ran 440 words per talk and had to be cut roughly in half; the cuts were all narrative connectives ("She then went on to...", "The most useful slide was...", "He tied it to the present by noting that..."), not technical content.

**How to apply:** Before drafting, skim the HW1 anchor to re-calibrate length. After drafting, reread every sanity check and intuition aside; if it runs past one to two sentences, cut it. Related: [[feedback_submission_voice]], [[feedback_no_em_dashes]].
