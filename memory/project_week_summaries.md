---
name: project_week_summaries
description: How to build the 80/20 master study summary the user wants for each week's course material
metadata:
  type: project
---

The user wants a condensed "master summary" of each week's readings/lessons: the ~20% of material that yields ~80% of the understanding, sized to roughly 20% (or less) of the source word count, so he can skip reading every document. Think retention-first (neuroscientist framing): hierarchy, bold-led lines, tables, boxed key equations, memory hooks/mnemonics, and a "Remember this" bottom line per reading.

**Visuals are required, not optional.** He explicitly called out that summaries usually omit visuals and he wants them included. Reuse the already-extracted figures in each week's `course_material/img/` folder (do NOT generate new ones). Images are OCR-extracted and quality varies: many are junk fragments (single characters, page furniture), so each candidate must be opened and visually inspected before embedding; keep only genuine legible charts/diagrams.

**Proven build method (Week 4):** the Lesson decks (`*.pptx`) are the professor's own framing and are the true spine of the 80/20; extract their text first (`unzip -p deck.pptx ppt/slides/slideN.xml | grep -oE '<a:t>[^<]*</a:t>'`) and use them to anchor which formulas/concepts matter (they map directly to that week's homework). Then fan out one subagent per reading in parallel, each told the professor's emphasis, told to vet its images, and told the zero-em-dash rule. Assemble into: Section 0 "The Spine" (concept + every HW formula), one section per reading with vetted figures, a formula+constants cheat sheet, and a homework crosswalk table.

**Output location/naming:** `wkNN/wkNN_master_summary.md`, with image paths relative as `course_material/img/NAME.png`. First instance: `wk04/wk04_master_summary.md` (43k source words -> ~6.3k, 22 figures).

Applies the standing rules: [[feedback_no_em_dashes]] (grep output for em/en dashes, expect zero) and [[feedback_conciseness]] density.
