from __future__ import annotations

from datetime import datetime
from html import escape

from .api import HalleyTrackerService


def _countdown_text(total_seconds: int) -> str:
    remaining = max(0, total_seconds)
    years, remaining = divmod(remaining, 365 * 24 * 60 * 60)
    months, remaining = divmod(remaining, 30 * 24 * 60 * 60)
    days, remaining = divmod(remaining, 24 * 60 * 60)
    hours, remaining = divmod(remaining, 60 * 60)
    minutes, seconds = divmod(remaining, 60)
    return (
        f"{years} Years {months} Months {days} Days "
        f"{hours} Hours {minutes} Minutes {seconds} Seconds"
    )


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
    countdown_text = escape(_countdown_text(countdown_seconds))
    distance_au = float(context["distance_au"])
    distance_km = float(context["distance_km"])
    last_updated = escape(str(context["last_updated"]))
    freshness_status = escape(str(context["freshness_status"]))

    return (
        '<section class="halley-tracker" data-freshness="{freshness}">'
        "<h3>{name} Returns</h3>"
        '<p class="halley-countdown">Countdown: {countdown}</p>'
        '<p class="halley-distance">Distance to Earth: {au:.6f} AU ({km:.0f} km)</p>'
        '<p class="halley-updated">Last updated: {updated}</p>'
        "</section>"
    ).format(
        freshness=freshness_status,
        name=object_name,
        countdown=countdown_text,
        au=distance_au,
        km=distance_km,
        updated=last_updated,
    )
