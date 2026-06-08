# Halley Tracker

Halley Tracker is a Python package that provides a UTC countdown to Halley’s next perihelion and daily Earth-distance output (AU + km), with a Django-friendly embed surface.

## Features

- Halley-only tracker contract (`1P/Halley`)
- Countdown output in UTC
- Daily snapshot payload with freshness fields
- Manual refresh workflow for operator use
- Django embed helpers and template-tag wiring
- Standalone preview web server for styling review

## Installation

### From PyPI-style local/editable source

```bash
pip install -e .
```

### With optional AstroPy dependency

```bash
pip install -e .[astro]
```

### From Git (pinned release/tag)

```bash
pip install "halley-tracker @ git+https://github.com/awarnock3/HalleyTracker.git@v0.1.0"
```

## CLI Usage

```bash
# Default snapshot + countdown
PYTHONPATH=src python -m halley_tracker

# Deterministic timestamp
PYTHONPATH=src python -m halley_tracker --now 2055-01-02T00:00:00Z

# Manual refresh result payload
PYTHONPATH=src python -m halley_tracker --refresh

# Cached-only read (can surface stale status)
PYTHONPATH=src python -m halley_tracker --cached-only

# Runtime/deployment diagnostics report
PYTHONPATH=src python -m halley_tracker --ops-report

# Standalone styled preview server
PYTHONPATH=src python -m halley_tracker --serve --host 127.0.0.1 --port 8765
```

## Python API

```python
from halley_tracker import HalleyTrackerService

svc = HalleyTrackerService()
snapshot = svc.get_snapshot()
refresh = svc.run_manual_refresh()
is_too_stale = svc.exceeds_stale_threshold(snapshot, max_age_days=1)
```

Key payload fields include:

- `countdown_seconds`
- `distance_au`, `distance_km`
- `computed_at_utc`
- `is_stale`, `age_days`, `freshness_status`, `stale_reason`
- `provenance`

## Django Integration

Use the built-in template tag module:

```django
{% load halley_tracker %}
{% halley_tracker_block %}
```

Or build/render directly in Python:

```python
from halley_tracker import build_embed_context, render_embed_block

ctx = build_embed_context()
html = render_embed_block(ctx)
```

## Development

Run tests:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

