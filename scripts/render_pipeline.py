"""Draw Folio's documented synthetic example as an explanatory animation.

This is an architectural illustration, not a recording or live telemetry.
Requires Pillow; the installed font is rasterized, not distributed.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = "/System/Library/Fonts/Avenir Next.ttc"
SIZE = (1200, 382)
SCALE = 2
BG, PANEL, INK = "#0B1417", "#111E22", "#EFE9DC"
MUTED, LINE, WARM, COOL = "#ABB8BB", "#2A3C41", "#E3A77C", "#7FBAB0"
STEPS = (
    ("01", "Document", "2 pages · 18 line items", "Bounded PDF intake"),
    ("02", "Extraction", "Provider output to schema", "Validated data contract"),
    ("03", "Verification", "Independent Decimal math", "USD 125.00 difference"),
    ("04", "Human review", "Flag, inspect, decide", "Original result preserved"),
)


def color(value):
    return tuple(int(value[i : i + 2], 16) for i in (1, 3, 5))


def blend(a, b, amount):
    return tuple(round(x + (y - x) * amount) for x, y in zip(color(a), color(b)))


def frame(progress):
    image = Image.new("RGB", (SIZE[0] * SCALE, SIZE[1] * SCALE), BG)
    draw = ImageDraw.Draw(image)

    def text(x, y, value, size=20, fill=INK, weight=5):
        draw.text(
            (x * SCALE, y * SCALE),
            value,
            font=ImageFont.truetype(FONT, size * SCALE, index=weight),
            fill=fill,
            anchor="lt",
        )

    def line(points, fill=LINE, width=1):
        draw.line(
            [(x * SCALE, y * SCALE) for x, y in points], fill=fill, width=width * SCALE
        )

    text(40, 30, "Folio", 38, weight=0)
    text(158, 42, "/   FROM DOCUMENT TO DECISION", 16, MUTED)
    text(
        40,
        83,
        "A model extracts. Code checks the numbers. A reviewer resolves exceptions.",
        22,
    )

    # A slow traveling signal explains order; the facts remain readable throughout.
    signal = 3 * min(1, max(0, (progress - 0.12) / 0.68))
    visibility = min(1, progress / 0.08, (1 - progress) / 0.08)
    line([(171, 140), (1029, 140)], width=2)
    for center in (314, 600, 886):
        line([(center - 5, 135), (center, 140), (center - 5, 145)], MUTED)
    for index, (number, heading, detail, caption) in enumerate(STEPS):
        left, top = 40 + index * 286, 166
        center = left + 131
        active = max(0, 1 - abs(signal - index)) * visibility
        accent = WARM if index >= 2 else COOL
        outline = blend(LINE, accent, 0.2 + 0.8 * active)
        draw.rounded_rectangle(
            (left * SCALE, top * SCALE, (left + 262) * SCALE, 288 * SCALE),
            radius=12 * SCALE,
            fill=PANEL,
            outline=outline,
            width=SCALE,
        )
        draw.ellipse(
            ((center - 7) * SCALE, 133 * SCALE, (center + 7) * SCALE, 147 * SCALE),
            fill=blend(LINE, accent, 0.2 + 0.8 * active),
        )
        text(left + 18, top + 18, number, 14, accent)
        text(left + 53, top + 15, heading, 24, weight=0)
        text(left + 18, top + 57, detail, 17, INK)
        text(left + 18, top + 88, caption, 16, MUTED)
    x = 171 + signal * 286
    draw.ellipse(
        ((x - 4) * SCALE, 136 * SCALE, (x + 4) * SCALE, 144 * SCALE),
        fill=blend(LINE, INK, visibility),
    )
    line([(40, 313), (1160, 313)])
    text(40, 331, "SYNTHETIC SCENARIO · ARCHITECTURE ILLUSTRATION", 13, MUTED)
    text(662, 328, "$60,283.67 printed  −  $60,158.67 checked  =  $125.00", 18, WARM)
    return image.resize(SIZE, Image.Resampling.LANCZOS)


def render():
    output = ROOT / "assets"
    first = frame(0)
    first.save(output / "folio-pipeline.png", optimize=True)
    palette = first.quantize(colors=96)
    frames = [
        frame(i / 200).quantize(palette=palette, dither=Image.Dither.NONE)
        for i in range(200)
    ]
    destination = output / "folio-pipeline.gif"
    frames[0].save(
        destination,
        save_all=True,
        append_images=frames[1:],
        duration=40,
        loop=0,
        optimize=True,
        disposal=1,
    )
    print(f"{destination.name}: {destination.stat().st_size:,} bytes; 8-second loop")
    render_mobile()


def render_mobile():
    """A narrow static diagram preserves readable labels on small screens."""
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="480" height="648" viewBox="0 0 480 648" role="img" aria-labelledby="title">',
        '<title id="title">Folio architecture: intake, extraction, verification and human review</title>',
        '<rect width="480" height="648" rx="14" fill="#0B1417"/>',
        '<g font-family="Arial,sans-serif">',
        '<text x="28" y="48" fill="#EFE9DC" font-size="32" font-weight="700">Folio</text>',
        '<text x="28" y="79" fill="#ABB8BB" font-size="16">FROM DOCUMENT TO DECISION</text>',
        '<path d="M36 155v349" fill="none" stroke="#35494F" stroke-width="2"/>',
    ]
    for index, (number, heading, detail, caption) in enumerate(STEPS):
        y = 112 + index * 107
        accent = COOL if index < 2 else WARM
        parts.extend(
            [
                f'<rect x="60" y="{y}" width="392" height="94" rx="10" fill="{PANEL}" stroke="{LINE}"/>',
                f'<circle cx="36" cy="{y + 42}" r="6" fill="{accent}"/>',
                f'<text x="77" y="{y + 30}" fill="{accent}" font-size="14">{number}</text>',
                f'<text x="113" y="{y + 30}" fill="{INK}" font-size="22" font-weight="700">{heading}</text>',
                f'<text x="77" y="{y + 57}" fill="{INK}" font-size="17">{detail}</text>',
                f'<text x="77" y="{y + 80}" fill="{MUTED}" font-size="15">{caption}</text>',
            ]
        )
    parts.extend(
        [
            '<text x="28" y="570" fill="#E3A77C" font-size="18">$60,283.67 printed − $60,158.67 checked</text>',
            '<text x="28" y="597" fill="#E3A77C" font-size="20" font-weight="700">USD 125.00 difference → human review</text>',
            '<text x="28" y="629" fill="#ABB8BB" font-size="12">SYNTHETIC SCENARIO · ARCHITECTURE ILLUSTRATION</text>',
            "</g></svg>\n",
        ]
    )
    (ROOT / "assets/folio-pipeline-mobile.svg").write_text("\n".join(parts))


if __name__ == "__main__":
    render()
