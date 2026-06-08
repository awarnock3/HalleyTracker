# IHWWebApp Integration Snippet (Phase 3)

Use this in a Django template inside `../IHWWebApp`:

```django
{% load halley_tracker %}
{% halley_tracker_block %}
```

Optional deterministic render for testing:

```django
{% halley_tracker_block now=some_utc_dt %}
```

Notes:
- Output includes countdown, distance (AU + km), and `Last updated`.
- `cached_only=True` can be passed when you explicitly want stale-state visibility from cache.
