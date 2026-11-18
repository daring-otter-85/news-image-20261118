#!/usr/bin/env python3
"""Draw the news poster for Wednesday, November 18, 2026.

A one-image summary of the day: a dated masthead and six panels, each
with a category tag, a small drawn icon, a bold headline and one short
factual line.  Drawn entirely with Pillow so every word stays crisp.
Running this file writes entry.png next to it.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (24, 28, 38)
MUTED = (96, 102, 112)
NAVY = (16, 34, 64)
RED = (178, 34, 44)

BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_KICKER = font(BOLD, 25)
F_TITLE = font(BOLD, 52)
F_SUB = font(REG, 24)
F_TAG = font(BOLD, 19)
F_HEAD = font(BOLD, 29)
F_DESC = font(REG, 21)
F_FOOT = font(REG, 19)


def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- icons
def icon_missile(d, x, y, s, color):
    d.polygon([(x + s * 0.5, y), (x + s * 0.72, y + s * 0.34),
               (x + s * 0.62, y + s * 0.78), (x + s * 0.38, y + s * 0.78),
               (x + s * 0.28, y + s * 0.34)], fill=color)
    d.polygon([(x + s * 0.38, y + s * 0.78), (x + s * 0.62, y + s * 0.78),
               (x + s * 0.5, y + s)], fill=(240, 140, 40))
    d.ellipse([x + s * 0.42, y + s * 0.3, x + s * 0.58, y + s * 0.46],
              fill=(255, 255, 255))


def icon_globe(d, x, y, s, color):
    d.ellipse([x + s * 0.08, y + s * 0.08, x + s * 0.92, y + s * 0.92],
              outline=color, width=6)
    d.ellipse([x + s * 0.34, y + s * 0.08, x + s * 0.66, y + s * 0.92],
              outline=color, width=4)
    d.line([x + s * 0.1, y + s * 0.38, x + s * 0.9, y + s * 0.38],
           fill=color, width=4)
    d.line([x + s * 0.1, y + s * 0.64, x + s * 0.9, y + s * 0.64],
           fill=color, width=4)


def icon_ballot(d, x, y, s, color):
    d.rectangle([x + s * 0.12, y + s * 0.52, x + s * 0.88, y + s * 0.9],
                fill=color)
    d.rectangle([x + s * 0.34, y + s * 0.06, x + s * 0.62, y + s * 0.58],
                fill=color)
    d.polygon([(x + s * 0.4, y + s * 0.3), (x + s * 0.46, y + s * 0.38),
               (x + s * 0.58, y + s * 0.2), (x + s * 0.58, y + s * 0.3),
               (x + s * 0.47, y + s * 0.46), (x + s * 0.4, y + s * 0.38)],
              fill=(255, 255, 255))
    d.rectangle([x + s * 0.24, y + s * 0.62, x + s * 0.76, y + s * 0.7],
                fill=(255, 255, 255))


def icon_bridge(d, x, y, s, color):
    d.arc([x, y + s * 0.05, x + s, y + s * 0.85], 180, 360, fill=color, width=6)
    for fx in (0.18, 0.38, 0.62, 0.82):
        d.line([x + s * fx, y + s * 0.28, x + s * fx, y + s * 0.62],
               fill=color, width=4)
    d.line([x, y + s * 0.62, x + s, y + s * 0.62], fill=color, width=7)
    d.line([x, y + s * 0.8, x + s, y + s * 0.8], fill=(70, 130, 200), width=5)
    d.line([x, y + s * 0.92, x + s, y + s * 0.92], fill=(70, 130, 200), width=5)


def icon_virus(d, x, y, s, color):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.26
    for ang in range(0, 360, 45):
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line([cx + dx * r * 0.8, cy + dy * r * 0.8,
                cx + dx * r * 1.45, cy + dy * r * 1.45], fill=color, width=5)
        d.ellipse([cx + dx * r * 1.45 - 6, cy + dy * r * 1.45 - 6,
                   cx + dx * r * 1.45 + 6, cy + dy * r * 1.45 + 6], fill=color)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    d.ellipse([cx - r * 0.45, cy - r * 0.2, cx - r * 0.1, cy + r * 0.15],
              fill=(255, 255, 255))
    d.ellipse([cx + r * 0.15, cy + r * 0.3, cx + r * 0.45, cy + r * 0.6],
              fill=(255, 255, 255))


def icon_gavel(d, x, y, s, color):
    d.polygon([(x + s * 0.3, y + s * 0.12), (x + s * 0.52, y + s * 0.34),
               (x + s * 0.4, y + s * 0.46), (x + s * 0.18, y + s * 0.24)],
              fill=color)
    d.line([x + s * 0.44, y + s * 0.4, x + s * 0.78, y + s * 0.74],
           fill=color, width=8)
    d.rectangle([x + s * 0.14, y + s * 0.84, x + s * 0.86, y + s * 0.92],
                fill=color)


ICONS = {
    "missile": icon_missile,
    "globe": icon_globe,
    "ballot": icon_ballot,
    "bridge": icon_bridge,
    "virus": icon_virus,
    "gavel": icon_gavel,
}

PANELS = [
    {
        "tag": "MIDDLE EAST", "color": (178, 34, 44), "icon": "missile",
        "headline": "IRAN STRIKES KUWAIT AND BAHRAIN",
        "desc": "Iran fired on U.S.-linked bases in Kuwait and Bahrain "
                "in reply to the U.S. strike on Qeshm Island.",
    },
    {
        "tag": "DIPLOMACY", "color": (38, 84, 160), "icon": "globe",
        "headline": "XI AND PUTIN MEET IN SHENZHEN",
        "desc": "China's Xi Jinping hosted Russia's Vladimir Putin ahead "
                "of a trilateral summit with President Trump.",
    },
    {
        "tag": "U.S. POLITICS", "color": (24, 120, 74), "icon": "ballot",
        "headline": "PELTOLA FLIPS ALASKA SENATE SEAT",
        "desc": "Democrat Mary Peltola beat incumbent Dan Sullivan, "
                "giving Democrats a 56-44 Senate majority.",
    },
    {
        "tag": "UKRAINE WAR", "color": (70, 96, 140), "icon": "bridge",
        "headline": "KERCH BRIDGE SPAN COLLAPSES",
        "desc": "Ukraine hit the Kerch Bridge for a second day; part of "
                "the road span collapsed into the strait.",
    },
    {
        "tag": "HEALTH", "color": (112, 62, 168), "icon": "virus",
        "headline": "EBOLA CASES PASS 11,000 IN CONGO",
        "desc": "The Ebola outbreak in DR Congo passed 11,000 cases, "
                "with children under five hit the hardest.",
    },
    {
        "tag": "ISRAEL", "color": (206, 110, 24), "icon": "gavel",
        "headline": "KNESSET ELECTS A NEW SPEAKER",
        "desc": "Israel's parliament elected Matan Kahana as speaker, a "
                "win for Prime Minister-elect Gadi Eisenkot.",
    },
]


def draw_panel(d, x, y, w, h, panel):
    color = panel["color"]
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=(255, 255, 255),
                        outline=(210, 204, 190), width=2)
    d.rounded_rectangle([x, y, x + w, y + 40], radius=14, fill=color)
    d.rectangle([x, y + 26, x + w, y + 40], fill=color)
    d.text((x + 16, y + 8), panel["tag"], font=F_TAG, fill=(255, 255, 255))
    bx, by, bs = x + 16, y + 56, 84
    d.rounded_rectangle([bx, by, bx + bs, by + bs], radius=12, fill=color)
    inner = Image.new("RGBA", (bs, bs), (0, 0, 0, 0))
    idraw = ImageDraw.Draw(inner)
    ICONS[panel["icon"]](idraw, 10, 10, bs - 20, (255, 255, 255))
    tx = x + 116
    head_lines = wrap(d, panel["headline"], F_HEAD, x + w - tx - 14)
    hy = y + 54
    for line in head_lines[:2]:
        d.text((tx, hy), line, font=F_HEAD, fill=INK)
        hy += 36
    desc_lines = wrap(d, panel["desc"], F_DESC, w - 32)
    dy = y + 152
    for line in desc_lines[:3]:
        d.text((x + 16, dy), line, font=F_DESC, fill=MUTED)
        dy += 28
    return inner, (bx, by)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 156], fill=RED)
    d.text((36, 18), "THE WORLD IN ONE PICTURE  ·  DAILY NEWS POSTER",
           font=F_KICKER, fill=(250, 205, 90))
    d.text((36, 50), "WEDNESDAY, NOVEMBER 18, 2026", font=F_TITLE,
           fill=(255, 255, 255))
    d.text((36, 116), "The six stories that defined the day, at a glance",
           font=F_SUB, fill=(190, 202, 224))

    margin, gap = 28, 16
    pw = (W - margin * 2 - gap) // 2
    ph = 258
    top = 172
    overlays = []
    for i, panel in enumerate(PANELS):
        col, row = i % 2, i // 2
        x = margin + col * (pw + gap)
        y = top + row * (ph + gap)
        inner, pos = draw_panel(d, x, y, pw, ph, panel)
        overlays.append((inner, pos))
    for inner, pos in overlays:
        img.paste(inner, pos, inner)

    d.text((36, H - 34),
           "Compiled from Reuters, AP, AFP and Just Security reporting.",
           font=F_FOOT, fill=MUTED)

    out = HERE / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
