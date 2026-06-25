# Master Workflow — Homework/Exam Pipeline

Execute all three stages below in sequence without waiting for my input between them. Produce a final summary message when complete.

---

## Stage 1 — Solution

Read and apply `1_solution_prompt_v9.3.md`. Follow every rule in that file. Produce:

- The submission document (`<course>_hw<N>_submission.md`)
- Runnable Python code (`<course>_hw<N>_solution.py`) **only if** the assignment warrants it per the Output 2 criteria in the solution prompt
- Any figures the script generates, saved to `figures/`

Validate the submission before moving on — run the script if one exists, confirm figures rendered, confirm boxed answers are present for every required result.

---

## Stage 2 — Grading loop (iterate until ≥95% or 3 attempts)

Read and apply `2_grading_prompt_v1.md` against the submission you just produced. The grading prompt will output a line formatted exactly as:

```
FINAL_SCORE: X
```

Parse `X` as an integer. Then follow this loop:

### Decision tree

- **If `X ≥ 95`:** Stage 2 is complete. Proceed to Stage 3.
- **If `X < 95` and you have made fewer than 3 revision attempts:**
  1. Read the "Major Issues" section of the grader's output carefully.
  2. Revise the submission document (and the Python script if the issues touch code) to address every major issue. Address minor issues too if the fix is small, but prioritize major issues.
  3. Re-run the grading prompt on the revised submission.
  4. Parse the new `FINAL_SCORE: X` line and return to the top of this decision tree.
- **If `X < 95` and you have already made 3 revision attempts:** STOP. Do not proceed to Stage 3. Write a summary explaining:
  - The final score and what's still wrong
  - What you tried across the 3 attempts
  - What you think is blocking further improvement (e.g., ambiguous problem statement, missing lecture material, suspected grader-prompt miscalibration, genuine conceptual gap)
  - What you need from me to unblock it

### Revision rules

- **Do not delete the previous submission on revision** — overwrite it in place. The git history is your version trail. Do not create `submission_v1.md`, `submission_v2.md`, etc.
- **Fix the issues the grader named.** Don't add unrelated changes or reorganize things the grader didn't complain about.
- **Keep the student voice intact** — the solution prompt's voice rules still apply to revised content. Don't let grader-driven revisions make the document sound more formal or textbook-like.
- **If the grader flags something you disagree with**, still address it in some way — either fix it, or add a short justification in the submission for why the original approach is correct. Don't silently ignore grader feedback.

### Revision counter

Track your revision attempts explicitly. Attempt 1 = the initial submission. Each re-grade after a revision is a new attempt. The 3-attempt cap means: initial grade + up to 3 revision-and-regrade cycles = a max of 4 grading passes total.

---

## Stage 3 — Walkthrough (only runs if Stage 2 hit ≥95%)

Read and apply `3_walkthrough_prompt_v3.md` against the final, verified-correct submission. This stage produces the Socratic study guide with visuals, retrieval prompts, formula/pseudocode table, self-test, and per-problem Feynman-test intuition lines.

The walkthrough should be built from the **final** submission (the one that scored ≥95%), not any earlier draft.

---

## Final Summary

When all applicable stages are complete (either all three, or Stages 1–2 if the loop stopped early), produce a concise closing message:

```
=== Homework Pipeline Complete ===

Final grading score: X/100
Revision attempts: N (of 3 max)
Submission file: <filename>
Walkthrough file: <filename or "NOT PRODUCED — score below 95% threshold">
Python script: <filename or "none — hand-calculation assignment">
Figures generated: <count>

<If stopped early: brief explanation of what's blocking>
<If complete: one sentence sanity-check observation about the final score>
```

---

## Execution notes

- **Don't ask me for input between stages.** Work through all three continuously. If you hit a genuinely unresolvable ambiguity (e.g., the problem statement is missing and you can't find it), then and only then stop and ask.
- **Trust the specialized prompts.** When you're in Stage 1, apply the solution prompt's rules. When you're in Stage 2, apply the grading prompt's rules. Don't let Stage 3's thoroughness rules bleed into Stage 1's conciseness rules or vice versa.
- **This master prompt is thin on purpose.** It only contains workflow logic — not voice rules, grading criteria, or pedagogy. Those live in the specialized prompts. If you find yourself wanting to bake detailed rules into this file, resist — that's the attention-dilution problem we built this three-prompt system to avoid.
