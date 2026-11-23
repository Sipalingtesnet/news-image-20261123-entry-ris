#!/usr/bin/env python3
"""Draw a newspaper front page summing up the world news of Monday 23 Nov 2026.

Deterministic: fixed layout, no randomness, no time, no network. Writes
entry.png (1024x1024) in the same directory as this script.
"""
import os
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# Colours (newsprint)
PAPER = (244, 240, 230)
INK = (28, 28, 30)
NAVY = (24, 44, 88)
TEAL = (18, 96, 96)
GREY = (120, 118, 112)
RED = (150, 40, 30)
ORANGE = (200, 110, 30)
YELLOW = (235, 190, 60)
SKY = (150, 180, 205)
SMOKE = (150, 150, 150)

W = 1024
H = 1024

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def text_w(draw, txt, fnt):
    b = draw.textbbox((0, 0), txt, font=fnt)
    return b[2] - b[0]


def text_h(draw, txt, fnt):
    b = draw.textbbox((0, 0), txt, font=fnt)
    return b[3] - b[1]


def wrap(draw, txt, fnt, max_w):
    words = txt.split()
    lines = []
    cur = ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def fit_summary(draw, txt, fnt, max_w, max_lines):
    if not txt.endswith("."):
        txt = txt + "."
    while True:
        lines = wrap(draw, txt, fnt, max_w)
        if len(lines) <= max_lines:
            return lines
        body = txt[:-1].rstrip()
        words = body.split()
        if len(words) <= 1:
            return lines
        txt = " ".join(words[:-1]) + "."


def center_x(draw, txt, fnt, cx):
    return cx - text_w(draw, txt, fnt) // 2


def draw_centered(draw, txt, fnt, cx, y, fill):
    draw.text((center_x(draw, txt, fnt, cx), y), txt, font=fnt, fill=fill)


# ---------------------------------------------------------------------------
# Masthead
# ---------------------------------------------------------------------------
def draw_masthead():
    title_f = font(BOLD, 58)
    date_f = font(BOLD, 26)
    cx = W // 2
    d.text((center_x(d, "THE DAY IN ONE IMAGE", title_f, cx), 26),
           "THE DAY IN ONE IMAGE", font=title_f, fill=INK)
    d.text((center_x(d, "MONDAY, 23 NOVEMBER 2026", date_f, cx), 96),
           "MONDAY, 23 NOVEMBER 2026", font=date_f, fill=NAVY)
    d.rectangle([60, 140, W - 60, 144], fill=NAVY)
    sec_f = font(BOLD, 20)
    d.text((60, 152), "WORLD REPORT", font=sec_f, fill=NAVY)


# ---------------------------------------------------------------------------
# Panel frame
# ---------------------------------------------------------------------------
def panel_box(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=PAPER, outline=INK, width=2)
    d.rectangle([x0, y0, x1, y0 + 8], fill=TEAL)


def panel_header(x0, y0, x1, label):
    f = font(BOLD, 20)
    d.text((x0 + 14, y0 + 16), label, font=f, fill=TEAL)
    d.line([x0 + 14, y0 + 44, x1 - 14, y0 + 44], fill=GREY, width=1)


def panel_headline(x0, y0, x1, txt, size):
    f = font(BOLD, size)
    lines = wrap(d, txt, f, (x1 - x0) - 28)
    y = y0
    for ln in lines:
        d.text((x0 + 14, y), ln, font=f, fill=INK)
        y += text_h(d, ln, f) + 4
    return y


def panel_summary(x0, y0, x1, txt, size, max_lines):
    f = font(REG, size)
    lines = fit_summary(d, txt, f, (x1 - x0) - 28, max_lines)
    y = y0
    for ln in lines:
        d.text((x0 + 14, y), ln, font=f, fill=INK)
        y += text_h(d, ln, f) + 3
    return y


