# Prompt Changelog

Historical version notes for all prompts in this directory. **This file is reference-only — do not feed it to the LLM as part of the active prompt.** The active prompts contain only the current rules.

---

# `0_master_workflow_prompt`

## v1 (2026-04-11)
- **Initial version.** Thin orchestrator that sequences the three specialized prompts (`1_solution` → `2_grading` → `3_walkthrough`) in a single Claude Code session. Executes Stage 1 → Stage 2 (grading loop, max 3 revision attempts, target ≥95%) → Stage 3. No checkpoints between stages.
- **Rationale:** Manual stage-by-stage execution works but requires the user to type "now grade it" / "now fix it" / "now do the walkthrough" between stages. The master prompt automates that sequencing without recreating the attention-dilution problem we split the prompts to avoid — this file is intentionally thin (~50 lines of workflow logic, no voice rules or grading criteria). The specialized prompts still do the heavy lifting; this one just coordinates.
- **Loop cap:** Hard-coded at 3 revision attempts. If the submission can't clear 95% in 3 tries, the orchestrator stops and reports what's blocking.
- **Requires `2_grading_prompt` to output `FINAL_SCORE: X` on its own line** for reliable parsing. See `2_grading_prompt` v1.2 entry below.

---

# `1_solution_prompt`

## v9.3 (2026-04-10, revised 2026-04-11)
- **Study guide / walkthrough separated into its own prompt** (`2_walkthrough_prompt_v1.md`). The submission and walkthrough optimize for opposite goals (conciseness vs. thoroughness), and combining both instruction sets caused attention dilution. The walkthrough prompt now contains its own learning science principles, visual generation requirements, pseudocode column rules, and KaTeX compatibility checks. Process updated to a two-prompt workflow: run the submission prompt first, then the walkthrough prompt.
- **File renamed** from `1_solution_and_guide_prompt_v9.2.md` to `1_solution_prompt_v9.3.md` — "guide" dropped because this prompt no longer produces a guide.
- **2026-04-11 cleanup sweep:** Removed all lingering study-guide references that survived the initial v9.3 split:
  - Deleted the `#### Study guide (thorough — teach the student)` subsection from Mathematical rigor.
  - Simplified the Mathematical rigor opener (was "These rules apply differently depending on which document you're writing").
  - Removed the entire "Output 2: Study Guide (Socratic Tutorial)" pointer section.
  - Renumbered "Output 3: Runnable Python Script" → "Output 2" and updated all internal "Output 3 criteria" references.
  - Stripped the parenthetical "(the study guide is always thorough regardless)" from the Problem Classification section.
  - Removed "(that's the study guide's job)" language from the Output 1 section.
- **Changelog extracted** to `CHANGELOG.md` to prevent attention dilution from historical version notes being read as active instructions.

## v9.2 (2026-04-06)
- **Python script now conditional.** The `.py` file and code appendix are only produced when the assignment involves numerical integration, iteration, figure generation, large tabular output, or multi-step computations where code is genuinely the proof of work. For pure hand-calculation assignments (dB arithmetic, single-formula evaluation, conceptual questions), the inline math in the submission is sufficient — no script needed. This was validated on HW6 (Chapter 16 link budgets), where the script added no value beyond repeating `10*log10(...)` calls already shown inline.
- **"No magic numbers" rule updated.** Traceability no longer requires a code cross-reference — a compact inline arithmetic chain is sufficient.
- **Computation problem description updated.** "The code appendix is the proof of work" replaced with "the inline arithmetic chain is the proof of work."

## v9.1 (2026-03-16)
- **Code appendix restored.** The full Python script is now appended to the submission document inside a fenced code block under `## Appendix: Python Solution Script`. This reverses the v8 change that removed the appendix — the professor requires code to be included in the submission so everything is in one file. The `.py` file is still delivered separately for runability. Deliverables table now goes before the appendix.

## v9 (2026-03-16)
- **Voice calibration from Exam 1 feedback.** After comparing the v8 output against a manually tone-edited version, four new voice rules were added to close the gap between "casual-but-formal" and the student's actual writing style:
  - **Rule 11 (Real-mission anchoring):** Conceptual answers must reference real missions/systems by name (Iridium, Hubble, Molniya, ISS) rather than answering in the abstract.
  - **Rule 12 (Substance guard for conceptual questions):** Casual tone must not come at the cost of point-earning detail. 10-point questions need 4-6 specific technical points, then a punchy closer — not just the closer.
  - **Rule 13 (Short declarative closers):** After striking results, follow with a short punchy sentence ("That's why graveyard exists."). Limited to 1-2 per submission to avoid overuse.
  - **Rule 14 (Fast computation sections):** For formula evaluation, skip the buildup — state source, show inputs, land on boxed answer. Explicit GOOD/BAD examples added.
