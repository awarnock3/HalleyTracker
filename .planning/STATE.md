# STATE: HalleyTracker

## Project Reference

**Core Value**: Always provide a clear, reliable Halley’s Comet countdown and Earth-distance display that can be embedded in the existing Django app.  
**Current Focus**: Phase 1 - Core Halley Computation Baseline

## Current Position

- **Current Phase**: 1 - Core Halley Computation Baseline
- **Current Plan**: Not started
- **Overall Status**: Planning complete; execution not started
- **Progress**: 0/4 phases complete (0%)

## Performance Metrics

- **v1 Requirements**: 13
- **Mapped to phases**: 13/13
- **Coverage**: 100%
- **Open blockers**: 0
- **Research confidence input**: Medium-High

## Accumulated Context

### Key Decisions

- Use AstroPy-centered computation for v1 astronomy values.
- Keep architecture Python-core first, Django integration as adapter layer.
- Keep v1 scope Halley-only, daily cadence, manual refresh path.
- Treat network resources as optional enrichment, not hard dependency where possible.

### TODOs

- Begin Phase 1 planning and implementation.
- Define canonical Halley perihelion constant/source and provenance format.
- Define daily snapshot schema shared by API and Django adapter.

### Known Risks

- Time-scale handling mistakes (UTC vs TT/TDB).
- Hidden network dependency drift.
- Staleness logic not consistently surfaced to users.

### Blockers

- None currently.

## Session Continuity

**Last completed step**: Roadmap generation and requirement-to-phase mapping.  
**Next command**: `/gsd-plan-phase 1`  
**Resume point**: Start executable plan decomposition for Phase 1 success criteria.
