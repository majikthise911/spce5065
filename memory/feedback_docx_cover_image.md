---
name: feedback_docx_cover_image
description: Pandoc silently drops the HTML cover image when building the submission .docx; use a markdown image inside the styled div
metadata:
  node_type: memory
  type: feedback
---

The submission cover page is a styled HTML `<div>` block (UCCS header bar, title, concept figure, name, date). When that block contains a raw `<img src="figures/figN.png">` tag, **pandoc parses the whole thing as a RawBlock and drops it for docx output**. The .docx builds with exit code 0 and no warning, and the cover image is simply gone. This is not cosmetic: the milestone rubrics award points for "cover page includes a conceptual figure of satellite(s)."

**The fix:** inside the div, put a blank line, a normal markdown image, and another blank line:

```
<div style="flex-grow: 1; text-align: center;" markdown="1">

![alt text](figures/fig0_concept.png)

</div>
```

Pandoc then emits the div as raw HTML (dropped in docx, harmless) and the image as a real Image element that gets embedded. HTML and markdown renderers still show it inside the styled div.

**Always verify rather than trusting the build**, because pandoc does not warn:

```bash
python3 -c "import zipfile; z=zipfile.ZipFile('X.docx'); \
print(len([n for n in z.namelist() if n.startswith('word/media/')]))"
```

The count must equal the number of figures **including** the cover. On MS2 this read 8 when it should have been 9.

**Why:** found while building the Milestone 2 docx. MS1's docx did contain its cover image, so the failure looked like a regression in the document rather than a conversion behavior, which is what made it easy to miss.

**How to apply:** after every `pandoc ... -o *.docx`, count `word/media/` entries and compare against the figure count before calling the submission done. Related: [[project_ms2_anchor]].
