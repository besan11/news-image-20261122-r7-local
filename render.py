#!/usr/bin/env python3
"""Render news-image-20261122 r7: Sunday 22 November 2026 in one picture.

Draws the whole 1024x1024 front page programmatically with Pillow:
masthead, stat row, region bar, UTC strip, 3 composed lead scenes,
12 mid panels with small drawn scenes, 21 one-line briefs, a dotted
world map with numbered pins, an itemised DATE CHECK and a footer.
Every story, number and date in this file was verified against wire
sources (see NOTES.md) with a wire cutoff of 23 Nov 03:00 UTC.
Deterministic: same input -> same PNG bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

CREAM = (248, 244, 232)
PAPER = (252, 250, 242)
NAVY = (16, 28, 51)
NAVY2 = (24, 44, 84)
RED = (179, 35, 27)
RED_DK = (140, 22, 16)
GOLD = (201, 162, 39)
INK = (24, 24, 24)
GREY = (90, 88, 80)
LINE = (180, 172, 150)
TEAL = (18, 92, 86)
GREEN = (34, 120, 60)
AMBER = (176, 118, 10)
BLUE = (30, 90, 160)
PURPLE = (110, 70, 140)
ORANGE = (198, 96, 20)
SKY = (214, 228, 238)
NIGHT = (14, 22, 46)

REGION_COLOR = {
    "EUROPE": (30, 90, 160), "MIDDLE EAST": (140, 60, 30),
    "ASIA-PACIFIC": (198, 120, 10), "AMERICAS": (34, 120, 60),
    "AFRICA": (110, 70, 140), "OCEANIA": (18, 120, 120),
    "WORLD": (100, 100, 100),
}
TAG_COLOR = {
    "REPORTED": (34, 120, 60), "CLAIM": (176, 118, 10),
    "ONGOING": (30, 90, 160), "FORECAST": (110, 110, 110),
    "CONFIRMED": (18, 92, 86),
}


def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, lh, max_lines=None):
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def chip(draw, x, y, text, fnt, bg, fg=(255, 255, 255), pad=4, h=14):
    w = int(draw.textlength(text, font=fnt)) + pad * 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    draw.text((x + pad, y + 2), text, font=fnt, fill=fg)
    return w


def scene_chip(draw, x, y, text, fnt):
    """Small dark chip with white text inside a scene."""
    w = int(draw.textlength(text, font=fnt)) + 8
    draw.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=(0, 0, 0))
    draw.text((x + 4, y + 2), text, font=fnt, fill=(255, 255, 255))
    return w


def star(draw, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- scenes
def scene_cop31(d, x, y, w, h):
    """Plenary hall at the moment the final text is rejected."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 58, 52))
    d.rectangle([x, y, x + w, y + 26], fill=(16, 40, 36))
    # globe, top left
    d.ellipse([x + 10, y + 34, x + 52, y + 76], fill=(70, 160, 150),
              outline=(220, 230, 220), width=2)
    d.ellipse([x + 20, y + 44, x + 42, y + 66], outline=(220, 230, 220), width=1)
    d.line([x + 10, y + 55, x + 52, y + 55], fill=(220, 230, 220), width=1)
    # delegate rows: seated dots + desks
    for r in range(3):
        yy = y + 82 + r * 11
        d.rectangle([x + 8, yy + 6, x + w - 60, yy + 9], fill=(120, 90, 50))
        for c in range(9):
            xx = x + 14 + c * 26
            d.ellipse([xx, yy - 2, xx + 7, yy + 5], fill=(232, 214, 170))
    # podium + president, right
    d.rectangle([x + w - 52, y + 62, x + w - 12, y + h - 8], fill=(90, 60, 30))
    d.rectangle([x + w - 56, y + 56, x + w - 8, y + 64], fill=(120, 85, 45))
    d.ellipse([x + w - 38, y + 36, x + w - 24, y + 50], fill=(232, 214, 170))
    d.rectangle([x + w - 40, y + 50, x + w - 22, y + 58], fill=(30, 30, 30))
    # walkout figures, centre
    for i, xx in enumerate((x + 150, x + 172, x + 194)):
        d.ellipse([xx, y + 40 + (i % 2) * 4, xx + 8, y + 48 + (i % 2) * 4],
                  fill=(232, 214, 170))
        d.rectangle([xx - 1, y + 48 + (i % 2) * 4, xx + 9,
                     y + 62 + (i % 2) * 4], fill=(RED if i == 1 else NAVY2))
    # red banner
    d.rectangle([x + 8, y + 6, x + w - 8, y + 22], fill=RED)
    d.text((x + 12, y + 8), "NO AGREEMENT ON THIS TEXT", font=SANS_B(10),
           fill=(255, 255, 255))
    # thermometer, far right edge
    d.rectangle([x + w - 8, y + 30, x + w - 4, y + 58], fill=(255, 255, 255))
    d.rectangle([x + w - 8, y + 30, x + w - 4, y + 40], fill=RED)
    d.text((x + w - 62, y + 30), "1.5°C", font=SANS_B(11), fill=(255, 220, 120))
    scene_chip(d, x + 8, y + h - 18, "~200 NATIONS", SANS_B(8))
    scene_chip(d, x + 96, y + h - 18, "44 HRS OVERTIME", SANS_B(8))
    scene_chip(d, x + 196, y + h - 18, "LONGEST COP EVER", SANS_B(8))