- **Existing rules 2, 4, 6, 7, 8 updated with stronger examples** drawn from the Exam 1 hybrid output (e.g., "punched it in", "fired up Newton-Raphson", "the bird is slowing down", "stupidly low", "basically a parachute").
- **Approach Overview examples replaced** with punchier exam-style examples that better match the target tone.
- **Problem statements now included in submission.** Each problem section opens with the original question in an italicized blockquote, making the submission self-contained. The old anti-pattern of "don't restate the problem" is reversed — the grader shouldn't have to flip back to the exam sheet.

## v8 (2026-03-14)
- **Voice overhaul — anti-textbook test.** Added an explicit test: "If a paragraph could appear in a Schaum's Outline or a Wikipedia article, rewrite it." Added rule #10 (narrated algebra) with concrete GOOD/BAD examples showing how derivations should read as things the student *did*, not things that *are*. Previous versions produced submissions that were mathematically correct but read like technical reports.
- **Code appendix removed.** The Python script is now delivered as a separate `.py` file, not embedded in the submission markdown. This was redundant when the `.py` file is already included in the submission package, and it bloated the document. *(Reversed in v9.1.)*
- **Deliverables table added.** Submissions now end with a table listing all files in the package (script, CSVs, figures) so the grader knows what's included.
- **Large tabular output rule added.** For problems with 200+ integration steps, export full results to CSV files and show only selected check rows inline. Reference the CSV by name.
- **Anti-pattern list added.** Explicit list of things NOT to do: university header divs, page-break divs, formal introductory paragraphs, restating the problem statement.
- **Approach Overview examples updated** with concrete examples from Exam 2 that demonstrate the right casual-but-technical tone.

## v7 (2026-03-01)
- **Submission vs. study guide role separation.** The submission document is now explicitly the *concise* deliverable — its job is to demonstrate understanding and present correct results, not to teach. The study guide is the *thorough* deliverable where all intermediate steps, trig evaluations, and detailed explanations live. Previously both documents ended up at similar verbosity levels. *(Study guide later moved to its own prompt in v9.3.)*
- **Problem classification table added.** Each problem/sub-part is now classified as Derivation, Computation, or Hybrid. The category controls submission verbosity: derivation problems get full algebra; computation problems get formula + cite + table + boxed answer.
- **Grouping related sub-parts.** New rule: if several sub-questions form a natural chain (e.g., JD → MJD → Besselian Year → UT1-UTC), collapse them into one section with a summary table rather than writing separate sections for each.
- **Mathematical rigor split by document.** The rigor rules are now split into submission-specific (concise) and study-guide-specific (thorough) sections. "No magic numbers" now explicitly allows code references as sufficient traceability for computation problems.
- **Target feel statement added.** "If the professor can read the submission in under 5 minutes and see that every answer is correct, cited, and physically reasonable — that's the right length."

## v6 (2026-02-23)
- **Writing voice integrated.** The submission document must now be written in the student's specific first-person casual voice from the first draft. Previously this required a separate humanization pass (prompt v3_humanize). The voice spec (first-person "I", Approach Overview, casual opinions, physical intuition, trap-pointing, bug-catching verification framing, cross-references between problems) is now baked into the main prompt under "Writing voice."
- **AI artifact prohibition added.** Explicit rule against meta-commentary on problem design, AI-sounding narration, filler phrases ("as expected", "interestingly"), and observations about convenient numbers.
- **Figure axis range rule added.** Figures must exclude invalid/singular data points from axis ranges rather than letting them dominate the scale.

## v5 (2026-02-16)
- **Figure labels:** Every figure must have a formal "Figure N:" caption rendered on the PNG itself (via `fig.text()`), italic and centered below the axes. The markdown alt text must match the figure number.
- **Table labels:** Every table must have a bold "**Table N:** Description" label on its own line directly above the table. Sequential numbering is global across the entire document.
- **No overlapping labels.** Added explicit requirement to prevent text overlap in figures. Use `annotate()` with `xytext` offset coordinates and leader lines for precise label placement. Position region labels away from annotation boxes. Use `bbox` backgrounds on labels over busy areas.
- **Full code restored in Appendix.** The Appendix must contain the complete Python code in a fenced block (self-contained submission). Do NOT replace with a summary or reference to an external file.
- **Inline code references.** Line-number cross-references to the Python script must appear inline with each problem (next to the boxed answer or key result), NOT collected in the Appendix. Example: *(Computed in `problem_1()`, lines 57–61.)*
- **Submission structure template updated** to show table/figure label placement and appendix code block.

