from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
    from pathlib import Path


def test_copy(testonto: "Ontology", repo_dir: "Path") -> None:
    """Test adding entities to ontology"""

    from ontopy import get_ontology
    from ontopy.utils import NoSuchLabelError

    # create new reference to ontology
    testonto = get_ontology(
        repo_dir / "tests" / "testonto" / "testonto.ttl"
    ).load()
    testonto_ref = testonto

    # add new entity to ontology
    testonto.new_entity("FantasyClass", testonto.TestClass)

    assert testonto_ref.FantasyClass == testonto.FantasyClass

    # make a copy and check that new entity in original is not in copy
    testonto_copy = testonto.copy()

    testonto.new_entity("FantasyClass2", testonto_copy.TestClass)

    assert testonto.FantasyClass2

    with pytest.raises(NoSuchLabelError):
        assert testonto_copy.FantasyClass2
