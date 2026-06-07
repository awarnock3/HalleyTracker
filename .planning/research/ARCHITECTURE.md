# Architecture Research

**Domain:** Python library + Django integration for Halley tracking  
**Researched:** 2026-06-07

## Suggested Architecture

Use a layered, offline-first design:

1. **Domain layer** (framework-independent): time/countdown math, distance models, units.
2. **Application layer**: orchestration use-cases (get snapshot, refresh snapshot).
3. **Provider layer**: astronomy adapters (AstroPy primary, optional Horizons integration).
4. **Storage/cache layer**: day-keyed snapshot persistence for low-cost daily updates.
5. **Integration layer**: Django template tag/view helper + management command wrapper.

## Boundaries

- Django code should call a single facade/API, not astronomy internals directly.
- Astronomy provider should hide data-source details from UI and calling app.
- UTC/time-scale conversion should happen at clear boundaries, not across templates/views.

## Data Flow

1. Request render/API call asks facade for today’s snapshot.
2. Snapshot cache hit returns immediately.
3. Cache miss triggers compute via astronomy provider, then persists snapshot.
4. Result normalized to AU + km + UTC countdown and returned to integration layer.

## Build Order

1. Core domain models and UTC/countdown contracts.
2. Astronomy provider and distance computation.
3. Snapshot repository/cache behavior.
4. Application facade/API surface.
5. Django embed integration.
6. Operational refresh command and deployment hardening.

## Sources

- https://docs.djangoproject.com/en/6.0/intro/reusable-apps/
- https://docs.djangoproject.com/en/stable/topics/cache/
- https://docs.astropy.org/en/stable/time/index.html
- https://docs.astropy.org/en/stable/coordinates/solarsystem.html

