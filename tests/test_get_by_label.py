import pytest

from ontopy import get_ontology
from ontopy.ontology import NoSuchLabelError


def test_get_by_label_onto() -> None:
    """Test that label annotations are added correctly if they are not added before
    using get_by_label
    """
    import owlready2

    testonto = get_ontology("http://domain_ontology/new_ontology")
    testonto.new_entity("Class", owlready2.Thing)
    assert testonto._label_annotations == None
    assert testonto.get_by_label("Class") == testonto.Class


def test_get_by_label_all_onto() -> None:
    """Test that label annotations are added correctly if they are not added before
    using get_by_label_all
    """
    import owlready2

    testonto = get_ontology("http://domain_ontology/new_ontology")
    testonto.new_entity("Class", owlready2.Thing)
    assert testonto._label_annotations == None
    assert testonto.get_by_label_all("*") == [testonto.Class]


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
