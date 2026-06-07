<!-- GSD:project-start source:PROJECT.md -->
## Project

**HalleyTracker**

HalleyTracker is a Python-first comet tracking component for Halley’s Comet, designed to embed into an existing Django site (`../IHWWebApp`) and also be reusable via a Python library API in other contexts. It provides a UTC countdown to the comet’s next perihelion and a daily-updated Earth distance readout in both kilometers and AU. The first milestone targets practical, low-complexity delivery rather than high-precision astronomical forecasting.

**Core Value:** Always provide a clear, reliable Halley’s Comet countdown and Earth-distance display that can be embedded in the existing Django app.

### Constraints

- **Runtime**: Must run inside the existing Django app and on a remote Ubuntu 24.04 server — aligns with current hosting/deployment environment.
- **Dependencies**: Avoid paid APIs; AstroPy is acceptable — controls cost and keeps astronomy implementation practical.
- **Connectivity**: Prefer offline-capable operation; explicitly identify anything requiring network access — supports constrained or disconnected operation.
- **Scope**: Single-object tracker (Halley only) with minimal display (time + distance) — keeps v1 small and shippable.
- **Update cadence**: Daily updates are sufficient — avoids unnecessary high-frequency compute complexity.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->
## Technology Stack

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
## What Not to Use in v1
- Mandatory runtime external API calls for every request.
- Heavy visualization frameworks or 3D rendering stack.
- New dedicated datastore for core countdown/distance feature.
## Version/Source Notes
- Django 5.2 LTS
- AstroPy 7.x
- Python 3.12
## Sources
- https://docs.djangoproject.com/en/5.2/releases/5.2/
- https://docs.djangoproject.com/en/dev/internals/release-process/
- https://docs.astropy.org/en/stable/install.html
- https://docs.astropy.org/en/stable/coordinates/solarsystem.html
- https://ssd.jpl.nasa.gov/api/horizons.api
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
