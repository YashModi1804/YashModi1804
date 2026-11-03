"""Render Yash's kinetic wordmark: continuity becomes the O in MODI.

Requires Pillow. Fonts are rendered into pixels, never redistributed. All motion
is periodic; GIF frames use an exact 40 ms duration for 25 frames per second.
"""

import argparse
import math
from pathlib import Path

from particle_wordmark import ParticleWordmark
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
W, H, SCALE = 1200, 680, 2
TAU = math.tau
CX, CY, OBJECT_SCALE = 535, 437, 60
FRAME_COUNT, FRAME_DURATION_MS = 300, 40
DELIVERY_SIZE = (960, 544)
PALETTES = {
    "light": {
        "background": "#F4EEE4",
        "ink": "#222A2C",
        "muted": "#706F66",
        "line": "#D8CDBB",
        "accent": "#B5623D",
        "surface": (78, 53, 39),
        "highlight": (237, 187, 124),
        "edge": (79, 52, 38),
        "glint": (255, 228, 179),
    },
    "dark": {
        "background": "#0B1417",
        "ink": "#EFE9DC",
        "muted": "#AFA99C",
        "line": "#334044",
        "accent": "#DF9668",
        "surface": (82, 50, 32),
        "highlight": (240, 197, 142),
        "edge": (62, 42, 29),
        "glint": (255, 235, 196),
    },
}


def mix(a, b, amount):
    return tuple(round(x + (y - x) * amount) for x, y in zip(a, b))


def rgb(value):
    return tuple(int(value[i : i + 2], 16) for i in (1, 3, 5))


def rotate(point, phase):
    x, y, z = point
    ax, ay, az = 0.59 + 0.10 * math.sin(phase), phase, 0.14 + 0.09 * math.sin(phase)
    y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    return x * math.cos(az) - y * math.sin(az), x * math.sin(az) + y * math.cos(az), z


def ribbon(t, u):
    radius = 1.73 + u * math.cos(t / 2)
    return radius * math.cos(t), radius * math.sin(t), u * math.sin(t / 2)


def project(point):
    x, y, z = point
    size = OBJECT_SCALE / (1 - z * 0.055)
    return ((CX + x * size) * SCALE, (CY - y * size) * SCALE)


def normal(a, b, c):
    u = tuple(y - x for x, y in zip(a, b))
    v = tuple(y - x for x, y in zip(a, c))
    cross = (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )
    length = math.sqrt(sum(n * n for n in cross)) or 1
    return tuple(n / length for n in cross)


def text(draw, xy, value, font, color, spacing=0):
    x, y = (coordinate * SCALE for coordinate in xy)
    if not spacing:
        draw.text((x, y), value, font=font, fill=color, anchor="lt")
        return
    for character in value:
        draw.text((x, y), character, font=font, fill=color, anchor="lt")
        x += draw.textlength(character, font=font) + spacing * SCALE


def line(draw, points, color, width=1):
    draw.line(
        [(x * SCALE, y * SCALE) for x, y in points],
        fill=color,
        width=max(1, round(width * SCALE)),
    )


