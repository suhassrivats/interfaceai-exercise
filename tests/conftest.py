"""Pytest configuration. Ensures database tables exist before tests run."""
import pytest

from app.database import init_db


@pytest.fixture(scope="session", autouse=True)
def ensure_db_tables():
    """Create database tables before any test runs."""
    init_db()
    yield
