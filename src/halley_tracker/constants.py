from __future__ import annotations

from datetime import UTC, datetime

HALLEY_OBJECT_ID = "1P/Halley"
HALLEY_OBJECT_NAME = "Halley's Comet"

# v1 contract uses a canonical UTC date for the next perihelion event.
NEXT_PERIHELION_UTC = datetime(2061, 7, 28, 0, 0, 0, tzinfo=UTC)
PERIHELION_SOURCE = "JPL SBDB calendar date for next Halley perihelion (2061-07-28 UTC)"
PERIHELION_SOURCE_URL = "https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=1P"

DISTANCE_METHOD = "AstroPy Time/units with two-body orbital approximation (offline-first v1)"
DISTANCE_CADENCE = "daily"

AU_TO_KM = 149_597_870.7
