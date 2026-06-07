# Technology Stack

**Project:** HalleyTracker  
**Researched:** 2026-06-07

## Recommended Stack

| Layer | Choice | Why |
|---|---|---|
| Runtime | Python 3.12 | Strong compatibility on Ubuntu 24.04 and current Django/AstroPy ecosystem |
| Web integration | Django 5.2 LTS | Stable long-support base for reusable app/component integration |
| Astronomy core | AstroPy 7.x | Time scales, units, and astronomy calculations in one maintained library |
| Ephemeris support | jplephem + local kernel data | Offline-capable orbital data handling without paid APIs |
| Optional data source | astroquery JPL Horizons | Network-backed enrichment path when online access is allowed |
| Numeric support | NumPy 2.x | Standard vector/math base for astronomy calculations |
| Validation/config | pydantic 2.x | Typed, reusable config for library + Django integration |
| Testing | pytest + pytest-django + freezegun | Deterministic UTC/countdown/distance tests |

## Preferred Approach

1. Use AstroPy as the primary runtime computation engine.
2. Keep offline-first behavior by bundling/pinning required ephemeris/time data where practical.
3. Treat network-backed sources as optional enhancements, not hard dependencies.
4. Avoid adding new infrastructure (e.g., Celery/Redis) in v1.

## What Not to Use in v1

- Mandatory runtime external API calls for every request.
- Heavy visualization frameworks or 3D rendering stack.
- New dedicated datastore for core countdown/distance feature.

## Version/Source Notes

Version pinning should be finalized during implementation, but recommendations align to current maintained lines:
- Django 5.2 LTS
- AstroPy 7.x
- Python 3.12

## Sources

- https://docs.djangoproject.com/en/5.2/releases/5.2/
- https://docs.djangoproject.com/en/dev/internals/release-process/
- https://docs.astropy.org/en/stable/install.html
- https://docs.astropy.org/en/stable/coordinates/solarsystem.html
- https://ssd.jpl.nasa.gov/api/horizons.api

