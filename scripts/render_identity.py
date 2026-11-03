"""Render Yash's original kinetic identity. No external artwork or animation service.

Requires Pillow. Supply an installed font with --font to render on another machine;
the default macOS Avenir Next is rendered into pixels, never redistributed.
"""

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
W, H, SCALE = 1200, 520, 2
TAU = math.tau
PALETTES = {
    "light": {
        "background": "#F1EEE7",
        "ink": "#172C2B",
        "muted": "#69756B",
        "line": "#D2D5C9",
        "accent": "#C3593E",
        "surface": (44, 72, 66),
        "highlight": (171, 189, 164),
        "edge": (17, 39, 35),
    },
    "dark": {
        "background": "#111C1C",
        "ink": "#F0EBDD",
        "muted": "#9CAA9C",
        "line": "#32433E",
        "accent": "#F18D68",
        "surface": (123, 142, 124),
        "highlight": (238, 231, 207),
        "edge": (51, 74, 65),
    },
}


def mix(a, b, amount):
    return tuple(round(x + (y - x) * amount) for x, y in zip(a, b))


def rotate(point, phase):
    x, y, z = point
    ax, ay, az = 0.68 + 0.12 * math.sin(phase), phase, 0.25 + 0.1 * math.sin(phase)
    y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    return x * math.cos(az) - y * math.sin(az), x * math.sin(az) + y * math.cos(az), z


def ribbon(t, u):
    radius = 1.73 + u * math.cos(t / 2)
    return radius * math.cos(t), radius * math.sin(t), u * math.sin(t / 2)


def project(point):
    x, y, z = point
    size = 92 / (1 - z * 0.075)
    return ((912 + x * size) * SCALE, (253 - y * size) * SCALE)


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


def base(theme, font_path):
    p = PALETTES[theme]
    image = Image.new("RGB", (W * SCALE, H * SCALE), p["background"])
    d = ImageDraw.Draw(image)
    font = lambda size, index=7: ImageFont.truetype(
        font_path, size * SCALE, index=index
    )
    text(d, (48, 37), "YM", font(19, 0), p["ink"])
    d.line(
        (97 * SCALE, 38 * SCALE, 97 * SCALE, 58 * SCALE), fill=p["line"], width=SCALE
    )
    text(d, (114, 39), "ENGINEER  /  INDIA", font(15, 5), p["muted"], 1.5)
    text(d, (48, 124), "YASH", font(137, 0), p["ink"], -7)
    text(d, (42, 255), "MODI", font(137, 0), p["ink"], -7)
    d.ellipse((51 * SCALE, 414 * SCALE, 59 * SCALE, 422 * SCALE), fill=p["accent"])
    text(d, (73, 408), "Associate Engineer at Oracle", font(24, 5), p["ink"])
    d.line(
        (48 * SCALE, 467 * SCALE, 1152 * SCALE, 467 * SCALE),
        fill=p["line"],
        width=SCALE,
    )
    text(
        d, (48, 486), "SOFTWARE  /  SYSTEMS  /  CURIOSITY", font(12, 5), p["muted"], 1.2
    )
    text(d, (930, 486), "01   /   CONTINUITY", font(12, 5), p["muted"], 1)
    # A quiet coordinate frame, independent of the moving surface.
    for x, y in ((670, 90), (1152, 90), (670, 420), (1152, 420)):
        d.line(
            ((x - 5) * SCALE, y * SCALE, (x + 5) * SCALE, y * SCALE),
            fill=p["line"],
            width=SCALE,
        )
        d.line(
            (x * SCALE, (y - 5) * SCALE, x * SCALE, (y + 5) * SCALE),
            fill=p["line"],
            width=SCALE,
        )
    return image


def frame(background, theme, phase):
    p = PALETTES[theme]
    image = background.copy()
    shadow = Image.new("RGBA", image.size)
    sd = ImageDraw.Draw(shadow)
    sd.ellipse(
        (756 * SCALE, 398 * SCALE, 1100 * SCALE, 425 * SCALE), fill=(13, 31, 26, 28)
    )
    image.paste(
        shadow.filter(ImageFilter.GaussianBlur(13 * SCALE)),
        (0, 0),
        shadow.filter(ImageFilter.GaussianBlur(13 * SCALE)),
    )
    d = ImageDraw.Draw(image)
    segments, bands = 144, 12
    points = [
        [
            rotate(ribbon(i / segments * TAU, -0.66 + j / bands * 1.32), phase)
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
            light = abs(n[0] * -0.38 + n[1] * 0.5 + n[2] * 0.77)
            tone = 0.12 + 0.78 * light
            fill = mix(p["surface"], p["highlight"], tone)
            faces.append((sum(v[2] for v in vertices) / 4, i, j, vertices, fill))
    for _, i, j, vertices, fill in sorted(faces, key=lambda face: face[0]):
        polygon = [project(v) for v in vertices]
        d.polygon(polygon, fill=fill)
        # 48 ribs are legible when the image scales to a narrow profile column.
        if i % 3 == 0:
            d.line(
                (polygon[0], polygon[3]), fill=mix(fill, p["edge"], 0.35), width=SCALE
            )
        if j in (0, bands - 1):
            edge = (polygon[0], polygon[1]) if j == 0 else (polygon[3], polygon[2])
            d.line(edge, fill=mix(fill, p["edge"], 0.5), width=2 * SCALE)
    # One marker travels across a two-sided surface and returns after a full loop.
    marker = rotate(ribbon(phase * 2 + 0.7, 0), phase)
    x, y = project(marker)
    d.ellipse(
        (x - 7 * SCALE, y - 7 * SCALE, x + 7 * SCALE, y + 7 * SCALE),
        fill=p["background"],
    )
    d.ellipse(
        (x - 4 * SCALE, y - 4 * SCALE, x + 4 * SCALE, y + 4 * SCALE), fill=p["accent"]
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
    count = 192
    # A shared palette avoids per-frame color shimmer and reduces the GIF size.
    sheet = Image.new("RGB", (W * 2, H * 2))
    for index, phase in enumerate((0, TAU / 4, TAU / 2, TAU * 3 / 4)):
        sheet.paste(
            frame(background, theme, phase), ((index % 2) * W, (index // 2) * H)
        )
    palette = sheet.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    frames = [
        frame(background, theme, i / count * TAU).quantize(
            palette=palette, dither=Image.Dither.NONE
        )
        for i in range(count)
    ]
    # GIF uses centiseconds. Alternate 60/70 ms for a smooth 12.48-second loop.
    frames[0].save(
        output / f"identity-{theme}.gif",
        save_all=True,
        append_images=frames[1:],
        duration=[60 if i % 2 == 0 else 70 for i in range(count)],
        loop=0,
        optimize=True,
        disposal=1,
    )
    print(
        theme,
        count,
        "frames",
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
