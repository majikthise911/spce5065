---
name: project_final_report_anchor
description: SPCE 5065 design-project Final Report anchor, its structure, the new analysis added past Milestone 2, and the macOS build pipeline
metadata:
  node_type: memory
  type: project
---

The MESA **final report** was written 7 Aug 2026 in `design_project/final_project/submission/`. It is cumulative from Milestone 2 and follows the **final rubric's own section order**, which differs from MS1/MS2: cover 2, intro 3, name and objectives 5, orbit 5, Sun-Earth 10, space weather 5, vacuum 5, TCS 10, plasma 10, radiation 10, ADACS 10, conclusions 3, references 2, grammar 10, simulations 10. Note the orbit section now comes **before** the environment sections that justify it, so Section 3 states the decision and forward-references Sections 4 to 6. The final grade sheet carries one handwritten instruction: **"Include page links in TOC."**

**New analysis added past MS2** (MS2's own conclusions listed most of it as remaining work):
- Section 7 closes all four budgets: mass 1,250 kg subsystems + 150 kg margin = 1,400 kg dry + 600 kg propellant; power 1,773 W peak against 2,984 W EOL; delta-v 463 m/s; cost allocated to exactly $100M.
- Propulsion split 520 kg xenon (Hall, 1,600 s, 40 mN) and 80 kg hydrazine (220 s). Only 165 kg is consumed in five years, and **capacity is hydrazine-limited at about ten client servicing cycles**, not xenon-limited. This **refines the MS2 claim that propellant is the life limiter**: with EP, propellant sizes servicing capacity and wear-out sets calendar life.
- Section 12.3 transient thermal: the 1,400 kg bus has an 11.3 h time constant against a 1.16 h eclipse, so it drops only **3.9 K**, not the 49.4 K steady-state bound. The zone that actually needs heaters is a 6 kg outboard propellant line, which hits -0.2 C, below hydrazine's 2 C freezing point. This is the strongest new result in the report.
- Section 13 adds MMOD (Grun flux, chi*G = 1.147 at GEO vs 1.266 at 400 km, so net flux is near orbit-independent; P(>=1 mm in 5 yr) = 11.9% over 52.2 m2; Whipple bumper 0.56 mm / wall 3.6 mm), the docking failure modes, and a ten-row risk register plotted before and after mitigation.
- Section 2.4 adds a concept of operations: a 242-day servicing cycle, six cycles in five years, ~80% of life mated.

**Counts to preserve:** 17 numbered figures plus the cover (18 images in the docx), 16 tables plus an unnumbered Table ES-1, 17 equations, 19 references ascending by first appearance.

**Build pipeline is macOS-native now** (MS2's assumed Windows and Word):
- `spce5065_final_figs.py` prints every number and writes figures 1 to 12, 16, 17. Figure functions are named by content, not number, so renumbering only touches filenames and captions.
- `stk/make_fig13|14|15.py` rebuild the STK captures. make_fig15 restamps the MS2 composite because its source screenshot only ever existed on the Windows machine.
- `build_pdf.py` is the one to trust: pandoc to HTML with `--mathml`, headless Chrome to PDF, then it reads the PDF back and stamps real page numbers into the markdown TOC. **Pandoc's MathML writer silently drops `\tag{n}` and Chrome will not render the `<menclose>` it emits for `\boxed{}`**, so `preprocess()` rewrites both into fenced divs. Do not remove that.
- `build_docx.py` + `make_reference_docx.py`: the reference docx exists only to block-justify body text, a grammar-rubric line item that the markdown `<style>` block cannot reach. The docx TOC field stays unpopulated until Word opens it, so **the PDF is the deliverable to hand in**.

**Why:** this is the capstone deliverable and its numbers, structure, and build steps would be expensive to re-derive. **How to apply:** run `spce5065_final_figs.py` first and read numbers from its console output, never retype them. Related: [[project_ms2_anchor]], [[feedback_references]], [[feedback_docx_cover_image]], [[project_hw5_anchor]].