def base(theme, font_path):
    p = PALETTES[theme]
    image = Image.new("RGB", (W * SCALE, H * SCALE), p["background"])
    d = ImageDraw.Draw(image)

    def font(size, index=0):
        return ImageFont.truetype(font_path, round(size * SCALE), index=index)

    d.ellipse((53 * SCALE, 44 * SCALE, 61 * SCALE, 52 * SCALE), fill=p["accent"])
    text(d, (75, 40), "ASSOCIATE ENGINEER AT ORACLE", font(17, 5), p["muted"], 1.1)
    text(d, (1080, 40), "INDIA", font(17, 5), p["muted"], 1.5)
    wordmask = Image.new("L", image.size)
    worddraw = ImageDraw.Draw(wordmask)
    text(worddraw, (43, 91), "YASH", font(280), 255, -13)

    # The exact quote from Yash's original profile, as a personal margin note.
    line(d, [(884, 135), (918, 135)], p["accent"], 2)
    for index, phrase in enumerate(
        ("In the stillness", "of the mind,", "one can find", "the universe!")
    ):
        text(d, (884, 158 + index * 29), phrase, font(22, 6), p["muted"])

    # A permanent O contour preserves the surname through every edge-on pose.
    text(worddraw, (42, 337), "M", font(295), 255)
    text(worddraw, (732, 337), "D", font(295), 255)
    text(worddraw, (1033, 337), "I", font(295), 255)
    d.ellipse(
        (
            (CX - 155) * SCALE,
            (CY - 118) * SCALE,
            (CX + 155) * SCALE,
            (CY + 118) * SCALE,
        ),
        outline=mix(rgb(p["line"]), rgb(p["ink"]), 0.28),
        width=4 * SCALE,
    )
    d.ellipse(
        (
            (CX - 164) * SCALE,
            (CY - 127) * SCALE,
            (CX + 164) * SCALE,
            (CY + 127) * SCALE,
        ),
        outline=mix(rgb(p["line"]), rgb(p["background"]), 0.45),
        width=SCALE,
    )

    shadow = Image.new("RGBA", image.size)
    sd = ImageDraw.Draw(shadow)
    sd.ellipse(
        (405 * SCALE, 548 * SCALE, 671 * SCALE, 564 * SCALE),
        fill=(0, 0, 0, 28 if theme == "light" else 65),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(9 * SCALE))
    image = Image.alpha_composite(image.convert("RGBA"), shadow).convert("RGB")
    d = ImageDraw.Draw(image)

    text(d, (53, 584), "CURRENTLY LEARNING", font(12, 5), p["muted"], 1.6)
    line(d, [(53, 613), (1147, 613)], p["line"])
    for x, label in (
        (53, "Low-latency software"),
        (475, "System design"),
        (886, "Cloud architecture"),
    ):
        d.ellipse(
            ((x - 3) * SCALE, 610 * SCALE, (x + 3) * SCALE, 616 * SCALE),
            fill=p["muted"],
        )
        text(d, (x, 631), label, font(18, 5), p["muted"])
    image.info["wordmark"] = ParticleWordmark(wordmask, SCALE)
    return image


def orbit(draw, theme, phase):
    """Two traveling arc segments give the permanent O contour a direction."""
    p = PALETTES[theme]
    background, accent = rgb(p["background"]), rgb(p["accent"])
    for offset, rx, ry, strength in ((0, 155, 118, 0.75), (math.pi, 164, 127, 0.32)):
        for step in range(28):
            t0 = -phase + offset + step / 28 * 0.85
            t1 = t0 + 0.85 / 28 + 0.005
            a = (CX + rx * math.cos(t0), CY + ry * math.sin(t0))
            b = (CX + rx * math.cos(t1), CY + ry * math.sin(t1))
            line(draw, (a, b), mix(background, accent, strength * (step + 1) / 28), 1.5)


