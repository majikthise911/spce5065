"""
Figure 15: STK Lifetime tool, inputs and result.

The composite itself was built during the Milestone 2 STK session on the Windows
machine that ran STK 13. Both halves are genuine STK output:

  left  : the Lifetime dialog, cropped from a screenshot of the running STK
          session, showing the MESA parameters the run actually used
  right : the verbatim string STK returned from the Lifetime command, captured
          from the scripted Connect run and stored in lifetime_result.txt

Nothing in it is reconstructed or paraphrased. The original build script needed
a scratch screenshot that only existed on that machine, so this script does the
two things the final report still needs: it carries the Milestone 2 composite
forward, restamps the baked-in caption from "Figure 11" to "Figure 15", and
repoints the closing note from Milestone 2's Section 7 to this report's
Section 3, where the orbital lifetime discussion now lives.

Run: python3 make_fig15.py
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "fig11_stk_lifetime.png")
OUT = os.path.join(HERE, "fig15_stk_lifetime.png")

CAPTION = ("Figure 15. STK Lifetime tool: MESA input parameters (left) and the "
           "returned result (right).")

NOTE = ["At GEO the orbit does not decay, so STK returns no decay",
        "date. This confirms Section 3, which puts the drag-decay",
        "timescale at 10^5 to 10^6 years."]

BG = (255, 255, 255)
FG = (0, 0, 0)
NOTE_FG = (60, 60, 60)
PAD = 16
CAP_BAND = 40      # height of the caption strip at the bottom of the composite
NOTE_BOX = (705, 310, 1285, 372)   # region holding the closing note
NOTE_LEADING = 19


def font(sz):
    for name in ("Arial.ttf", "Helvetica.ttc",
                 "/System/Library/Fonts/Supplemental/Arial.ttf"):
        try:
            return ImageFont.truetype(name, sz)
        except Exception:
            continue
    return ImageFont.load_default()


def main():
    if not os.path.exists(SRC):
        raise SystemExit("missing Milestone 2 composite: %s" % SRC)

    img = Image.open(SRC).convert("RGB")
    d = ImageDraw.Draw(img)

    # Wipe the old caption strip and write the new one in its place.
    d.rectangle([0, img.height - CAP_BAND, img.width, img.height], fill=BG)
    d.text((PAD, img.height - CAP_BAND + 14), CAPTION, fill=FG, font=font(13))

    # Repoint the closing note at this report's section numbering.
    d.rectangle(list(NOTE_BOX), fill=BG)
    y = NOTE_BOX[1] + 3
    for line in NOTE:
        d.text((NOTE_BOX[0] + 4, y), line, fill=NOTE_FG, font=font(12))
        y += NOTE_LEADING

    img.save(OUT)
    print("wrote %s (%d x %d)" % (OUT, img.width, img.height))


if __name__ == "__main__":
    main()
