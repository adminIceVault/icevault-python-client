"""Shared pytest fixtures for unit and integration tests."""

from __future__ import annotations

import pytest


@pytest.fixture
def api_key() -> str:
    """Return a placeholder API key for tests."""
    return "test-api-key"


@pytest.fixture
def base_url() -> str:
    """Return a placeholder API base URL for tests."""
    return "https://api.icevault.example/v1"
