# Project Research Summary

**Project:** HalleyTracker  
**Domain:** Offline-first Halley countdown and Earth-distance tracker (Python library + Django integration)  
**Researched:** 2026-06-07  
**Confidence:** MEDIUM-HIGH

## Executive Summary

HalleyTracker should ship as a focused, offline-first astronomy component that reliably provides:
1. UTC countdown to Halley’s next perihelion.
2. Daily Halley-to-Earth distance in AU and km.
3. Embeddable Django output plus reusable Python API.

The strongest v1 path is AstroPy-centered computation behind a layered architecture (domain/application/provider/integration) with day-keyed snapshot caching. Optional online resources (such as JPL Horizons) should be enrichment paths, never mandatory runtime dependencies.

## Key Findings

### Stack

- Python 3.12 + Django 5.2 LTS is a stable baseline for Ubuntu 24.04 deployment.
- AstroPy 7.x should be the primary astronomy engine.
- Keep offline-capable data handling; treat external APIs as optional.

### Feature Priorities

**v1 table stakes:**
- UTC perihelion countdown
- Daily AU + km distance
- Data freshness/source disclosure
- Django embed + reusable Python API

**Defer to later:**
- Visualization, alerts, multi-object support, advanced personalization

### Architecture

- Core logic should stay framework-independent.
- Django integration should call a facade, not raw astronomy internals.
- Cache daily snapshots and return normalized output objects for UI/API consumers.

### Pitfalls to Guard Against

- Time-scale mismatches (UTC vs TT/TDB)
- Ambiguous Halley record/solution selection
- Hidden network dependencies in production
- Naive/aware datetime mixing
- Unpinned data/dependency versions
- Stale manual-refresh data without freshness checks

## Roadmap Implications

Recommended build sequence:
1. Time/object correctness baseline
2. Snapshot/cache + public API facade
3. Django embedding and user-visible output
4. Operational hardening and optional enrichment

## Sources

- https://docs.djangoproject.com/en/5.2/releases/5.2/
- https://docs.djangoproject.com/en/dev/internals/release-process/
- https://docs.astropy.org/en/stable/time/index.html
- https://docs.astropy.org/en/stable/coordinates/solarsystem.html
- https://ssd.jpl.nasa.gov/api/horizons.api
- https://www.heavens-above.com/comets.aspx
- https://in-the-sky.org/data/comets.php

---
*Research completed: 2026-06-07*
