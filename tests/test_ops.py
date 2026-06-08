from __future__ import annotations

from unittest import TestCase

from halley_tracker.ops import dependency_matrix, operator_report, runtime_check


class OpsDiagnosticsTests(TestCase):
    def test_dependency_matrix_contains_offline_and_network_sections(self) -> None:
        matrix = dependency_matrix()
        self.assertIn("offline_capable", matrix)
        self.assertIn("optional_network_enrichment", matrix)

    def test_runtime_check_contains_capability_flags(self) -> None:
        runtime = runtime_check()
        self.assertIn("python_version", runtime)
        self.assertIn("astropy_available", runtime)
        self.assertIn("django_available", runtime)

    def test_operator_report_contains_commands(self) -> None:
        report = operator_report()
        self.assertIn("dependency_matrix", report)
        self.assertIn("runtime", report)
        self.assertIn("manual_refresh_command", report)
        self.assertIn("smoke_command", report)
