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


def test_copy_with_save(testonto: "Ontology", tmp_path: "Path") -> None:
    """Test saving an ontology and then copying it.
    When saving an ontology without keeping the python name triples
    it is actually copied before saving.

    This test checks that the local ontology is not changed when
    saving and that saving is done with or without python name triples
    as requested.
    """

    from ontopy import get_ontology
    from ontopy.utils import NoSuchLabelError

    def python_name_triples(ontology):
        return ontology.get_triples(
            s=None,
            p=ontology._abbreviate(
                "http://www.lesfleursdunormal.fr/static/_downloads/"
                "owlready_ontology.owl#python_name"
            ),
            o=None,
        )

    assert len(list(python_name_triples(testonto))) == 0

    # owlready2 adds python_name triples for properties
    testonto.sync_python_names()

    assert len(list(python_name_triples(testonto))) == 3

    # save, not keeping python name triples in the saved ontology
    testonto.save(
        tmp_path / "testonto_1.ttl",
        keep_python_names=False,
        recursive=True,
        write_catalog_file=True,
    )

    # load the saved ontology and check that python name triples are not there
    testonto1 = get_ontology(tmp_path / "testonto_1.ttl").load()

    assert len(list(python_name_triples(testonto1))) == 0

    # check that the python name triples are still in the ontology

    assert len(list(python_name_triples(testonto))) == 3

    # save, keeping python name triples in the saved ontology
    testonto.save(tmp_path / "testonto_2.ttl", keep_python_names=True)

    # load the saved ontology and check that python name triples are there
    testonto2 = get_ontology(tmp_path / "testonto_2.ttl").load()

    assert len(list(python_name_triples(testonto2))) == 3

    assert testonto2 == testonto


def test_copy_emmo(emmo: "Ontology") -> None:
    """Test copying the emmo ontology"""

    from emmopy import get_emmo

    new_emmo = emmo.copy()

    assert new_emmo == emmo

    emmo_from_web = get_emmo()

    assert new_emmo == emmo_from_web
