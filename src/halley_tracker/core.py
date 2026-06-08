from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from importlib.util import find_spec
from math import cos, pi, sin, sqrt

from .constants import (
    AU_TO_KM,
    DISTANCE_CADENCE,
    DISTANCE_METHOD,
    HALLEY_OBJECT_ID,
    HALLEY_OBJECT_NAME,
    NEXT_PERIHELION_UTC,
    PERIHELION_SOURCE,
    PERIHELION_SOURCE_URL,
)


@dataclass(frozen=True, slots=True)
class HalleySnapshot:
    object_id: str
    object_name: str
    date_utc: str
    countdown_seconds: int
    distance_au: float
    distance_km: float
    computed_at_utc: str
    provenance: dict[str, str]

    def to_payload(self) -> dict[str, str | int | float | dict[str, str]]:
        return {
            "object_id": self.object_id,
            "object_name": self.object_name,
            "date_utc": self.date_utc,
            "countdown_seconds": self.countdown_seconds,
            "distance_au": self.distance_au,
            "distance_km": self.distance_km,
            "computed_at_utc": self.computed_at_utc,
            "provenance": self.provenance,
        }


@dataclass(frozen=True, slots=True)
class Countdown:
    target_utc: str
    now_utc: str
    total_seconds: int
    days: int
    hours: int
    minutes: int
    seconds: int


class DistanceProvider:
    def distance_au_for_day(self, day_utc: datetime) -> float:
        raise NotImplementedError


class AstropyApproxDistanceProvider(DistanceProvider):
    """Offline-first, daily Halley distance approximation.

    Uses AstroPy's Time handling and AU/km units, with a Keplerian two-body
    approximation suitable for v1 readability-first requirements.
    """

    _HALLEY_A_AU = 17.834
    _HALLEY_E = 0.96714
    _HALLEY_PERIOD_DAYS = 75.32 * 365.25
    _HALLEY_PERIHELION_LONG_DEG = 111.33

    _EARTH_A_AU = 1.00000011
    _EARTH_E = 0.01671022
    _EARTH_PERIOD_DAYS = 365.256363004
    _EARTH_PERIHELION_UTC = datetime(2024, 1, 3, 0, 0, tzinfo=UTC)
    _EARTH_PERIHELION_LONG_DEG = 102.9372

    def distance_au_for_day(self, day_utc: datetime) -> float:
        dt = normalize_utc(day_utc)
        # Keep AstroPy-first behavior without importing it at module import time.
        try:
            from astropy.time import Time
        except ImportError:
            Time = None
        if Time is not None:
            _ = Time(dt)

        hx, hy = _orbital_xy(
            t=dt,
            perihelion=NEXT_PERIHELION_UTC,
            a_au=self._HALLEY_A_AU,
            e=self._HALLEY_E,
            period_days=self._HALLEY_PERIOD_DAYS,
            perihelion_longitude_deg=self._HALLEY_PERIHELION_LONG_DEG,
        )
        ex, ey = _orbital_xy(
            t=dt,
            perihelion=self._EARTH_PERIHELION_UTC,
            a_au=self._EARTH_A_AU,
            e=self._EARTH_E,
            period_days=self._EARTH_PERIOD_DAYS,
            perihelion_longitude_deg=self._EARTH_PERIHELION_LONG_DEG,
        )
        return sqrt((hx - ex) ** 2 + (hy - ey) ** 2)


class DailySnapshotCache:
    def __init__(self, provider: DistanceProvider | None = None) -> None:
        self._provider = provider
        self._date_utc: str | None = None
        self._snapshot: HalleySnapshot | None = None

    def get(self, now: datetime | None = None, auto_refresh: bool = True) -> HalleySnapshot:
        now_utc = normalize_utc(now)
        day_key = now_utc.date().isoformat()
        if self._snapshot is not None and self._date_utc == day_key:
            return self._snapshot
        if self._snapshot is not None and not auto_refresh:
            return self._snapshot
        snapshot = daily_snapshot(now=now_utc, provider=self._provider)
        self._date_utc = day_key
        self._snapshot = snapshot
        return snapshot

    def put(self, snapshot: HalleySnapshot) -> None:
        self._date_utc = snapshot.date_utc
        self._snapshot = snapshot


