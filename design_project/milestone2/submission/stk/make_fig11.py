"""
Figure 11: STK Lifetime tool, inputs and result.

Why this is a composite rather than one screenshot. At GEO the orbit never
decays, so STK stores no lifetime value and its "Report ..." button returns
"the lifetime has not been computed". The tool's answer exists only as a transient
modal popup, which cannot be captured reliably. Both halves below are genuine STK
output:

  left  : the Lifetime dialog itself, cropped from a screenshot of the running
          STK session, showing the MESA parameters the run actually used
  right : the verbatim string STK returned from the Lifetime command, captured
          from the scripted Connect run and stored in lifetime_result.txt

Nothing here is reconstructed or paraphrased.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\jclay\AppData\Local\Temp\claude\C--Users-jclay-Desktop-main-code\61a50e77-eea2-478c-bef5-17fd6e464fc9\scratchpad\lifetime_crop.png"
OUT = os.path.join(HERE, "fig11_stk_lifetime.png")

# Bounding box of the "Lifetime for MESA" dialog inside lifetime_crop.png
DIALOG_BOX = (270, 785, 945, 1150)

RESULT_LINE = "MESA does not decay within the 36500.0 day limit."

PARAMS = [
    ("Drag coefficient, Cd", "2.2"),
    ("Reflection coefficient, Cr", "1.0"),
    ("Drag area", "16.54 m2"),
    ("Area exposed to Sun", "10.24 m2"),
    ("Mass", "2,000 kg"),
    ("Duration limit", "36,500 days (100 yr)"),
]

BG = (255, 255, 255)
FG = (0, 0, 0)
PAD = 16
GAP = 18
CAP_H = 34


def font(sz, bold=False, mono=False):
    names = ["consola.ttf"] if mono else (["arialbd.ttf"] if bold else ["arial.ttf"])
    for n in names + ["segoeui.ttf", "arial.ttf"]:
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            continue
    return ImageFont.load_default()


def main():
    if not os.path.exists(SRC):
        raise SystemExit("missing source screenshot: %s" % SRC)

    dlg = Image.open(SRC).convert("RGB").crop(DIALOG_BOX)

    panel_w = 560
    h = dlg.height
    w = PAD * 2 + dlg.width + GAP + panel_w
    canvas = Image.new("RGB", (w, PAD * 2 + h + CAP_H), BG)
    canvas.paste(dlg, (PAD, PAD))

    d = ImageDraw.Draw(canvas)
    x0 = PAD + dlg.width + GAP
    y = PAD + 8

    d.text((x0, y), "STK Lifetime tool result", fill=FG, font=font(17, bold=True))
    y += 34

    d.text((x0, y), "Parameters used:", fill=(70, 70, 70), font=font(13))
    y += 24
    for label, val in PARAMS:
        d.text((x0 + 8, y), label, fill=(40, 40, 40), font=font(12.5))
        d.text((x0 + 250, y), val, fill=(0, 0, 0), font=font(12.5, bold=True))
        y += 21

    y += 14
    d.text((x0, y), "Returned by STK:", fill=(70, 70, 70), font=font(13))
    y += 24

    box_h = 54
    d.rectangle([x0, y, x0 + panel_w - PAD, y + box_h], fill=(244, 244, 244),
                outline=(150, 150, 150))
    # Wrap on a word boundary so the quoted string stays readable.
    words = RESULT_LINE.split()
    line1, line2 = [], []
    for word in words:
        if len(" ".join(line1 + [word])) <= 40:
            line1.append(word)
        else:
            line2.append(word)
    d.text((x0 + 10, y + 9), " ".join(line1), fill=(0, 0, 0), font=font(12, mono=True))
    d.text((x0 + 10, y + 28), " ".join(line2), fill=(0, 0, 0), font=font(12, mono=True))
    y += box_h + 18

    note = ("At GEO the orbit does not decay, so STK returns no decay\n"
            "date. This confirms Section 7, which puts the drag-decay\n"
            "timescale at 10^5 to 10^6 years.")
    for line in note.split("\n"):
        d.text((x0, y), line, fill=(60, 60, 60), font=font(12))
        y += 18

    d.rectangle([PAD - 1, PAD - 1, PAD + dlg.width, PAD + h], outline=(150, 150, 150))

    cap = "Figure 11. STK Lifetime tool: MESA input parameters (left) and the returned result (right)."
    d.text((PAD, PAD + h + 10), cap, fill=FG, font=font(13))

    canvas.save(OUT)
    print("wrote %s (%d x %d)" % (OUT, canvas.width, canvas.height))


if __name__ == "__main__":
    main()
