from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ontopy.ontology import Ontology


@pytest.mark.skip("FOAF is currently unavailable.")
def test_import_foaf(emmo: "Ontology") -> None:
    """Test importing foaf

    foaf is the Friend-of-a-Friend ontology.

    This test serves more like an example.
    TODO: Move to `examples/`
    """
    from ontopy import get_ontology

    skos = get_ontology("http://www.w3.org/2004/02/skos/core#").load()
    foaf = get_ontology("http://xmlns.com/foaf/0.1/")

    # Needed since foaf refer to skos without importing it
    foaf.imported_ontologies.append(skos)

    # Turn off label lookup.  Needed because foaf uses labels that are not
    # valid Python identifiers
    foaf._special_labels = ()

    # Now we can load foaf
    foaf.load()

    with emmo:

        class Person(emmo.Interpreter):
            equivalent_to = [foaf.Person]