# ---------------------------------------------------------------------------
# Illustrations (PIL shapes only)
# ---------------------------------------------------------------------------
def draw_story1(cx, cy):
    """Apartment block with drone silhouette above and searchlight beams."""
    d.polygon([(cx - 150, cy + 60), (cx - 40, cy - 40), (cx - 10, cy - 40), (cx - 110, cy + 60)],
              fill=(235, 230, 190))
    d.polygon([(cx + 150, cy + 60), (cx + 40, cy - 40), (cx + 10, cy - 40), (cx + 110, cy + 60)],
              fill=(235, 230, 190))
    bx0, by0 = cx - 70, cy - 30
    bx1, by1 = cx + 70, cy + 60
    d.rectangle([bx0, by0, bx1, by1], fill=(205, 190, 165), outline=INK, width=2)
    for r in range(3):
        for c in range(3):
            wx = bx0 + 12 + c * 42
            wy = by0 + 12 + r * 34
            d.rectangle([wx, wy, wx + 22, wy + 18], fill=(250, 240, 170), outline=INK, width=1)
    dx, dy = cx, by0 - 34
    d.line([(dx - 34, dy), (dx + 34, dy)], fill=INK, width=3)
    d.ellipse([dx - 8, dy - 8, dx + 8, dy + 8], fill=INK)
    d.line([(dx - 34, dy), (dx - 46, dy - 10)], fill=INK, width=2)
    d.line([(dx + 34, dy), (dx + 46, dy - 10)], fill=INK, width=2)
    d.line([(dx, dy - 14), (dx, dy - 2)], fill=INK, width=2)


def draw_story2(cx, cy):
    """Factory building with flames and a rescue helmet."""
    bx0, by0 = cx - 80, cy - 10
    bx1, by1 = cx + 80, cy + 60
    d.rectangle([bx0, by0, bx1, by1], fill=(200, 185, 160), outline=INK, width=2)
    d.rectangle([cx - 20, by0 - 55, cx - 5, by0], fill=(170, 160, 140), outline=INK, width=1)
    d.polygon([(cx - 40, by0), (cx - 25, by0 - 30), (cx - 10, by0)], fill=ORANGE)
    d.polygon([(cx - 30, by0), (cx - 18, by0 - 22), (cx - 6, by0)], fill=YELLOW)
    d.polygon([(cx - 18, by0), (cx - 8, by0 - 26), (cx + 4, by0)], fill=ORANGE)
    d.ellipse([cx - 22, by0 - 58, cx - 3, by0 - 44], fill=SMOKE)
    d.ellipse([cx - 30, by0 - 70, cx - 6, by0 - 53], fill=SMOKE)
    for c in range(3):
        wx = bx0 + 14 + c * 48
        d.rectangle([wx, by0 + 14, wx + 26, by0 + 34], fill=(250, 240, 170), outline=INK, width=1)
    hx, hy = cx + 70, cy + 50
    d.arc([hx - 18, hy - 18, hx + 18, hy + 18], 180, 360, fill=RED, width=4)
    d.arc([hx - 18, hy - 18, hx + 18, hy + 18], 0, 180, fill=RED, width=4)
    d.line([(hx - 18, hy), (hx + 18, hy)], fill=RED, width=4)


def draw_story3(cx, cy):
    """Globe with factory chimneys and a cracked document labelled DEAL."""
    d.ellipse([cx - 55, cy - 55, cx + 55, cy + 55], fill=(170, 200, 220), outline=INK, width=3)
    d.ellipse([cx - 55, cy - 20, cx + 55, cy + 20], outline=(120, 160, 185), width=1)
    d.ellipse([cx - 20, cy - 55, cx + 20, cy + 55], outline=(120, 160, 185), width=1)
    for ox in (-30, 0, 30):
        d.rectangle([cx + ox - 6, cy - 78, cx + ox + 6, cy - 55], fill=(120, 120, 120), outline=INK, width=1)
        d.polygon([(cx + ox - 6, cy - 78), (cx + ox, cy - 80), (cx + ox + 6, cy - 78)], fill=SMOKE)
    dx0, dy0 = cx - 62, cy + 30
    dx1, dy1 = cx + 62, cy + 62
    d.rectangle([dx0, dy0, dx1, dy1], fill=(250, 248, 240), outline=INK, width=2)
    f = font(BOLD, 20)
    d.text((center_x(d, "DEAL", f, cx), dy0 + 6), "DEAL", font=f, fill=RED)
    d.line([(dx0 + 20, dy0), (cx, dy0 + 16), (dx1 - 10, dy0 + 6)], fill=INK, width=2)


