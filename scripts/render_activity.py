"""Render public profile metrics without external widgets, fonts or dependencies."""

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEMES = {
    "light": ("#F4EEE4", "#222A2C", "#706F66", "#D8CDBB"),
    "dark": ("#0B1417", "#EFE9DC", "#AFA99C", "#334044"),
}
COLORS = ["#D68A5E", "#82A19A", "#B9A777", "#879DAE", "#AC8F9E", "#9BA17F", "#99968E"]


def render(data, theme):
    background, ink, muted, line = THEMES[theme]
    repo, activity = data["repositories"], data["contributions"]
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="640" viewBox="0 0 1200 640" role="img" aria-labelledby="title desc">',
        '<title id="title">Yash Modi — the activity ledger</title>',
        f'<desc id="desc">{activity["total"]} profile contributions over 365 days; {repo["public"]} public repositories; {repo["stars"]} stars on original public repositories. Current streak {activity["current_streak"]} days; best streak in this window {activity["longest_streak"]} days.</desc>',
        f'<rect width="1200" height="640" fill="{background}"/>',
        f'<g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif" fill="{ink}">',
    ]

    def text(x, y, value, size=18, color=ink, weight=400, extra=""):
        out.append(
            f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{escape(str(value))}</text>'
        )

    def rule(x1, y, x2):
        out.append(f'<path d="M{x1} {y}H{x2}" stroke="{line}"/>')

    text(48, 48, "THE ACTIVITY LEDGER", 15, muted, 600, 'letter-spacing="2"')
    text(
        1152,
        48,
        f"AS OF {data['generated_at'][:10]}",
        15,
        muted,
        500,
        'text-anchor="end"',
    )
    rule(48, 72, 1152)
    metrics = [
        (48, activity["total"], "Profile contributions", "last 365 days"),
        (
            432,
            repo["public"],
            "Public repositories",
            f"{repo['original']} original · {repo['public'] - repo['original']} forks",
        ),
        (816, repo["stars"], "Stars earned", "original public repositories"),
    ]
    for x, value, label, note in metrics:
        text(x, 161, f"{value:,}", 72, ink, 600, 'letter-spacing="-3"')
        text(x, 199, label, 21, ink, 500)
        text(x, 227, note, 16, muted)
    rule(48, 259, 1152)
    text(48, 297, "CONTINUITY", 15, muted, 600, 'letter-spacing="2"')
    text(48, 336, f"{activity['current_streak']} day current streak", 23, ink, 500)
    text(48, 371, f"{activity['longest_streak']} day best streak · 365d", 19, muted)
    text(48, 401, f"{activity['active_days']} active days in this window", 16, muted)
    days = activity["days"]
    weeks = [
        sum(day["count"] for day in days[i : i + 7]) for i in range(0, len(days), 7)
    ]
    maximum = max(weeks) or 1
    for index, count in enumerate(weeks):
        height = 3 if count == 0 else max(7, 100 * count / maximum)
        x = 435 + index * 13.45
        out.append(
            f'<rect x="{x:.2f}" y="{402 - height:.2f}" width="8" height="{height:.2f}" rx="2" fill="{COLORS[0] if count else line}"/>'
        )
    text(432, 291, "Contributions per week", 16, muted)
    text(432, 430, data["period"]["from"], 13, muted)
    text(1152, 430, data["period"]["to"], 13, muted, extra='text-anchor="end"')
    rule(48, 455, 1152)
    text(48, 494, "LANGUAGE MIX", 15, muted, 600, 'letter-spacing="2"')
    text(
        1152,
        494,
        "Public source bytes · forks & HTML excluded",
        15,
        muted,
        extra='text-anchor="end"',
    )
    x = 48
    languages = data["languages"]["items"]
    if len(languages) > 8:
        languages = languages[:7] + [
            {"name": "Other", "bytes": sum(item["bytes"] for item in languages[7:])}
        ]
    total = data["languages"]["total_bytes"] or 1
    for index, item in enumerate(languages):
        width = item["bytes"] / total * 1104
        out.append(
            f'<rect x="{x:.3f}" y="518" width="{width:.3f}" height="14" fill="{COLORS[index % len(COLORS)]}"/>'
        )
        x += width
    for index, item in enumerate(languages):
        x, y = 48 + (index % 4) * 282, 565 + (index // 4) * 30
        percent = item["bytes"] / total * 100
        label = f"{percent:.1f}%" if percent >= 0.1 else "<0.1%"
        out.append(
            f'<circle cx="{x + 4}" cy="{y - 5}" r="4" fill="{COLORS[index % len(COLORS)]}"/>'
        )
        text(x + 17, y, f"{item['name']}  {label}", 16, ink)
    out.append("</g></svg>")
    return "\n".join(out)


if __name__ == "__main__":
    data = json.loads((ROOT / "data/activity.json").read_text())
    (ROOT / "assets").mkdir(exist_ok=True)
    for theme in THEMES:
        (ROOT / f"assets/activity-{theme}.svg").write_text(render(data, theme))
