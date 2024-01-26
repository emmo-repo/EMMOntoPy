from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
    from pathlib import Path


def test_copy(testonto: "Ontology") -> None:
    """Test copying an ontology"""

    from ontopy import get_ontology
    from ontopy.utils import NoSuchLabelError

    testonto_ref = testonto

    # Add new entity to ontology
    testonto.new_entity("FantasyClass", testonto.TestClass)
    assert testonto_ref.FantasyClass == testonto.FantasyClass

    # Make a copy and check that new entity in original is not in copy
    testonto_copy = testonto.copy()

    # Check that the name of the cipy is the same
    assert testonto_copy.name == testonto.name

    testonto.new_entity("FantasyClass2", testonto.TestClass)

    assert testonto.FantasyClass2
    print("testonto", list(testonto.classes()))
    print(list(testonto_copy.classes()))
    print("copied label annotations", testonto_copy.label_annotations)
    print("copied prefix", testonto_copy.prefix)
    assert testonto_copy.FantasyClass
    print("*************************************")
    print(set(testonto.classes()).difference(testonto_copy.classes()))

    print("*************************")
    with pytest.raises(NoSuchLabelError):
        assert testonto_copy.FantasyClass2


def test_copy_emmo() -> None:
    """Test copying the emmo ontology is done in test_save.py as not to
    Import emmo more times than necessary"""
