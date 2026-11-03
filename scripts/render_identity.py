"""Render a compact personal profile introduction with dispersed text particles.

The static poster and full-resolution frames are 1200 x 360. Delivery GIFs are
960 x 288 at 25 fps. This is decorative typography, not a physical simulation.
"""

import argparse
import math
from pathlib import Path

from particle_wordmark import ParticleWordmark
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
W, H, SCALE = 1200, 360, 2
TAU = math.tau
FRAME_COUNT, FRAME_DURATION_MS = 300, 40
DELIVERY_SIZE = (960, 288)
PALETTES = {
    "dark": {
        "background": "#0B1417",
        "ink": "#EFE9DC",
        "muted": "#AFA99C",
        "support": "#D7D2C7",
        "line": "#293438",
        "accent": "#DF9668",
    },
    "light": {
        "background": "#F4EEE4",
        "ink": "#222A2C",
        "muted": "#706F66",
        "support": "#4F5654",
        "line": "#D8CDBB",
        "accent": "#B5623D",
    },
}


def text(draw, xy, value, font, color):
    draw.text(
        tuple(coordinate * SCALE for coordinate in xy),
        value,
        font=font,
        fill=color,
        anchor="lt",
    )


def base(theme, font_path):
    p = PALETTES[theme]
    image = Image.new("RGB", (W * SCALE, H * SCALE), p["background"])
    d = ImageDraw.Draw(image)

    def font(size, index=5):
        return ImageFont.truetype(font_path, round(size * SCALE), index=index)

    d.ellipse((56 * SCALE, 43 * SCALE, 64 * SCALE, 51 * SCALE), fill=p["accent"])
    text(d, (78, 38), "ASSOCIATE ENGINEER AT ORACLE · INDIA", font(20), p["muted"])

    # Normal title-case type, without a logo, sculpture, or stationary replacement
    # letter. Every letter belongs to the same particle mask.
    wordmask = Image.new("L", image.size)
    text(ImageDraw.Draw(wordmask), (54, 122), "Yash Modi", font(88, 2), 255)

    d.line(
        (56 * SCALE, 270 * SCALE, 1144 * SCALE, 270 * SCALE),
        fill=p["line"],
        width=SCALE,
    )
    text(
        d,
        (56, 295),
        "Building software from interface to infrastructure.",
        font(26),
        p["support"],
    )
    image.info["wordmark"] = ParticleWordmark(wordmask, SCALE, count=3000)
    return image


def frame(background, theme, phase):
    image = background.copy()
    background.info["wordmark"].draw(image, phase, PALETTES[theme])
    return image.resize((W, H), Image.Resampling.LANCZOS)


def render(theme, font_path, still_only):
    output = ROOT / "assets"
    output.mkdir(exist_ok=True)
    background = base(theme, font_path)
    frame(background, theme, 0).save(output / f"identity-{theme}.png", optimize=True)
    for index, progress in enumerate((0.23, 0.39, 0.64, 0.84)):
        frame(background, theme, progress * TAU).save(
            output / f".review-{theme}-{index}.png"
        )
    if still_only:
        return

    width, height = DELIVERY_SIZE
    sheet = Image.new("RGB", (width * 2, height * 2))
    for index, progress in enumerate((0, 0.23, 0.39, 0.64)):
        sheet.paste(
            frame(background, theme, progress * TAU).resize(
                DELIVERY_SIZE, Image.Resampling.LANCZOS
            ),
            ((index % 2) * width, (index // 2) * height),
        )
    palette = sheet.quantize(colors=64, method=Image.Quantize.MEDIANCUT)
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
        "source frames",
        FRAME_DURATION_MS,
        "ms/frame",
        (output / f"identity-{theme}.gif").stat().st_size,
        "bytes",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--font", default="/System/Library/Fonts/Avenir Next.ttc")
    parser.add_argument("--still-only", action="store_true")
    parser.add_argument("--theme", choices=["light", "dark", "both"], default="dark")
    args = parser.parse_args()
    for theme in PALETTES if args.theme == "both" else [args.theme]:
        render(theme, args.font, args.still_only)
