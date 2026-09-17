"""Test ontodoc"""

import os

import pytest


# if True:
def test_ontodoc():
    """Test ontodoc."""
    from ontopy import get_ontology
    from ontopy.ontodoc_rst import (
        OntologyDocumentation,
        ReferenceDocumentation,
    )
    from ontopy.testutils import ontodir
    import owlready2

    # onto = get_ontology("https://w3id.org/emmo/1.0.0-rc1").load()
    onto = get_ontology(ontodir / "mammal.ttl").load()
    # onto.sync_reasoner(include_imported=True)

    od = OntologyDocumentation(
        onto, recursive=True, iri_regex="https://w3id.org/emmo"
    )
    ref = ReferenceDocumentation(
        onto,
        recursive=True,
        iri_regex="https://w3id.org/emmo",
        title="Mammal Reference",
    )

    od.add_reference(
        onto,
        recursive=True,
        iri_regex="https://w3id.org/emmo",
        title="Second Mammal Reference",
        docfile="mammal-second.rst",
        subsections="classes",
    )

    assert "Mammal Reference" in ref.get_refdoc()
    combined = od.get_combined_refdoc()
    assert "Reference Index" in combined
    assert "Second Mammal Reference" in combined
    assert od.get_refdoc(reference_index=1) == od.get_refdoc(
        reference_index=1,
        subsections="classes",
    )
    print(od.get_refdoc())


def test_ontodoc_slash_namespace_internal_links():
    """Internal links should stay distinct for same labels across ontologies."""
    import owlready2

    from ontopy import get_ontology
    from ontopy.ontodoc_rst import ReferenceDocumentation

    onto = get_ontology("http://example.com/onto/")
    onto2 = get_ontology("http://example.com/anotheronto/")
    onto.imported_ontologies.append(onto2)

    with onto2:

        class Animal(owlready2.Thing):
            pass

    with onto:

        class Animal(owlready2.Thing):
            pass

        class Dog(Animal, onto2.Animal):
            pass

    doc = ReferenceDocumentation(onto, imported=False).get_refdoc(
        subsections="classes"
    )

    assert '<div id="Animal"></div>' in doc
    assert "href='#http://example.com/onto/Animal'" not in doc
    assert "href='#http://example.com/anotheronto/Animal'" not in doc
    assert (
        "<a href='#Animal' onclick=\"if(!document.getElementById('Animal'))"
        "{window.location.href='http://example.com/onto/Animal'; "
        'return false;}">Animal</a>'
    ) in doc
    assert ("<a href='http://example.com/anotheronto/Animal'>Animal</a>") in doc
    assert (
        "<a href='#Animal' onclick=\"if(!document.getElementById('Animal'))"
        "{window.location.href='http://example.com/anotheronto/Animal'; "
        'return false;}">Animal</a>'
    ) not in doc
