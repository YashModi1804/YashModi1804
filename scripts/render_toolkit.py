"""Build self-contained profile toolkit panels from pinned, local logo sources.

Uses only the standard library. Icon source revisions and licenses are retained in
assets/icons; the generated SVGs contain their vector paths, never remote images.
"""

import re
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")

BACKGROUND = "#0B1417"
PANEL = "#111E23"
INK = "#EFE9DC"
MUTED = "#AFA99C"
LINE = "#2C3D43"
ACCENT = "#DF9668"
PLATE = "#F2EDE4"
FONT = "-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif"


def text(x, y, value, size=18, fill=INK, weight=500, spacing=None):
    tracking = f' letter-spacing="{spacing}"' if spacing is not None else ""
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-family="{FONT}" '
        f'font-size="{size}" font-weight="{weight}"{tracking}>{escape(value)}</text>'
    )


def icon(key, x, y, size=34, prefix="icon"):
    """Inline trusted local paths and isolate gradient/clip identifiers."""
    source = ASSETS / "icons" / f"{key}.svg"
    root = ET.fromstring(source.read_text())
    if root.tag != f"{{{SVG_NS}}}svg":
        raise ValueError(f"Not an SVG: {source.name}")
    ids = {
        element.attrib["id"]: f"{prefix}-{key}-{element.attrib['id']}"
        for element in root.iter()
        if "id" in element.attrib
    }
    for element in root.iter():
        name = element.tag.rsplit("}", 1)[-1]
        if name in {"script", "foreignObject", "image", "a", "animate", "set"}:
            raise ValueError(
                f"Unexpected active or external SVG content in {source.name}"
            )
        for attribute, value in list(element.attrib.items()):
            if attribute.lower().startswith("on"):
                raise ValueError(f"Unexpected event attribute in {source.name}")
            if attribute == "id":
                element.set(attribute, ids[value])
                continue
            if attribute.rsplit("}", 1)[-1] == "href" and not value.startswith("#"):
                raise ValueError(f"External reference in {source.name}")
            for old, new in ids.items():
                value = value.replace(f"url(#{old})", f"url(#{new})")
                if value == f"#{old}":
                    value = f"#{new}"
            element.set(attribute, value)
        if name == "style":
            raise ValueError(f"Unscoped CSS in {source.name}")
    left, top, width, height = map(float, root.attrib.pop("viewBox").split())
    scale = size / max(width, height)
    offset_x = x + (size - width * scale) / 2
    offset_y = y + (size - height * scale) / 2
    for attribute in ("x", "y", "width", "height", "preserveAspectRatio", "version"):
        root.attrib.pop(attribute, None)
    root.tag = f"{{{SVG_NS}}}g"
    root.set("color", "#222A2C")
    wrapper = ET.Element(
        f"{{{SVG_NS}}}g",
        {
            "transform": f"translate({offset_x:g} {offset_y:g}) scale({scale:g}) translate({-left:g} {-top:g})"
        },
    )
    wrapper.append(root)
    return ET.tostring(wrapper, encoding="unicode")


def item(key, label, x, y, prefix):
    return "\n".join(
        (
            f'<rect x="{x}" y="{y}" width="50" height="50" rx="13" fill="{PLATE}"/>',
            icon(key, x + 8, y + 8, prefix=prefix),
            text(x + 64, y + 31, label, 18, weight=500),
        )
    )


def frame(width, height, title, description):
    return [
        (
            f'<svg xmlns="{SVG_NS}" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
        ),
        f'<title id="title">{escape(title)}</title>',
        f'<desc id="desc">{escape(description)}</desc>',
        (
            f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" '
            f'rx="20" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/>'
        ),
    ]


def card(number, title, groups, filename):
    description = "; ".join(
        f"{name}: {', '.join(label for _, label in members)}"
        for name, members in groups
    )
    out = frame(480, 490, title, description)
    out.extend(
        (
            text(28, 37, f"{number} / TOOLKIT", 12, ACCENT, 600, 2),
            text(28, 77, title, 27, weight=600),
            f'<path d="M28 100H452" stroke="{LINE}"/>',
        )
    )
    for index, (name, members) in enumerate(groups):
        top = 133 + index * 179
        out.append(text(28, top, name.upper(), 12, MUTED, 600, 1.7))
        for item_index, (key, label) in enumerate(members):
            x = 28 + item_index % 2 * 226
            y = top + 20 + item_index // 2 * 67
            out.append(item(key, label, x, y, filename))
        if index == 0:
            out.append(f'<path d="M28 284H452" stroke="{LINE}"/>')
    out.append("</svg>")
    (ASSETS / f"{filename}.svg").write_text("\n".join(out) + "\n")