## v4 (2026-02-16)
- **Figures:** Replaced ASCII diagram requirement with matplotlib/plotly figure generation. Figures must be saved as PNG to `figures/` and referenced in the submission via markdown image syntax.
- **No magic numbers:** Added explicit requirement that every numerical value in the submission must be traceable — either shown inline or cross-referenced to a specific line in the Python script.
- **Coefficient validation:** Added requirement to validate textbook empirical coefficients against lecture slide tables (e.g., extracting the Moon perturbation coefficient from multiple orbit examples in the slide data and verifying consistency).
- **Unit conversion explicitness:** Added requirement to show unit conversions step-by-step when equating expressions from different sources with different unit systems.
- **Equation citations upgraded:** Strengthened citation requirements to include specific table names and slide numbers (e.g., "Table 9-4, Class 4, slide 18"), not just equation numbers.
- **Appendix restructured:** The submission appendix now references the standalone script by filename with line-number cross-references instead of duplicating the full code inline.
- **Script structure updated:** Added figure functions to the standard script structure; increased target line count to 100-450 to accommodate figure generation code.
- **Process step added:** Added step 3 (validate key equations) and step 7 (run script to verify figures) to the workflow.

## v3
- Initial version with three-output structure, Socratic study guide, citation requirements, and verification rules.

---

# `2_grading_prompt`

## v1.2 (2026-04-11, later in day)
- **Machine-parseable score format.** The first non-caveat line of grading output is now required to be `FINAL_SCORE: X` on its own line, where X is an integer 0–100, with no markdown decoration. Previously the format was `Final Score: X/100` which was parseable but fragile — drift to `**Final Score:** 92/100` or `Final Score: 92 / 100` would break automated parsing. The new format is bulletproof because the orchestrator (`0_master_workflow_prompt`) looks for exactly this literal pattern.
- **Major Issues section now required to be actionable.** Each bullet must be specific enough that a reviser can fix the issue without asking clarifying questions. This matters because the master workflow feeds these bullets directly to a revision pass.
- No other content changes — evaluation criteria, weights, and partial credit rules are unchanged.

## v1.1 (2026-04-11, later in day)
- **Renumbered from `3_` to `2_`.** Earlier today this was placed at position 3 under the assumption that grading was a final sanity check. Revised: grading now runs *second* because it's part of an iterative quality loop (solve → grade → revise → grade → ... → walkthrough once ≥95%). The walkthrough was moved to position 3 to reflect that it's the final stage, built from a known-correct submission.
- No content changes to the grading prompt itself — pure rename.

## v1 (2026-04-11)
- **File renamed** from `2_gradeing_prompt.md` to `3_grading_prompt_v1.md` (later re-renamed to `2_grading_prompt_v1.md` — see above). Two fixes in one: corrected the "gradeing" → "grading" typo, and eliminated the prefix collision with `2_walkthrough_prompt`.

---

# `3_walkthrough_prompt`

## v3 (2026-05-02)
- **Feynman-test rule added.** Every problem must now end with a one-sentence "Feynman test" blockquote — a layman-readable distillation of *why this trick actually works at all*, with no jargon, no formulas, no Greek letters. Placed immediately after the Key Takeaway, so each problem closes with a technical-→-intuitive escalation. Named after Feynman's principle that if you can't explain it in plain English, you don't understand it well enough yet.
- **Rationale.** v2 walkthroughs already had two layers of consolidation per problem: short "Reflection" lines after each subsection (1-2 sentences of physical intuition) and a Key Takeaway blockquote at the end of each problem (2-3 sentences of technical summary). Both layers stay technical — they reference vector geometry, formula structure, choice of period, etc. The user identified a missing third layer: the highest-compression, layman-readable "why this works at all" sentence. The motivating example was a Grok exchange about HCW where the user distilled a long technical answer into the one-sentence intuition *"If they're close enough, the nonlinear forces are almost the same for both, so the difference between them behaves linearly."* That kind of single-sentence Feynman-test compression is now required for every problem.
- **Format and placement codified.** New principle 7 in the "Core Learning Science Principles" section spells out the rule: exactly one sentence, no jargon, no formulas, prefer analogies and mental pictures (clocks running at different speeds, leaky bucket draining at constant flow, swapping one velocity vector for another). Document Structure template updated to show the Feynman-test blockquote immediately after the Key Takeaway. Process step 8 added; final review (step 11) now checks that every problem has both a Key Takeaway and a Feynman test.
- **Examples and anti-patterns** included in the prompt body to lock in voice — GOOD examples (HCW, plane change, phase rate, linear closure) plus BAD examples that the rule rejects (jargon-laden, multi-sentence, just-restating-the-formula, meta-pedagogy commentary).
- **File renamed** from `3_walkthrough_prompt_v2.md` to `3_walkthrough_prompt_v3.md`. References updated in `0_master_workflow_prompt.md`, `1_solution_prompt_v9.3.md`, and `README.md`. Mirrored across both `spce_5025` and `spce_5045` course directories.
- No other rules changed — Part-to-section mapping, pseudocode clustering, KaTeX compatibility, learning-science principles 1–6, visual generation, length calibration, and tone all carry through unchanged from v2.