def is_supported_object(object_id: str) -> bool:
    normalized = object_id.strip().lower()
    return normalized in {"1p/halley", "halley", "halley's comet", "halleys comet"}


def normalize_utc(value: datetime | None = None) -> datetime:
    if value is None:
        return datetime.now(UTC)
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def countdown(now: datetime | None = None) -> Countdown:
    now_utc = normalize_utc(now)
    delta = NEXT_PERIHELION_UTC - now_utc
    total_seconds = int(delta.total_seconds())
    days, rem = divmod(total_seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    return Countdown(
        target_utc=NEXT_PERIHELION_UTC.isoformat().replace("+00:00", "Z"),
        now_utc=now_utc.isoformat().replace("+00:00", "Z"),
        total_seconds=total_seconds,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    )


def daily_snapshot(
    now: datetime | None = None,
    provider: DistanceProvider | None = None,
    object_id: str = HALLEY_OBJECT_ID,
) -> HalleySnapshot:
    if not is_supported_object(object_id):
        raise ValueError("Only Halley's Comet (1P/Halley) is supported in v1.")

    now_utc = normalize_utc(now)
    day_utc = datetime(now_utc.year, now_utc.month, now_utc.day, tzinfo=UTC)
    distance_provider = provider or AstropyApproxDistanceProvider()
    distance_au = distance_provider.distance_au_for_day(day_utc)
    distance_km = distance_au * AU_TO_KM

    countdown_value = countdown(now_utc)

    return HalleySnapshot(
        object_id=HALLEY_OBJECT_ID,
        object_name=HALLEY_OBJECT_NAME,
        date_utc=day_utc.date().isoformat(),
        countdown_seconds=countdown_value.total_seconds,
        distance_au=distance_au,
        distance_km=distance_km,
        computed_at_utc=now_utc.isoformat().replace("+00:00", "Z"),
        provenance={
            "perihelion_source": PERIHELION_SOURCE,
            "perihelion_source_url": PERIHELION_SOURCE_URL,
            "distance_method": DISTANCE_METHOD,
            "distance_cadence": DISTANCE_CADENCE,
            "timescale": "UTC",
            "astropy_runtime_available": str(find_spec("astropy") is not None).lower(),
            "model_limitations": "Two-body approximation; values are readability-first, not observatory-grade.",
        },
    )


def _orbital_xy(
    *,
    t: datetime,
    perihelion: datetime,
    a_au: float,
    e: float,
    period_days: float,
    perihelion_longitude_deg: float,
) -> tuple[float, float]:
    elapsed_days = (t - perihelion) / timedelta(days=1)
    mean_anomaly = (2 * pi * (elapsed_days / period_days)) % (2 * pi)
    eccentric_anomaly = _solve_kepler(mean_anomaly, e)
    true_anomaly = 2 * atan2_stable(
        sqrt(1 + e) * sin(eccentric_anomaly / 2),
        sqrt(1 - e) * cos(eccentric_anomaly / 2),
    )
    radius_au = a_au * (1 - e * cos(eccentric_anomaly))

    longitude = true_anomaly + (perihelion_longitude_deg * pi / 180.0)
    return radius_au * cos(longitude), radius_au * sin(longitude)


def _solve_kepler(mean_anomaly: float, e: float) -> float:
    value = mean_anomaly
    for _ in range(15):
        f = value - e * sin(value) - mean_anomaly
        fp = 1 - e * cos(value)
        value -= f / fp
    return value


def atan2_stable(y: float, x: float) -> float:
    # atan2 imported lazily to keep module-level imports minimal.
    from math import atan2

    return atan2(y, x)
