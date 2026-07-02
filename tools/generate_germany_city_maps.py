from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


WIDTH, HEIGHT = 1586, 992
OUT_DIR = Path("assets/visual/generated")


CITY_SPECS = {
    "freiburg": {
        "accent": (93, 146, 112),
        "water": "bach",
        "landmarks": ["minster", "forest", "bachle"],
        "roof": (168, 91, 61),
    },
    "stuttgart": {
        "accent": (108, 143, 114),
        "water": "pond",
        "landmarks": ["museum", "avenue", "garden"],
        "roof": (166, 94, 59),
    },
    "heidelberg": {
        "accent": (113, 139, 103),
        "water": "river",
        "landmarks": ["castle", "bridge", "philosopher"],
        "roof": (159, 84, 57),
    },
    "frankfurt": {
        "accent": (105, 140, 147),
        "water": "river",
        "landmarks": ["skyline", "romer", "museum"],
        "roof": (152, 89, 63),
    },
    "cologne": {
        "accent": (102, 130, 144),
        "water": "river",
        "landmarks": ["cathedral", "bridge", "promenade"],
        "roof": (154, 86, 61),
    },
    "aachen": {
        "accent": (126, 138, 103),
        "water": "spring",
        "landmarks": ["chapel", "thermal", "square"],
        "roof": (154, 88, 59),
    },
    "bremen": {
        "accent": (101, 139, 126),
        "water": "river",
        "landmarks": ["townhall", "musicians", "schnoor"],
        "roof": (162, 89, 62),
    },
    "hamburg": {
        "accent": (88, 132, 149),
        "water": "harbor",
        "landmarks": ["warehouse", "philharmonic", "ferry"],
        "roof": (145, 82, 65),
    },
    "lubeck": {
        "accent": (111, 138, 129),
        "water": "canal",
        "landmarks": ["gate", "island", "marzipan"],
        "roof": (151, 80, 60),
    },
    "berlin": {
        "accent": (118, 134, 145),
        "water": "river",
        "landmarks": ["gate", "museum_island", "wall"],
        "roof": (151, 88, 63),
    },
    "dresden": {
        "accent": (128, 137, 116),
        "water": "river",
        "landmarks": ["frauenkirche", "zwinger", "terrace"],
        "roof": (158, 88, 60),
    },
    "leipzig": {
        "accent": (117, 139, 115),
        "water": "canal",
        "landmarks": ["church", "spinnerei", "oldhall"],
        "roof": (156, 87, 61),
    },
    "nuremberg": {
        "accent": (123, 132, 103),
        "water": "river",
        "landmarks": ["castle", "market", "toy"],
        "roof": (160, 83, 56),
    },
    "rothenburg": {
        "accent": (133, 138, 97),
        "water": "brook",
        "landmarks": ["wall", "plonlein", "christmas"],
        "roof": (168, 87, 56),
    },
    "ulm": {
        "accent": (104, 140, 136),
        "water": "river",
        "landmarks": ["minster", "fishermen", "danube"],
        "roof": (158, 90, 60),
    },
    "munich": {
        "accent": (96, 143, 119),
        "water": "river",
        "landmarks": ["marienplatz", "garden", "museum"],
        "roof": (154, 92, 62),
    },
    "fussen": {
        "accent": (104, 139, 150),
        "water": "lake",
        "landmarks": ["neuschwanstein", "alps", "oldtown"],
        "roof": (157, 88, 61),
    },
}


def jitter(rng: random.Random, value: float, amount: float) -> float:
    return value + rng.uniform(-amount, amount)


def poly(draw: ImageDraw.ImageDraw, points, fill, outline=None, width=1):
    draw.polygon([(round(x), round(y)) for x, y in points], fill=fill, outline=outline)
    if outline:
        draw.line([(round(x), round(y)) for x, y in points + [points[0]]], fill=outline, width=width, joint="curve")


def line(draw, points, fill, width=3):
    draw.line([(round(x), round(y)) for x, y in points], fill=fill, width=width, joint="curve")