def draw_story4(cx, cy):
    """Cargo ship on waves with flames and smoke."""
    for i in range(6):
        wx = cx - 90 + i * 34
        d.arc([wx, cy + 30, wx + 40, cy + 60], 180, 360, fill=(90, 130, 165), width=3)
    d.polygon([(cx - 80, cy + 10), (cx + 80, cy + 10), (cx + 60, cy + 40), (cx - 60, cy + 40)],
              fill=(90, 90, 95), outline=INK, width=2)
    d.rectangle([cx - 40, cy - 30, cx + 40, cy + 10], fill=(150, 150, 155), outline=INK, width=2)
    d.rectangle([cx - 15, cy - 55, cx + 15, cy - 30], fill=(150, 150, 155), outline=INK, width=2)
    d.polygon([(cx - 35, cy - 30), (cx - 22, cy - 55), (cx - 9, cy - 30)], fill=ORANGE)
    d.polygon([(cx - 28, cy - 30), (cx - 16, cy - 48), (cx - 4, cy - 30)], fill=YELLOW)
    d.ellipse([cx + 18, cy - 60, cx + 44, cy - 40], fill=SMOKE)
    d.ellipse([cx + 28, cy - 72, cx + 56, cy - 50], fill=SMOKE)


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
MARGIN = 40
GAP = 18
top = 168
bottom = 830
panel_h = (bottom - top - GAP) // 2
panel_w = (W - 2 * MARGIN - GAP) // 2
row0y = top
row1y = top + panel_h + GAP

draw_masthead()

# Panel 1 - Kyiv drone strike
x0, y0 = MARGIN, row0y
x1, y1 = MARGIN + panel_w, row0y + panel_h
panel_box(x0, y0, x1, y1)
panel_header(x0, y0, x1, "EUROPE")
panel_headline(x0, y0 + 52, x1, "KYIV DRONE STRIKE", 30)
panel_summary(x0, y0 + 108, x1,
              "At least 14 people are missing after a Russian drone hit a "
              "residential building in the Kyiv region.", 20, 3)
draw_story1(x0 + panel_w // 2, y0 + 255)

# Panel 2 - Indonesia factory fire
x0, y0 = MARGIN + panel_w + GAP, row0y
x1, y1 = MARGIN + panel_w + GAP + panel_w, row0y + panel_h
panel_box(x0, y0, x1, y1)
panel_header(x0, y0, x1, "ASIA")
panel_headline(x0, y0 + 52, x1, "INDONESIA FACTORY FIRE", 30)
panel_summary(x0, y0 + 108, x1,
              "Seven bodies recovered and dozens of workers still missing "
              "after a fire at a confectionery factory.", 20, 3)
draw_story2(x0 + panel_w // 2, y0 + 255)

# Panel 3 - COP31 climate talks collapse
x0, y0 = MARGIN, row1y
x1, y1 = MARGIN + panel_w, row1y + panel_h
panel_box(x0, y0, x1, y1)
panel_header(x0, y0, x1, "CLIMATE")
panel_headline(x0, y0 + 52, x1, "COP31 TALKS COLLAPSE", 30)
panel_summary(x0, y0 + 108, x1,
              "No deal in Antalya after the EU rejected a draft dropping "
              "fossil-fuel phase-out language.", 20, 3)
draw_story3(x0 + panel_w // 2, y0 + 255)

# Panel 4 - Russian ship ablaze
x0, y0 = MARGIN + panel_w + GAP, row1y
x1, y1 = MARGIN + panel_w + GAP + panel_w, row1y + panel_h
panel_box(x0, y0, x1, y1)
panel_header(x0, y0, x1, "BALTIC")
panel_headline(x0, y0 + 52, x1, "RUSSIAN SHIP ABLAZE", 30)
panel_summary(x0, y0 + 108, x1,
              "A Russian cargo ship still burns off Finland after a strike "
              "in the Gulf of Finland.", 20, 3)
draw_story4(x0 + panel_w // 2, y0 + 255)


# ---------------------------------------------------------------------------
# Bottom ticker strip (ALSO headlines)
# ---------------------------------------------------------------------------
tick_top = 844
tick_bot = 1014
d.rectangle([MARGIN, tick_top, W - MARGIN, tick_bot], fill=(235, 230, 218),
            outline=INK, width=2)
lab_f = font(BOLD, 20)
d.text((MARGIN + 14, tick_top + 10), "ALSO", font=lab_f, fill=NAVY)

tick_f = font(REG, 18)
tick_items = [
    "24 civilians killed in South Sudan",
    "6.1 quake jolts northern Japan",
    "S. Korea minister quits over AI exam scandal",
    "Liverpool beat ten-man Man United",
    "FIFA to confirm UK as 2035 Women's World Cup host",
    "UN to keep talks on lethal AI weapons",
    "India v New Zealand Test to final day",
]
tx = MARGIN + 14
ty = tick_top + 42
dot = " \u00b7 "
for item in tick_items:
    seg = item + dot
    wseg = text_w(d, seg, tick_f)
    if tx + wseg > W - MARGIN - 14:
        tx = MARGIN + 14
        ty += 26
    d.text((tx, ty), seg, font=tick_f, fill=INK)
    tx += wseg


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG")
print("wrote", out)
