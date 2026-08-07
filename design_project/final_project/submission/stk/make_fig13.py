"""
Compose Figure 13 for the final report from two STK 3D window captures.

Why two panels: STK substitutes a point marker for the 3D model beyond a certain
viewing range, so a single frame cannot show both the spacecraft model and the
full GEO orbit at readable size. Panel (a) is the model, panel (b) is the orbit.
Both are captures of the same MESA_MS2 scenario at the same epoch.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

# Both panels are manual captures from the running STK session, and both must use
# the SAME model the analysis used (Space/a2100.glb). An earlier scripted panel (a)
# still showed anik_f1.glb and was inconsistent with the Solar Panel results.
# The three-quarter view here reads far better than a flat-on scripted capture.
PANEL_A = os.path.join(HERE, "fig9_panel_a_model.png")
# Panel (b) is a wider manual capture: the complete GEO ring around Earth, which
# reads far better than the near-edge-on trail the scripted view produced.
PANEL_B = os.path.join(HERE, "fig9_stk_3d_zoomed_out.png")
OUT = os.path.join(HERE, "fig13_stk_3d.png")

CAP_A = "(a) MESA 3D model, bus with two deployed solar wings"
CAP_B = "(b) MESA on station in the GEO ring at 105 deg W"

BG = (255, 255, 255)
FG = (0, 0, 0)
PAD = 14
CAP_H = 34
GAP = 14


def load_font(size=15):
    for name in ("arial.ttf", "segoeui.ttf", "calibri.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def main():
    for p in (PANEL_A, PANEL_B):
        if not os.path.exists(p):
            raise SystemExit("missing panel: %s" % p)

    a = Image.open(PANEL_A).convert("RGB")
    b = Image.open(PANEL_B).convert("RGB")

    # Match heights so the two panels sit on a common baseline.
    h = min(a.height, b.height)
    if a.height != h:
        a = a.resize((round(a.width * h / a.height), h), Image.LANCZOS)
    if b.height != h:
        b = b.resize((round(b.width * h / b.height), h), Image.LANCZOS)

    w = PAD * 2 + a.width + GAP + b.width
    total_h = PAD * 2 + h + CAP_H

    canvas = Image.new("RGB", (w, total_h), BG)
    canvas.paste(a, (PAD, PAD))
    canvas.paste(b, (PAD + a.width + GAP, PAD))

    draw = ImageDraw.Draw(canvas)
    font = load_font(15)

    def centered(text, x0, width, y):
        try:
            tw = draw.textlength(text, font=font)
        except Exception:
            tw = len(text) * 7
        draw.text((x0 + (width - tw) / 2, y), text, fill=FG, font=font)

    cap_y = PAD + h + 9
    centered(CAP_A, PAD, a.width, cap_y)
    centered(CAP_B, PAD + a.width + GAP, b.width, cap_y)

    # Thin border so the black 3D captures read as figure panels on a white page.
    draw.rectangle([PAD - 1, PAD - 1, PAD + a.width, PAD + h], outline=(120, 120, 120))
    x0 = PAD + a.width + GAP
    draw.rectangle([x0 - 1, PAD - 1, x0 + b.width, PAD + h], outline=(120, 120, 120))

    canvas.save(OUT)
    print("wrote %s  (%d x %d)" % (OUT, canvas.width, canvas.height))


if __name__ == "__main__":
    main()
