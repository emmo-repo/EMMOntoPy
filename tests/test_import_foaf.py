from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ontopy.ontology import Ontology


# @pytest.mark.skip("FOAF is currently unavailable.")
# def test_import_foaf(emmo: "Ontology") -> None:
if True:
    """Test importing foaf

    foaf is the Friend-of-a-Friend ontology.

    This test serves more like an example.
    TODO: Move to `examples/`
    """
    from ontopy import get_ontology

    emmo = get_ontology("emmo").load()
    # skos = get_ontology("https://www.w3.org/2009/08/skos-reference/skos.html#SKOS-RDF").load()
    foaf = get_ontology("http://xmlns.com/foaf/spec/index.rdf").load()

    # Needed since foaf refer to skos without importing it
    # foaf.imported_ontologies.append(skos)

    # Turn off label lookup.  Needed because foaf uses labels that are not
    # valid Python identifiers
    # foaf._special_labels = ()

    # Now we can load foaf
    # foaf.load()

    with emmo:

        class Person(emmo.Interpreter):
            equivalent_to = [foaf.Person]
