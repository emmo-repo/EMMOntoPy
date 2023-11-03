from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
    from pathlib import Path

    from ontopy.ontology import Ontology


def test_sync_reasoner_hermit() -> None:
    """Test `ontopy:Ontology.sync_reasoner()` with HermiT."""
    from ontopy import get_ontology

    testonto = get_ontology("../testonto/testonto_for_reasoner.ttl")
    print(testonto)
    testonto.sync_reasoner(reasoner="HermiT")


def test_sync_reasoner_pellet() -> None:
    """Test `ontopy:Ontology.sync_reasoner()` with Pellet"""
    from ontopy import get_ontology

    testonto = get_ontology("../testonto/testonto_for_reasoner.ttl")
    print(testonto)

    testonto.sync_reasoner(reasoner="Pellet")


def test_sync_reasoner_fact() -> None:
    """Test `ontopy:Ontology.sync_reasoner()` with FaCT++"""
    from ontopy import get_ontology

    testonto = get_ontology("../testonto/testonto_for_reasoner.ttl")
    print(testonto)

    testonto.sync_reasoner(reasoner="FaCT++")


def test_sync_reasoner_wrong(testonto: "Ontology") -> None:
    """Test `ontopy:Ontology.sync_reasoner()` with wrong reasoner."""
    with pytest.raises(ValueError) as excinfo:
        testonto.sync_reasoner(reasoner="NonExistingReasoner")
    assert str(excinfo.value) == (
        "Unknown reasoner 'NonExistingReasoner'. "
        "Supported reasoners are 'Pellet', 'HermiT' and 'FaCT++'."
    )
