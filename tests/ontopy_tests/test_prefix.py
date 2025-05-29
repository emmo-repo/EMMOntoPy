from typing import TYPE_CHECKING
import pytest
from ontopy.utils import NoSuchLabelError
import warnings

from pathlib import Path


def test_prefix() -> None:
    """Test prefix in ontology"""
    from emmopy import get_emmo
    from ontopy import get_ontology

    emmo = get_emmo()
    repo_dir = Path(__file__).resolve().parent.parent.parent
    onto_dir = repo_dir / "tests" / "testonto"

    testonto = get_ontology(onto_dir / "testonto.ttl").load()

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
    from emmopy import get_emmo

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