## v2 (2026-04-20)
- **Part-to-section mapping for sub-parted problems.** When a problem statement has explicit sub-parts (a), (b), (c), (d), the walkthrough must now include a three-layer directory structure so the reader can find any part's answer at a glance:
  1. Every subsection header is tagged with the part letter(s) it answers — `### 2.4 (a, b, c, d) Rise, set, and maximum elevation`.
  2. Immediately after the "punchline first," a Part-to-Section Map table lists each part, its headline answer, and the section number that derives it.
  3. Each sub-parted problem ends with a Results blockquote (`> **Results for Problem N**`) restating every part letter with its boxed answer, placed immediately before the Key Takeaway.
- **Rationale.** v1 walkthroughs organized subsections purely by concept. That respects the derivation logic but hides which subsection answers which part. Concrete failure case: on `wk11_ex3` Problem 2, parts (a)–(d) were all bundled into a single §2.4 with no tagging or map. A student reviewing before an exam could not find part (b) without scanning the whole problem. v2 adds the mapping layer so the reader gets both concept-organized content *and* a directory to navigate it.
- **Concept-organization preserved.** The rule explicitly warns against splitting a single derivation into per-part subsections just to get one subsection per part. If parts (a) and (c) share a derivation, keep them in one subsection tagged `(a, c)` — don't fragment the teaching logic.
- **Document Structure template updated** to show the Part-to-Section Map placement (after "punchline first") and the Results blockquote placement (before Key Takeaway).
- **Process section updated** — step 2 now calls out sub-part detection; steps 5 and 7 reference the mapping requirements; step 10 adds a per-problem consistency check.
- No changes to any other rules — pseudocode clustering, KaTeX compatibility, learning-science principles, visual generation, length calibration, and tone all carry through unchanged from v1.

## v1.1 (2026-04-11, later in day)
- **Renumbered from `2_` to `3_`.** The walkthrough now runs *last*, after the submission has been iteratively graded and revised to ≥95%. Rationale: a learning walkthrough is most valuable when built from a known-correct submission, so running it before grading risks baking mistakes into the study material. No content changes to the prompt itself — pure rename.

## v1 (2026-04-10)
- **Initial version** extracted from the combined submission+walkthrough prompt (formerly `1_solution_and_guide_prompt_v9.2.md`, now `1_solution_prompt_v9.3.md`). The walkthrough is now a standalone prompt to prevent attention dilution — the submission optimizes for conciseness and voice, the walkthrough optimizes for learning depth and pedagogy.
- **Learning science principles codified:** Lead-with-punchline (Ausubel), specific retrieval prompts (Roediger & Karpicke), define-once (Mayer redundancy principle), consolidation moments (Oberauer), visual dual coding (Paivio), self-test (spacing effect). Each principle includes a citation and concrete GOOD/BAD examples.
- **Visual requirements added:** Dark-themed matplotlib figures for waterfall charts, signal path diagrams, comparison charts, and curve plots. Color scheme and style guide specified.
- **Pseudocode column required** in the Important Formulas table, matching the master pseudocode file format.
- **Variables and acronyms table required** with every symbol and abbreviation used in the document.
- **KaTeX compatibility rules added:** `\cdot` not `·`, `\times` not `×` inside math environments.
- **Length calibration added:** Target 2-2.5x submission length. Explicit anti-bloat rules (define once, back-reference).
- **Figure generation workflow:** Separate `.py` scripts in `figures/` for reproducibility.
