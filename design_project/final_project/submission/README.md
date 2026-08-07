# MESA final report, build notes

Everything here is generated from two sources: the markdown report and the
analysis script. Nothing is retyped between them.

## What to hand in

**`Clayton_spce5065_final_submission.pdf`.** Its table of contents carries real
page numbers and clickable links, which is what the grade sheet's handwritten
note asks for. The docx is provided too, but its table of contents is a Word
field that stays blank until Word opens the file, so if you submit the docx,
open it in Word once and save first.

Ship `stk/MESA_MS2.zip` alongside it. That is the STK scenario behind
Figures 13 to 15, and it was agreed during Milestone 2 that submitting it as a
separate file is fine.

## Build order

```bash
python3 spce5065_final_figs.py     # prints every number, writes figures 1-12, 16, 17
cd stk && python3 make_fig13.py && python3 make_fig14.py && python3 make_fig15.py && cd ..
python3 build_pdf.py               # the deliverable
python3 build_docx.py              # optional second format
```

`make_reference_docx.py` only needs re-running if pandoc is upgraded. It builds
`reference.docx`, whose sole job is to block-justify body text in the docx.

## Things that will bite you

- **Pandoc's MathML writer drops `\tag{n}` and Chrome ignores the `<menclose>`
  it emits for `\boxed{}`.** `build_pdf.py:preprocess()` rewrites both into
  fenced divs before pandoc runs. Remove it and every equation number and boxed
  answer disappears from the PDF. The docx path does not need it; OMML handles
  both.
- **`build_pdf.py` edits the markdown.** It writes the printed page numbers back
  into the `TOC:START..TOC:END` block, so the numbers are only as fresh as the
  last run.
- **The cover image is a markdown image inside a styled div, not an `<img>`
  tag.** Pandoc drops raw HTML images in docx output without warning, and the
  cover figure is worth rubric points. `build_docx.py` verifies the image count
  is 18 for exactly this reason.
- **Renumbering a figure means three edits:** the savefig filename, the caption
  baked onto the PNG, and the markdown reference. The figure functions are named
  by content rather than by number so the function names do not also churn.
- `stk/make_fig15.py` restamps the Milestone 2 composite rather than rebuilding
  it. The screenshot it was originally built from only existed on the Windows
  machine that ran STK.
