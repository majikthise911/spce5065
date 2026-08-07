"""
Build the final report PDF, with a table of contents that carries real page
numbers and clickable links.

Why this exists alongside build_docx.py. The docx gets its table of contents
from a Word field, which only fills in when Word itself opens the file, and
Word is not installed on this machine. The grade sheet asks for page links in
the table of contents, so the PDF has to be right on its own. This script:

  1. converts the markdown to a standalone HTML file with pandoc, using --mathml
     so the equations render with no external scripts,
  2. prints that HTML to PDF with headless Chrome, which preserves the in-page
     anchor links so every table of contents entry stays clickable,
  3. reads the printed PDF back, finds which page each heading landed on,
     stamps those numbers into the TOC:START..TOC:END block of the markdown,
     and reprints.

One wrinkle needs handling before pandoc runs. Pandoc's MathML writer silently
drops \tag{n}, and Chrome does not render the <menclose> element it emits for
\boxed{}, so a straight conversion loses every equation number and every boxed
answer. Since the body text refers to results by equation number throughout,
preprocess() rewrites those two constructs into fenced divs that carry the
number as text and the box as a CSS border. The markdown on disk is left alone,
because pandoc's docx writer handles both correctly through OMML.

Step 3 runs twice, because writing the numbers can shift the layout slightly.
It converges immediately in practice since the table of contents is a fixed
number of lines.

Run: python3 build_pdf.py
"""

import os
import re
import shutil
import subprocess
import sys

from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, "Clayton_spce5065_final_submission.md")
HTML = os.path.join(HERE, "_build.html")
STAGED = os.path.join(HERE, "_build_pdf.md")
OUT = os.path.join(HERE, "Clayton_spce5065_final_submission.pdf")

TOC_START = "<!-- TOC:START"
TOC_END = "<!-- TOC:END -->"
LINK = re.compile(r"^(\d+)\. \[([^\]]+)\]\(#([^)]+)\)(?:\s+\.{3}\s+\d+)?\s*$")

PANDOC_CANDIDATES = ["/opt/homebrew/bin/pandoc", "/usr/local/bin/pandoc", "pandoc"]
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]

# Print CSS. Chrome's --print-to-pdf ignores @page margins set through the
# command line, so they go here instead.
CSS = """
@page { size: Letter; margin: 0.9in 0.85in; }
body { font-family: Georgia, 'Times New Roman', serif; font-size: 10.5pt;
       line-height: 1.42; color: #111; }
h1, h2, h3, h4 { font-family: Georgia, serif; color: #00205B;
                 page-break-after: avoid; }
h2 { font-size: 15pt; margin-top: 1.5em; border-bottom: 1px solid #d5d9e0;
     padding-bottom: 3px; }
h3 { font-size: 12pt; margin-top: 1.2em; }
p, li { text-align: justify; }
img { max-width: 100%; height: auto; display: block; margin: 0.7em auto; }
table { border-collapse: collapse; width: 100%; font-size: 9.5pt;
        margin: 0.7em 0; page-break-inside: avoid; }
tr { page-break-inside: avoid; }
thead { display: table-header-group; }
th, td { border: 1px solid #b9bfc9; padding: 4px 7px; }
th { background: #eef1f5; }
code { font-size: 9.5pt; }
figure, table, .page-break { page-break-inside: avoid; }
.page-break { page-break-after: always; break-after: page; }
a { color: #00205B; text-decoration: none; }
math { font-size: 1.02em; }

/* Numbered display equations. See preprocess(). */
.eq { display: flex; align-items: center; gap: 0.8em; margin: 0.9em 0;
      page-break-inside: avoid; }
.eq-body { flex: 1 1 auto; text-align: center; }
.eq-body p { text-align: center; margin: 0.2em 0; }
.eq-body.boxed { border: 1.3px solid #00205B; border-radius: 3px;
                 padding: 7px 10px; background: #f7f9fc; }
.eq-num { flex: 0 0 3em; text-align: right; }

/* Cover page. Its inline styles are tuned for a screen viewport, so they
   overflow a Letter page and push the date onto a second sheet. These rules
   pull it back onto one page without touching the markdown. */
body > div:first-of-type > div { padding-top: 16px !important;
                                 padding-bottom: 16px !important; }
body > div:first-of-type h1 { font-size: 42pt !important; margin: 0 !important; }
body > div:first-of-type img { max-height: 3.1in; width: auto; margin: 0.3em auto; }
body > div:first-of-type p { text-align: center; }
"""


def which(cands, what):
    for c in cands:
        if os.path.exists(c) or shutil.which(c):
            return c
    raise SystemExit("%s not found. Tried:\n  %s" % (what, "\n  ".join(cands)))


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


EQ = re.compile(r"^\$\$(?P<body>.+?)\\tag\{(?P<num>\d+)\}\$\$\s*$", re.M)


def strip_boxed(tex):
    r"""Unwrap a leading \boxed{...}. Returns (inner_tex, was_boxed)."""
    tex = tex.strip()
    key = r"\boxed{"
    if not tex.startswith(key):
        return tex, False
    depth, i = 0, len(key) - 1
    while i < len(tex):
        if tex[i] == "{":
            depth += 1
        elif tex[i] == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    if i >= len(tex):
        return tex, False
    inner = tex[len(key):i]
    trailing = tex[i + 1:].strip()
    return (inner + (" " + trailing if trailing else "")), True


