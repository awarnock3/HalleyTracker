# Pitfalls Research

**Domain:** Halley countdown/distance tracker  
**Researched:** 2026-06-07

## High-Risk Pitfalls and Prevention

| Pitfall | Warning Signs | Prevention | Phase |
|---|---|---|---|
| UTC vs TDB/TT confusion | Inconsistent countdown vs distance values | Canonical UTC contract; convert only at astronomy boundaries | Phase 1 |
| Ambiguous Halley object selection | Multiple-match query results; output drift | Pin explicit Halley record/solution and log provenance | Phase 1 |
| Hidden network dependencies | Offline/server failures, cold-start download errors | Bundle required data; document online-only paths clearly | Phase 3 |
| Naive/aware datetime mixing | DST/timezone bugs across environments | Use timezone-aware UTC datetimes end-to-end | Phase 1-2 |
| Unpinned data/dependency versions | Same code produces different numbers over time | Pin versions and include source/version metadata in diagnostics | Phase 3 |
| Manual refresh staleness | “Daily” values become stale silently | Store computed_at; add staleness checks and operator runbook | Phase 4 |

## Operational Guardrails

- Always expose `last_updated` in outputs.
- Keep a clear offline vs online behavior statement in docs.
- Validate cache/data paths on deployment target (Ubuntu 24.04 host).

## Security/Robustness Notes

- Keep date-range and object inputs bounded to prevent expensive misuse.
- Avoid surfacing raw astronomy-library exceptions to end users.

## Sources

- https://docs.astropy.org/en/stable/time/index.html
- https://docs.astropy.org/en/stable/coordinates/solarsystem.html
- https://docs.python.org/3/library/datetime.html
- https://docs.djangoproject.com/en/stable/topics/i18n/timezones/
- https://ssd.jpl.nasa.gov/api/horizons.api

