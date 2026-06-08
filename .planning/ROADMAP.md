# ROADMAP: HalleyTracker

## Phases

- [ ] **Phase 1: Core Halley Computation Baseline** - Deliver correct Halley-only countdown/distance domain outputs with provenance.
- [ ] **Phase 2: Public API + Freshness Workflow** - Expose reusable Python API with manual refresh and stale-data behavior.
- [ ] **Phase 3: Django Embed Surface** - Deliver Django adapter + embeddable display block with timestamped output.
- [ ] **Phase 4: Deployment & Offline/Network Ops** - Validate hosted-environment runtime and clearly define offline vs network dependencies.

## Phase Details

### Phase 1: Core Halley Computation Baseline
**Goal**: Users get reliable Halley-only UTC countdown and daily Earth-distance values with source transparency.  
**Mode:** mvp  
**Depends on**: Nothing (first phase)  
**Requirements**: CORE-01, CORE-02, CORE-03, CORE-04, API-03  
**Success Criteria** (what must be TRUE):
1. User can view a UTC countdown to Halley’s next perihelion.
2. User can view daily-updated Halley Earth distance in both AU and kilometers.
3. User can view source/provenance metadata for displayed astronomy values.
4. User-facing tracker behavior is limited to Halley’s Comet only.
**Plans**:
1. **P1.1 UTC + provenance contract** — define canonical perihelion source constant, UTC handling boundary, and provenance fields carried in outputs.
2. **P1.2 Core astronomy compute** — implement Halley-only countdown and Earth-distance calculation (AU + km) using AstroPy-first provider logic.
3. **P1.3 Daily snapshot baseline** — define day-keyed snapshot payload shape used by later API/Django layers (value fields + provenance + computed_at).
4. **P1.4 Domain verification set** — add deterministic tests for UTC handling, unit conversion consistency, Halley-only constraints, and metadata presence.

### Phase 2: Public API + Freshness Workflow
**Goal**: Developers and operators can reliably fetch and refresh tracker data with visible freshness state.  
**Mode:** mvp  
**Depends on**: Phase 1  
**Requirements**: API-01, OPS-01, OPS-03  
**Success Criteria** (what must be TRUE):
1. Developer can call a Python API and receive countdown + distance payloads for application use.
2. Operator can run a manual refresh workflow and see tracker data update.
3. User can see explicit stale/freshness indication when data is outside intended daily cadence.
**Plans**:
1. **P2.1 Public Python facade** — implement stable `get_snapshot()`/`refresh_snapshot()`-style API boundary returning normalized tracker payloads.
2. **P2.2 Manual refresh operation** — provide operator-invoked refresh entrypoint (CLI/management command-ready) with explicit success/failure signals.
3. **P2.3 Freshness policy + staleness state** — add cadence policy (daily) and stale-state fields surfaced to callers.
4. **P2.4 API reliability tests** — verify refresh behavior, stale transitions, and error handling paths without leaking provider internals.

### Phase 3: Django Embed Surface
**Goal**: Users can see tracker outputs directly inside Django-rendered pages through a supported adapter path.  
**Mode:** mvp  
**Depends on**: Phase 2  
**Requirements**: DISP-01, DISP-02, API-02  
**Success Criteria** (what must be TRUE):
1. User can view the tracker as an embeddable block on Django-rendered pages.
2. Developer can integrate tracker output via a documented Django adapter surface (tag/helper/view path).
3. User can view a `last_updated` timestamp with tracker data.
**Plans**:
1. **P3.1 Django adapter boundary** — add integration surface (template tag/helper/view adapter) that depends only on Phase 2 facade.
2. **P3.2 Embeddable tracker block** — render countdown, AU/km distance, provenance, and `last_updated` with clear fallback states.
3. **P3.3 Integration guidance for IHWWebApp** — document wiring path and minimal integration steps for `../IHWWebApp`.
4. **P3.4 UI/output verification** — verify template output contract and required fields across fresh/stale/error states.
**UI hint**: yes

### Phase 4: Deployment & Offline/Network Ops
**Goal**: Tracker runs in target hosting environment with clear operational expectations for connectivity.  
**Mode:** mvp  
**Depends on**: Phase 3  
**Requirements**: OPS-02, OPS-04  
**Success Criteria** (what must be TRUE):
1. Operator can clearly identify which tracker resources are offline-capable vs network-dependent.
2. Application runs in the existing hosted setup, including remote Ubuntu 24.04 deployment target.
**Plans**:
1. **P4.1 Connectivity contract** — publish offline-first behavior matrix and explicitly mark optional network enrichment paths.
2. **P4.2 Ubuntu runtime validation** — verify dependency/runtime compatibility for target Ubuntu 24.04 deployment environment.
3. **P4.3 Operational runbook** — document manual refresh procedure, stale-data response, and troubleshooting expectations.
4. **P4.4 Deployment verification pass** — run end-to-end checks proving tracker behavior matches documented offline/network contract.

## Requirement Coverage Map

- CORE-01 → Phase 1
- CORE-02 → Phase 1
- CORE-03 → Phase 1
- CORE-04 → Phase 1
- DISP-01 → Phase 3
- DISP-02 → Phase 3
- API-01 → Phase 2
- API-02 → Phase 3
- API-03 → Phase 1
- OPS-01 → Phase 2
- OPS-02 → Phase 4
- OPS-03 → Phase 2
- OPS-04 → Phase 4

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Core Halley Computation Baseline | 4/4 | Complete | 01-01, 01-02, 01-03, 01-04 |
| 2. Public API + Freshness Workflow | 4/4 | Complete | 02-01, 02-02, 02-03, 02-04 |
| 3. Django Embed Surface | 4/4 | Complete | 03-01, 03-02, 03-03, 03-04 |
| 4. Deployment & Offline/Network Ops | 1/4 | In progress | 04-01 |

---
*Last updated: 2026-06-07 continuing plan development from prior research notes*
