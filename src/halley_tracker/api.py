from __future__ import annotations

from datetime import datetime

from .core import DailySnapshotCache, DistanceProvider, daily_snapshot, normalize_utc


class HalleyTrackerService:
    def __init__(self, provider: DistanceProvider | None = None) -> None:
        self._provider = provider
        self._cache = DailySnapshotCache(provider=provider)

    def get_snapshot(self, now: datetime | None = None) -> dict:
        now_utc = normalize_utc(now)
        snapshot = self._cache.get(now_utc)
        payload = snapshot.to_payload()
        payload.update(self._freshness_fields(now_utc, payload["date_utc"]))
        return payload

    def get_cached_snapshot(self, now: datetime | None = None) -> dict:
        now_utc = normalize_utc(now)
        snapshot = self._cache.get(now_utc, auto_refresh=False)
        payload = snapshot.to_payload()
        payload.update(self._freshness_fields(now_utc, payload["date_utc"]))
        return payload

    def refresh_snapshot(self, now: datetime | None = None) -> dict:
        now_utc = normalize_utc(now)
        snapshot = daily_snapshot(now=now_utc, provider=self._provider)
        self._cache = DailySnapshotCache(provider=self._provider)
        self._cache.put(snapshot)
        payload = snapshot.to_payload()
        payload.update(self._freshness_fields(now_utc, payload["date_utc"]))
        return payload

    def run_manual_refresh(self, now: datetime | None = None) -> dict:
        now_utc = normalize_utc(now)
        before = self.get_snapshot(now_utc)
        after = self.refresh_snapshot(now_utc)
        return {
            "status": "refreshed",
            "refreshed_at_utc": now_utc.isoformat().replace("+00:00", "Z"),
            "was_stale": before["is_stale"],
            "age_days_before": before["age_days"],
            "distance_changed": before["distance_au"] != after["distance_au"],
            "snapshot": after,
        }

    @staticmethod
    def exceeds_stale_threshold(payload: dict, max_age_days: int = 1) -> bool:
        return int(payload.get("age_days", 0)) > max_age_days

    @staticmethod
    def _freshness_fields(
        now_utc: datetime, snapshot_date: str
    ) -> dict[str, int | bool | str]:
        snapshot_day = datetime.fromisoformat(snapshot_date).date()
        age_days = (now_utc.date() - snapshot_day).days
        if age_days < 0:
            age_days = 0
        is_stale = age_days > 0
        return {
            "is_stale": is_stale,
            "age_days": age_days,
            "freshness_status": "stale" if is_stale else "fresh",
            "stale_reason": "snapshot date is older than current UTC date" if is_stale else "",
        }
