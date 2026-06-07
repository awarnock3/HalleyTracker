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
**Plans**: TBD

### Phase 2: Public API + Freshness Workflow
**Goal**: Developers and operators can reliably fetch and refresh tracker data with visible freshness state.  
**Mode:** mvp  
**Depends on**: Phase 1  
**Requirements**: API-01, OPS-01, OPS-03  
**Success Criteria** (what must be TRUE):
1. Developer can call a Python API and receive countdown + distance payloads for application use.
2. Operator can run a manual refresh workflow and see tracker data update.
3. User can see explicit stale/freshness indication when data is outside intended daily cadence.
**Plans**: TBD

### Phase 3: Django Embed Surface
**Goal**: Users can see tracker outputs directly inside Django-rendered pages through a supported adapter path.  
**Mode:** mvp  
**Depends on**: Phase 2  
**Requirements**: DISP-01, DISP-02, API-02  
**Success Criteria** (what must be TRUE):
1. User can view the tracker as an embeddable block on Django-rendered pages.
2. Developer can integrate tracker output via a documented Django adapter surface (tag/helper/view path).
3. User can view a `last_updated` timestamp with tracker data.
**Plans**: TBD  
**UI hint**: yes

### Phase 4: Deployment & Offline/Network Ops
**Goal**: Tracker runs in target hosting environment with clear operational expectations for connectivity.  
**Mode:** mvp  
**Depends on**: Phase 3  
**Requirements**: OPS-02, OPS-04  
**Success Criteria** (what must be TRUE):
1. Operator can clearly identify which tracker resources are offline-capable vs network-dependent.
2. Application runs in the existing hosted setup, including remote Ubuntu 24.04 deployment target.
**Plans**: TBD

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
| 1. Core Halley Computation Baseline | 0/TBD | Not started | - |
| 2. Public API + Freshness Workflow | 0/TBD | Not started | - |
| 3. Django Embed Surface | 0/TBD | Not started | - |
| 4. Deployment & Offline/Network Ops | 0/TBD | Not started | - |
