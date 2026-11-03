"""Refresh a public-only GitHub profile snapshot using the Python standard library.

Repository metadata and language bytes use GitHub's documented public REST API.
Daily contributions are read anonymously from GitHub's public profile calendar:
they may include private contribution counts the owner has chosen to publicize.
No private repository names, code, or authenticated contribution data are read.
GitHub's calendar HTML is not a versioned API, so changes fail closed rather than
silently replacing missing counts with zero. The previous snapshot stays intact.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import time
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_USERNAME = "YashModi1804"
API_ROOT = "https://api.github.com"
EXCLUDED_LANGUAGES = {"HTML"}
MAX_REPOSITORY_PAGES = 20


class MetricsError(ValueError):
    """A source did not provide a complete, verifiable snapshot."""


def nonnegative_int(value: object, label: str) -> int:
    if type(value) is not int or value < 0:
        raise MetricsError(f"Invalid or missing {label}")
    return value


def fetch(url: str, *, api: bool = False) -> bytes:
    headers = {
        "User-Agent": "YashModi1804-public-profile-metrics",
        "Accept-Language": "en-US",
    }
    if api:
        if not url.startswith(API_ROOT + "/"):
            raise MetricsError("API requests must use api.github.com")
        headers["Accept"] = "application/vnd.github+json"
        headers["X-GitHub-Api-Version"] = "2022-11-28"
        # The workflow's repository token raises the public REST rate limit.
        # It is never used for github.com/profile calendar requests.
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers=headers), timeout=30) as response:
                return response.read()
        except HTTPError as error:
            if error.code in (429, 500, 502, 503, 504) and attempt < 2:
                time.sleep(2**attempt)
                continue
            raise MetricsError(f"GitHub returned HTTP {error.code}") from None
        except (URLError, TimeoutError):
            if attempt < 2:
                time.sleep(2**attempt)
                continue
            raise MetricsError("GitHub request failed after three attempts") from None
    raise MetricsError("GitHub request failed")


def fetch_json(url: str) -> object:
    try:
        return json.loads(fetch(url, api=True))
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise MetricsError("GitHub API returned invalid JSON") from None


def public_repositories(username: str) -> list[dict]:
    repos: list[dict] = []
    seen_ids: set[int] = set()
    for page in range(1, MAX_REPOSITORY_PAGES + 1):
        query = urlencode({"type": "owner", "per_page": 100, "page": page})
        payload = fetch_json(f"{API_ROOT}/users/{username}/repos?{query}")
        if not isinstance(payload, list):
            raise MetricsError("Repository listing is not a list")
        for repo in payload:
            if not isinstance(repo, dict):
                raise MetricsError("Malformed repository metadata")
            if repo.get("private") is not False:
                raise MetricsError("Public repository listing contained nonpublic data")
            if repo.get("owner", {}).get("login", "").casefold() != username.casefold():
                raise MetricsError(
                    "Repository listing contained another owner's repository"
                )
            repo_id = nonnegative_int(repo.get("id"), "repository ID")
            if repo_id in seen_ids:
                raise MetricsError("Repository listing changed during pagination")
            if type(repo.get("fork")) is not bool or not repo.get("name"):
                raise MetricsError("Missing repository identity or fork status")
            nonnegative_int(repo.get("stargazers_count"), "stargazer count")
            seen_ids.add(repo_id)
            repos.append(repo)
        if len(payload) < 100:
            return repos
    raise MetricsError("Repository pagination limit reached; snapshot not updated")


def language_metrics(language_maps: list[dict]) -> dict:
    totals: Counter[str] = Counter()
    for language_map in language_maps:
        if not isinstance(language_map, dict):
            raise MetricsError("Malformed language response")
        for name, value in language_map.items():
            if not isinstance(name, str) or not name:
                raise MetricsError("Invalid language name")
            count = nonnegative_int(value, "language byte count")
            if name not in EXCLUDED_LANGUAGES:
                totals[name] += count
    total_bytes = sum(totals.values())
    items = [
        {"name": name, "bytes": count, "percent": round(count / total_bytes * 100, 1)}
        for name, count in sorted(totals.items(), key=lambda item: (-item[1], item[0]))
        if count > 0
    ]
    return {
        "total_bytes": total_bytes,
        "items": items,
        "excluded": sorted(EXCLUDED_LANGUAGES),
        "scope": "Language bytes in owned public nonfork repositories; HTML excluded. "
        "This measures repository code, not proficiency or time spent.",
    }


class CalendarParser(HTMLParser):
    """Join public day cells to their exact-count accessibility tooltips."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.cells: dict[str, str] = {}
        self.counts: dict[str, int] = {}
        self.tooltips: dict[str, str] = {}
        self.tooltip_target: str | None = None
        self.tooltip_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        day = attributes.get("data-date")
        if day:
            try:
                date.fromisoformat(day)
            except ValueError:
                raise MetricsError("Calendar contains an invalid date") from None
            cell_id = attributes.get("id")
            if cell_id:
                if cell_id in self.cells:
                    raise MetricsError("Calendar contains duplicate day IDs")
                self.cells[cell_id] = day
            raw_count = attributes.get("data-count")
            if raw_count is not None:
                if not raw_count.isdigit():
                    raise MetricsError(
                        "Calendar contains an invalid contribution count"
                    )
                self.add_count(day, int(raw_count))
        if tag == "tool-tip":
            self.tooltip_target = attributes.get("for")
            self.tooltip_text = []

    def handle_data(self, text: str) -> None:
        if self.tooltip_target is not None:
            self.tooltip_text.append(text)

    def handle_endtag(self, tag: str) -> None:
        if tag == "tool-tip" and self.tooltip_target is not None:
            target = self.tooltip_target
            if target in self.tooltips:
                raise MetricsError("Calendar contains duplicate contribution tooltips")
            self.tooltips[target] = " ".join("".join(self.tooltip_text).split())
            self.tooltip_target = None
            self.tooltip_text = []

    def add_count(self, day: str, count: int) -> None:
        if day in self.counts and self.counts[day] != count:
            raise MetricsError("Calendar contains conflicting contribution counts")
        self.counts[day] = count

    def result(self) -> dict[str, int]:
        for cell_id, day in self.cells.items():
            tooltip = self.tooltips.get(cell_id)
            if tooltip is None:
                if day in self.counts:
                    continue
                raise MetricsError("Calendar is missing a contribution tooltip")
            match = re.match(r"^(No|[0-9][0-9,]*) contributions? on ", tooltip)
            if match is None:
                raise MetricsError("Calendar contribution tooltip format changed")
            value = match.group(1)
            self.add_count(day, 0 if value == "No" else int(value.replace(",", "")))
        if not self.counts:
            raise MetricsError("GitHub returned no public contribution calendar")
        return self.counts