def scene_kyiv(d, x, y, w, h):
    """Night skyline under the 186-drone raid, with a searchlight."""
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    d.ellipse([x + w - 52, y + 8, x + w - 22, y + 38], fill=(235, 225, 190))
    # searchlight beam
    d.polygon([(x + 60, y + h), (x + 150, y + 6), (x + 178, y + 6),
               (x + 110, y + h)], fill=(120, 140, 190))
    # buildings
    import random
    rnd = random.Random(22)
    bx = x + 6
    while bx < x + w - 30:
        bw = rnd.randint(22, 38)
        bh = rnd.randint(28, 62)
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(8, 12, 30))
        for wy in range(y + h - bh + 6, y + h - 6, 10):
            for wx in range(bx + 4, bx + bw - 4, 9):
                if rnd.random() < 0.5:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 90))
        bx += bw + 4
    # drone trails + drones
    for tx, ty, ln in ((x + 40, y + 18, 46), (x + 130, y + 30, 60),
                       (x + 210, y + 14, 40), (x + 250, y + 44, 52)):
        for i in range(0, ln, 6):
            d.ellipse([tx + i, ty, tx + i + 2, ty + 2], fill=(255, 255, 255))
        d.line([tx - 3, ty + 1, tx + 3, ty + 1], fill=(255, 255, 255), width=2)
        d.line([tx, ty - 2, tx, ty + 4], fill=(255, 255, 255), width=2)
    # blast on a tower + Dymer block inset
    star(d, x + 96, y + 52, 14, (255, 140, 30))
    star(d, x + 96, y + 52, 7, (255, 220, 120))
    d.rectangle([x + w - 108, y + h - 34, x + w - 14, y + h - 8],
                fill=(40, 30, 30), outline=(255, 140, 30), width=1)
    d.text((x + w - 104, y + h - 32), "DYMER BLOCK HIT",
           font=SANS_B(8), fill=(255, 200, 120))
    scene_chip(d, x + 8, y + h - 18, "186 FIRED", SANS_B(8))
    scene_chip(d, x + 76, y + h - 18, "161 DOWNED", SANS_B(8))
    scene_chip(d, x + 152, y + h - 18, "18 SITES HIT", SANS_B(8))


def scene_bahrain(d, x, y, w, h):
    """Radar base at dusk: dishes, fire, a tanker offshore."""
    d.rectangle([x, y, x + w, y + h], fill=(52, 38, 62))
    d.rectangle([x, y, x + w, y + 52], fill=(96, 62, 70))
    d.ellipse([x + 14, y + 10, x + 44, y + 40], fill=(240, 200, 120))
    # sea
    d.rectangle([x, y + 78, x + w, y + h], fill=(28, 52, 86))
    for i in range(5):
        d.line([x + 10 + i * 60, y + 88 + (i % 2) * 8,
                x + 40 + i * 60, y + 88 + (i % 2) * 8],
               fill=(120, 160, 210), width=2)
    # tanker
    d.rectangle([x + 200, y + 82, x + w - 16, y + 96], fill=(20, 20, 20))
    d.rectangle([x + 232, y + 70, x + w - 40, y + 82], fill=(20, 20, 20))
    d.rectangle([x + 250, y + 62, x + 256, y + 70], fill=(20, 20, 20))
    # base buildings + radar dishes
    d.rectangle([x + 10, y + 56, x + 90, y + 78], fill=(70, 70, 78))
    d.rectangle([x + 100, y + 62, x + 150, y + 78], fill=(60, 60, 68))
    for cx in (x + 130, x + 175):
        d.line([cx, y + 62, cx, y + 44], fill=(200, 200, 200), width=2)
        d.pieslice([cx - 16, y + 22, cx + 16, y + 54], 200, 340,
                   fill=(210, 210, 210))
    # fire at industrial site
    for fx, fh in ((x + 96, 26), (x + 108, 34), (x + 118, 22)):
        d.polygon([(fx - 8, y + 78), (fx, y + 78 - fh), (fx + 8, y + 78)],
                  fill=(255, 120, 20))
        d.polygon([(fx - 4, y + 78), (fx, y + 78 - fh + 12), (fx + 4, y + 78)],
                  fill=(255, 210, 80))
    scene_chip(d, x + 8, y + h - 18, "2 RADARS CLAIMED", SANS_B(8))
    scene_chip(d, x + 112, y + h - 18, "AL-RIFFA + AWALI", SANS_B(8))
    scene_chip(d, x + 212, y + h - 18, "NO CASUALTIES", SANS_B(8))


