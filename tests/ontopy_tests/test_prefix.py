from typing import TYPE_CHECKING
import pytest
from ontopy.utils import NoSuchLabelError
import warnings

if TYPE_CHECKING:
    from pathlib import Path


def test_prefix():
    """Test prefix in ontology"""
    from ontopy.testutils import get_testonto

    testonto = get_testonto()

    print(testonto.get_by_label_all("*"))
    assert len(testonto.get_by_label_all("*")) == 15
    assert set(testonto.get_by_label_all("*", prefix="testonto")) == set(
        [
            testonto.alternative,
            testonto.homepage,
            testonto.status,
            testonto.preferredNamespacePrefix,
            testonto.preferredNamespaceUri,
            testonto.created,
            testonto.hasFormat,
            testonto.hasObjectProperty,
            testonto.TestClass,
            testonto.TestClass2,
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


def test_prefix_emmo() -> None:
    """Test prefix in ontology"""
    from ontopy.testutils import get_emmo

    emmo = get_emmo()

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


def test_prefix_emmo_unsquashed() -> None:
    """Test prefix in ontology"""
    from ontopy.testutils import get_emmo

    emmo = get_emmo(squashed=False)

    # Check that the prefix of emmo-inferred becomes emmo
    assert emmo.Atom.namespace.ontology.prefix == "physicalistic"
    assert emmo.get_by_label("Atom", prefix="physicalistic") == emmo.Atom
    assert emmo.get_by_label("physicalistic:Atom") == emmo.Atom
    assert emmo["physicalistic:Atom"] == emmo.Atom

    emmo_asserted = get_emmo("emmo")
    assert emmo_asserted.Atom.namespace.ontology.prefix == "emmo"
    assert (
        emmo_asserted.get_by_label("Atom", prefix="emmo") == emmo_asserted.Atom
    )
