# SPCE 5065 — Project Conventions

## Project memory lives IN this repo

The canonical memory store is the `memory/` folder at the repo root (relative to this file):

```
./memory/
```

This is committed to git on purpose so the accumulated context syncs across machines on push/pull. **Read it and write it here — not in the machine-local `~/.claude/projects/.../memory/` folder**, whose name is derived from the absolute repo path and therefore does NOT transfer between machines (it will be empty on a fresh clone). The harness still auto-loads the machine-local copy if present, but the in-repo `./memory/` is the source of truth; the local one only holds a redirect pointer.

## Before drafting any homework or exam submission

Read `./memory/MEMORY.md` (the index) first, then any feedback or project memory files that look relevant to the task. If `./memory/MEMORY.md` is missing or empty, surface that to the user. When you learn something worth persisting, write a new memory file into `./memory/` and add its one-line pointer to `./memory/MEMORY.md`.

**Submission voice calibration:** no canonical anchor has been set yet for 5065. Once a graded submission lands that captures the right density, record it here and in `feedback_submission_voice.md` (mirroring the 5025 convention).

## Workflow prompts

No `prompts/` pipeline exists for 5065 yet. The 5025 project runs homework/exam work through `prompts/0_master_workflow_prompt.md`, which sequences:
1. `1_solution_prompt_v9.3.md` — solution + submission doc
2. `2_grading_prompt_v1.md` — grading loop (≥95% target, max 3 revision attempts)
3. `3_walkthrough_prompt_v2.md` — Socratic study guide (only after grading passes)

When the user is ready to stand up the same pipeline here, port those prompts over and update this section to point at them.

## File naming

- Submissions: `spce_5065_<hwN|exN>_submission.md`
- Solution scripts: `spce_5065_<hwN|exN>_solution.py`
- Walkthroughs: `spce_5065_<hwN|exN>_walkthrough.md`
- CSVs: `spce_5065_<hwN|exN>_<purpose>.csv`
- Figures: `figures/figN_<short_name>.png` (submission) or `figures/walkthrough_figN_<short_name>.png` (walkthrough)
