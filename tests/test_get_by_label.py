import pytest

from ontopy import get_ontology
from ontopy.ontology import NoSuchLabelError


def test_get_by_label_onto(repo_dir) -> None:
    """Test that label annotations are added correctly if they are not added before
    using get_by_label
    """
    import owlready2

    testonto = get_ontology("http://domain_ontology/new_ontology")
    testonto.new_entity("Class", owlready2.Thing)

    # THIS IS NOT NONE ANYMORE
    # assert testonto.label_annotations == None

    assert testonto.get_by_label("Class") == testonto.Class

    imported_onto = testonto.world.get_ontology(
        repo_dir / "tests" / "testonto" / "testonto.ttl"
    ).load()
    testonto.imported_ontologies.append(imported_onto)
    assert imported_onto.get_by_label("TestClass")
    assert imported_onto.get_by_label("models:TestClass")

    # THIS IS NOW DEPRECATED
    # testonto.set_default_label_annotations()

    assert testonto.get_by_label("TestClass")


def test_get_by_label_all_onto() -> None:
    """Test that label annotations are added correctly if they are not added before
    using get_by_label_all
    """
    import owlready2

    testonto = get_ontology("http://domain_ontology/new_ontology")
    testonto.new_entity("Class", owlready2.Thing)
    assert testonto.get_by_label_all("*") == {testonto.Class}
    testonto.new_annotation_property(
        "SpecialAnnotation", owlready2.AnnotationProperty
    )
    testonto.Class.SpecialAnnotation.append("This is a comment")

    testonto.new_entity("Klasse", testonto.Class)

    # THESE NOW FAILS, SINCE prefLabel AND altLabel ARE NOT DEFINED in testonto
    # I THINK THIS IS THE RIGHT BEHAVIOUR.
    # assert testonto.Klasse.prefLabel == ["Klasse"]
    # testonto.Klasse.altLabel = "Class2"
    assert testonto.get_by_label_all("*") == {
        # testonto.prefLabel,
        # testonto.altLabel,
        testonto.Class,
        testonto.SpecialAnnotation,
        testonto.Klasse,
    }
    assert testonto.get_by_label_all("Class*") == {
        testonto.Class,
    }


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


import pytest

from ontopy import get_ontology
from ontopy.ontology import NoSuchLabelError


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
