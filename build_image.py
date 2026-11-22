#!/usr/bin/env python3
"""Build entry.png: the world news of Saturday 21 November 2026 in one image.
Newspaper front page: crisp PIL text + flat editorial illustrations per story.
Canvas 1024x1024 (competition limit), PNG under 1 MiB.
The six illustrations (illo_*.png, AI-generated, cream #F7F3EA background) are
read from an assets folder next to this script; entry.png as committed is the
finished artifact that main.ts serves. Falls back to line icons if an
illustration is missing.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = 1024
BG = (247, 243, 234)
INK = (24, 26, 32)
RED = (178, 34, 44)
BLUE = (30, 74, 140)
TEAL = (14, 116, 110)
GOLD = (176, 124, 22)
GREEN = (46, 110, 54)
GREY = (92, 96, 104)
PANEL = (255, 255, 255)
LINE = (210, 203, 188)
CREAM = (247, 243, 234)

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
FILES = ["illo_icj.png", "illo_missile.png", "illo_cop.png",
         "illo_market.png", "illo_iran.png", "illo_summit.png"]

FB = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FX = "/usr/share/fonts/truetype/noto/NotoSans-ExtraBold.ttf"
FR = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
FS = "/usr/share/fonts/truetype/noto/NotoSans-SemiBold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, W), BG)
d = ImageDraw.Draw(img)

def wrap(text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

# ---------- header ----------
d.rectangle([0, 0, W, 196], fill=INK)
d.text((48, 24), "THE WORLD IN ONE DAY", font=font(FS, 29), fill=(233, 226, 208))
badge_f = font(FX, 27)
bw = d.textlength("SATURDAY", font=badge_f) + 36
d.rectangle([W - 48 - bw, 20, W - 48, 62], fill=RED)
d.text((W - 48 - bw + 18, 27), "SATURDAY", font=badge_f, fill=(255, 255, 255))
d.text((48, 58), "21 NOVEMBER 2026", font=font(FX, 80), fill=(255, 255, 255))
d.text((48, 156), "Six stories that shaped the day: justice, war, climate, markets, diplomacy",
       font=font(FR, 24), fill=(196, 200, 210))

# ---------- fallback icons (from v3) ----------
def icon_scales(cx, cy, s, color):
    d.line([cx, cy - s, cx, cy + s * 0.8], fill=color, width=7)
    d.line([cx - s, cy - s * 0.55, cx + s, cy - s * 0.55], fill=color, width=7)
    for sx in (-s, s):
        d.line([cx + sx, cy - s * 0.55, cx + sx - s * 0.38, cy + s * 0.25], fill=color, width=5)
        d.line([cx + sx, cy - s * 0.55, cx + sx + s * 0.38, cy + s * 0.25], fill=color, width=5)
        d.arc([cx + sx - s * 0.38, cy + s * 0.05, cx + sx + s * 0.38, cy + s * 0.45], 0, 180, fill=color, width=6)
    d.rectangle([cx - s * 0.55, cy + s * 0.85, cx + s * 0.55, cy + s], fill=color)

def icon_missile(cx, cy, s, color):
    import math
    ux, uy = -0.707, 0.707
    px, py = -uy, ux
    nose = (cx - ux * s * 0.95, cy - uy * s * 0.95)
    tail = (cx + ux * s * 0.55, cy + uy * s * 0.55)
    wdt = s * 0.30
    body = [(nose[0], nose[1]),
            (tail[0] + px * wdt, tail[1] + py * wdt),
            (tail[0] - px * wdt, tail[1] - py * wdt)]
    d.polygon(body, fill=color)
    d.polygon([(tail[0] + px * wdt, tail[1] + py * wdt),
               (tail[0] + px * wdt * 2.6, tail[1] + py * wdt * 2.6),
               (tail[0] - ux * s * 0.28 + px * wdt, tail[1] - uy * s * 0.28 + py * wdt)], fill=RED)
    d.polygon([(tail[0] - px * wdt, tail[1] - py * wdt),
               (tail[0] - px * wdt * 2.6, tail[1] - py * wdt * 2.6),
               (tail[0] - ux * s * 0.28 - px * wdt, tail[1] - uy * s * 0.28 - py * wdt)], fill=RED)
    tip = (tail[0] - ux * s * 0.75, tail[1] - uy * s * 0.75)
    d.polygon([(tail[0] + px * wdt * 0.7, tail[1] + py * wdt * 0.7), tip,
               (tail[0] - px * wdt * 0.7, tail[1] - py * wdt * 0.7)], fill=GOLD)
    d.rectangle([cx - s, cy + s * 1.08, cx + s, cy + s * 1.34], fill=(255, 255, 255), outline=LINE, width=2)
    d.rectangle([cx - s, cy + s * 1.21, cx + s, cy + s * 1.34], fill=RED)

def icon_globe(cx, cy, s, color):
    d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=color, width=7)
    d.ellipse([cx - s * 0.45, cy - s, cx + s * 0.45, cy + s], outline=color, width=4)
    d.line([cx - s, cy, cx + s, cy], fill=color, width=4)
    d.arc([cx - s, cy - s * 0.55, cx + s, cy + s * 0.45], 0, 180, fill=color, width=4)
    d.arc([cx - s, cy - s * 0.45, cx + s, cy + s * 0.55], 180, 360, fill=color, width=4)
    d.rectangle([cx + s * 0.72, cy - s * 0.9, cx + s * 0.95, cy + s * 0.35], fill=RED)
    d.ellipse([cx + s * 0.6, cy + s * 0.2, cx + s * 1.07, cy + s * 0.68], fill=RED)

def icon_chart(cx, cy, s, color):
    d.line([cx - s, cy + s * 0.9, cx + s, cy + s * 0.9], fill=GREY, width=5)
    d.line([cx - s, cy - s * 0.9, cx - s, cy + s * 0.9], fill=GREY, width=5)
    pts = [(cx - s * 0.8, cy - s * 0.55), (cx - s * 0.35, cy - s * 0.1), (cx + s * 0.05, cy - s * 0.45),
           (cx + s * 0.45, cy + s * 0.25), (cx + s * 0.82, cy + s * 0.62)]
    d.line(pts, fill=RED, width=9, joint="curve")
    x, y = pts[-1]
    d.polygon([(x, y), (x - s * 0.34, y - s * 0.02), (x - s * 0.02, y + s * 0.34)], fill=RED)

def icon_chat(cx, cy, s, color):
    d.rounded_rectangle([cx - s, cy - s * 0.85, cx + s * 0.15, cy + s * 0.3], radius=16, outline=color, width=7)
    d.polygon([(cx - s * 0.55, cy + s * 0.3), (cx - s * 0.55, cy + s * 0.75), (cx - s * 0.1, cy + s * 0.3)], fill=color)
    d.rounded_rectangle([cx - s * 0.15, cy - s * 0.3, cx + s, cy + s * 0.85], radius=16, outline=TEAL, width=7)
    d.polygon([(cx + s * 0.55, cy + s * 0.85), (cx + s * 0.55, cy + s * 1.28), (cx + s * 0.1, cy + s * 0.85)], fill=TEAL)
    for yy in (cy - s * 0.42, cy - s * 0.05):
        d.line([cx - s * 0.72, yy, cx - s * 0.12, yy], fill=color, width=6)
    for yy in (cy + s * 0.12, cy + s * 0.49):
        d.line([cx + s * 0.12, yy, cx + s * 0.72, yy], fill=TEAL, width=6)

def icon_flags(cx, cy, s, color):
    flags = [(66, 103, 178), (222, 41, 16), (36, 74, 165)]
    x0 = cx - s
    for i, main in enumerate(flags):
        x = x0 + i * s * 0.72
        d.line([x, cy - s, x, cy + s], fill=INK, width=5)
        d.rectangle([x, cy - s, x + s * 0.58, cy - s * 0.42], fill=main)
    d.rectangle([cx - s * 1.05, cy + s * 0.82, cx + s * 1.05, cy + s], fill=color)

ICONS = [icon_scales, icon_missile, icon_globe, icon_chart, icon_chat, icon_flags]
COLORS = [BLUE, INK, TEAL, RED, GREEN, GOLD]
TINTS = [(232, 238, 248), (238, 238, 240), (230, 243, 241),
         (250, 233, 233), (233, 243, 234), (248, 240, 222)]

STORIES = [
    ("ICJ RULES MYANMAR COMMITTED GENOCIDE",
     "World Court judgment in The Hague on the 2017 Rohingya crackdown case"),
    ("RUSSIAN MISSILE CRASHES IN POLAND",
     "NATO jets scramble during Russia's huge air attack on Ukraine"),
    ("COP31 TALKS MISS THEIR DEADLINE",
     "Antalya climate summit deadlocked over fossil fuels and finance"),
    ("WALL STREET SLIDES INTO CORRECTION",
     "AI-led selloff at Friday's close: S&P 500 -3.7%, Nasdaq -5.3%"),
    ("IRAN SEEKS TALKS; TRUMP REJECTS TERMS",
     "Tehran wants diplomacy to end the war; Trump says it may run into 2027"),
    ("U.S., CHINA & RUSSIA LEADERS IN SHENZHEN",
     "Joint declaration; pledge: humans keep control of military AI"),
]

def paste_illo(i, x, y, size):
    """Paste illustration i into a size x size box at (x, y); True if asset used."""
    path = os.path.join(ASSETS, FILES[i])
    if not os.path.exists(path):
        return False
    a = Image.open(path).convert("RGB")
    # center-crop to square, then resize
    w0, h0 = a.size
    m = min(w0, h0)
    a = a.crop(((w0 - m) // 2, (h0 - m) // 2, (w0 + m) // 2, (h0 + m) // 2))
    a = a.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size, size], radius=14, fill=255)
    img.paste(a, (x, y), mask)
    return True

# ---------- panels ----------
margin, gap = 36, 20
top = 224
ph = 236
pw = (W - margin * 2 - gap) // 2
head_f = font(FX, 25)
sub_f = font(FR, 21)
ILLO = 148
for i, (head, sub) in enumerate(STORIES):
    col, row = i % 2, i // 2
    x = margin + col * (pw + gap)
    y = top + row * (ph + gap)
    d.rounded_rectangle([x, y, x + pw, y + ph], radius=14, fill=TINTS[i], outline=LINE, width=2)
    d.rectangle([x, y, x + pw, y + 10], fill=COLORS[i])
    # illustration block (left)
    ix, iy = x + 18, y + 26
    if not paste_illo(i, ix, iy, ILLO):
        d.rounded_rectangle([ix, iy, ix + ILLO, iy + ILLO], radius=14, fill=CREAM, outline=LINE, width=2)
        ICONS[i](ix + ILLO // 2, iy + ILLO // 2, 44, COLORS[i])
    else:
        d.rounded_rectangle([ix, iy, ix + ILLO, iy + ILLO], radius=14, outline=LINE, width=2)
    # number badge
    bx, by = x + pw - 44, y + 22
    d.ellipse([bx, by, bx + 30, by + 30], fill=COLORS[i])
    num = str(i + 1)
    nf = font(FX, 19)
    nw = d.textlength(num, font=nf)
    d.text((bx + 15 - nw / 2, by + 4), num, font=nf, fill=(255, 255, 255))
    # headline (right of illustration)
    tx = ix + ILLO + 16
    hl = wrap(head, head_f, x + pw - 62 - tx)
    d.multiline_text((tx, y + 30), "\n".join(hl), font=head_f, fill=INK, spacing=3)
    # subline (bottom, full width)
    sl = wrap(sub, sub_f, pw - 40)
    d.multiline_text((x + 20, y + ph - 56), "\n".join(sl[:2]), font=sub_f, fill=(52, 56, 64), spacing=3)

# ---------- footer ----------
fy = top + 3 * ph + 2 * gap + 8
d.line([margin, fy, W - margin, fy], fill=LINE, width=2)
d.text((margin, fy + 8), "As reported on 21 Nov 2026 by wire and news services worldwide.",
       font=font(FR, 22), fill=GREY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("saved", out, img.size, os.path.getsize(out))
