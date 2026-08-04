"""
Build the Milestone 2 docx.

Run this instead of calling pandoc directly:

    python build_docx.py

Pandoc alone is not sufficient. The document injects a real Word TOC field via a
```{=openxml}``` block so the table of contents carries page numbers and
hyperlinks (a Milestone 1 grammar deduction was "TOC set up incorrectly"). That
field is marked w:dirty="true", which only marks it stale; it does NOT make Word
populate it. Word fills a dirty field on open only when the document also sets

    <w:updateFields w:val="true"/>

in word/settings.xml, which pandoc does not write. Without it the reader sees the
placeholder line instead of a table of contents, which is exactly the deduction
we are trying to fix.

This script runs pandoc and then injects that setting, and verifies the result.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Clayton_spce5065_ms2_submission.md")
OUT = os.path.join(HERE, "Clayton_spce5065_ms2_submission.docx")

PANDOC_CANDIDATES = [
    r"C:\Users\jclay\AppData\Local\Pandoc\pandoc.exe",
    r"C:\Program Files\Pandoc\pandoc.exe",
    "pandoc",
]

UPDATE_FIELDS = '<w:updateFields w:val="true"/>'


def find_pandoc():
    for c in PANDOC_CANDIDATES:
        if os.path.exists(c):
            return c
    if shutil.which("pandoc"):
        return "pandoc"
    raise SystemExit("pandoc not found. Tried:\n  " + "\n  ".join(PANDOC_CANDIDATES))


def inject_update_fields(docx_path):
    """Add <w:updateFields w:val="true"/> to word/settings.xml."""
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".docx", dir=HERE)
    os.close(tmp_fd)

    with zipfile.ZipFile(docx_path, "r") as zin:
        names = zin.namelist()
        with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in names:
                data = zin.read(item)
                if item == "word/settings.xml":
                    xml = data.decode("utf-8")
                    if "updateFields" in xml:
                        pass
                    else:
                        # Must be a direct child of <w:settings>. Order is lenient
                        # in practice; placing it first is what Word itself does.
                        idx = xml.find(">", xml.find("<w:settings")) + 1
                        xml = xml[:idx] + UPDATE_FIELDS + xml[idx:]
                    data = xml.encode("utf-8")
                zout.writestr(item, data)

    os.replace(tmp_path, docx_path)


PLACEHOLDER = "Right-click this line and choose Update Field"


def verify(docx_path):
    """Check the delivered file, not the intermediate one.

    Once Word has populated the TOC it drops w:dirty and updateFields, because
    the field no longer needs refreshing. So the meaningful test is whether the
    TOC holds real entries: the placeholder line gone, and PAGEREF entries
    present pointing at the headings.
    """
    problems = []
    with zipfile.ZipFile(docx_path) as z:
        doc = z.read("word/document.xml").decode("utf-8")
        media = [n for n in z.namelist() if n.startswith("word/media/")]

    has_field = "fldChar" in doc and "TOC" in doc
    populated = PLACEHOLDER not in doc
    entries = doc.count("PAGEREF")

    if not has_field:
        problems.append("document.xml has no TOC field")
    if not populated:
        problems.append("TOC still shows placeholder text, Word did not populate it")
    if entries < 10:
        problems.append("TOC has only %d PAGEREF entries, expected 18" % entries)
    if len(media) != 12:
        problems.append("image count is %d, expected 12" % len(media))

    print("  TOC field present      : %s" % has_field)
    print("  TOC populated          : %s" % populated)
    print("  TOC entries (PAGEREF)  : %d" % entries)
    print("  image count            : %d" % len(media))

    return problems


TOC_START = "<!-- TOC:START"
TOC_END = "<!-- TOC:END -->"

# \h makes every entry a hyperlink, which is what makes the docx TOC clickable.
# \o "1-2" takes Heading 1 and 2. The visible text is placeholder until Word
# populates the field; update_toc.ps1 does that at build time.
OPENXML_TOC = r"""```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
<w:p><w:pPr><w:spacing w:before="240" w:after="180"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr><w:t>Table of Contents</w:t></w:r></w:p>
<w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r><w:r><w:instrText xml:space="preserve"> TOC \o "1-2" \h \z \u </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>Right-click this line and choose Update Field to build the table of contents.</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```"""


def preprocess(md_text):
    """Swap the markdown TOC for a real Word TOC field.

    The .md carries a plain markdown TOC so it renders and is clickable in any
    previewer. Word needs a field instead, to get page numbers. Feeding both to
    pandoc would produce two tables of contents, so the markdown one is removed
    here and the field takes its place.
    """
    i = md_text.find(TOC_START)
    j = md_text.find(TOC_END)
    if i < 0 or j < 0:
        raise SystemExit("TOC markers not found in the markdown; cannot build")
    return md_text[:i] + OPENXML_TOC + md_text[j + len(TOC_END):]


def main():
    pandoc = find_pandoc()
    print("pandoc: %s" % pandoc)

    with open(SRC, encoding="utf-8") as fh:
        md = fh.read()
    staged = os.path.join(HERE, "_build_staged.md")
    with open(staged, "w", encoding="utf-8") as fh:
        fh.write(preprocess(md))
    print("staged markdown with Word TOC field substituted")

    try:
        res = subprocess.run([pandoc, staged, "-o", OUT],
                             capture_output=True, text=True)
    finally:
        if os.path.exists(staged):
            os.remove(staged)
    if res.returncode != 0:
        print(res.stderr)
        raise SystemExit("pandoc failed")

    warnings = [l for l in res.stderr.splitlines() if "Could not convert" in l]
    if warnings:
        print("\nMATH CONVERSION WARNINGS (these degrade to raw TeX in the docx):")
        for w in warnings:
            print("  " + w)
    else:
        print("no math conversion warnings")

    inject_update_fields(OUT)

    # Drive Word once to compute the TOC entries and page numbers and bake them
    # into the file. Without this the delivered docx still holds placeholder text,
    # so any reader that is not Word (a markdown preview, a docx viewer, a grader
    # who does not press F9) sees no table of contents at all. This is the
    # Milestone 1 "TOC set up incorrectly" deduction, so it has to be real content.
    ps = os.path.join(HERE, "update_toc.ps1")
    if os.path.exists(ps):
        print("\npopulating TOC via Word...")
        r2 = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps],
            capture_output=True, text=True)
        for line in r2.stdout.splitlines():
            print("  " + line)
        if r2.returncode != 0:
            print("  WARNING: Word step failed, TOC will show placeholder text")
            print("  " + r2.stderr.strip()[:300])
    else:
        print("\nWARNING: update_toc.ps1 missing, TOC will show placeholder text")

    print("\nverification:")
    problems = verify(OUT)
    if problems:
        print("\nFAILED:")
        for p in problems:
            print("  " + p)
        sys.exit(1)

    print("\nbuilt %s" % OUT)


if __name__ == "__main__":
    main()
