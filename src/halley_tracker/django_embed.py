from __future__ import annotations

from datetime import datetime
from html import escape

from .api import HalleyTrackerService


def build_embed_context(
    now: datetime | None = None,
    *,
    cached_only: bool = False,
    service: HalleyTrackerService | None = None,
) -> dict:
    svc = service or HalleyTrackerService()
    payload = svc.get_cached_snapshot(now) if cached_only else svc.get_snapshot(now)
    return {
        "tracker": payload,
        "object_name": payload["object_name"],
        "countdown_seconds": payload["countdown_seconds"],
        "distance_au": payload["distance_au"],
        "distance_km": payload["distance_km"],
        "last_updated": payload["computed_at_utc"],
        "freshness_status": payload["freshness_status"],
    }


def render_embed_block(context: dict) -> str:
    object_name = escape(str(context["object_name"]))
    countdown_seconds = int(context["countdown_seconds"])
    distance_au = float(context["distance_au"])
    distance_km = float(context["distance_km"])
    last_updated = escape(str(context["last_updated"]))
    freshness_status = escape(str(context["freshness_status"]))

    return (
        '<section class="halley-tracker" data-freshness="{freshness}">'
        "<h3>{name}</h3>"
        '<p class="halley-countdown">Countdown: {countdown}s</p>'
        '<p class="halley-distance">Distance: {au:.6f} AU ({km:.0f} km)</p>'
        '<p class="halley-updated">Last updated: {updated}</p>'
        "</section>"
    ).format(
        freshness=freshness_status,
        name=object_name,
        countdown=countdown_seconds,
        au=distance_au,
        km=distance_km,
        updated=last_updated,
    )
