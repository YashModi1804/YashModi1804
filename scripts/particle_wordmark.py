"""Deterministic, bounded nano-particle choreography for Yash's wordmark."""

import math
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter


def ease(value):
    value = min(1.0, max(0.0, value))
    return value * value * (3.0 - 2.0 * value)


def scatter_at(phase):
    """Hold, disassemble, flow, reform, hold; the loop seam is a long still hold."""
    progress = (phase / math.tau) % 1.0
    if progress < 0.18 or progress >= 0.73:
        return 0.0
    if progress < 0.34:
        return ease((progress - 0.18) / 0.16)
    if progress < 0.43:
        return 1.0
    return 1.0 - ease((progress - 0.43) / 0.30)


class ParticleWordmark:
    """A pixel mask plus seeded trajectories; no per-frame random variation.

    Quadratic Bezier paths stay inside the convex hull of their control points.
    Top/bottom strip bounds protect the static role, quote, O and learning labels.
    Coherent undulation stays inside an additional safety margin.
    """

    def __init__(self, mask, scale=2, count=4500):
        self.mask = mask
        self.scale = scale
        width, height = mask.width // scale, mask.height // scale
        source = mask.resize((width, height), Image.Resampling.LANCZOS)
        pixels = source.load()
        rng = random.Random(1804)

        # Soft, fixed material variation makes the solid letters disassemble in
        # small patches. A continuous threshold avoids binary sparkle/flicker.
        noise = Image.new("L", (max(1, width // 11), max(1, height // 11)))
        noise.putdata(
            [rng.randrange(30, 226) for _ in range(noise.width * noise.height)]
        )
        self.field = noise.resize(mask.size, Image.Resampling.BICUBIC).filter(
            ImageFilter.GaussianBlur(3 * scale)
        )
        field_small = self.field.resize((width, height), Image.Resampling.LANCZOS)

        self.particles = []
        while len(self.particles) < count:
            x, y = rng.uniform(38, 1120), rng.uniform(91, 548)
            if pixels[int(x), int(y)] < 220:
                continue
            bounds = (40, 830, 80, 307) if y < 310 else (42, 1146, 322, 561)
            left, right, top, bottom = bounds
            # Three curved material streams flow around the continuous bronze O.
            # Their shaped boundaries avoid rectangular random-noise plumes.
            if y < 310:
                u, v = (x - 38) / 720, (y - 91) / 209
                dest_x = 45 + u * 770 + rng.uniform(-8, 8)
                dest_y = (
                    193
                    + 52 * math.sin(u * math.tau * 1.1 + 0.2)
                    + (v - 0.5) * 70
                    + rng.uniform(-6, 6)
                )
            elif x < 360:
                u, v = (x - 63) / 240, (y - 337) / 211
                dest_x = 50 + u * 275 + rng.uniform(-8, 8)
                dest_y = (
                    425
                    + 45 * math.sin(u * math.pi + 0.2)
                    + (v - 0.5) * 78
                    + rng.uniform(-6, 6)
                )
            else:
                u, v = (x - 754) / 351, (y - 337) / 211
                dest_x = 735 + u * 390 + rng.uniform(-8, 8)
                dest_y = (
                    423
                    + 53 * math.sin(u * math.tau * 0.9 + 0.4)
                    + (v - 0.5) * 78
                    + rng.uniform(-6, 6)
                )
            dest_x = min(right - 5, max(left + 5, dest_x))
            dest_y = min(bottom - 5, max(top + 5, dest_y))
            control_x = min(
                right - 5, max(left + 5, (x + dest_x) / 2 + rng.uniform(-34, 34))
            )
            control_y = min(
                bottom - 5, max(top + 5, (y + dest_y) / 2 + rng.uniform(-40, 40))
            )
            self.particles.append(
                (
                    x,
                    y,
                    control_x,
                    control_y,
                    dest_x,
                    dest_y,
                    rng.uniform(0.65, 1.65),
                    rng.random(),
                    rng.uniform(0, math.tau),
                    field_small.getpixel((int(x), int(y))),
                    rng.uniform(0.65, 1.0),
                )
            )

    def draw(self, image, phase, palette):
        amount = scatter_at(phase)
        if amount <= 0:
            image.paste(palette["ink"], (0, 0), self.mask)
            return

        threshold = -35 + amount * 650
        lookup = [
            round(255 * ease((value - threshold + 28) / 56)) for value in range(256)
        ]
        solid = ImageChops.multiply(self.mask, self.field.point(lookup))
        image.paste(palette["ink"], (0, 0), solid)

        def rgb(value):
            return tuple(int(value[i : i + 2], 16) for i in (1, 3, 5))

        background, ink, accent = (
            rgb(palette[key]) for key in ("background", "ink", "accent")
        )
        draw = ImageDraw.Draw(image)
        inv = 1 - amount
        drift = amount * amount
        for (
            x,
            y,
            cx,
            cy,
            dx,
            dy,
            radius,
            tint,
            seed_phase,
            field,
            strength,
        ) in self.particles:
            # The particle fades in where its corresponding patch of solid type
            # recedes; color and radius remain deterministic throughout the loop.
            visibility = 1 - ease((field - threshold + 35) / 70)
            if visibility < 0.005:
                continue
            px = inv * inv * x + 2 * inv * amount * cx + amount * amount * dx
            py = inv * inv * y + 2 * inv * amount * cy + amount * amount * dy
            px += drift * (5 * math.sin(phase * 2 + x / 125) + math.sin(seed_phase))
            py += drift * (7 * math.sin(phase * 2 + x / 95) + math.cos(seed_phase))
            target = accent if tint > 0.65 else ink
            alpha = visibility * strength
            color = tuple(
                round(a + (b - a) * alpha) for a, b in zip(background, target)
            )
            radius *= self.scale
            px, py = px * self.scale, py * self.scale
            draw.ellipse(
                (px - radius, py - radius, px + radius, py + radius), fill=color
            )
