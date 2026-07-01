# SPCE 5065 — Project Conventions

## Project memory lives IN this repo

The canonical memory store is the `memory/` folder at the repo root (relative to this file):

```
./memory/
```

This is committed to git on purpose so the accumulated context syncs across machines on push/pull. **Read it and write it here — not in the machine-local `~/.claude/projects/.../memory/` folder**, whose name is derived from the absolute repo path and therefore does NOT transfer between machines (it will be empty on a fresh clone). The harness still auto-loads the machine-local copy if present, but the in-repo `./memory/` is the source of truth; the local one only holds a redirect pointer.

## Before drafting any homework or exam submission

Read `./memory/MEMORY.md` (the index) first, then any feedback or project memory files that look relevant to the task. If `./memory/MEMORY.md` is missing or empty, surface that to the user. When you learn something worth persisting, write a new memory file into `./memory/` and add its one-line pointer to `./memory/MEMORY.md`.

**Submission voice calibration:** HW1 (`wk01/hw/Clayton_spce_5065_hw1_submission.md`) scored 96/100 and is the first in-course anchor for density and tone. For voice, also see `feedback_submission_voice.md`.

## Submission requirements (from HW1 grader feedback)

HW1 scored 96/100; both deductions were reference formatting, not physics. On every submission:

1. **Number references by first appearance in the text** (AIAA). The first source cited in the body is [1], the next new source [2], and so on. Do not number by importance. After drafting, walk the body top to bottom, renumber the [n] markers, and reorder the Sources list to match.
2. **Cite every external value inline at the point of use.** Published constants, quotes, and data each need an [n] right where they appear, not only in the Sources list. Do not drop inline citations when condensing or rewriting a section.

Detail and the exact grader comments are in `./memory/feedback_references.md`.

## Workflow prompts

No `prompts/` pipeline exists for 5065 yet. The 5025 project runs homework/exam work through `prompts/0_master_workflow_prompt.md`, which sequences:
1. `1_solution_prompt_v9.4.md` — solution + submission doc
2. `2_grading_prompt_v1.md` — grading loop (≥95% target, max 3 revision attempts)
3. `3_walkthrough_prompt_v2.md` — Socratic study guide (only after grading passes)

When the user is ready to stand up the same pipeline here, port those prompts over and update this section to point at them.

## File naming

- Submissions: `spce_5065_<hwN|exN>_submission.md`
- Solution scripts: `spce_5065_<hwN|exN>_solution.py`
- Walkthroughs: `spce_5065_<hwN|exN>_walkthrough.md`
- CSVs: `spce_5065_<hwN|exN>_<purpose>.csv`
- Figures: `figures/figN_<short_name>.png` (submission) or `figures/walkthrough_figN_<short_name>.png` (walkthrough)
