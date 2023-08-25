import pytest

from ontopy import get_ontology
from ontopy.ontology import NoSuchLabelError


def test_get_by_label_onto(repo_dir) -> None:
    """Test that label annotations are added correctly if they are not added before
    using get_by_label
    """
    import owlready2
    from ontopy.ontology import DEFAULT_LABEL_ANNOTATIONS

    # create ontology with one class and check that it is found
    testonto = get_ontology("http://domain_ontology/new_ontology")
    testonto.new_entity("Class", owlready2.Thing)

    assert testonto.label_annotations == DEFAULT_LABEL_ANNOTATIONS
    assert testonto.get_by_label("Class") == testonto.Class
    assert testonto.get_by_label_all("*") == {testonto.Class}

    testonto.new_annotation_property(
        "SpecialAnnotation", owlready2.AnnotationProperty
    )
    testonto.Class.SpecialAnnotation.append("This is a comment")

    testonto.new_entity("Klasse", testonto.Class)

    with pytest.raises(AttributeError):
        assert testonto.Klasse.prefLabel == ["Klasse"]

    assert testonto.get_by_label_all("*") == {
        testonto.Class,
        testonto.SpecialAnnotation,
        testonto.Klasse,
    }

    # Add prefLabel to ontology
    preflabel = testonto.new_annotation_property(
        "prefLabel",
        parent=[owlready2.AnnotationProperty],
    )
    preflabel.iri = "http://www.w3.org/2004/02/skos/core#prefLabel"

    # After prefLabel was added to the ontology, prefLabels can be accessed
    with pytest.raises(AssertionError):
        assert testonto.prefLabel.prefLabel == ["prefLabel"]
    testonto.prefLabel.prefLabel = "prefLabel"
    assert testonto.prefLabel.prefLabel == ["prefLabel"]

    with pytest.raises(AssertionError):
        assert testonto.Klasse.prefLabel == ["Klasse"]

    testonto.new_entity("UnderKlasse", testonto.Klasse)
    assert testonto.UnderKlasse.prefLabel == ["UnderKlasse"]

    assert testonto.get_by_label_all("*") == {
        testonto.prefLabel,
        testonto.Class,
        testonto.SpecialAnnotation,
        testonto.Klasse,
        testonto.UnderKlasse,
    }
    assert testonto.get_by_label_all("Class*") == {
        testonto.Class,
    }

    # Check that imported ontologies are searched
    imported_onto = testonto.world.get_ontology(
        repo_dir / "tests" / "testonto" / "testonto.ttl"
    ).load()
    testonto.imported_ontologies.append(imported_onto)
    assert imported_onto.get_by_label("TestClass")
    assert imported_onto.get_by_label("models:TestClass")

    assert testonto.get_by_label("TestClass")

    assert testonto.get_by_label_all("Clas*", exact_match=True) == {}


def test_get_by_label_emmo(emmo: "Ontology") -> None:
    # Loading emmo-inferred where everything is sqashed into one ontology
    emmo = get_ontology().load()
    assert emmo[emmo.Atom.name] == emmo.Atom
    assert emmo[emmo.Atom.iri] == emmo.Atom

    # Load an ontology with imported sub-ontologies
    onto = get_ontology(
        "https://raw.githubusercontent.com/BIG-MAP/BattINFO/master/battinfo.ttl"
    ).load()
    assert onto.Electrolyte.prefLabel.first() == "Electrolyte"

    # Check colon_in_name argument
    onto.Atom.altLabel.append("Element:X")
    with pytest.raises(NoSuchLabelError):
        onto.get_by_label("Element:X")

    assert onto.get_by_label("Element:X", colon_in_label=True) == onto.Atom
