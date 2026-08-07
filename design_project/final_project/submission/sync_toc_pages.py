"""
Write page numbers into the markdown table of contents, reading them back from
a PDF that already exists.

Use this when the delivered PDF was produced somewhere other than build_pdf.py,
for example by printing the markdown preview from the browser. Those renderers
paginate differently, so the numbers build_pdf.py stamped will be wrong.

    python3 sync_toc_pages.py [printed.pdf]

Defaults to Clayton_spce5065_final_submission.pdf. It reads the PDF and edits
only the TOC:START..TOC:END block of the markdown. It never writes a PDF, so
the file you hand in is left exactly as it was.

IMPORTANT: the numbers are a snapshot of one render. After editing the report,
reprint the PDF and run this again. Reprinting is also required after this
script runs, so the table of contents inside the PDF shows the new numbers;
that second print does not shift pagination, because every entry keeps its
line.

Note that build_pdf.py does its own stamping and will overwrite both the PDF
and these numbers. Do not run it if the browser-printed PDF is the deliverable.
"""

import os
import re
import sys

from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, "Clayton_spce5065_final_submission.md")
DEFAULT_PDF = os.path.join(HERE, "Clayton_spce5065_final_submission.pdf")

TOC_START = "<!-- TOC:START"
TOC_END = "<!-- TOC:END -->"
LINK = re.compile(r"^(\d+)\. \[([^\]]+)\]\(#([^)]+)\)(?:\s+\.{3}\s+\d+)?\s*$")


def norm(s):
    """Collapse whitespace and fold the ligatures PDF text extraction returns."""
    s = s.replace("ﬁ", "fi").replace("ﬂ", "fl").replace("ﬀ", "ff")
    s = s.replace("ﬃ", "ffi").replace("ﬄ", "ffl")
    return re.sub(r"\s+", " ", s).strip()


def heading_for_anchor(md, anchor):
    """Recover the literal heading text that produced a given anchor slug."""
    for m in re.finditer(r"^## (.+)$", md, re.M):
        h = m.group(1).strip()
        slug = re.sub(r"[^\w\s-]", "", h.lower())
        slug = re.sub(r"[\s_]+", "-", slug).strip("-")
        if slug == anchor:
            return h
    return None


def main():
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PDF
    if not os.path.exists(pdf_path):
        raise SystemExit("printed PDF not found: %s" % pdf_path)

    md = open(MD, encoding="utf-8").read()
    i, j = md.find(TOC_START), md.find(TOC_END)
    if i < 0 or j < 0:
        raise SystemExit("TOC markers not found in the markdown")

    pages = [norm(p.extract_text() or "") for p in PdfReader(pdf_path).pages]
    print("read %s (%d pages)" % (os.path.basename(pdf_path), len(pages)))

    # Everything before and including the contents page is skipped, otherwise
    # each unnumbered heading matches its own entry in the contents list.
    first_body = 0
    for k, text in enumerate(pages):
        if "Table of Contents" in text:
            first_body = k + 1
            break

    out_lines, changes, missing = [], 0, []
    for line in md[i:j].splitlines():
        m = LINK.match(line.strip())
        if not m:
            out_lines.append(line)
            continue
        num, label, anchor = m.groups()
        target = norm(heading_for_anchor(md, anchor) or label)
        page = next((k + 1 for k in range(first_body, len(pages))
                     if target in pages[k]), None)
        if page is None:
            missing.append(target)
            page = 0
        new = "%s. [%s](#%s) ... %d" % (num, label, anchor, page)
        if new != line.strip():
            changes += 1
        out_lines.append(new)
        print("  p%-3d %s" % (page, target))

    for t in missing:
        print("  WARNING: no page found for %r" % t)

    with open(MD, "w", encoding="utf-8") as fh:
        fh.write(md[:i] + "\n".join(out_lines) + md[j:])
    print("\n%d entries updated. Reprint the PDF so its contents page shows them."
          % changes)


if __name__ == "__main__":
    main()
