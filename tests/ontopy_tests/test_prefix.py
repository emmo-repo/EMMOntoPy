from typing import TYPE_CHECKING
import pytest
from ontopy.utils import NoSuchLabelError
import warnings

if TYPE_CHECKING:
    from pathlib import Path


def test_prefix(testonto: "Ontology", emmo: "Ontology") -> None:
    """Test prefix in ontology"""

    assert len(testonto.get_by_label_all("*")) == 7
    assert set(testonto.get_by_label_all("*", prefix="testonto")) == set(
        [
            testonto.hasObjectProperty,
            testonto.TestClass,
            testonto.hasAnnotationProperty,
            testonto.hasDataProperty,
        ]
    )
    assert (
        testonto.get_by_label("TestClass", prefix="testonto")
        == testonto.TestClass
    )
    assert (
        str(testonto.get_by_label("TestClass", prefix="models"))
        == "models.TestClass"
    )

    with pytest.raises(NoSuchLabelError):
        testonto.get_by_label("TestClassClass", prefix="models")

    assert testonto.prefix == "testonto"
    assert testonto.get_imported_ontologies()[0].prefix == "models"

    assert testonto.get_by_label("models:TestClass") == testonto.get_by_label(
        "TestClass", prefix="models"
    )

    with pytest.raises(ValueError):
        testonto.get_by_label_all(" ")

    with pytest.raises(TypeError):
        testonto.get_by_label(1)


def test_prefix_emmo(emmo: "Ontology") -> None:
    """Test prefix in ontology"""
    from emmopy import get_emmo

    # Check that the prefix of emmo-inferred becomes emmo
    assert emmo.Atom.namespace.ontology.prefix == "emmo"
    assert emmo.get_by_label("Atom", prefix="emmo") == emmo.Atom
    assert emmo.get_by_label("emmo:Atom") == emmo.Atom
    assert emmo["emmo:Atom"] == emmo.Atom

    emmo_asserted = get_emmo("emmo")
    assert emmo_asserted.Atom.namespace.ontology.prefix == "emmo"
    assert (
        emmo_asserted.get_by_label("Atom", prefix="emmo") == emmo_asserted.Atom
    )
