# HalleyTracker

## What This Is

HalleyTracker is a Python-first comet tracking component for Halley’s Comet, designed to embed into an existing Django site (`../IHWWebApp`) and also be reusable via a Python library API in other contexts. It provides a UTC countdown to the comet’s next perihelion and a daily-updated Earth distance readout in both kilometers and AU. The first milestone targets practical, low-complexity delivery rather than high-precision astronomical forecasting.

## Core Value

Always provide a clear, reliable Halley’s Comet countdown and Earth-distance display that can be embedded in the existing Django app.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Deliver a reusable Python module that computes Halley’s Comet countdown to next perihelion in UTC.
- [ ] Deliver daily Halley-to-Earth distance computation using AstroPy at runtime, exposed through a clean Python API.
- [ ] Deliver Django-embeddable rendering/output surface for countdown + distance (km and AU) for `../IHWWebApp`.
- [ ] Document data dependencies and clearly identify any features/resources that require network access vs offline operation.
- [ ] Support deployment to the existing remote Ubuntu 24.04 server environment used by the current web app.

### Out of Scope

- Additional celestial objects beyond Halley’s Comet — explicitly deferred to keep v1 focused.
- Notifications, alerts, and charts — not required for v1.
- Precision optimization for long-horizon scientific-grade forecasting — unnecessary for current user value.
- Automated/scheduled ephemeris refresh jobs — v1 uses manual refresh/maintenance only.

## Context

The project is intended for integration with an existing Django web application located at `../IHWWebApp`, with a secondary goal of reusable Python-component usage in other contexts. The user explicitly allows using AstroPy and does not require strict numerical accuracy because the event is far in the future; readability and usability are prioritized. The deployment target includes exporting to a remote Ubuntu 24.04 host. The system should run offline where possible and call out any optional external APIs/resources that would require network access.

## Constraints

- **Runtime**: Must run inside the existing Django app and on a remote Ubuntu 24.04 server — aligns with current hosting/deployment environment.
- **Dependencies**: Avoid paid APIs; AstroPy is acceptable — controls cost and keeps astronomy implementation practical.
- **Connectivity**: Prefer offline-capable operation; explicitly identify anything requiring network access — supports constrained or disconnected operation.
- **Scope**: Single-object tracker (Halley only) with minimal display (time + distance) — keeps v1 small and shippable.
- **Update cadence**: Daily updates are sufficient — avoids unnecessary high-frequency compute complexity.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use AstroPy for runtime distance computation | Approved dependency, avoids paid data sources, suitable for domain calculations | — Pending |
| Prioritize Django embed + Python API in v1 | Matches immediate usage target and reusability goal | — Pending |
| Use UTC countdown and show distance in km + AU | Explicit display requirement and clear user-facing consistency | — Pending |
| Manual data refresh/ops for v1 | Lower operational complexity for first release | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-06-07 after initialization*
