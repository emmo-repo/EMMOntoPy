def test_import_foaf() -> None:
    """Test importing foaf

    This test serves more like an example
    """

    from ontopy import get_ontology

    skos = get_ontology('http://www.w3.org/2004/02/skos/core#').load()
    foaf = get_ontology("http://xmlns.com/foaf/0.1/")

    # Needed since foaf refer to skos without importing it
    foaf.imported_ontologies.append(skos)

    # Turn off label lookup.  Needed because foaf uses labels that are not
    # valid Python identifiers
    foaf._special_labels = ()

    # Now we can load foaf
    foaf.load()


    emmo = get_ontology().load()

    with emmo:

        class Person(emmo.Interpreter):
            equivalent_to = [foaf.Person]