def draw_paper(rng):
    base = Image.new("RGB", (WIDTH, HEIGHT), (242, 232, 207))
    px = base.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            noise = rng.randint(-12, 12)
            warm = int(8 * math.sin((x + y) / 170))
            r, g, b = px[x, y]
            px[x, y] = (
                max(0, min(255, r + noise + warm)),
                max(0, min(255, g + noise // 2 + warm // 2)),
                max(0, min(255, b + noise // 3)),
            )
    return base.filter(ImageFilter.GaussianBlur(0.25))


def draw_water(draw, rng, kind):
    water = (115, 180, 188, 205)
    edge = (77, 132, 142, 170)
    if kind in {"river", "harbor", "canal", "lake"}:
        if kind == "harbor":
            pts = [(-80, 610), (240, 555), (520, 650), (850, 610), (1180, 710), (1670, 630), (1670, 1050), (-80, 1050)]
        elif kind == "lake":
            pts = [(780, 660), (1000, 565), (1300, 610), (1560, 780), (1430, 1000), (750, 1010), (600, 850)]
        else:
            pts = [(-60, 720), (180, 655), (420, 700), (650, 610), (900, 670), (1180, 610), (1660, 700), (1660, 1030), (-60, 1030)]
        poly(draw, [(jitter(rng, x, 18), jitter(rng, y, 18)) for x, y in pts], water, edge, 3)
        for i in range(10):
            y = 710 + i * 26 + rng.randint(-16, 16)
            line(draw, [(50, y), (340, y - 28), (680, y + 8), (980, y - 22), (1390, y + 12)], (239, 248, 238, 100), 2)
    if kind in {"bach", "brook", "spring"}:
        for offset in [0, 44] if kind == "bach" else [0]:
            pts = [(40, 690 + offset), (260, 650 + offset), (470, 710 + offset), (700, 660 + offset), (950, 720 + offset), (1240, 680 + offset), (1540, 725 + offset)]
            line(draw, pts, (92, 165, 176, 185), 13 if kind == "bach" else 20)
            line(draw, pts, (230, 247, 241, 140), 3)


def draw_roads(draw, rng):
    road = (223, 207, 169, 210)
    edge = (157, 135, 99, 110)
    paths = [
        [(70, 550), (260, 470), (520, 500), (750, 420), (1020, 455), (1430, 355)],
        [(170, 835), (370, 690), (620, 635), (840, 545), (1110, 560), (1500, 500)],
        [(520, 170), (620, 330), (690, 510), (720, 730), (760, 950)],
    ]
    for pts in paths:
        pts = [(jitter(rng, x, 10), jitter(rng, y, 10)) for x, y in pts]
        line(draw, pts, edge, 22)
        line(draw, pts, road, 16)
        line(draw, pts, (248, 240, 214, 155), 4)


def draw_tree(draw, rng, x, y, scale=1):
    trunk = (118, 91, 66, 185)
    greens = [(89, 132, 82, 190), (112, 151, 92, 180), (142, 162, 99, 170)]
    line(draw, [(x, y + 18 * scale), (x + rng.uniform(-3, 3), y + 46 * scale)], trunk, max(2, int(5 * scale)))
    for _ in range(5):
        r = rng.uniform(15, 28) * scale
        cx = x + rng.uniform(-16, 16) * scale
        cy = y + rng.uniform(-12, 12) * scale
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rng.choice(greens), outline=(77, 111, 72, 105), width=1)


def draw_house(draw, rng, x, y, w, h, roof, wall=None):
    wall = wall or rng.choice([(226, 199, 145), (232, 214, 177), (216, 181, 139), (238, 222, 184), (199, 184, 147)])
    skew = rng.uniform(-10, 10)
    body = [(x, y), (x + w, y + skew), (x + w, y + h), (x, y + h - skew)]
    poly(draw, body, wall, (114, 99, 82, 145), 2)
    roof_pts = [(x - 8, y + 3), (x + w * 0.52, y - h * 0.38), (x + w + 10, y + skew + 3), (x + w, y + skew + 18), (x, y + 18)]
    poly(draw, roof_pts, tuple(max(0, min(255, c + rng.randint(-14, 14))) for c in roof), (103, 73, 58, 145), 2)
    for col in range(max(1, int(w // 34))):
        for row in range(max(1, int(h // 34))):
            wx = x + 13 + col * 32
            wy = y + 22 + row * 30
            draw.rectangle((wx, wy, wx + 10, wy + 13), fill=(101, 130, 137, 130), outline=(87, 82, 74, 120), width=1)
    if rng.random() < 0.35:
        line(draw, [(x + w * 0.2, y + 10), (x + w * 0.86, y + 20)], (98, 79, 65, 120), 3)


def draw_bridge(draw, x, y, w):
    line(draw, [(x, y), (x + w, y - 26)], (160, 139, 111, 190), 22)
    line(draw, [(x, y - 11), (x + w, y - 37)], (240, 228, 202, 210), 13)
    for i in range(6):
        cx = x + i * w / 5
        draw.arc((cx - 50, y - 42, cx + 50, y + 34), 190, 350, fill=(114, 100, 85, 160), width=4)


def draw_cathedral(draw, x, y, scale, roof=(91, 92, 89)):
    stone = (182, 172, 148, 220)
    dark = (82, 79, 75, 170)
    draw.rectangle((x - 55 * scale, y, x + 55 * scale, y + 145 * scale), fill=stone, outline=dark, width=max(2, int(3 * scale)))
    for dx in [-42, -18, 18, 42]:
        draw.rectangle((x + dx * scale - 6 * scale, y + 38 * scale, x + dx * scale + 6 * scale, y + 92 * scale), fill=(78, 103, 119, 145), outline=dark)
    for sx in [-56, 56]:
        draw.rectangle((x + sx * scale - 24 * scale, y - 25 * scale, x + sx * scale + 24 * scale, y + 135 * scale), fill=stone, outline=dark, width=max(2, int(3 * scale)))
        poly(draw, [(x + sx * scale - 34 * scale, y - 24 * scale), (x + sx * scale, y - 128 * scale), (x + sx * scale + 34 * scale, y - 24 * scale)], roof, dark, 2)
    draw.ellipse((x - 18 * scale, y + 88 * scale, x + 18 * scale, y + 124 * scale), fill=(80, 104, 119, 130), outline=dark)


def draw_castle(draw, x, y, scale, roof):
    stone = (190, 176, 142, 220)
    dark = (94, 84, 72, 165)
    draw.rectangle((x - 150 * scale, y, x + 150 * scale, y + 92 * scale), fill=stone, outline=dark, width=3)
    for dx in [-125, 0, 125]:
        draw.rectangle((x + dx * scale - 30 * scale, y - 40 * scale, x + dx * scale + 30 * scale, y + 92 * scale), fill=stone, outline=dark, width=3)
        poly(draw, [(x + dx * scale - 42 * scale, y - 40 * scale), (x + dx * scale, y - 100 * scale), (x + dx * scale + 42 * scale, y - 40 * scale)], roof, dark, 2)
    for i in range(7):
        wx = x - 125 * scale + i * 42 * scale
        draw.rectangle((wx, y + 30 * scale, wx + 14 * scale, y + 52 * scale), fill=(89, 110, 116, 130), outline=dark)


def draw_gate(draw, x, y, scale):
    brick = (177, 104, 78, 220)
    dark = (105, 72, 62, 170)
    for dx in [-58, 58]:
        draw.rectangle((x + dx * scale - 34 * scale, y - 92 * scale, x + dx * scale + 34 * scale, y + 100 * scale), fill=brick, outline=dark, width=3)
        poly(draw, [(x + dx * scale - 43 * scale, y - 92 * scale), (x + dx * scale, y - 145 * scale), (x + dx * scale + 43 * scale, y - 92 * scale)], (72, 88, 92), dark, 2)
    draw.rectangle((x - 92 * scale, y - 6 * scale, x + 92 * scale, y + 98 * scale), fill=(206, 185, 142, 210), outline=dark, width=3)
    draw.arc((x - 34 * scale, y + 28 * scale, x + 34 * scale, y + 122 * scale), 180, 360, fill=dark, width=6)


def draw_skyline(draw, x, y, scale):
    colors = [(142, 151, 156, 190), (178, 164, 138, 200), (122, 143, 151, 190)]
    for i, h in enumerate([170, 230, 145, 260, 190, 120]):
        w = [46, 54, 40, 62, 48, 42][i] * scale
        xx = x + (i - 3) * 58 * scale
        draw.rectangle((xx, y - h * scale, xx + w, y), fill=colors[i % len(colors)], outline=(85, 92, 94, 140), width=2)
        for yy in range(int(y - h * scale + 20), int(y - 10), int(28 * scale)):
            draw.line((xx + 8, yy, xx + w - 8, yy), fill=(240, 225, 169, 130), width=2)


def draw_landmarks(draw, rng, spec):
    roof = spec["roof"]
    landmarks = spec["landmarks"]
    if any(name in landmarks for name in ["minster", "cathedral", "chapel", "church", "frauenkirche"]):
        draw_cathedral(draw, 1030, 385, 1.05, roof=(78, 82, 82))
    if any(name in landmarks for name in ["castle", "neuschwanstein"]):
        draw_castle(draw, 1050, 275, 1.05, roof)
    if "skyline" in landmarks:
        draw_skyline(draw, 1080, 395, 1.0)
    if "gate" in landmarks:
        draw_gate(draw, 1035, 375, 1.0)
    if "warehouse" in landmarks:
        for i in range(5):
            draw_house(draw, rng, 890 + i * 80, 335 + (i % 2) * 18, 76, 130, (126, 67, 58), (165, 95, 78))
    if "philharmonic" in landmarks:
        poly(draw, [(1220, 270), (1320, 230), (1440, 270), (1430, 350), (1220, 350)], (204, 223, 221, 190), (81, 111, 127, 150), 2)
        for x in range(1230, 1430, 26):
            line(draw, [(x, 342), (x + 8, 260 + rng.randint(-18, 18))], (91, 128, 148, 125), 2)
    if "wall" in landmarks:
        line(draw, [(745, 210), (830, 260), (930, 220), (1040, 280)], (143, 117, 92, 190), 14)
        for x in range(755, 1030, 42):
            draw.rectangle((x, 205 + rng.randint(-10, 10), x + 16, 225 + rng.randint(8, 22)), fill=rng.choice([(207, 118, 96), (99, 139, 174), (226, 188, 90)]))
    if "alps" in landmarks:
        for x, h in [(930, 230), (1100, 290), (1290, 250)]:
            poly(draw, [(x - 180, 420), (x, 420 - h), (x + 220, 420)], (126, 145, 141, 190), (84, 102, 101, 130), 2)
            poly(draw, [(x - 58, 420 - h + 75), (x, 420 - h), (x + 70, 420 - h + 84)], (236, 239, 225, 210), None)
    if "bridge" in landmarks:
        draw_bridge(draw, 780, 650, 440)
    if "musicians" in landmarks:
        for i, r in enumerate([28, 22, 17, 13]):
            cx, cy = 445, 430 - i * 38
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(96, 82, 67, 190), outline=(67, 57, 49, 150), width=2)


def draw_city_map(city_id, spec):
    rng = random.Random(city_id)
    img = draw_paper(rng).convert("RGBA")
    wash = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(wash, "RGBA")
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(255, 248, 226, 42))

    draw_water(draw, rng, spec["water"])
    draw_roads(draw, rng)

    for _ in range(135):
        draw_tree(draw, rng, rng.randint(20, WIDTH - 20), rng.randint(120, HEIGHT - 80), rng.uniform(0.55, 1.05))

    clusters = [
        (250, 480, 6, 3),
        (470, 560, 6, 4),
        (720, 500, 5, 4),
        (930, 570, 5, 3),
        (1180, 500, 4, 4),
        (620, 735, 5, 2),
    ]
    for bx, by, cols, rows in clusters:
        for row in range(rows):
            for col in range(cols):
                if rng.random() < 0.14:
                    continue
                x = bx + col * rng.randint(58, 72) + rng.randint(-15, 15)
                y = by + row * rng.randint(54, 66) + rng.randint(-14, 14)
                draw_house(draw, rng, x, y, rng.randint(44, 72), rng.randint(48, 84), spec["roof"])

    draw_landmarks(draw, rng, spec)

    accent = spec["accent"]
    for _ in range(22):
        x, y = rng.randint(60, WIDTH - 60), rng.randint(140, HEIGHT - 70)
        r = rng.randint(10, 24)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(*accent, rng.randint(45, 80)))

    for _ in range(32):
        x, y = rng.randint(40, WIDTH - 40), rng.randint(180, HEIGHT - 50)
        line(draw, [(x, y), (x + rng.randint(-9, 9), y + rng.randint(16, 30))], (84, 77, 67, 135), 2)
        draw.ellipse((x - 4, y - 7, x + 4, y + 1), fill=(95, 74, 62, 145))

    img.alpha_composite(wash)
    texture = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 0))
    td = ImageDraw.Draw(texture, "RGBA")
    for _ in range(900):
        x, y = rng.randint(0, WIDTH), rng.randint(0, HEIGHT)
        td.point((x, y), fill=(78, 65, 49, rng.randint(10, 34)))
    img = Image.alpha_composite(img, texture.filter(ImageFilter.GaussianBlur(0.4))).convert("RGB")
    return img.filter(ImageFilter.UnsharpMask(radius=1, percent=75, threshold=3))


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for city_id, spec in CITY_SPECS.items():
        out = OUT_DIR / f"map-{city_id}-city-handdrawn.png"
        draw_city_map(city_id, spec).save(out, optimize=True)
        print(out)


if __name__ == "__main__":
    main()
