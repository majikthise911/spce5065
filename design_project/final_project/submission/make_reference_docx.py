"""
Build the pandoc reference document used by build_docx.py.

The grade sheet awards grammar points for a block-justified paper, and pandoc's
default docx template leaves body text ragged-right. The `<style>` block at the
top of the markdown handles this for the HTML and PDF paths, but raw CSS does
nothing for docx.

The fix is a reference document. This script pulls pandoc's own default one,
adds `<w:jc w:val="both"/>` to the paragraph properties of the styles that
carry body text, and writes it back out. It only needs re-running if pandoc is
upgraded.

Run: python3 make_reference_docx.py
"""

import os
import re
import shutil
import subprocess
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "reference.docx")

PANDOC_CANDIDATES = ["/opt/homebrew/bin/pandoc", "/usr/local/bin/pandoc", "pandoc"]

# Styles that hold running text. Headings, captions, and table text are left
# alone: justifying a two-word caption looks worse than leaving it ragged.
JUSTIFY_STYLES = ("BodyText", "FirstParagraph", "Compact")


def find_pandoc():
    for c in PANDOC_CANDIDATES:
        if os.path.exists(c) or shutil.which(c):
            return c
    raise SystemExit("pandoc not found")


def justify(styles_xml):
    """Insert <w:jc w:val="both"/> into the pPr of each body-text style."""
    out = styles_xml
    for name in JUSTIFY_STYLES:
        # Match the whole <w:style ...w:styleId="NAME">...</w:style> block.
        pat = re.compile(
            r'(<w:style [^>]*w:styleId="%s"[^>]*>)(.*?)(</w:style>)' % name,
            re.S)
        m = pat.search(out)
        if not m:
            print("  style %s not found, skipped" % name)
            continue
        head, body, tail = m.groups()
        if "<w:jc " in body:
            body = re.sub(r'<w:jc w:val="[^"]*"/>', '<w:jc w:val="both"/>', body)
        elif "<w:pPr>" in body:
            body = body.replace("<w:pPr>", '<w:pPr><w:jc w:val="both"/>', 1)
        else:
            body = '<w:pPr><w:jc w:val="both"/></w:pPr>' + body
        out = out[:m.start()] + head + body + tail + out[m.end():]
        print("  justified style %s" % name)
    return out


def main():
    pandoc = find_pandoc()
    res = subprocess.run([pandoc, "--print-default-data-file", "reference.docx"],
                         capture_output=True)
    if res.returncode != 0:
        raise SystemExit("could not read pandoc's default reference.docx")

    tmp = os.path.join(HERE, "_reference_default.docx")
    with open(tmp, "wb") as fh:
        fh.write(res.stdout)

    with zipfile.ZipFile(tmp) as zin:
        names = zin.namelist()
        with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in names:
                data = zin.read(item)
                if item == "word/styles.xml":
                    data = justify(data.decode("utf-8")).encode("utf-8")
                zout.writestr(item, data)
    os.remove(tmp)
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
