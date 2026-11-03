"""Small self-contained SVGs for project navigation and contact links."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def render():
    assets = ROOT / "assets"
    for filename, label, width, icon in (
        (
            "contact-email.svg",
            "Email me",
            150,
            '<rect x="18" y="14" width="20" height="15" rx="2"/><path d="m18 15 10 8 10-8"/>',
        ),
        (
            "contact-linkedin.svg",
            "LinkedIn",
            148,
            '<circle cx="27" cy="16" r="4"/><path d="M19 31v-3a8 8 0 0 1 16 0v3"/>',
        ),
        (
            "contact-questions.svg",
            "Ask a question",
            192,
            '<path d="M19 14h20v14H28l-7 5v-5h-2z"/><path d="M24 19h10M24 23h7"/>',
        ),
    ):
        (assets / filename).write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="44" viewBox="0 0 {width} 44">'
            f'<rect x=".5" y=".5" width="{width - 1}" height="43" rx="8" fill="#132126" stroke="#35494F"/>'
            f'<g fill="none" stroke="#E3A77C" stroke-width="1.5" stroke-linejoin="round">{icon}</g>'
            f'<text x="49" y="28" fill="#EFE9DC" font-family="Arial,sans-serif" font-size="15">{label}</text>'
            "</svg>\n"
        )

    (
        assets / "scholarship-workflow.svg"
    ).write_text("""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="264" viewBox="0 0 1200 264" role="img" aria-labelledby="title desc">
  <title id="title">Scholarship workflow — React, Express and MongoDB</title>
  <desc id="desc">Source-backed project overview: student and administrative screens connected to staged verification records. Architecture illustration, not a product screenshot.</desc>
  <rect width="1200" height="264" rx="16" fill="#0B1417"/>
  <g font-family="Arial,sans-serif">
    <text x="40" y="43" font-size="14" letter-spacing="2" fill="#E3A77C">MORE OF MY WORK / 02</text>
    <text x="40" y="95" font-size="34" font-weight="700" fill="#EFE9DC">Scholarship workflow</text>
    <text x="40" y="134" font-size="20" fill="#ABB8BB">Student and admin screens.</text>
    <text x="40" y="163" font-size="20" fill="#ABB8BB">Staged verification records.</text>
    <text x="40" y="221" font-size="16" fill="#7FBAB0">React  /  Node.js  /  Express  /  MongoDB</text>
    <g fill="#111E22" stroke="#2A3C41">
      <rect x="635" y="38" width="184" height="67" rx="9"/>
      <rect x="635" y="159" width="184" height="67" rx="9"/>
      <rect x="927" y="99" width="235" height="67" rx="9"/>
    </g>
    <g fill="#EFE9DC" font-size="20">
      <text x="661" y="79">Student views</text>
      <text x="663" y="200">Admin views</text>
      <text x="949" y="139">Verification records</text>
    </g>
    <path d="M819 71h45v61h63M819 192h45v-60M917 126l10 6-10 6" fill="none" stroke="#7FBAB0" stroke-width="2"/>
    <circle cx="864" cy="132" r="5" fill="#E3A77C"/>
    <text x="927" y="195" font-size="13" letter-spacing="1" fill="#ABB8BB">SCREENS + DATA MODEL</text>
  </g>
</svg>
""")


if __name__ == "__main__":
    render()
