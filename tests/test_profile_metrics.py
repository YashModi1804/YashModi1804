"""Offline boundary and source-validation tests. No GitHub requests are made."""

import importlib.util
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch

SPEC = importlib.util.spec_from_file_location(
    "profile_metrics",
    Path(__file__).resolve().parents[1] / "scripts" / "profile_metrics.py",
)
metrics = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(metrics)


class ContributionTests(unittest.TestCase):
    def summarize(self, values, start=date(2025, 12, 29)):
        from datetime import timedelta

        days = {
            (start + timedelta(days=i)).isoformat(): count
            for i, count in enumerate(values)
        }
        return metrics.contribution_metrics(
            days, start, start + timedelta(days=len(values) - 1)
        )

    def test_zero_today_keeps_yesterday_streak_across_year(self):
        result = self.summarize([0, 2, 1, 3, 0])
        self.assertEqual(
            (result["total"], result["current_streak"], result["longest_streak"]),
            (6, 3, 3),
        )
        self.assertEqual(result["active_days"], 3)

    def test_two_inactive_days_break_current_streak(self):
        result = self.summarize([1, 4, 0, 0])
        self.assertEqual((result["current_streak"], result["longest_streak"]), (0, 2))

    def test_current_day_counts_and_longest_does_not_bridge_gap(self):
        result = self.summarize([2, 3, 1, 0, 4, 5])
        self.assertEqual((result["current_streak"], result["longest_streak"]), (2, 3))

    def test_empty_activity_and_one_day_window(self):
        self.assertEqual(self.summarize([0])["current_streak"], 0)
        self.assertEqual(self.summarize([7])["current_streak"], 1)

    def test_leap_day_is_consecutive(self):
        result = self.summarize([1, 1, 1], date(2024, 2, 28))
        self.assertEqual(result["days"][1]["date"], "2024-02-29")
        self.assertEqual(result["longest_streak"], 3)

    def test_missing_day_never_becomes_zero(self):
        with self.assertRaises(metrics.MetricsError):
            metrics.contribution_metrics(
                {"2026-01-01": 1}, date(2026, 1, 1), date(2026, 1, 2)
            )

    def test_invalid_counts_are_rejected(self):
        for value in (None, -1, "2", True):
            with self.subTest(value=value), self.assertRaises(metrics.MetricsError):
                self.summarize([value])


class CalendarTests(unittest.TestCase):
    def test_tooltips_join_by_id_not_document_order(self):
        html = """<td data-date="2026-01-02" id="b"></td><td id="a" data-date="2026-01-01"></td>
        <tool-tip for="a">1,234 contributions on January 1st.</tool-tip>
        <tool-tip for="b">No contributions on January 2nd.</tool-tip>"""
        self.assertEqual(
            metrics.parse_calendar(html), {"2026-01-01": 1234, "2026-01-02": 0}
        )

    def test_legacy_explicit_count_is_supported(self):
        self.assertEqual(
            metrics.parse_calendar('<rect data-date="2026-01-01" data-count="5"/>'),
            {"2026-01-01": 5},
        )

    def test_missing_or_changed_markup_fails_closed(self):
        for html in (
            "<html>Please sign in</html>",
            '<td id="a" data-date="2026-01-01"></td>',
            '<td id="a" data-date="2026-01-01"></td><tool-tip for="a">Unexpected format</tool-tip>',
        ):
            with self.subTest(html=html), self.assertRaises(metrics.MetricsError):
                metrics.parse_calendar(html)

    def test_conflicting_counts_are_rejected(self):
        html = """<td id="a" data-date="2026-01-01" data-count="4"></td>
        <tool-tip for="a">3 contributions on January 1st.</tool-tip>"""
        with self.assertRaises(metrics.MetricsError):
            metrics.parse_calendar(html)


class LanguageTests(unittest.TestCase):
    def test_sum_bytes_before_computing_shares_and_exclude_html(self):
        result = metrics.language_metrics(
            [
                {"Python": 150, "HTML": 1000, "C++": 50},
                {"C++": 100, "JavaScript": 300},
            ]
        )
        self.assertEqual(result["total_bytes"], 600)
        self.assertEqual(
            result["items"],
            [
                {"name": "JavaScript", "bytes": 300, "percent": 50.0},
                {"name": "C++", "bytes": 150, "percent": 25.0},
                {"name": "Python", "bytes": 150, "percent": 25.0},
            ],
        )

    def test_empty_language_response_is_valid_but_missing_is_not(self):
        self.assertEqual(metrics.language_metrics([{}])["items"], [])
        with self.assertRaises(metrics.MetricsError):
            metrics.language_metrics([None])

    def test_invalid_language_bytes_are_rejected(self):
        with self.assertRaises(metrics.MetricsError):
            metrics.language_metrics([{"Python": None}])


class RepositoryTests(unittest.TestCase):
    def test_private_data_never_accepted(self):
        with (
            patch.object(metrics, "fetch_json", return_value=[{"private": True}]),
            self.assertRaises(metrics.MetricsError),
        ):
            metrics.public_repositories("example")

    def test_another_owners_repository_never_accepted(self):
        with (
            patch.object(
                metrics,
                "fetch_json",
                return_value=[{"private": False, "owner": {"login": "other"}}],
            ),
            self.assertRaises(metrics.MetricsError),
        ):
            metrics.public_repositories("example")


class RefreshSafetyTests(unittest.TestCase):
    def test_public_calendar_request_never_uses_api_token(self):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = b"calendar"
        with (
            patch.dict(metrics.os.environ, {"GITHUB_TOKEN": "test-only-token"}),
            patch.object(metrics, "urlopen", return_value=response) as opener,
        ):
            metrics.fetch("https://github.com/users/example/contributions")
        request = opener.call_args.args[0]
        self.assertIsNone(request.get_header("Authorization"))

    def test_failure_preserves_existing_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            snapshot = Path(directory) / "activity.json"
            snapshot.write_text('{"previous": "verified"}\n')
            with (
                patch.object(
                    metrics.sys, "argv", ["metrics", "--output", str(snapshot)]
                ),
                patch.object(
                    metrics, "collect", side_effect=metrics.MetricsError("missing day")
                ),
                patch.object(metrics.sys, "stderr"),
            ):
                self.assertEqual(metrics.main(), 1)
            self.assertEqual(snapshot.read_text(), '{"previous": "verified"}\n')


if __name__ == "__main__":
    unittest.main()
