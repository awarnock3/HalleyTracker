from __future__ import annotations

from datetime import UTC, datetime
from unittest import TestCase

from halley_tracker.api import HalleyTrackerService
from halley_tracker.core import DistanceProvider


class IncrementingProvider(DistanceProvider):
    def __init__(self) -> None:
        self.calls = 0

    def distance_au_for_day(self, day_utc: datetime) -> float:
        self.calls += 1
        return 1.0 + self.calls


class ServiceApiTests(TestCase):
    def test_get_snapshot_returns_freshness_fields(self) -> None:
        svc = HalleyTrackerService(provider=IncrementingProvider())
        payload = svc.get_snapshot(now=datetime(2055, 1, 2, 0, 0, tzinfo=UTC))
        self.assertIn("is_stale", payload)
        self.assertIn("age_days", payload)
        self.assertIn("freshness_status", payload)
        self.assertIn("stale_reason", payload)
        self.assertEqual(payload["is_stale"], False)
        self.assertEqual(payload["age_days"], 0)
        self.assertEqual(payload["freshness_status"], "fresh")

    def test_get_snapshot_reuses_daily_cache(self) -> None:
        provider = IncrementingProvider()
        svc = HalleyTrackerService(provider=provider)
        first = svc.get_snapshot(now=datetime(2055, 1, 2, 0, 0, tzinfo=UTC))
        second = svc.get_snapshot(now=datetime(2055, 1, 2, 23, 0, tzinfo=UTC))
        self.assertEqual(provider.calls, 1)
        self.assertEqual(first["distance_au"], second["distance_au"])

    def test_refresh_snapshot_forces_recompute(self) -> None:
        provider = IncrementingProvider()
        svc = HalleyTrackerService(provider=provider)
        first = svc.get_snapshot(now=datetime(2055, 1, 2, 0, 0, tzinfo=UTC))
        refreshed = svc.refresh_snapshot(now=datetime(2055, 1, 2, 12, 0, tzinfo=UTC))
        self.assertEqual(provider.calls, 2)
        self.assertNotEqual(first["distance_au"], refreshed["distance_au"])

    def test_manual_refresh_operation_contract(self) -> None:
        provider = IncrementingProvider()
        svc = HalleyTrackerService(provider=provider)
        result = svc.run_manual_refresh(now=datetime(2055, 1, 2, 10, 0, tzinfo=UTC))
        self.assertEqual(result["status"], "refreshed")
        self.assertIn("refreshed_at_utc", result)
        self.assertIn("snapshot", result)
        self.assertIn("distance_changed", result)

    def test_freshness_age_uses_day_delta(self) -> None:
        fields = HalleyTrackerService._freshness_fields(
            datetime(2055, 1, 4, 0, 0, tzinfo=UTC),
            "2055-01-02",
        )
        self.assertEqual(fields["age_days"], 2)
        self.assertEqual(fields["is_stale"], True)
        self.assertEqual(fields["freshness_status"], "stale")
        self.assertNotEqual(fields["stale_reason"], "")

    def test_get_cached_snapshot_surfaces_stale_state(self) -> None:
        provider = IncrementingProvider()
        svc = HalleyTrackerService(provider=provider)
        svc.get_snapshot(now=datetime(2055, 1, 2, 0, 0, tzinfo=UTC))
        cached = svc.get_cached_snapshot(now=datetime(2055, 1, 4, 0, 0, tzinfo=UTC))
        self.assertEqual(cached["is_stale"], True)
        self.assertEqual(cached["age_days"], 2)
        self.assertEqual(provider.calls, 1)

    def test_exceeds_stale_threshold_helper(self) -> None:
        payload = {"age_days": 3}
        self.assertEqual(HalleyTrackerService.exceeds_stale_threshold(payload, 1), True)
        self.assertEqual(HalleyTrackerService.exceeds_stale_threshold(payload, 5), False)
