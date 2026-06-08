from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import datetime

from .api import HalleyTrackerService
from .core import countdown
from .ops import operator_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="halley-tracker",
        description="Print Halley Tracker countdown and daily snapshot output.",
    )
    parser.add_argument(
        "--now",
        help="ISO-8601 UTC datetime for deterministic output (example: 2055-01-02T00:00:00Z).",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Run manual refresh workflow and print refresh result payload.",
    )
    parser.add_argument(
        "--cached-only",
        action="store_true",
        help="Read cached snapshot without auto-refresh so stale state can be observed.",
    )
    parser.add_argument(
        "--ops-report",
        action="store_true",
        help="Print operator runtime/dependency diagnostics report.",
    )
    return parser.parse_args()


def parse_now(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def main() -> int:
    args = parse_args()
    now = parse_now(args.now)
    service = HalleyTrackerService()

    if args.ops_report:
        print("ops_report")
        print(json.dumps(operator_report(), indent=2, sort_keys=True))
        return 0

    countdown_value = countdown(now)
    if args.refresh:
        snapshot_payload = service.run_manual_refresh(now)
        label = "refresh"
    elif args.cached_only:
        snapshot_payload = service.get_cached_snapshot(now)
        label = "snapshot_cached"
    else:
        snapshot_payload = service.get_snapshot(now)
        label = "snapshot"

    print("countdown")
    print(json.dumps(asdict(countdown_value), indent=2, sort_keys=True))
    print("")
    print(label)
    print(json.dumps(snapshot_payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
