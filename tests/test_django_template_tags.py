from __future__ import annotations

from datetime import UTC, datetime
from unittest import TestCase

from halley_tracker.django_template_tags import halley_tracker_context, halley_tracker_html


class DjangoTemplateTagTests(TestCase):
    def test_halley_tracker_context_has_tracker_payload(self) -> None:
        ctx = halley_tracker_context(now=datetime(2055, 1, 2, 0, 0, tzinfo=UTC))
        self.assertIn("tracker", ctx)
        self.assertIn("last_updated", ctx)

    def test_halley_tracker_html_returns_embeddable_markup(self) -> None:
        html = halley_tracker_html(now=datetime(2055, 1, 2, 0, 0, tzinfo=UTC))
        self.assertIn("halley-tracker", str(html))
        self.assertIn("Last updated:", str(html))
