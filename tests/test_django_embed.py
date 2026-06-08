from __future__ import annotations

from datetime import UTC, datetime
from unittest import TestCase

from halley_tracker.api import HalleyTrackerService
from halley_tracker.core import DistanceProvider
from halley_tracker.django_embed import build_embed_context, render_embed_block


class FixedProvider(DistanceProvider):
    def distance_au_for_day(self, day_utc: datetime) -> float:
        return 2.5


class DjangoEmbedTests(TestCase):
    def test_build_embed_context_contains_required_fields(self) -> None:
        svc = HalleyTrackerService(provider=FixedProvider())
        context = build_embed_context(
            now=datetime(2055, 1, 2, 0, 0, tzinfo=UTC),
            service=svc,
        )
        self.assertIn("tracker", context)
        self.assertIn("last_updated", context)
        self.assertIn("distance_au", context)
        self.assertIn("freshness_status", context)

    def test_render_embed_block_includes_timestamp_and_distance(self) -> None:
        svc = HalleyTrackerService(provider=FixedProvider())
        context = build_embed_context(
            now=datetime(2055, 1, 2, 0, 0, tzinfo=UTC),
            service=svc,
        )
        html = render_embed_block(context)
        self.assertIn("Last updated:", html)
        self.assertIn("Distance to Earth:", html)
        self.assertIn("Years", html)
        self.assertIn("halley-tracker", html)
