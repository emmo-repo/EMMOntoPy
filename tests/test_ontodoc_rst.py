"""Test ontodoc"""

if True:
    # def test_ontodoc():
    """Test ontodoc."""
    from pathlib import Path

    from ontopy import get_ontology
    from ontopy.ontodoc_rst import OntologyDocumentation
    import owlready2

    # emmo = get_ontology("https://w3id.org/emmo/1.0.0-rc1").load()
    emmo = get_ontology("../EMMO/emmo.ttl").load()
    # emmo.sync_reasoner(include_imported=True)

    od = OntologyDocumentation(
        emmo, recursive=True, iri_regex="https://w3id.org/emmo"
    )
    print(od.get_refdoc())
