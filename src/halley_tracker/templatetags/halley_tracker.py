from __future__ import annotations

from datetime import datetime

from halley_tracker.django_template_tags import halley_tracker_html

DJANGO_AVAILABLE = False

try:
    from django import template
    from django.utils.safestring import mark_safe

    DJANGO_AVAILABLE = True
    register = template.Library()
except ImportError:
    register = None
    mark_safe = None


def halley_tracker_block(now: datetime | None = None, cached_only: bool = False):
    html = halley_tracker_html(now=now, cached_only=cached_only)
    if DJANGO_AVAILABLE and mark_safe is not None:
        return mark_safe(str(html))
    return str(html)


if DJANGO_AVAILABLE and register is not None:
    register.simple_tag(halley_tracker_block)


def django_template_usage_snippet() -> str:
    return (
        "{% load halley_tracker %}\n"
        "<!-- Optional deterministic timestamp for tests: {% halley_tracker_block now=some_utc_dt %} -->\n"
        "{% halley_tracker_block %}\n"
    )
