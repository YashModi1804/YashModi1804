"""Deterministic decorative particles that disperse and reassemble a text mask.

This is a designed animation, not a physical nanoparticle simulation.
"""

import math
import random
from dataclasses import dataclass

from PIL import Image, ImageChops, ImageDraw, ImageFilter


def ease(value):
    value = min(1.0, max(0.0, value))
    return value * value * (3.0 - 2.0 * value)


def scatter_at(phase):
    progress = (phase / math.tau) % 1.0
    if progress < 0.16 or progress >= 0.78:
        return 0.0
    if progress < 0.31:
        return ease((progress - 0.16) / 0.15)
    if progress < 0.48:
        return 1.0
    return 1.0 - ease((progress - 0.48) / 0.30)


@dataclass(frozen=True)
class Particle:
    x: float
    y: float
    cx: float
    cy: float
    dx: float
    dy: float
    radius: float
    tint: float
    phase: float
    field: int
    strength: float
    delay: float


class ParticleWordmark:
    """All glyph pixels, including the o in Modi, follow the same choreography.

    Destinations are independently sampled in a wide ellipse. They have no
    positional relationship to source letters, so the name disappears completely
    at maximum dispersion. Fixed paths and low-frequency drifting prevent jitter.
    """

    def __init__(self, mask, scale=2, count=3000):
        self.mask, self.scale = mask, scale
        width, height = mask.width // scale, mask.height // scale
        source = mask.resize((width, height), Image.Resampling.LANCZOS)
        pixels = source.load()
        left, top, right, bottom = source.getbbox()
        rng = random.Random(1804)

        noise = Image.new("L", (max(1, width // 8), max(1, height // 8)))
        noise.putdata(
            [rng.randrange(30, 226) for _ in range(noise.width * noise.height)]
        )
        self.field = noise.resize(mask.size, Image.Resampling.BICUBIC).filter(
            ImageFilter.GaussianBlur(2 * scale)
        )
        field_small = self.field.resize((width, height), Image.Resampling.LANCZOS)

        self.particles = []
        while len(self.particles) < count:
            x, y = rng.uniform(left, right - 1), rng.uniform(top, bottom - 1)
            if pixels[int(x), int(y)] < 220:
                continue
            # Uniform independent points in a broad ellipse: no source-coordinate
            # terms appear in these destination equations.
            angle, radius = rng.uniform(0, math.tau), math.sqrt(rng.random())
            dx = 600 + 515 * radius * math.cos(angle)
            dy = 164 + 82 * radius * math.sin(angle)
            cx = min(1125, max(75, (x + dx) / 2 + rng.uniform(-85, 85)))
            cy = min(247, max(81, (y + dy) / 2 + rng.uniform(-58, 58)))
            self.particles.append(
                Particle(
                    x,
                    y,
                    cx,
                    cy,
                    dx,
                    dy,
                    rng.uniform(0.65, 1.65),
                    rng.random(),
                    rng.uniform(0, math.tau),
                    field_small.getpixel((int(x), int(y))),
                    rng.uniform(0.65, 1.0),
                    rng.uniform(0, 0.14),
                )
            )

    def draw(self, image, phase, palette):
        amount = scatter_at(phase)
        if amount <= 0:
            image.paste(palette["ink"], (0, 0), self.mask)
            return

        threshold = amount * 370
        lookup = [
            round(255 * ease((value - threshold + 24) / 48)) for value in range(256)
        ]
        solid = ImageChops.multiply(self.mask, self.field.point(lookup))
        image.paste(palette["ink"], (0, 0), solid)

        def rgb(value):
            return tuple(int(value[i : i + 2], 16) for i in (1, 3, 5))

        background, ink, accent = (
            rgb(palette[key]) for key in ("background", "ink", "accent")
        )
        draw = ImageDraw.Draw(image)
        for p in self.particles:
            visibility = 1 - ease((p.field - threshold + 30) / 60)
            if visibility < 0.005:
                continue
            travel = ease((amount - p.delay) / (1 - p.delay))
            inv = 1 - travel
            px = inv * inv * p.x + 2 * inv * travel * p.cx + travel * travel * p.dx
            py = inv * inv * p.y + 2 * inv * travel * p.cy + travel * travel * p.dy
            # Loose independent drifting only becomes strong in the dispersed
            # cloud; it vanishes exactly when a particle reaches its source glyph.
            drift = travel * travel
            px += 18 * drift * math.sin(phase * 2 + p.phase)
            py += 9 * drift * math.cos(phase * 2 + p.phase)
            target = accent if p.tint > 0.82 else ink
            alpha = visibility * p.strength
            color = tuple(
                round(a + (b - a) * alpha) for a, b in zip(background, target)
            )
            radius = p.radius * self.scale
            px, py = px * self.scale, py * self.scale
            draw.ellipse(
                (px - radius, py - radius, px + radius, py + radius), fill=color
            )
