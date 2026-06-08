from __future__ import annotations

import platform
from importlib.util import find_spec


def dependency_matrix() -> dict:
    return {
        "offline_capable": [
            "core countdown and daily snapshot calculations",
            "public API service cache/refresh logic",
            "django embed helper and templatetag rendering",
        ],
        "optional_network_enrichment": [
            "future external ephemeris enrichment (not required in v1)",
        ],
        "required_runtime": [
            "python>=3.12",
        ],
    }


def runtime_check() -> dict:
    return {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "astropy_available": find_spec("astropy") is not None,
        "django_available": find_spec("django") is not None,
    }


def operator_report() -> dict:
    return {
        "dependency_matrix": dependency_matrix(),
        "runtime": runtime_check(),
        "manual_refresh_command": "PYTHONPATH=src python -m halley_tracker --refresh",
        "smoke_command": "PYTHONPATH=src python -m halley_tracker --now 2055-01-02T00:00:00Z",
    }
