#!/usr/bin/env python3
"""Render the 25 November 2026 world-news front page to entry.png (1024x1024).

Drawn with Pillow and real fonts (Liberation Serif/Sans): every glyph is real
text, so nothing in the image is garbled. Run: python3 build/render.py
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 231)
INK = (26, 26, 26)
RED = (163, 22, 33)
MUTED = (107, 100, 85)
BODY = (51, 48, 42)
RULE_LIGHT = (201, 192, 171)
CREAM = (246, 241, 231)

F = "/usr/share/fonts/truetype/liberation/"


def font(name, size):
    return ImageFont.truetype(F + name, size)


SERIF_B = lambda s: font("LiberationSerif-Bold.ttf", s)
SERIF = lambda s: font("LiberationSerif-Regular.ttf", s)
SANS = lambda s: font("LiberationSans-Regular.ttf", s)
SANS_B = lambda s: font("LiberationSans-Bold.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill, leading):
    lines = wrap(draw, text, fnt, width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text, size=15):
    draw.text((x, y), text, font=SANS_B(size), fill=RED)
    return y + size + 8


def icon_box(draw, x, y, color, draw_fn):
    draw.rounded_rectangle([x, y, x + 52, y + 52], radius=6, fill=color)
    draw_fn(draw, x, y)


def icon_tower(d, x, y):
    # skyscraper: three bars with windows
    d.rectangle([x + 14, y + 8, x + 20, y + 44], fill=CREAM)
    d.rectangle([x + 24, y + 16, x + 30, y + 44], fill=CREAM)
    d.rectangle([x + 32, y + 24, x + 38, y + 44], fill=CREAM)
    d.rectangle([x + 10, y + 45, x + 42, y + 47], fill=CREAM)


def icon_search(d, x, y):
    d.ellipse([x + 10, y + 9, x + 26, y + 25], outline=CREAM, width=3)
    d.line([x + 23, y + 23, x + 32, y + 32], fill=CREAM, width=4)


def icon_boat(d, x, y):
    d.polygon([(x + 8, y + 26), (x + 44, y + 26), (x + 38, y + 36), (x + 14, y + 36)], fill=CREAM)
    d.polygon([(x + 24, y + 10), (x + 24, y + 24), (x + 34, y + 24)], fill=CREAM)
    d.line([x + 24, y + 10, x + 24, y + 26], fill=CREAM, width=2)
    d.arc([x + 6, y + 40, x + 46, y + 48], start=0, end=180, fill=CREAM, width=2)


def icon_feather(d, x, y):
    d.polygon([(x + 26, y + 6), (x + 38, y + 18), (x + 30, y + 34), (x + 20, y + 26)], fill=CREAM)
    d.line([x + 26, y + 6, x + 20, y + 40], fill=CREAM, width=2)
    d.line([x + 20, y + 40, x + 12, y + 46], fill=CREAM, width=2)


def icon_heli(d, x, y):
    d.ellipse([x + 24, y + 12, x + 32, y + 20], fill=CREAM)
    d.line([x + 6, y + 12, x + 46, y + 12], fill=CREAM, width=3)
    d.rectangle([x + 12, y + 22, x + 32, y + 32], fill=CREAM)
    d.rectangle([x + 32, y + 25, x + 44, y + 29], fill=CREAM)
    d.line([x + 16, y + 34, x + 14, y + 42], fill=CREAM, width=2)
    d.line([x + 28, y + 34, x + 30, y + 42], fill=CREAM, width=2)
    d.line([x + 10, y + 42, x + 34, y + 42], fill=CREAM, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    L, R = 44, W - 44
    content_w = R - L

    # Top bar
    d.text((L, 30), "WORLD NEWS \u00b7 ONE DAY \u00b7 ONE IMAGE", font=SANS_B(15), fill=MUTED)
    right = "25 NOV 2026"
    d.text((R - d.textlength(right, font=SANS_B(15)), 30), right, font=SANS_B(15), fill=MUTED)

    # Masthead
    title = "The World in One Day"
    tf = SERIF_B(72)
    d.text(((W - d.textlength(title, font=tf)) / 2, 56), title, font=tf, fill=INK)
    date = "W E D N E S D A Y ,  2 5  N O V E M B E R  2 0 2 6"
    df = SANS_B(21)
    d.text(((W - d.textlength(date, font=df)) / 2, 148), date, font=df, fill=RED)

    # Double rule
    d.line([L, 186, R, 186], fill=INK, width=4)
    d.line([L, 193, R, 193], fill=INK, width=1)

    # Lead story
    y = kicker(d, L, 208, "UKRAINE \u00b7 RUSSIA")
    y = draw_wrapped(d, L, y, "Putin warns retaliation is \u201cinevitable\u201d as Ukraine keeps striking Russian oil refineries",
                     SERIF_B(40), content_w, INK, 46)
    y = draw_wrapped(d, L, y + 6, "Moscow says it will answer Kyiv\u2019s campaign against its refineries, as the war\u2019s long-range strikes reach deeper into Russia.",
                     SANS(18), content_w, BODY, 25)

    # Story grid: 2 columns x 2 rows
    stories = [
        ("MIDDLE EAST", "Houthis strike Riyadh\u2019s tallest tower; 11 wounded",
         "Saudi Arabia condemns the attack on the PIF Tower, home to the sovereign wealth fund \u2014 the second strike on the skyscraper in a week.", icon_tower),
        ("CHINA", "Shanghai pledges loyalty as Chen Jining probe widens",
         "The Shanghai party chief and Politburo member is under investigation for suspected serious discipline violations \u2014 the fourth Politburo member probed since 2025.", icon_search),
        ("MIGRATION", "About 175 migrants missing as boat from Senegal vanishes",
         "The boat was bound for Europe when contact was lost; a search is under way for those on board.", icon_boat),
        ("UNITED STATES", "Trump pardons turkeys Freedom and Feathers",
         "The annual White House ceremony, a day before Thanksgiving, spares the two birds their fate at the dinner table.", icon_feather),
    ]
    col_w = (content_w - 28) // 2
    grid_y = y + 16
    row_h = 168
    for i, (kick, head, summ, icon) in enumerate(stories):
        cx = L + (i % 2) * (col_w + 28)
        cy = grid_y + (i // 2) * row_h
        d.line([cx, cy, cx + col_w, cy], fill=RULE_LIGHT, width=1)
        icon_box(d, cx, cy + 12, INK, icon)
        tx = cx + 64
        ty = kicker(d, tx, cy + 12, kick, size=14)
        ty = draw_wrapped(d, tx, ty, head, SERIF_B(24), col_w - 64, INK, 28)
        draw_wrapped(d, tx, ty + 4, summ, SANS(15), col_w - 64, BODY, 20)

    # T\u00fcrkiye band
    band_y = grid_y + 2 * row_h + 8
    d.line([L, band_y, R, band_y], fill=RULE_LIGHT, width=1)
    icon_box(d, L, band_y + 12, RED, icon_heli)
    tx = L + 64
    ty = kicker(d, tx, band_y + 12, "T\u00dcRKIYE", size=14)
    ty = draw_wrapped(d, tx, ty, "Five killed as Turkish military helicopter crashes",
                      SERIF_B(23), content_w - 64, INK, 27)
    end_y = draw_wrapped(d, tx, ty + 3, "The helicopter came down during a training flight in western T\u00fcrkiye.",
                         SANS(15), content_w - 64, BODY, 20)
    band_bottom = end_y + 10
    d.line([L, band_bottom, R, band_bottom], fill=RULE_LIGHT, width=1)

    # Also today
    by = band_bottom + 14
    by = kicker(d, L, by, "ALSO TODAY")
    briefs = [
        "Gunmen take 25 hostage at a supermarket in Cartagena, Colombia",
        "DR Congo rebels call off their advance on Bunia and pull back",
        "Trump awards Rudy Giuliani the Medal of Freedom",
    ]
    bw = (content_w - 44) // 3
    for i, b in enumerate(briefs):
        bx = L + i * (bw + 22)
        d.line([bx, by, bx + 3, by + 52], fill=RED, width=3)
        draw_wrapped(d, bx + 12, by, b, SANS(15), bw - 12, INK, 20)

    # Footer
    fy = H - 56
    d.line([L, fy, R, fy], fill=INK, width=4)
    foot = "All stories reported on Wednesday 25 November 2026 \u00b7 Sources: Reuters, AP, SCMP, CNN"
    ff = SANS(13)
    d.text(((W - d.textlength(foot, font=ff)) / 2, fy + 12), foot, font=ff, fill=MUTED)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