def frame(background, theme, phase):
    p = PALETTES[theme]
    image = background.copy()
    background.info["wordmark"].draw(image, phase, p)
    d = ImageDraw.Draw(image)
    orbit(d, theme, phase)
    segments, bands = 144, 16
    points = [
        [
            rotate(ribbon(i / segments * TAU, -0.65 + j / bands * 1.30), phase)
            for j in range(bands + 1)
        ]
        for i in range(segments + 1)
    ]
    faces = []
    for i in range(segments):
        for j in range(bands):
            vertices = [
                points[i][j],
                points[i + 1][j],
                points[i + 1][j + 1],
                points[i][j + 1],
            ]
            n = normal(vertices[0], vertices[1], vertices[3])
            light = abs(n[0] * -0.4 + n[1] * 0.42 + n[2] * 0.81)
            # A continuous moving highlight adds motion without floating markers
            # that would incorrectly shine through the rear of the surface.
            highlight = max(0, math.cos(i / segments * TAU - phase * 2 - 0.4)) ** 12
            tone = min(1, 0.12 + 0.77 * light + 0.11 * highlight)
            fill = mix(p["surface"], p["highlight"], tone)
            if highlight > 0.5:
                fill = mix(fill, p["glint"], (highlight - 0.5) * 0.22)
            faces.append((sum(v[2] for v in vertices) / 4, i, j, vertices, fill))
    for _, i, j, vertices, fill in sorted(faces, key=lambda face: face[0]):
        polygon = [project(v) for v in vertices]
        d.polygon(polygon, fill=fill)
        if i % 6 == 0:
            d.line(
                (polygon[0], polygon[3]), fill=mix(fill, p["edge"], 0.18), width=SCALE
            )
        if j in (0, bands - 1):
            edge = (polygon[0], polygon[1]) if j == 0 else (polygon[3], polygon[2])
            d.line(edge, fill=mix(fill, p["glint"], 0.24), width=SCALE)

    # One signal connects the three explicitly labeled learning interests.
    progress = 0.5 - 0.5 * math.cos(phase)
    span = 1094
    signal_x = 53 + progress * span
    for index in range(-44, 45):
        x = signal_x + index * 2
        if 53 <= x <= 1147:
            strength = math.exp(-((index / 24) ** 2))
            color = mix(rgb(p["line"]), rgb(p["accent"]), strength)
            line(d, ((x, 613), (min(1147, x + 2.5), 613)), color, 2)
    d.ellipse(
        ((signal_x - 3) * SCALE, 610 * SCALE, (signal_x + 3) * SCALE, 616 * SCALE),
        fill=p["accent"],
    )
    return image.resize((W, H), Image.Resampling.LANCZOS)


def render(theme, font_path, still_only):
    output = ROOT / "assets"
    output.mkdir(exist_ok=True)
    background = base(theme, font_path)
    still = frame(background, theme, 0)
    still.save(output / f"identity-{theme}.png", optimize=True)
    for index, phase in enumerate((TAU / 4, TAU / 2, TAU * 3 / 4)):
        frame(background, theme, phase).save(output / f".review-{theme}-{index}.png")
    if still_only:
        return

    # One shared palette prevents shimmer across the material and particle phases.
    width, height = DELIVERY_SIZE
    sheet = Image.new("RGB", (width * 2, height * 2))
    for index, phase in enumerate((0, TAU / 4, TAU / 2, TAU * 3 / 4)):
        sheet.paste(
            frame(background, theme, phase).resize(
                DELIVERY_SIZE, Image.Resampling.LANCZOS
            ),
            ((index % 2) * width, (index // 2) * height),
        )
    # Give the curved bronze surface enough palette weight to avoid broad bands
    # beside the much larger flat lettering and particle field.
    surface = frame(background, theme, TAU * 3 / 4).crop((370, 318, 700, 565))
    sheet.paste(
        surface.resize(DELIVERY_SIZE, Image.Resampling.LANCZOS), (width, height)
    )
    palette = sheet.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    frames = [
        frame(background, theme, i / FRAME_COUNT * TAU)
        .resize(DELIVERY_SIZE, Image.Resampling.LANCZOS)
        .quantize(palette=palette, dither=Image.Dither.NONE)
        for i in range(FRAME_COUNT)
    ]
    frames[0].save(
        output / f"identity-{theme}.gif",
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        optimize=True,
        disposal=1,
    )
    print(
        theme,
        FRAME_COUNT,
        "frames",
        FRAME_DURATION_MS,
        "ms/frame",
        (output / f"identity-{theme}.gif").stat().st_size,
        "bytes",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--font", default="/System/Library/Fonts/Avenir Next.ttc")
    parser.add_argument("--still-only", action="store_true")
    parser.add_argument("--theme", choices=["light", "dark", "both"], default="both")
    args = parser.parse_args()
    for theme in PALETTES if args.theme == "both" else [args.theme]:
        render(theme, args.font, args.still_only)
