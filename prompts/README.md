# Prompts

Claude prompts for homework/exam work. The workflow is a **quality-gated loop**:

```
┌──────────────┐      ┌─────────────┐      ≥95%?     ┌────────────────┐
│ 1_solution   │ ───▶ │ 2_grading   │ ───────▶ yes ─▶│ 3_walkthrough  │
│ (solve it)   │      │ (score it)  │               │ (learn it)     │
└──────────────┘      └─────────────┘               └────────────────┘
                            │  ▲
                            │  │ re-grade (up to 3 attempts)
                            ▼  │
                      revise submission
```

## How to run it

**The easy way — one command, fully automatic:**

Point Claude at `0_master_workflow_prompt.md`. It sequences through all three stages automatically, runs the grading loop (up to 3 revision attempts), and stops only if it can't clear 95% — in which case it tells you why. No intervention between stages.

**The manual way — run each stage yourself:**

1. Point Claude at `1_solution_prompt_v9.3.md` → produces the submission.
2. Point Claude at `2_grading_prompt_v1.md` → produces a score and feedback.
3. If score < 95%: tell Claude to revise based on the feedback, then re-run step 2. Loop until ≥95%.
4. Point Claude at `3_walkthrough_prompt_v3.md` → produces the Socratic study guide.

## Files

| File | Purpose | Stage |
|---|---|---|
| `0_master_workflow_prompt.md` | Thin orchestrator that runs all three stages in sequence | Entrypoint for automated runs |
| `1_solution_prompt_v9.3.md` | Produces a submission-ready homework paper + optional runnable code | 1 — first pass |
| `2_grading_prompt_v1.md` | Grades the submission as a strict expert grader | 2 — iterates with revisions until ≥95% |
| `3_walkthrough_prompt_v3.md` | Produces a Socratic, learning-optimized study guide with visuals and a per-problem part-to-section map for sub-parted problems | 3 — runs once quality is locked in |
| `30k_overview_prompt.md` | Helper used by the walkthrough prompt (not run standalone) | — |
| `CHANGELOG.md` | Historical version notes — reference only, never include in active prompts | — |

## ⚠️ This directory is a synced copy

**The canonical source lives in `spce_5045/prompts/`.** Edits made here will be overwritten the next time the sync script runs.

To change a prompt, edit it in `spce_5045/prompts/` and then run:

```bash
~/code/spce_5045/scripts/sync_prompts.sh --check    # dry run first
~/code/spce_5045/scripts/sync_prompts.sh            # apply
```

Then commit both repos. The script handles course-number substitution (`5045` → `5025`) automatically.

See `spce_5045/prompts/README.md` for the full workflow rationale, editing guidelines, and why this directory exists.