# ------------------------------------------------------- mid mini-scenes
def mini_vote(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 84, 150))
    d.rectangle([x + w // 2 - 26, y + 14, x + w // 2 + 26, y + h - 6],
                fill=(200, 170, 90), outline=(90, 70, 20), width=2)
    d.rectangle([x + w // 2 - 12, y + 8, x + w // 2 + 12, y + 16],
                fill=(255, 255, 255), outline=(90, 70, 20), width=1)
    d.text((x + 6, y + 4), "98.79%", font=SANS_B(11), fill=(255, 255, 255))


def mini_race(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 36))
    for r in range(2):
        for c in range(6):
            if (r + c) % 2 == 0:
                d.rectangle([x + 8 + c * 10, y + 6 + r * 10,
                             x + 18 + c * 10, y + 16 + r * 10],
                            fill=(255, 255, 255))
    d.rectangle([x + 78, y + 22, x + w - 10, y + h - 8], fill=(200, 40, 30))
    d.ellipse([x + 86, y + h - 12, x + 96, y + h - 2], fill=(20, 20, 20))
    d.ellipse([x + w - 24, y + h - 12, x + w - 14, y + h - 2],
              fill=(20, 20, 20))
    d.text((x + 8, y + h - 16), "75th WIN", font=SANS_B(10),
           fill=(255, 220, 80))


def mini_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 110, 58))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(120, 90, 50))
    for sx in (x + 20, x + 28, x + 36):
        d.rectangle([sx, y + 8, sx + 3, y + 22], fill=(240, 220, 140))
    d.ellipse([x + w - 34, y + 10, x + w - 22, y + 22], fill=(200, 40, 30))
    d.text((x + 8, y + h - 16), "720/9", font=SANS_B(12),
           fill=(255, 255, 255))


def mini_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 52, 86))
    d.rectangle([x + 20, y + 22, x + w - 20, y + 34], fill=(30, 30, 30))
    d.rectangle([x + 60, y + 10, x + 78, y + 22], fill=(30, 30, 30))
    d.polygon([(x + 84, y + 22), (x + 92, y + 2), (x + 100, y + 22)],
              fill=(255, 120, 20))
    d.polygon([(x + 90, y + 22), (x + 96, y + 10), (x + 102, y + 22)],
              fill=(255, 210, 80))
    d.text((x + 8, y + h - 16), "STILL BURNING", font=SANS_B(9),
           fill=(255, 220, 120))


def mini_power(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 40, 48))
    d.polygon([(x + 78, y + 4), (x + 52, y + 26), (x + 70, y + 26),
               (x + 58, y + h - 4), (x + 92, y + 18), (x + 74, y + 18)],
              fill=(255, 220, 60))
    d.text((x + 8, y + 4), "2 HRS/DAY", font=SANS_B(10),
           fill=(255, 255, 255))


