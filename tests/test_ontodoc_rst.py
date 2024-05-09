"""Test ontodoc"""


# if True:
def test_ontodoc():
    """Test ontodoc."""
    from pathlib import Path

    from ontopy import get_ontology
    from ontopy.ontodoc_rst import OntologyDocumentation
    from ontopy.testutils import ontodir
    import owlready2

    # onto = get_ontology("https://w3id.org/emmo/1.0.0-rc1").load()
    onto = get_ontology(ontodir / "animal.ttl").load()
    # onto.sync_reasoner(include_imported=True)

    od = OntologyDocumentation(
        onto, recursive=True, iri_regex="https://w3id.org/emmo"
    )
    print(od.get_refdoc())
