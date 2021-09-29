"""Pytest fixtures and setup functions."""
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ontopy.ontology import Ontology


@pytest.fixture(scope="session")
def repo_dir() -> Path:
    """Absolute path to the repository directory."""
    return Path(__file__).parent.parent.resolve()


@pytest.fixture
def emmo() -> "Ontology":
    """Load and return EMMO."""
    from emmopy import get_emmo

    emmo = get_emmo()

    return emmo


@pytest.fixture
def tmpdir() -> Path:
    """Create a temporary directory that lasts the runtime of the test."""
    from tempfile import TemporaryDirectory

    res = TemporaryDirectory()
    yield Path(res.name)
    res.cleanup()
