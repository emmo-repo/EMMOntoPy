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

    # Check that the name of the copy is the same
    assert testonto_copy.name == testonto.name

    # create a new entity in the original and check that it is there
    # and not in the copy

    testonto.new_entity("FantasyClass2", testonto.TestClass)
    assert testonto.FantasyClass2
    assert testonto_copy.FantasyClass  # Class in ontology before copying
    with pytest.raises(NoSuchLabelError):
        assert testonto_copy.FantasyClass2

    assert testonto.prefix == testonto_copy.prefix


def test_copy_emmo() -> None:
    """Test copying the emmo ontology is done in test_save.py as not to
    Import emmo more times than necessary"""
