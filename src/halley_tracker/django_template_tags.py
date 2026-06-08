from __future__ import annotations

from datetime import datetime

from .django_embed import build_embed_context, render_embed_block

try:
    from django.utils.safestring import mark_safe
except ImportError:
    mark_safe = None


def halley_tracker_context(now: datetime | None = None, *, cached_only: bool = False) -> dict:
    return build_embed_context(now=now, cached_only=cached_only)


def halley_tracker_html(now: datetime | None = None, *, cached_only: bool = False):
    context = halley_tracker_context(now=now, cached_only=cached_only)
    html = render_embed_block(context)
    if mark_safe is not None:
        return mark_safe(html)
    return html
