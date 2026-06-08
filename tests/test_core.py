from __future__ import annotations

import os
import subprocess
import sys
from datetime import UTC, datetime
from unittest import TestCase

from halley_tracker.constants import AU_TO_KM, HALLEY_OBJECT_ID, NEXT_PERIHELION_UTC
from halley_tracker.core import (
    AstropyApproxDistanceProvider,
    DailySnapshotCache,
    DistanceProvider,
    countdown,
    daily_snapshot,
    is_supported_object,
    normalize_utc,
)


class FixedDistanceProvider(DistanceProvider):
    def __init__(self, au: float) -> None:
        self.au = au

    def distance_au_for_day(self, day_utc: datetime) -> float:
        return self.au


class CountingDistanceProvider(DistanceProvider):
    def __init__(self, au: float) -> None:
        self.au = au
        self.calls = 0

    def distance_au_for_day(self, day_utc: datetime) -> float:
        self.calls += 1
        return self.au


class CoreContractTests(TestCase):
    def test_normalize_utc_attaches_utc_for_naive_datetimes(self) -> None:
        value = datetime(2030, 1, 2, 3, 4, 5)
        normalized = normalize_utc(value)
        self.assertEqual(normalized.tzinfo, UTC)

    def test_countdown_uses_utc_target(self) -> None:
        now = datetime(2060, 7, 28, 0, 0, 0, tzinfo=UTC)
        result = countdown(now)
        expected = int((NEXT_PERIHELION_UTC - now).total_seconds())

        self.assertEqual(result.total_seconds, expected)
        self.assertTrue(result.target_utc.endswith("Z"))
        self.assertTrue(result.now_utc.endswith("Z"))

    def test_daily_snapshot_contains_halley_only_and_provenance(self) -> None:
        provider = FixedDistanceProvider(1.2345)
        now = datetime(2050, 8, 1, 15, 30, tzinfo=UTC)
        snapshot = daily_snapshot(now=now, provider=provider)

        self.assertEqual(snapshot.object_id, HALLEY_OBJECT_ID)
        self.assertEqual(snapshot.date_utc, "2050-08-01")
        self.assertIn("perihelion_source", snapshot.provenance)
        self.assertIn("distance_method", snapshot.provenance)
        self.assertEqual(snapshot.provenance["timescale"], "UTC")

    def test_daily_snapshot_has_consistent_au_km_values(self) -> None:
        provider = FixedDistanceProvider(2.0)
        snapshot = daily_snapshot(
            now=datetime(2055, 1, 2, 0, 0, tzinfo=UTC), provider=provider
        )
        self.assertAlmostEqual(snapshot.distance_au, 2.0, places=9)
        self.assertAlmostEqual(snapshot.distance_km, 2.0 * AU_TO_KM, places=4)

    def test_snapshot_payload_contains_stable_keys(self) -> None:
        snapshot = daily_snapshot(
            now=datetime(2055, 1, 2, 0, 0, tzinfo=UTC),
            provider=FixedDistanceProvider(2.0),
        )
        payload = snapshot.to_payload()
        self.assertEqual(payload["object_id"], HALLEY_OBJECT_ID)
        self.assertEqual(payload["date_utc"], "2055-01-02")
        self.assertIn("distance_au", payload)
        self.assertIn("provenance", payload)

    def test_daily_snapshot_cache_reuses_same_day_snapshot(self) -> None:
        provider = CountingDistanceProvider(1.1)
        cache = DailySnapshotCache(provider=provider)

        first = cache.get(datetime(2055, 1, 2, 1, 0, tzinfo=UTC))
        second = cache.get(datetime(2055, 1, 2, 23, 0, tzinfo=UTC))
        self.assertEqual(provider.calls, 1)
        self.assertIs(first, second)

    def test_daily_snapshot_cache_recomputes_on_new_day(self) -> None:
        provider = CountingDistanceProvider(1.1)
        cache = DailySnapshotCache(provider=provider)

        first = cache.get(datetime(2055, 1, 2, 23, 0, tzinfo=UTC))
        second = cache.get(datetime(2055, 1, 3, 0, 1, tzinfo=UTC))
        self.assertEqual(provider.calls, 2)
        self.assertIsNot(first, second)

    def test_supported_object_recognizes_halley_variants(self) -> None:
        self.assertTrue(is_supported_object("1P/Halley"))
        self.assertTrue(is_supported_object("halley"))
        self.assertFalse(is_supported_object("2P/Encke"))

    def test_daily_snapshot_rejects_non_halley_object(self) -> None:
        with self.assertRaises(ValueError):
            daily_snapshot(
                now=datetime(2055, 1, 2, 0, 0, tzinfo=UTC),
                provider=FixedDistanceProvider(1.0),
                object_id="2P/Encke",
            )

    def test_provenance_contains_runtime_diagnostics(self) -> None:
        snapshot = daily_snapshot(
            now=datetime(2055, 1, 2, 0, 0, tzinfo=UTC),
            provider=FixedDistanceProvider(2.0),
        )
        self.assertIn("astropy_runtime_available", snapshot.provenance)
        self.assertIn("model_limitations", snapshot.provenance)

    def test_countdown_is_zero_at_perihelion_timestamp(self) -> None:
        result = countdown(NEXT_PERIHELION_UTC)
        self.assertEqual(result.total_seconds, 0)
        self.assertEqual(result.days, 0)
        self.assertEqual(result.hours, 0)
        self.assertEqual(result.minutes, 0)
        self.assertEqual(result.seconds, 0)

    def test_default_provider_produces_positive_finite_distance(self) -> None:
        provider = AstropyApproxDistanceProvider()
        value = provider.distance_au_for_day(datetime(2055, 1, 2, tzinfo=UTC))
        self.assertGreater(value, 0.0)
        self.assertLess(value, 100.0)

    def test_cli_smoke_output(self) -> None:
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.join(root, "src")

        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "halley_tracker",
                "--now",
                "2055-01-02T00:00:00Z",
            ],
            cwd=root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("countdown", proc.stdout)
        self.assertIn("snapshot", proc.stdout)
        self.assertIn("distance_au", proc.stdout)

    def test_cli_refresh_mode_output(self) -> None:
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.join(root, "src")

        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "halley_tracker",
                "--now",
                "2055-01-02T00:00:00Z",
                "--refresh",
            ],
            cwd=root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("refresh", proc.stdout)
        self.assertIn("\"status\": \"refreshed\"", proc.stdout)

    def test_cli_ops_report_output(self) -> None:
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.join(root, "src")

        proc = subprocess.run(
            [sys.executable, "-m", "halley_tracker", "--ops-report"],
            cwd=root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("ops_report", proc.stdout)
        self.assertIn("dependency_matrix", proc.stdout)
