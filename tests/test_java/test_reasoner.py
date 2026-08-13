from typing import TYPE_CHECKING
import pytest

from ontopy.exceptions import _require_java

if TYPE_CHECKING:
    from pathlib import Path

    from ontopy.ontology import Ontology

try:
    _require_java()
except RuntimeError as e:
    pytest.skip(
        "Java not available, skipping this test", allow_module_level=True
    )


def test_sync_reasoner_hermit(repo_dir: "Path") -> None:
    """Test `ontopy:Ontology.sync_reasoner()` with HermiT."""
    from ontopy import get_ontology

    testonto = get_ontology(
        repo_dir / "tests" / "testonto" / "testonto_for_reasoner.ttl"
    ).load()
    assert testonto.Avocado
    assert not isinstance(testonto.Avocado, testonto.NaturalDye)
    testonto.sync_reasoner(reasoner="HermiT")
    assert isinstance(testonto.Avocado, testonto.NaturalDye)


def test_sync_reasoner_pellet(repo_dir: "Path") -> None:
    """Test `ontopy:Ontology.sync_reasoner()` with Pellet"""
    from ontopy import get_ontology

    testonto = get_ontology(
        repo_dir / "tests" / "testonto" / "testonto_for_reasoner.ttl"
    ).load()

    assert testonto.Avocado
    assert not isinstance(testonto.Avocado, testonto.NaturalDye)
    testonto.sync_reasoner(reasoner="Pellet")
    assert isinstance(testonto.Avocado, testonto.NaturalDye)


def test_sync_reasoner_fact(repo_dir: "Path") -> None:
    """Test `ontopy:Ontology.sync_reasoner()` with FaCT++"""
    from ontopy import get_ontology

    testonto = get_ontology(
        repo_dir / "tests" / "testonto" / "testonto_for_reasoner.ttl"
    ).load()
    assert testonto.Avocado
    assert not isinstance(testonto.Avocado, testonto.NaturalDye)
    testonto.sync_reasoner(reasoner="FaCT++")
    assert isinstance(testonto.Avocado, testonto.NaturalDye)


def test_sync_reasoner_wrong(testonto: "Ontology") -> None:
    """Test `ontopy:Ontology.sync_reasoner()` with wrong reasoner."""
    with pytest.raises(ValueError) as excinfo:
        testonto.sync_reasoner(reasoner="NonExistingReasoner")
    assert str(excinfo.value) == (
        "Unknown reasoner 'NonExistingReasoner'. "
        "Supported reasoners are 'Pellet', 'HermiT' and 'FaCT++'."
    )
