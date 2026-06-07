# Feature Research

**Domain:** Halley-focused comet tracker  
**Researched:** 2026-06-07

## Table Stakes

- UTC countdown to next perihelion.
- Current Halley-to-Earth distance.
- Display in both AU and km.
- Last-updated timestamp and data-source attribution.
- Easy embeddable output surface.

## Differentiators (Defer-Friendly)

- Observer-location visibility windows.
- Lightweight orbital path view.
- Timeline of key Halley milestones.
- Explainability panel for method/assumptions.

## Anti-Features for v1

- Multi-object comet support.
- High-frequency “live” recompute loop.
- Heavy 3D visualization stack.
- Notifications/reminders infrastructure.

## Dependency Notes

- Distance/countdown features depend on a stable ephemeris/time pipeline.
- Visibility and charts should build on the same core orbit/time compute layer.
- Any future alerts should wait for freshness and reliability guardrails.

## MVP Recommendation

Ship in v1:
1. UTC perihelion countdown.
2. Daily Earth-distance (AU + km).
3. Data freshness/source labeling.
4. Django embeddable component and reusable Python API.

Defer to later:
- Visualization, location-personalized views, alerts, and multi-object expansion.

## Sources

- https://thehalleyproject.org/
- https://spacein3d.com/where-is-comet-halley-live-tracker/
- https://www.heavens-above.com/comets.aspx
- https://in-the-sky.org/data/comets.php

