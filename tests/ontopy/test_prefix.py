from typing import TYPE_CHECKING
import pytest
from ontopy.utils import NoSuchLabelError

if TYPE_CHECKING:
    from pathlib import Path


def test_prefix(repo_dir: "Path") -> None:
    """Test get_version function in ontology"""
    from ontopy import get_ontology
    from emmopy import get_emmo

    ontopath = repo_dir / "tests" / "testonto"
    testonto = get_ontology(str(ontopath) + "/testonto.ttl").load()

    assert len(testonto.get_by_label_all("*")) == 2
    assert testonto.get_by_label_all("*", prefix="testonto") == [
        testonto.TestClass
    ]
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

    emmo = get_emmo("emmo")

    assert emmo.Atom.namespace.ontology.prefix == "emmo"
    assert emmo.get_by_label("Atom", prefix="emmo") == emmo.Atom

    # To be added when emmo-inferred is released with the correcto iri
    # emmo_inferred = get_emmo()

    # assert emmo_inferred.Atom.namespace.ontology.prefix == 'emmo'
    # assert emmo_inferred.get_by_label('Atom', prefix='emmo') == emmo_inferred.Atom
