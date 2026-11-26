"""Placeholder integration test to prevent pytest exit code 5 (no tests collected)."""

import pytest


@pytest.mark.integration
def test_integration_placeholder():
    """Placeholder integration test.

    Real integration tests require external services (ChromaDB, Redis, LMStudio).
    This placeholder ensures the integration test suite collects at least one test.
    """
    assert True
