"""Pytest fixtures and setup functions."""

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ontopy.ontology import Ontology
    from typing import Sequence
import sys, os

# Add test-specific utilities to path
sys.path.append(os.path.join(os.path.dirname(__file__), "utilities"))


@pytest.fixture(scope="session")
def repo_dir() -> Path:
    """Absolute path to the repository directory."""
    return Path(__file__).parent.parent.resolve()


@pytest.fixture
def emmo() -> "Ontology":
    """Load and return EMMO.

    Note that this loads the version of EMMO that is
    the current defailt in ontopy.

    When updating the defeault EMMO for ontopy,
    tests might need to be updated.
    """
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


@pytest.fixture
def testonto() -> "Ontology":
    """Load and return the local testonto."""
    from ontopy import get_ontology

    path = Path(__file__).parent.parent.resolve() / "tests" / "testonto"

    testonto = get_ontology(str(path) + "/testonto.ttl").load()

    return testonto
