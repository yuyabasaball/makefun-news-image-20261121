#!/usr/bin/env python3
"""Build the v7 entry image for the make.fun bounty "news-image-20261121".

Same six illustrated lead stories as v6, widened into a full front page:
a stats strip, six smaller verified story cards, and an "Also on Saturday"
list - 23 stories in all, every one checked against news reports dated
Saturday 21 November 2026. Ink/paper/red like v6, DejaVu throughout.
Repo copy: the six illustrations live in ./assets next to this script
(not tracked in git); output is ./entry.png (1024x1024), palette-encoded.
Running it with the illustrations in place reproduces entry.png exactly.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
MARGIN = 20
INK = (17, 20, 26)
PAPER = (244, 241, 234)
RED = (178, 34, 44)
GREY = (96, 100, 108)
CARD = (255, 254, 250)
CHIP_COLORS = [(29, 78, 137), (178, 34, 44), (15, 118, 110), (51, 65, 85),
               (146, 64, 14), (76, 29, 149)]

FD = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)
FB = "DejaVuSans-Bold.ttf"
FR = "DejaVuSans.ttf"

F_KICKER = font(FB, 21)
F_DATE = font(FB, 80)
F_BADGE = font(FB, 22)
F_SUB = font(FR, 16)
F_STAT_N = font(FB, 30)
F_STAT_L = font(FB, 10)
F_HEAD = font(FB, 20)
F_TAG = font(FB, 11)
F_CARD_H = font(FB, 17)
F_CARD_L = font(FR, 12)
F_SEC = font(FB, 17)
F_ALSO_PLACE = font(FB, 13)
F_ALSO = font(FR, 13)
F_FOOT = font(FR, 12)
F_REGION = font(FB, 13)
F_NUM = font(FB, 15)

def tw(d, s, f):
    return d.textlength(s, font=f)

def wrap(d, s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def paste_cover(canvas, path, box, focus=0.5):
    x, y, w, h = box
    a = Image.open(path).convert("RGB")
    w0, h0 = a.size
    scale = max(w / w0, h / h0)
    nw, nh = int(w0 * scale + 0.5), int(h0 * scale + 0.5)
    a = a.resize((nw, nh), Image.LANCZOS)
    ox = (nw - w) // 2
    oy = int((nh - h) * focus)
    canvas.paste(a.crop((ox, oy, ox + w, oy + h)), (x, y))

LEADS = [
    ("illo_icj.png", "ICJ RULES MYANMAR COMMITTED GENOCIDE",
     "WORLD COURT - THE HAGUE - ROHINGYA CASE", 0.49),
    ("illo_missile.png", "TWO RUSSIAN MISSILES FALL IN POLAND",
     "NATO CHIEF VOWS TO DEFEND 'EVERY INCH'", 0.38),
    ("illo_cop.png", "COP31 CLIMATE TALKS MISS THEIR DEADLINE",
     "DEADLOCKED OVER FOSSIL FUELS", 0.5),
    ("illo_market.png", "WALL STREET SLIDES INTO CORRECTION",
     "AI-LED SELLOFF AT FRIDAY'S CLOSE", 0.5),
    ("illo_iran.png", "IRAN SEEKS TALKS; TRUMP REJECTS TERMS",
     "TEHRAN SEEKS DIPLOMACY TO END THE WAR", 0.58),
    ("illo_summit.png", "U.S., CHINA & RUSSIA LEADERS IN SHENZHEN",
     "JOINT PLEDGE: HUMANS CONTROL MILITARY AI", 0.6),
]

STATS = [
    ("6.7", "PERU QUAKE MAGNITUDE"),
    ("3", "HOOTHI MISSILES DOWNED"),
    ("146", "PEOPLE SAFE IN DAVAO"),
    ("60", "WOUNDED IN KRYVYI RIH"),
    ("24+", "DEAD IN NIGERIA BOAT"),
    ("8 YRS", "BEPICOLOMBO TO MERCURY"),
]

CARDS = [
    ("3 HOOTHI MISSILES DOWNED OVER RIYADH", "Second attack on the capital in days"),
    ("M6.7 EARTHQUAKE SHAKES CENTRAL PERU", "No deaths; minor damage near Junin"),
    ("KRYVYI RIH: 2 KILLED, 60 WOUNDED", "Rescuers hit by follow-up strikes"),
    ("ALL 146 SAFE AS JET LANDS IN DAVAO", "Air Niugini 767 in engine-fire alert"),
    ("BEPICOLOMBO ENTERS MERCURY ORBIT", "Eight-year journey; 2nd Mercury orbiter"),
    ("BITCOIN FALLS TO A TWO-YEAR LOW", "Under $60,000 as the selloff spreads"),
]

ALSO = [
    ("KYIV", "Zelenskyy: the Crimea Bridge \"will not stay\""),
    ("HORMUZ", "Iran says it downed a U.S. MQ-9 drone"),
    ("NAYPYITAW", "Myanmar calls the ICJ ruling \"unfair\""),
    ("BRUSSELS", "UK and EU seal a post-Brexit reset deal"),
    ("BAYELSA", "At least 24 dead as a funeral boat capsizes"),
    ("WELLINGTON", "Rahul's 136 puts India in charge"),
    ("LAS VEGAS", "Verstappen inherits pole; Antonelli penalised"),
    ("WASHINGTON", "Trump threatens tax on data centres abroad"),
    ("BEIJING", "China tells Japan to \"correct\" its Taiwan words"),
    ("GULF OF FINLAND", "Drone strike sets a Russian cargo ship ablaze"),
    ("HORMUZ", "Two tankers struck in the strait, UKMTO says"),
]

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- header -------------------------------------------------------------
d.rectangle([0, 0, W, 118], fill=INK)
d.text((MARGIN, 12), "THE WORLD IN ONE DAY", font=F_KICKER, fill=PAPER)
bw = tw(d, "SATURDAY", F_BADGE) + 26
d.rectangle([W - MARGIN - bw, 8, W - MARGIN, 42], fill=RED)
d.text((W - MARGIN - bw + 13, 14), "SATURDAY", font=F_BADGE, fill=(255, 255, 255))
d.text((MARGIN - 2, 38), "21 NOVEMBER 2026", font=F_DATE, fill=(255, 255, 255))
d.text((MARGIN, 124), "23 stories that shaped the day - justice, war, climate, "
       "markets, diplomacy, sport", font=F_SUB, fill=GREY)

# ---- stats strip ----------------------------------------------------------
sy = 148
sh = 46
cw = (W - 2 * MARGIN) // 6
d.rectangle([MARGIN, sy, W - MARGIN, sy + sh], fill=INK)
for i, (num, label) in enumerate(STATS):
    x = MARGIN + i * cw
    if i:
        d.line([x, sy + 6, x, sy + sh - 6], fill=(70, 74, 84), width=1)
    d.text((x + 10, sy + 4), num, font=F_STAT_N, fill=(255, 255, 255))
# labels sit in a second ink band directly under the numbers
d.rectangle([MARGIN, sy + sh, W - MARGIN, sy + sh + 14], fill=INK)
for i, (num, label) in enumerate(STATS):
    x = MARGIN + i * cw
    d.text((x + 10, sy + sh + 1), label, font=F_STAT_L, fill=(198, 202, 210))

# ---- lead panels ----------------------------------------------------------
py = sy + sh + 27
pw = (W - 2 * MARGIN - 2 * 12) // 3
ph_img, ph_ban = 84, 72
for i, (fname, head, tag, focus) in enumerate(LEADS):
    x = MARGIN + (i % 3) * (pw + 12)
    y = py + (i // 3) * (ph_img + ph_ban + 12)
    paste_cover(img, os.path.join(ASSETS, fname), (x, y, pw, ph_img), focus)
    d.rounded_rectangle([x, y, x + pw, y + ph_img + ph_ban], radius=8,
                        outline=(190, 186, 176), width=1)
    by = y + ph_img
    d.rectangle([x, by, x + pw, by + ph_ban], fill=INK)
    r = 13
    cx, cy = x + 17, y + 17
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CHIP_COLORS[i])
    ns = str(i + 1)
    d.text((cx - tw(d, ns, F_NUM) / 2, cy - 9), ns, font=F_NUM, fill=(255, 255, 255))
    ty = by + 6
    for ln in wrap(d, head, F_HEAD, pw - 16)[:2]:
        d.text((x + 8, ty), ln, font=F_HEAD, fill=(255, 255, 255))
        ty += 23
    d.text((x + 8, by + ph_ban - 17), tag, font=F_TAG, fill=(198, 202, 210))
    if i == 3:
        chip = "S&P 500 -3.7%  -  NASDAQ -5.3%"
        chw = tw(d, chip, F_TAG) + 16
        d.rectangle([x + pw - chw - 6, y + 6, x + pw - 6, y + 25], fill=RED)
        d.text((x + pw - chw + 2, y + 10), chip, font=F_TAG, fill=(255, 255, 255))

# ---- story cards ----------------------------------------------------------
cy0 = py + 2 * (ph_img + ph_ban) + 12 + 14
ch = 70
for i, (head, line) in enumerate(CARDS):
    x = MARGIN + (i % 3) * (pw + 12)
    y = cy0 + (i // 3) * (ch + 10)
    d.rounded_rectangle([x, y, x + pw, y + ch], radius=8, fill=CARD,
                        outline=(190, 186, 176), width=1)
    d.rectangle([x, y, x + 5, y + ch], fill=CHIP_COLORS[i])
    ns = str(i + 7)
    d.text((x + 14, y + 8), ns, font=F_CARD_H, fill=CHIP_COLORS[i])
    tx = x + 14 + tw(d, ns, F_CARD_H) + 8
    ty = y + 7
    for ln in wrap(d, head, F_CARD_H, x + pw - tx - 6)[:2]:
        d.text((tx, ty), ln, font=F_CARD_H, fill=INK)
        ty += 21
    d.text((x + 14, y + ch - 19), line, font=F_CARD_L, fill=GREY)

# ---- also on saturday -----------------------------------------------------
ay = cy0 + 2 * ch + 10 + 16
d.rectangle([MARGIN, ay, W - MARGIN, ay + 26], fill=RED)
d.text((MARGIN + 10, ay + 4), "ALSO ON SATURDAY 21 NOVEMBER", font=F_SEC,
       fill=(255, 255, 255))
colw = (W - 2 * MARGIN - 24) // 2
ly = ay + 36
for i, (place, text) in enumerate(ALSO):
    x = MARGIN + (i % 2) * (colw + 24)
    y = ly + (i // 2) * 27
    label = f"{i + 13}. {place} - "
    d.text((x, y), label, font=F_ALSO_PLACE, fill=INK)
    d.text((x + tw(d, label, F_ALSO_PLACE), y), text, font=F_ALSO, fill=(52, 56, 64))

# ---- footer ---------------------------------------------------------------
fy = ly + 6 * 27 + 8
d.line([MARGIN, fy, W - MARGIN, fy], fill=(190, 186, 176), width=1)
regions = "EUROPE 6  -  ASIA 5  -  AMERICAS 5  -  MIDDLE EAST 4  -  AFRICA 1  -  OCEANIA 1  -  SPACE 1"
d.text((MARGIN, fy + 7), regions, font=F_REGION, fill=INK)
d.rectangle([MARGIN, fy + 32, W - MARGIN, H - 14], outline=RED, width=2)
d.text((MARGIN + 10, fy + 38),
       "DATE CHECK - every story happened or was first reported on Saturday "
       "21 November 2026.", font=F_FOOT, fill=INK)
d.text((MARGIN + 10, fy + 54),
       "Anything we could not confirm in two independent reports was left out.",
       font=F_FOOT, fill=GREY)

img.quantize(colors=256, method=Image.MEDIANCUT).save(OUT, optimize=True)
print("saved", OUT, os.path.getsize(OUT))
