import pytest

from ontopy import get_ontology
from ontopy.ontology import NoSuchLabelError


def test_classes(repo_dir) -> None:
    """Test that classes are returned from imported ontologies when
    asked for, but not for the whole world
    """
    import ontopy
    import owlready2

    world = ontopy.World()
    testonto = world.get_ontology("http://domain_ontology/new_ontology")
    testonto.new_entity("Class", owlready2.Thing)

    imported_onto = world.get_ontology(
        repo_dir / "tests" / "testonto" / "testonto.ttl"
    ).load()
    testonto.imported_ontologies.append(imported_onto)

    assert set(testonto.classes(imported=True)) == {
        testonto.TestClass,
        testonto.get_by_label("models:TestClass"),
        testonto.Class,
    }
    assert set(imported_onto.classes(imported=True)) == {
        imported_onto.TestClass,
        imported_onto.get_by_label("models:TestClass"),
    }
    assert set(imported_onto.classes(imported=False)) == {
        imported_onto.TestClass
    }

    assert (
        set(testonto.individuals(imported=True)) == set()
    )  # We currently do not have examples with individuals.
    assert set(testonto.individuals(imported=False)) == set()

    assert set(testonto.object_properties(imported=True)) == {
        testonto.hasObjectProperty
    }
    assert set(testonto.object_properties(imported=False)) == set()

    assert set(testonto.annotation_properties(imported=True)) == {
        testonto.prefLabel,
        testonto.altLabel,
        testonto.hasAnnotationProperty,
    }
    assert set(testonto.annotation_properties(imported=False)) == set()

    assert set(testonto.data_properties(imported=True)) == {
        testonto.hasDataProperty
    }
    assert set(testonto.data_properties(imported=False)) == set()