def project_strip():
    title = "Folio · project stack"
    members = (
        ("python", "Python"),
        ("fastapi", "FastAPI"),
        ("pydantic", "Pydantic"),
        ("postgresql", "PostgreSQL"),
        ("docker", "Docker"),
    )
    out = frame(
        960,
        186,
        title,
        "Technologies used in Folio's invoice-verification engine: "
        + ", ".join(label for _, label in members)
        + ". This identifies project technologies, not proficiency levels.",
    )
    out.extend(
        (
            text(28, 42, title, 25, weight=600),
            text(
                28,
                69,
                "Technologies used in the invoice-verification engine.",
                15,
                MUTED,
            ),
            f'<path d="M28 86H932" stroke="{LINE}"/>',
        )
    )
    for index, (key, label) in enumerate(members):
        out.append(item(key, label, 28 + index * 188, 108, "toolkit-project"))
    out.append("</svg>")
    (ASSETS / "toolkit-project.svg").write_text("\n".join(out) + "\n")


def project_mobile():
    title = "Folio · project stack"
    members = (
        ("python", "Python", 80, 107),
        ("fastapi", "FastAPI", 240, 107),
        ("pydantic", "Pydantic", 400, 107),
        ("postgresql", "PostgreSQL", 160, 218),
        ("docker", "Docker", 320, 218),
    )
    out = frame(
        480,
        340,
        title,
        "Folio project technologies: Python, FastAPI, Pydantic, PostgreSQL, Docker.",
    )
    out.extend(
        (
            text(28, 42, title, 25, weight=600),
            text(28, 69, "Invoice-verification engine", 15, MUTED),
            f'<path d="M28 86H452" stroke="{LINE}"/>',
        )
    )
    for key, label, center, top in members:
        out.append(
            f'<rect x="{center - 25}" y="{top}" width="50" height="50" '
            f'rx="13" fill="{PLATE}"/>'
        )
        out.append(icon(key, center - 17, top + 8, prefix="toolkit-project-mobile"))
        out.append(
            text(center, top + 77, label, 18).replace(
                "<text ", '<text text-anchor="middle" ', 1
            )
        )
    out.append("</svg>")
    (ASSETS / "toolkit-project-mobile.svg").write_text("\n".join(out) + "\n")


def validate_outputs():
    for path in ASSETS.glob("toolkit-*.svg"):
        source = path.read_text()
        root = ET.fromstring(source)
        ids = [
            element.attrib["id"] for element in root.iter() if "id" in element.attrib
        ]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate SVG identifier in {path.name}")
        if re.search(r"<(?:image|script|foreignObject)\b", source):
            raise ValueError(f"Unexpected external or active content in {path.name}")
        print(f"{path.name}: {path.stat().st_size:,} bytes, embedded vectors only")


if __name__ == "__main__":
    card(
        "01",
        "Code & interface",
        (
            (
                "Languages",
                (
                    ("c", "C"),
                    ("cplusplus", "C++"),
                    ("javascript", "JavaScript"),
                    ("typescript", "TypeScript"),
                ),
            ),
            ("Interface", (("react", "React"), ("html5", "HTML"), ("css3", "CSS"))),
        ),
        "toolkit-code",
    )
    card(
        "02",
        "Server & workflow",
        (
            (
                "Server & data",
                (
                    ("nodejs", "Node.js"),
                    ("express", "Express"),
                    ("mongodb", "MongoDB"),
                    ("mysql", "MySQL"),
                ),
            ),
            ("Workflow", (("git", "Git"), ("github", "GitHub"), ("vscode", "VS Code"))),
        ),
        "toolkit-systems",
    )
    project_strip()
    project_mobile()
    validate_outputs()
