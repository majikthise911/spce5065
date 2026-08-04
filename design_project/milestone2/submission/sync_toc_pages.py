"""
Write page numbers into the markdown table of contents.

A markdown render has no pages, so the TOC in the .md normally carries links but
no page numbers. If you print the preview to PDF from the browser, that PDF does
have pages, and this script reads it back and stamps those numbers into the TOC.

    python sync_toc_pages.py [printed.pdf]

Safe to run: build_docx.py strips the whole TOC:START..TOC:END block and
substitutes a real Word TOC field, so nothing here reaches the .docx. These
numbers only affect the markdown preview and anything printed from it.

IMPORTANT: the numbers are a snapshot. Edit the report and they are stale. Re-print
the PDF and re-run this before submitting anything that shows them.
"""

import os
import re
import sys

from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, "Clayton_spce5065_ms2_submission.md")
DEFAULT_PDF = os.path.join(HERE, "Clayton_spce5065_ms2_submission.pdf")

TOC_START = "<!-- TOC:START"
TOC_END = "<!-- TOC:END -->"

LINK = re.compile(r"^(\d+)\. \[([^\]]+)\]\(#([^)]+)\)(?:\s+\.{3}\s+\d+)?\s*$")


def norm(s):
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
        raise SystemExit("printed PDF not found: %s\nPrint the preview to PDF first." % pdf_path)

    md = open(MD, encoding="utf-8").read()
    i, j = md.find(TOC_START), md.find(TOC_END)
    if i < 0 or j < 0:
        raise SystemExit("TOC markers not found in the markdown")

    reader = PdfReader(pdf_path)
    pages = [norm(p.extract_text() or "") for p in reader.pages]
    print("read %s (%d pages)" % (os.path.basename(pdf_path), len(pages)))

    # The TOC page lists every heading, so skip it when searching.
    toc_page = next((n for n, t in enumerate(pages) if "Table of Contents" in t), None)

    block = md[i:j]
    out_lines, hits, misses = [], 0, []
    for line in block.split("\n"):
        m = LINK.match(line)
        if not m:
            out_lines.append(line)
            continue
        num, label, anchor = m.groups()
        heading = heading_for_anchor(md, anchor)
        page = None
        if heading:
            key = norm(heading)
            for n, txt in enumerate(pages):
                if n == toc_page:
                    continue
                if key in txt:
                    page = n + 1
                    break
        if page:
            out_lines.append("%s. [%s](#%s) ... %d" % (num, label, anchor, page))
            hits += 1
        else:
            out_lines.append(line)
            misses.append(label)

    open(MD, "w", encoding="utf-8").write(md[:i] + "\n".join(out_lines) + md[j:])

    print("stamped page numbers on %d of %d entries" % (hits, hits + len(misses)))
    if misses:
        print("no page found for:")
        for x in misses:
            print("   " + x)


if __name__ == "__main__":
    main()