def mini_hoops(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 70, 20))
    d.ellipse([x + w // 2 - 20, y + 4, x + w // 2 + 20, y + 44],
              fill=(230, 110, 30), outline=(255, 255, 255), width=2)
    d.line([x + w // 2 - 20, y + 24, x + w // 2 + 20, y + 24],
           fill=(255, 255, 255), width=2)
    d.text((x + 8, y + h - 16), "50 PTS", font=SANS_B(12),
           fill=(255, 255, 255))


def mini_tennis(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 110, 70))
    d.rectangle([x + 10, y + 8, x + w - 10, y + h - 8], fill=(60, 140, 95),
                outline=(255, 255, 255), width=1)
    d.line([x + w // 2, y + 8, x + w // 2, y + h - 8], fill=(255, 255, 255),
           width=1)
    d.ellipse([x + w - 30, y + 10, x + w - 18, y + 22], fill=(200, 230, 60))
    d.text((x + 8, y + h - 16), "6-2, 7-6(7)", font=SANS_B(10),
           fill=(255, 255, 255))


def mini_football(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 100, 50))
    d.rectangle([x + 8, y + 8, x + w - 8, y + h - 8], outline=(255, 255, 255),
                width=1)
    d.ellipse([x + w // 2 - 8, y + h // 2 - 8, x + w // 2 + 8,
               y + h // 2 + 8], outline=(255, 255, 255), width=1)
    d.ellipse([x + 16, y + 12, x + 28, y + 24], fill=(255, 255, 255))
    d.text((x + 40, y + 4), "4-0", font=SANS_B(14), fill=(255, 255, 255))
    d.text((x + 8, y + h - 16), "ANFIELD", font=SANS_B(9),
           fill=(255, 255, 255))


def mini_health(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(230, 230, 225))
    d.rectangle([x + w // 2 - 6, y + 8, x + w // 2 + 6, y + h - 8],
                fill=(180, 40, 30))
    d.rectangle([x + w // 2 - 18, y + 18, x + w // 2 + 18, y + 30],
                fill=(180, 40, 30))
    d.text((x + 8, y + h - 14), "ICU", font=SANS_B(10), fill=(180, 40, 30))


def mini_cyber(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 30, 50))
    d.rectangle([x + 34, y + 8, x + w - 34, y + h - 14], fill=(60, 90, 140),
                outline=(180, 200, 230), width=1)
    d.rectangle([x + 28, y + h - 12, x + w - 28, y + h - 8],
                fill=(120, 130, 150))
    d.rectangle([x + w // 2 - 7, y + 16, x + w // 2 + 7, y + 26],
                outline=(255, 220, 80), width=2)
    d.rectangle([x + w // 2 - 9, y + 24, x + w // 2 + 9, y + 32],
                fill=(255, 220, 80))


def mini_travel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(140, 180, 220))
    d.polygon([(x + 20, y + 22), (x + w - 30, y + 14), (x + w - 30, y + 26),
               (x + 20, y + 30)], fill=(255, 255, 255))
    d.polygon([(x + 70, y + 22), (x + 90, y + 6), (x + 100, y + 22)],
              fill=(255, 255, 255))
    d.polygon([(x + 70, y + 26), (x + 90, y + 40), (x + 100, y + 26)],
              fill=(255, 255, 255))
    d.text((x + 8, y + h - 16), "GROUNDED", font=SANS_B(10), fill=NAVY)


def mini_alert(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 30, 25))
    d.rectangle([x + w // 2 - 12, y + 10, x + w // 2 + 12, y + h - 12],
                fill=(220, 200, 160), outline=(90, 60, 20), width=1)
    d.text((x + w // 2 - 4, y + 12), "!", font=SANS_B(16), fill=(120, 30, 25))
    d.text((x + 8, y + h - 16), "TOLL 19", font=SANS_B(10),
           fill=(255, 255, 255))


MINI = {"vote": mini_vote, "race": mini_race, "cricket": mini_cricket,
        "ship": mini_ship, "power": mini_power, "hoops": mini_hoops,
        "tennis": mini_tennis, "football": mini_football,
        "health": mini_health, "cyber": mini_cyber, "travel": mini_travel,
        "alert": mini_alert}

# ------------------------------------------------------------- story data
# (num, region, kicker, headline, body, tag, source, scene)
LEADS = [
    (1, "EUROPE", "ANTALYA, TÜRKIYE — CLIMATE",
     "COP31 ends with no deal — final text rejected",
     "The presidency's ten-page final text, with no mention of fossil "
     "fuels, was refused in the closing plenary. President Murat Kurum: "
     "\"There is no agreement on this text.\"",
     "REPORTED", "Reuters, AFP, The Guardian", "cop31"),
    (2, "EUROPE", "KYIV REGION, UKRAINE — WAR",
     "Russia fires 186 drones: a Kyiv-region block is destroyed",
     "Air defences downed or jammed 161 of 186 strike drones overnight. "
     "One five-storey block in Dymer was destroyed; three killed, 14 feared "
     "trapped. Hits were recorded at 18 locations.",
     "REPORTED", "Ukrainian Air Force via Reuters", "kyiv"),
    (3, "MIDDLE EAST", "MANAMA, BAHRAIN — IRAN",
     "Iran claims two US radars hit; Bahrain denies it",
     "The IRGC says its forces hit two US Patriot radars at Al-Riffa and "
     "Awali. Bahrain says its defences intercepted the attack; a civilian "
     "industrial site burned and two people were hurt.",
     "CLAIM", "IRGC, Bahrain Interior Ministry, Reuters", "bahrain"),
]

MIDS = [
    (4, "ASIA-PACIFIC", "HONG KONG — ELECTION",
     "Hong Kong elects its Election Committee",
     "Record 98.79% turnout: 5,640 of 5,709 voters. 856 candidates for "
     "723 seats across 31 subsectors.", "CONFIRMED",
     "info.gov.hk, SCMP", "vote"),
    (5, "AMERICAS", "LAS VEGAS — FORMULA 1",
     "Verstappen takes the Las Vegas Grand Prix",
     "+0.639s clear of Norris; his 75th win. Russell hit the wall late "
     "and fell to 5th.", "REPORTED", "Reuters, F1", "race"),
    (6, "ASIA-PACIFIC", "WELLINGTON — CRICKET",
     "India declare on 720/9 — a record in New Zealand",
     "Pant 128, Rahul 136; hosts 119/2, trailing by 235.", "REPORTED",
     "Reuters", "cricket"),
    (7, "EUROPE", "GULF OF FINLAND — SEA",
     "Russian cargo ship Sparta II still smouldering",
     "Hit by two drones on Saturday; 16 crew evacuated. Fire still "
     "burning Sunday; Finland leads salvage.", "REPORTED",
     "Reuters", "ship"),
    (8, "MIDDLE EAST", "TEHRAN — ENERGY",
     "Iran begins rationing electricity",
     "Rolling cuts of up to two hours a day as gas output falls and "
     "war damage bites.", "REPORTED", "Reuters, AFP", "power"),
    (9, "AMERICAS", "SAN ANTONIO — NBA",
     "Wembanyama scores 50 as the Spurs roll on",
     "50 pts, 19 rebounds in a 114–91 win over New Orleans.", "REPORTED",
     "Reuters, AP", "hoops"),
    (10, "WORLD", "TURIN — TENNIS",
     "Alcaraz beats Zverev to win the ATP Finals",
     "6-2, 7-6(7) in Turin — his first ATP Finals crown, 30th career "
     "title; saved three set points.", "REPORTED", "Reuters, ATP",
     "tennis"),
    (11, "EUROPE", "LIVERPOOL — FOOTBALL",
     "Liverpool thrash Man Utd 4-0 on Pochettino debut",
     "Yoro sent off after 8 minutes; Szoboszlai 10', Wirtz 13', "
     "Ngumoha 66', Muñoz 82'.", "REPORTED", "Reuters", "football"),
    (12, "AMERICAS", "BRASÍLIA — HEALTH",
     "Bolsonaro in intensive care in Brasília",
     "Bowel obstruction; stable and breathing on his own. "
     "Surgery still possible.", "REPORTED", "Al Jazeera, Reuters",
     "health"),
    (13, "AMERICAS", "WASHINGTON — CYBER",
     "FBI probes apparent hack of its crime database",
     "Washington State pauses gun-dealer checks; the scope of the "
     "breach is unknown.", "REPORTED", "AP, BBC", "cyber"),
    (14, "EUROPE", "BRUSSELS — TRAVEL",
     "Belgian controllers join Monday's national strike",
     "Most flights grounded 07:00–21:00 Monday; the strike was "
     "announced on Sunday.", "REPORTED", "Reuters", "travel"),
    (15, "ASIA-PACIFIC", "MANIPUR — POISONING",
     "Toxic-liquor toll climbs to 19 in Manipur",
     "About 600 in hospital; six held. The toll rose from the "
     "earlier count.", "REPORTED", "Xinhua, Reuters", "alert"),
]

BRIEFS = [
    (16, "ASIA-PACIFIC", "Cikande candy-factory fire, Serang: 3 dead, 36 missing", "Detiknews"),
    (17, "AMERICAS", "Peru quake toll updated: 1 dead, 16 hurt, 170 homes damaged", "Reuters"),
    (18, "EUROPE", "Estonia to shut five Russia border crossings on 1 Dec", "Reuters"),
    (19, "EUROPE", "Denmark expels Russian attaché over alleged plot", "Guardian"),
    (20, "ASIA-PACIFIC", "Nepal PM Shah lands in Delhi on first visit; meets Modi Monday", "IANS"),
    (21, "ASIA-PACIFIC", "Chinese bomber turns back 170 km from Manila", "AP"),
    (22, "ASIA-PACIFIC", "Philippines M-5.9 quake off Palawan", "EMSC"),
    (23, "AFRICA", "Somalia expels UAE ambassador, recalls its envoy", "Reuters"),
    (24, "AFRICA", "Sudan: RSF accused of killing civilians incl. 3 children", "Reuters"),
    (25, "OCEANIA", "Melbourne: 70 years since the 1956 Olympics opened", "ABC"),
    (26, "OCEANIA", "Cummins keeps Australia's Test captaincy", "Reuters"),
    (27, "MIDDLE EAST", "Eisenkot invites Likud to coalition talks", "Times of Israel"),
    (28, "MIDDLE EAST", "Trump seeks 'permanent' deal with Iran; Doha talks on", "Al Jazeera"),
    (29, "EUROPE", "Pope Leo XIV hosts 1,300 poor guests for World Day of the Poor", "Vatican News"),
    (30, "ASIA-PACIFIC", "Snow strands about 1,500 in Japan village", "dpa"),
    (31, "OCEANIA", "Marles rejects US report on AUKUS subs", "Reuters"),
    (32, "EUROPE", "Geneva talks on AI weapons end without rules", "Wires"),
    (33, "MIDDLE EAST", "Hamas seeks urgent talks after aid-van strike", "Al Jazeera"),
    (34, "WORLD", "Bitcoin holds above $60,000 after Saturday's $55.1k flush", "Market data"),
    (35, "AFRICA", "Sudan army retakes about 30 towns in Kordofan", "FT"),
    (36, "EUROPE", "Venice Biennale closes after six months", "ANSA"),
]

REGION_COUNTS = [("EUROPE", 10), ("MIDDLE EAST", 5), ("ASIA-PACIFIC", 8),
                 ("AMERICAS", 5), ("AFRICA", 3), ("OCEANIA", 3),
                 ("WORLD", 2)]
STATS = [("~200", "NATIONS AT THE COP31 TALKS"),
         ("03:00", "GMT — OBJECTIONS DEADLINE"),
         ("186", "DRONES FIRED AT UKRAINE"),
         ("161", "DOWNED OR JAMMED"),
         ("2", "US RADARS CLAIMED IN BAHRAIN"),
         ("98.79%", "HONG KONG TURNOUT — FINAL")]
UTC_EVENTS = [("01:00", "HK polls open"), ("03:00", "COP31 objections close"),
              ("06:00", "COP31 approval due"), ("08:00", "161 of 186 downed"),
              ("18:00", "HK close — 98.79%"), ("19:17", "Alcaraz wins ATP")]


# ------------------------------------------------------------------- map
# Stylised continents (rough polygons in a 300x140 box) + numbered pins.
CONTINENTS = {
    "NA": [(10, 28), (62, 16), (96, 26), (90, 52), (58, 58), (30, 50), (10, 42)],
    "SA": [(76, 72), (100, 68), (110, 94), (96, 124), (80, 104)],
    "EU": [(140, 24), (176, 16), (186, 34), (164, 48), (144, 40)],
    "AF": [(140, 54), (176, 50), (190, 74), (170, 104), (150, 88)],
    "AS": [(188, 18), (262, 14), (286, 40), (260, 70), (210, 60), (190, 44)],
    "OC": [(250, 100), (276, 94), (280, 114), (254, 118)],
}
# story num -> (x, y) pin position on the 300x140 map
PINS = {1: (146, 20), 2: (186, 38), 3: (192, 64), 4: (262, 46),
        5: (36, 34), 6: (268, 112), 7: (168, 10), 8: (208, 50),
        9: (46, 56), 10: (138, 44), 11: (128, 28), 12: (86, 92),
        13: (58, 48), 14: (164, 48), 15: (248, 52)}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 224, 234))
    # dotted lat/long grid
    for gx in range(x + 12, x + w, 18):
        for gy in range(y + 8, y + h, 14):
            d.ellipse([gx, gy, gx + 1, gy + 1], fill=(160, 180, 195))
    for poly in CONTINENTS.values():
        pts = [(x + px, y + py) for px, py in poly]
        d.polygon(pts, fill=(222, 206, 160), outline=(170, 150, 110))
    for num, (px, py) in PINS.items():
        cx, cy = x + px, y + py
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(num)
        tw = d.textlength(t, font=SANS_B(7))
        d.text((cx - tw / 2, cy - 4), t, font=SANS_B(7), fill=(255, 255, 255))
    d.text((x + 4, y + h - 13), "PINS 1–15 MATCH STORY NUMBERS",
           font=SANS_B(7), fill=(70, 70, 70))


# -------------------------------------------------------------- assembly
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    x0, x1 = 14, W - 14

    # masthead
    d.rectangle([0, 0, W, 24], fill=NAVY)
    d.text((14, 5), "THE WORLD IN ONE DAY", font=SANS_B(13),
           fill=(255, 255, 255))
    rt = "36 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    d.text((W - 14 - d.textlength(rt, font=SANS_B(10)), 6), rt,
           font=SANS_B(10), fill=(200, 200, 200))
    # title + sub-dek
    title = "Sunday 22 November 2026"
    d.text(((W - d.textlength(title, font=SERIF_B(52))) / 2, 28), title,
           font=SERIF_B(52), fill=INK)
    sub = ("COP31 ends with no deal  ·  186 drones over Ukraine  ·  "
           "Iran's radar claim meets Bahrain's denial")
    d.text(((W - d.textlength(sub, font=SERIF(15))) / 2, 86), sub,
           font=SERIF(15), fill=RED)
    # stat row
    y = 108
    cw = (x1 - x0) / 6
    for i, (num, lab) in enumerate(STATS):
        cx = x0 + i * cw
        d.text((cx + (cw - d.textlength(num, font=SERIF_B(26))) / 2, y), num,
               font=SERIF_B(26), fill=RED)
        d.text((cx + (cw - d.textlength(lab, font=SANS_B(8))) / 2, y + 30),
               lab, font=SANS_B(8), fill=GREY)
        if i:
            d.line([cx, y + 2, cx, y + 40], fill=LINE, width=1)
    d.line([x0, y + 46, x1, y + 46], fill=NAVY, width=1)
    # region bar
    y = 158
    total = sum(c for _, c in REGION_COUNTS)
    rx = x0
    for name, cnt in REGION_COUNTS:
        seg = (x1 - x0) * cnt / total
        d.rectangle([rx, y, rx + seg - 1, y + 18], fill=REGION_COLOR[name])
        lab = "%s %d" % (name, cnt)
        tw = d.textlength(lab, font=SANS_B(9))
        if tw < seg - 6:
            d.text((rx + (seg - tw) / 2, y + 4), lab, font=SANS_B(9),
                   fill=(255, 255, 255))
        rx += seg
    # UTC strip
    y = 180
    d.rectangle([x0, y, x1, y + 20], fill=NAVY)
    d.text((x0 + 6, y + 5), "THE DAY IN UTC", font=SANS_B(9), fill=GOLD)
    ux = x0 + 118
    for tm, ev in UTC_EVENTS:
        d.text((ux, y + 5), tm, font=SANS_B(9), fill=GOLD)
        ux += d.textlength(tm, font=SANS_B(9)) + 4
        d.text((ux, y + 5), ev, font=SANS(9), fill=(255, 255, 255))
        ux += d.textlength(ev, font=SANS(9)) + 9
    # leads
    y = 206
    lead_w = int((x1 - x0 - 16) / 3)
    lead_h = 246
    scenes = {"cop31": scene_cop31, "kyiv": scene_kyiv, "bahrain": scene_bahrain}
    for i, (num, region, kicker, head, body, tag, src, scene) in enumerate(LEADS):
        lx = x0 + i * (lead_w + 8)
        scenes[scene](d, lx, y, lead_w, 112)
        ly = y + 118
        d.text((lx, ly), "%d · %s" % (num, kicker), font=SANS_B(9),
               fill=REGION_COLOR[region])
        chip(d, lx + lead_w - 62, ly - 2, tag, SANS_B(8), TAG_COLOR[tag])
        ly += 15
        hl = wrap(d, head, SERIF_B(16), lead_w)
        ly = draw_lines(d, hl, lx, ly, SERIF_B(16), INK, 19, max_lines=2)
        bl = wrap(d, body, SANS(10), lead_w)
        ly = draw_lines(d, bl, lx, ly + 2, SANS(10), (50, 50, 50), 12,
                        max_lines=3)
        d.text((lx, y + lead_h - 12), "Sources: " + src, font=SANS(8),
               fill=GREY)
    # mids: 6 columns x 2 rows
    y = 458
    mid_w = int((x1 - x0 - 40) / 6)
    mid_h = 112
    for i, (num, region, kicker, head, body, tag, src, scene) in enumerate(MIDS):
        row, col = divmod(i, 6)
        mx = x0 + col * (mid_w + 8)
        my = y + row * (mid_h + 8)
        MINI[scene](d, mx, my, mid_w, 42)
        my2 = my + 46
        d.text((mx, my2), "%d · %s" % (num, kicker.split(" — ")[0]),
               font=SANS_B(8), fill=REGION_COLOR[region])
        chip(d, mx + mid_w - 58, my2 - 1, tag, SANS_B(7), TAG_COLOR[tag])
        my2 += 13
        hl = wrap(d, head, SANS_B(10), mid_w)
        my2 = draw_lines(d, hl, mx, my2, SANS_B(10), INK, 11, max_lines=2)
        bl = wrap(d, body, SANS(8.5), mid_w)
        draw_lines(d, bl, mx, my2 + 1, SANS(8.5), (60, 60, 60), 10,
                   max_lines=2)
        d.text((mx, my + mid_h - 10), src, font=SANS(7), fill=GREY)
    # briefs header
    y = 694
    d.text((x0, y), "ALSO ON SUNDAY 22 NOVEMBER — 21 MORE STORIES",
           font=SANS_B(11), fill=NAVY)
    d.line([x0, y + 15, x1, y + 15], fill=NAVY, width=1)
    # bottom zone: map left, briefs right (2 columns)
    y = 714
    map_w, map_h = 296, 138
    d.text((x0, y), "WHERE IT HAPPENED", font=SANS_B(10), fill=NAVY)
    draw_map(d, x0, y + 14, map_w, map_h)
    bx = x0 + map_w + 14
    col_w = int((x1 - bx - 10) / 2)
    for i, (num, region, text, src) in enumerate(BRIEFS):
        col, row = divmod(i, 11)
        px = bx + col * (col_w + 10)
        py = y + row * 13
        d.text((px, py), "%d" % num, font=SANS_B(9), fill=RED)
        line = "%s (%s)" % (text, src)
        lines = wrap(d, line, SANS(9), col_w - 20)
        draw_lines(d, lines, px + 20, py, SANS(9), INK, 11, max_lines=1)
    # DATE CHECK
    y = 862
    d.rectangle([x0, y, x1, y + 92], outline=RED, width=2)
    d.text((x0 + 6, y + 4), "DATE CHECK — READ THIS FIRST",
           font=SANS_B(10), fill=RED)
    d.text((x0 + 6, y + 18),
           "Every story here happened, or was first reported, on Sun 22 Nov "
           "2026 (UTC). Wires read up to 23 Nov 03:00 UTC.",
           font=SANS(9), fill=INK)
    d.text((x0 + 6, y + 34), "LEFT OUT — OTHER DAYS' NEWS:",
           font=SANS_B(8), fill=RED_DK)
    left = ("400-drone barrage (Thu 19–Fri 20 Nov) — tonight's barrage was "
           "186, not 400 · Peru quake origin (Fri 20 Nov — toll updated Sun) "
           "· 'El Chapo Isidro' captured (Fri 20 Nov night) · Kryvyi Rih "
           "double-tap (Fri 20–Sat 21 Nov) · Gaza aid-van strike (Sat 21 Nov) "
           "· BepiColombo Mercury burn (Sat 21 Nov) · Shenzhen summit "
           "(Wed 19 Nov) · Myanmar genocide ruling (Thu 19 Nov) · Nvidia SEC "
           "probe (Fri 20 Nov) · NWSL final (Sat 21 Nov) · Fred Nile death "
           "(Sat 21 Nov)")
    draw_lines(d, wrap(d, left, SANS(8.5), x1 - x0 - 12), x0 + 6, y + 45,
               SANS(8.5), INK, 11, max_lines=3)
    d.text((x0 + 6, y + 78), "NOT YET DECIDED: COP31 — no new text will be "
           "offered (Kurum) · Sparta II salvage ongoing · Manipur toll may rise.",
           font=SANS(8.5), fill=INK)
    # footer
    y = 960
    d.text((x0, y), "Every story here happened, or was first reported, on Sun "
           "22 Nov 2026. Scenes are drawn illustrations of reported events, "
           "not photographs.", font=SANS(9), fill=INK)
    y += 13
    d.text((x0, y), "HOW TO READ THE TAGS:  REPORTED = carried by the day's "
           "wires  ·  CLAIM = one side's account, labelled as such  ·  "
           "CONFIRMED = official count  ·  ONGOING = still developing  ·  "
           "FORECAST = still to happen when drawn",
           font=SANS(8), fill=GREY)
    y += 13
    d.text((x0, y), "Wires read up to 23 Nov 03:00 UTC  ·  Sources named on "
           "every story  ·  The World in One Day", font=SANS(8), fill=GREY)
    return img


if __name__ == "__main__":
    out = os.path.join(HERE, "entry.png")
    build().save(out, format="PNG")
    print("wrote", out)
