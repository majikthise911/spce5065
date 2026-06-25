# Prompt: Master Pseudocode Formula Table Generator

Use this prompt with Claude Code (or any capable LLM) to generate a master pseudocode formula table for a course. Feed it the course content files and it produces a single organized reference document.

---

## The Prompt

You are building a **master pseudocode formula reference table** for a graduate-level astrodynamics course. Your job is to extract every important formula from the provided course materials and organize them into a single, study-ready reference document.

### Output Format

The document must follow this exact structure:

```
# Master Pseudocode Formula Reference — [COURSE ID]

*Every key formula from [COURSE NAME], organized by workflow. LaTeX for precision, pseudo-code for intuition.*

---

#### [Section Title — What You're Trying to Do]

*[One sentence explaining WHEN and WHY you reach for these formulas — the workflow context, not a textbook definition.]*

| # | Formula | Physics Pseudo-Code | Description |
|---|---|---|---|
| N | $[LaTeX]$ | [Same formula written in plain English, step by step] | [One-line name or context] |

---

[Next section...]

---

### Variables and Acronyms

| Symbol / Acronym | Name | Units | Description |
|---|---|---|---|
| $\mu$ | Earth gravitational parameter | km³/s² | 398,600.4418 |
[...]
```

### Column Rules

1. **# column** — Sequential number across the entire document (1, 2, 3... not restarting per section)
2. **Formula column** — LaTeX math. Use `\dfrac` for readability. Include ALL variables — no implicit assumptions.
3. **Physics Pseudo-Code column** — The same formula rewritten in plain English words. This is the KEY column. Rules:
   - Write it as if you're reading the formula aloud to someone who can't see it
   - Use the full English name of every variable the first time ("semi-major axis", not "a")
   - Use standard math words ("squared", "square root of", "cross", "dot product")
   - Parentheses and order of operations must be unambiguous
   - Example: `Semi-major axis = 1 / (2 / position magnitude − velocity squared / gravitational parameter μ)`
4. **Description column** — One short phrase. What IS this formula / when do you use it. Max ~10 words.

### Section Organization Rules

- **Group by workflow/pipeline**, not by week or lecture number. Think: "what am I trying to DO?" not "what week was this?"
- Each section gets a `#### Header` and a one-line *italic context sentence*
- Sections are separated by `---` horizontal rules
- Within a section, formulas should be in the order you'd USE them (pipeline order)
- If a formula is used in multiple workflows, put it in the FIRST workflow where it appears and reference it by number in later sections if needed

### What to Extract

- Every formula from "Toolbox" sections in weekly WES (Mastery Enlightenment Summary) files
- Every formula from exam walkthrough "Important Formulas" tables
- Key formulas from worked examples that aren't in the toolbox (e.g., sanity check formulas, intermediate results that are reusable)
- Constants and their values go in the Variables table, not as standalone formula rows

### What NOT to Include

- Derivation steps that aren't reusable (intermediate algebra)
- Formulas that are just rearrangements of another formula already in the table (unless the rearranged form is the one you'd actually reach for in practice)
- MATLAB-specific syntax (datenum, datevec, etc.) — this is a physics reference, not a code reference
- Duplicate formulas that appear in multiple weeks — include once, in the most natural workflow section

### Quality Checks

After generating the table, verify:
- [ ] Every formula has all three non-trivial columns filled (no empty Pseudo-Code or Description)
- [ ] The Pseudo-Code column is unambiguous — could someone reconstruct the formula from ONLY the English text?
- [ ] No two rows are the same formula in different notation
- [ ] Section headers describe actions/goals, not topics (e.g., "Propagate Position Forward in Time" not "Kepler's Equation")
- [ ] Variables table includes every symbol used in any formula row
- [ ] Numbers are sequential 1 through N with no gaps

---

## How to Use

### For a new course:
```
Read all WES toolbox sections and exam walkthroughs for [COURSE], then generate a master pseudocode formula table following the prompt above. Save to /Volumes/Marvin SSD/Projects/[course_dir]/master_pseudocode.md
```

### To update an existing table with new content:
```
Read [new file]. Extract any formulas not already in /Volumes/Marvin SSD/Projects/[course_dir]/master_pseudocode.md. Add them to the appropriate workflow section, maintaining sequential numbering.
```