def parse_calendar(html: str) -> dict[str, int]:
    parser = CalendarParser()
    parser.feed(html)
    parser.close()
    return parser.result()


def contribution_metrics(counts: dict[str, int], start: date, end: date) -> dict:
    if start > end:
        raise MetricsError("Contribution period is reversed")
    days = []
    current = start
    longest = running = 0
    while current <= end:
        day = current.isoformat()
        if day not in counts:
            raise MetricsError(f"Contribution calendar is missing {day}")
        count = nonnegative_int(counts[day], "daily contribution count")
        days.append({"date": day, "count": count})
        running = running + 1 if count > 0 else 0
        longest = max(longest, running)
        current += timedelta(days=1)

    # An unfinished current day does not break a streak active yesterday.
    index = len(days) - 1
    if days[index]["count"] == 0:
        index -= 1
    streak = 0
    while index >= 0 and days[index]["count"] > 0:
        streak += 1
        index -= 1
    return {
        "total": sum(day["count"] for day in days),
        "current_streak": streak,
        "longest_streak": longest,
        "active_days": sum(day["count"] > 0 for day in days),
        "days": days,
        "scope": "Counts visible on the anonymous public GitHub profile, which may include "
        "anonymized private activity the owner chooses to share; not a commit count.",
        "streak_rule": "Consecutive calendar days with at least one profile contribution. "
        "Current streak may end today or yesterday. Streaks are bounded by this snapshot's "
        "365-day window; today is the UTC snapshot date and day counts are supplied by GitHub.",
    }


def collect(username: str, now: datetime) -> dict:
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", username):
        raise MetricsError("Invalid GitHub username")
    end = now.astimezone(timezone.utc).date()
    start = end - timedelta(days=364)
    repos = public_repositories(username)
    originals = [repo for repo in repos if not repo["fork"]]
    language_maps = []
    for repo in originals:
        name = quote(repo["name"], safe="")
        language_maps.append(
            fetch_json(f"{API_ROOT}/repos/{username}/{name}/languages")
        )

    counts: dict[str, int] = {}
    calendar_urls = []
    # GitHub serves a complete calendar year for these public calendar requests.
    for year in range(start.year, end.year + 1):
        query = urlencode({"from": f"{year}-01-01", "to": f"{year}-12-31"})
        url = f"https://github.com/users/{username}/contributions?{query}"
        calendar_urls.append(url)
        calendar = parse_calendar(fetch(url).decode("utf-8"))
        for day, count in calendar.items():
            if day in counts and counts[day] != count:
                raise MetricsError("Public calendar changed during collection")
            counts[day] = count

    contributions = contribution_metrics(counts, start, end)
    contributions["source"] = "GitHub anonymous public contribution calendar"
    return {
        "schema_version": 1,
        "username": username,
        "generated_at": now.astimezone(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "period": {"from": start.isoformat(), "to": end.isoformat(), "days": 365},
        "repositories": {
            "public": len(repos),
            "original": len(originals),
            "stars": sum(repo["stargazers_count"] for repo in originals),
            "scope": "Owned public repositories, including forks; originals and earned stars exclude forks.",
        },
        "contributions": contributions,
        "languages": language_metrics(language_maps),
        "sources": {
            "repositories": f"{API_ROOT}/users/{username}/repos?type=owner",
            "calendar": calendar_urls,
            "documentation": [
                "https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user",
                "https://docs.github.com/en/rest/repos/repos#list-repository-languages",
                "https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference",
            ],
        },
    }


def write_snapshot(snapshot: dict, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    contents = json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n"
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=destination.parent, delete=False
        ) as file:
            temporary = Path(file.name)
            file.write(contents)
        temporary.replace(destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default=DEFAULT_USERNAME)
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "activity.json")
    args = parser.parse_args()
    try:
        snapshot = collect(args.username, datetime.now(timezone.utc))
        write_snapshot(snapshot, args.output)
    except (MetricsError, OSError, UnicodeDecodeError) as error:
        print(
            f"Profile refresh failed; previous snapshot preserved: {error}",
            file=sys.stderr,
        )
        return 1
    print(
        f"Updated public profile snapshot for {args.username} through {snapshot['period']['to']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
