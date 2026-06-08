from __future__ import annotations

from datetime import UTC, datetime
from unittest import TestCase

from halley_tracker.templatetags.halley_tracker import (
    DJANGO_AVAILABLE,
    django_template_usage_snippet,
    halley_tracker_block,
)


class DjangoTemplateTagsModuleTests(TestCase):
    def test_halley_tracker_block_returns_html_string(self) -> None:
        output = halley_tracker_block(
            now=datetime(2055, 1, 2, 0, 0, tzinfo=UTC),
            cached_only=False,
        )
        self.assertIn("halley-tracker", str(output))
        self.assertIn("Last updated:", str(output))

    def test_django_available_flag_is_boolean(self) -> None:
        self.assertIn(DJANGO_AVAILABLE, (True, False))

    def test_usage_snippet_contains_load_and_tag(self) -> None:
        snippet = django_template_usage_snippet()
        self.assertIn("{% load halley_tracker %}", snippet)
        self.assertIn("{% halley_tracker_block %}", snippet)