def preprocess(md):
    r"""Turn $$...\tag{n}$$ into a fenced div that survives the MathML writer.

    Pandoc drops \tag and Chrome ignores the <menclose> it emits for \boxed,
    so the equation number becomes text in its own div and the box becomes a
    CSS border. The markdown on disk is untouched; the docx writer needs the
    original form.
    """
    def sub(m):
        body, boxed = strip_boxed(m.group("body"))
        cls = "{.eq-body .boxed}" if boxed else "{.eq-body}"
        return ("::: eq\n"
                "::: " + cls + "\n"
                "$$" + body + "$$\n"
                ":::\n"
                "::: eq-num\n"
                # Escaped parens: a bare "(4)" at the start of a line is an
                # ordered list item to pandoc, and renders as "4.".
                "\\(" + m.group("num") + "\\)\n"
                ":::\n"
                ":::")
    return EQ.sub(sub, md)


def build_html(pandoc):
    css_path = os.path.join(HERE, "_build.css")
    with open(css_path, "w", encoding="utf-8") as fh:
        fh.write(CSS)
    with open(MD, encoding="utf-8") as fh:
        with open(STAGED, "w", encoding="utf-8") as out:
            out.write(preprocess(fh.read()))
    # pagetitle, not title: pandoc's standalone HTML template renders `title`
    # as an <h1> at the top of the body, which would sit above the cover page.
    cmd = [pandoc, STAGED, "-s", "--mathml", "--css", "_build.css",
           "--metadata", "pagetitle=MESA Final Report", "-o", HTML]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(res.stderr)
        raise SystemExit("pandoc failed")
    warn = [l for l in res.stderr.splitlines() if "Could not convert" in l]
    for w in warn:
        print("  MATH WARNING: " + w)
    return css_path


def print_pdf(chrome):
    cmd = [chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
           "--run-all-compositor-stages-before-draw",
           "--virtual-time-budget=20000",
           "--print-to-pdf=%s" % OUT, "file://%s" % HTML]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(OUT):
        print(res.stderr[-1500:])
        raise SystemExit("chrome did not produce a PDF")


def heading_for_anchor(md, anchor):
    """Recover the literal heading text that produced a given anchor slug."""
    for m in re.finditer(r"^## (.+)$", md, re.M):
        h = m.group(1).strip()
        slug = re.sub(r"[^\w\s-]", "", h.lower())
        slug = re.sub(r"[\s_]+", "-", slug).strip("-")
        if slug == anchor:
            return h
    return None


def stamp_page_numbers():
    """Write the printed page numbers back into the markdown TOC. True if changed."""
    md = open(MD, encoding="utf-8").read()
    i, j = md.find(TOC_START), md.find(TOC_END)
    if i < 0 or j < 0:
        raise SystemExit("TOC markers not found in the markdown")

    pages = [norm(p.extract_text() or "") for p in PdfReader(OUT).pages]
    first_body = 0
    for k, text in enumerate(pages):
        if "Table of Contents" in text:
            first_body = k + 1
            break

    block = md[i:j]
    out_lines, missing = [], []
    for line in block.splitlines():
        m = LINK.match(line.strip())
        if not m:
            out_lines.append(line)
            continue
        num, label, anchor = m.groups()
        heading = heading_for_anchor(md, anchor) or label
        target = norm(heading)
        page = None
        # Start looking after the table of contents page, otherwise every
        # unnumbered heading matches its own entry in the contents list.
        for k in range(first_body, len(pages)):
            if target in pages[k]:
                page = k + 1
                break
        if page is None:
            missing.append(heading)
            page = 0
        out_lines.append("%s. [%s](#%s) ... %d" % (num, label, anchor, page))

    new = md[:i] + "\n".join(out_lines) + md[j:]
    for h in missing:
        print("  WARNING: no page found for heading %r" % h)
    changed = new != md
    if changed:
        with open(MD, "w", encoding="utf-8") as fh:
            fh.write(new)
    return changed


def main():
    pandoc = which(PANDOC_CANDIDATES, "pandoc")
    chrome = which(CHROME_CANDIDATES, "a Chromium-based browser")
    print("pandoc: %s" % pandoc)
    print("chrome: %s" % chrome)

    css_path = build_html(pandoc)
    print_pdf(chrome)
    print("first pass: %d pages" % len(PdfReader(OUT).pages))

    for attempt in (1, 2):
        changed = stamp_page_numbers()
        build_html(pandoc)
        print_pdf(chrome)
        print("pass %d: TOC page numbers %s, %d pages"
              % (attempt, "updated" if changed else "already correct",
                 len(PdfReader(OUT).pages)))
        if not changed:
            break

    for tmp in (HTML, css_path, STAGED):
        if os.path.exists(tmp):
            os.remove(tmp)
    print("\nbuilt %s" % OUT)


if __name__ == "__main__":
    main()
