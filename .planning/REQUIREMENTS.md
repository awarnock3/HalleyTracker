# Requirements: HalleyTracker

**Defined:** 2026-06-07  
**Core Value:** Always provide a clear, reliable Halley’s Comet countdown and Earth-distance display that can be embedded in the existing Django app.

## v1 Requirements

### Core Computation

- [ ] **CORE-01**: User can view a UTC countdown to Halley’s next perihelion.
- [ ] **CORE-02**: User can view Halley’s Earth distance computed on a daily cadence.
- [ ] **CORE-03**: User can view distance values in both AU and kilometers.
- [ ] **CORE-04**: User can view source/provenance metadata for computed astronomy values.

### Display

- [ ] **DISP-01**: User can view the tracker as an embeddable display block within Django-rendered pages.
- [ ] **DISP-02**: User can view a `last_updated` timestamp for displayed tracker data.

### Integration & API

- [ ] **API-01**: Developer can call a reusable Python API to fetch countdown and distance values.
- [ ] **API-02**: Developer can integrate tracker output through a Django adapter surface (template tag/helper/view integration path).
- [ ] **API-03**: User-facing behavior remains scoped to Halley’s Comet only.

### Operations & Reliability

- [ ] **OPS-01**: Operator can perform manual refresh of tracker data/workflow when needed.
- [ ] **OPS-02**: Operator can identify which data/resources require network access vs offline operation.
- [ ] **OPS-03**: User can see when data is stale or freshness is outside intended cadence.
- [ ] **OPS-04**: Application can run in the existing hosted environment including remote Ubuntu 24.04 deployment target.

## v2 Requirements

### Deferred Features

- **VIS-01**: User can view comet visibility/status guidance beyond basic countdown/distance.
- **VIS-02**: User can view a lightweight orbital/trajectory visualization.
- **NOTF-01**: User can subscribe to notifications/reminders for comet milestones.
- **MULT-01**: User can track additional comets/objects beyond Halley.
- **OPS-05**: Operator can run scheduled automated refresh jobs.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Multi-object catalog in v1 | Explicitly constrained to Halley-only focus |
| Notifications/reminders in v1 | Deferred to avoid operational complexity in first release |
| Heavy charting/3D visualization in v1 | Not required for initial user value |
| High-frequency real-time recompute | Daily cadence is sufficient for this long-horizon use case |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CORE-01 | Phase 1 | Pending |
| CORE-02 | Phase 1 | Pending |
| CORE-03 | Phase 1 | Pending |
| CORE-04 | Phase 1 | Pending |
| DISP-01 | Phase 3 | Pending |
| DISP-02 | Phase 3 | Pending |
| API-01 | Phase 2 | Pending |
| API-02 | Phase 3 | Pending |
| API-03 | Phase 1 | Pending |
| OPS-01 | Phase 2 | Pending |
| OPS-02 | Phase 4 | Pending |
| OPS-03 | Phase 2 | Pending |
| OPS-04 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 13 total
- Mapped to phases: 13
- Unmapped: 0 ✅

---
*Requirements defined: 2026-06-07*
*Last updated: 2026-06-07 after roadmap creation*
