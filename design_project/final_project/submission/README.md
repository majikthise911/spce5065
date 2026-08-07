# MESA final report, build notes

Everything here is generated from two sources: the markdown report and the
analysis script. Nothing is retyped between them.

## What to hand in

**`Clayton_spce5065_final_submission.pdf`.** The delivered copy is a 30-page
print of the markdown preview from the browser, which is where its visible page
numbers come from. Its table of contents carries those page numbers and
clickable links, which is what the grade sheet's handwritten note asks for. The
docx is provided too, but its table of contents is a Word field that stays
blank until Word opens the file, so if you submit the docx, open it in Word
once and save first.

Ship `stk/MESA_MS2.zip` alongside it. That is the STK scenario behind
Figures 13 to 15, and it was agreed during Milestone 2 that submitting it as a
separate file is fine.

## Build order

```bash
python3 spce5065_final_figs.py     # prints every number, writes figures 1-12, 16, 17
cd stk && python3 make_fig13.py && python3 make_fig14.py && python3 make_fig15.py && cd ..
python3 build_docx.py              # optional second format
```

Then print the preview to PDF from the browser and run:

```bash
python3 sync_toc_pages.py          # stamps that render's page numbers into the TOC
```

and print once more, so the contents page in the PDF shows the numbers. That
second print does not move anything, because every entry keeps its line.

**`build_pdf.py` is the alternative pipeline, not the current one.** It renders
the report through pandoc and headless Chrome, which paginates completely
differently (49 pages against the browser preview's 30), and it overwrites both
the PDF and the table of contents numbers. Do not run it while the
browser-printed PDF is the deliverable.

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
