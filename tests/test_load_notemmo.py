from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
    from pathlib import Path

from pathlib import Path


def test_load_rdfs() -> None:
    """Test to load non-emmo based ontologies rdf and rdfs"""
    from ontopy import get_ontology

    rdf_onto = get_ontology(
        "https://www.w3.org/1999/02/22-rdf-syntax-ns.ttl"
    ).load(emmo_based=False)
    rdfs_onto = get_ontology("https://www.w3.org/2000/01/rdf-schema.ttl").load(
        emmo_based=False
    )
    rdfs_onto.Class  # Needed to initialize rdfs_onto
    assert rdf_onto.HTML.is_a[0].iri == rdfs_onto.Datatype.iri


def test_load_schema() -> None:
    """Test to load non-emmo based ontologies rdf and rdfs"""
    from ontopy import get_ontology

    repo_dir = Path(__file__).resolve().parent
    onto = get_ontology(repo_dir / "testonto" / "minischema.ttl").load(
        emmo_based=False
    )
    assert list(onto.classes()) == [onto.AMRadioChannel]
    onto_owlclass = get_ontology(
        repo_dir / "testonto" / "minischema_owlclass.ttl"
    ).load(emmo_based=False)
    assert list(onto_owlclass.classes()) == [onto_owlclass.AMRadioChannel]

    assert list(onto.properties()) == ["https://schema.org/abridged"]

    # Should be:
    # assert list(onto.properties()) == [onto.abridged]


# def test_import_foaf(emmo: "Ontology") -> None:
#    """Test importing foaf
#
#    foaf is the Friend-of-a-Friend ontology.
#
#    This test serves more like an example.
#    TODO: Move to `examples/`
#    """
#    from ontopy import get_ontology
#
#    emmo = get_ontology("emmo").load()
#    # skos = get_ontology("https://www.w3.org/2009/08/skos-reference/skos.html#SKOS-RDF").load()
#    foaf = get_ontology("http://xmlns.com/foaf/spec/index.rdf").load()
#
#    # Needed since foaf refer to skos without importing it
#    # foaf.imported_ontologies.append(skos)
#
#    # Turn off label lookup.  Needed because foaf uses labels that are not
#    # valid Python identifiers
#    # foaf._special_labels = ()
#
#    # Now we can load foaf
#    # foaf.load()
#
#    with emmo:
#
#        class Person(emmo.Interpreter):
#            equivalent_to = [foaf.Person]


# def test_load_qudt:
# if True:
#    units = get_ontology("http://qudt.org/2.1/vocab/unit").load()
# rdflib comppains. Apparently it cannot serialize it once it is loaded.
