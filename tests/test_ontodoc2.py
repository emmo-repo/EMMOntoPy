"""Test ontodoc"""


# if True:
def test_ontodoc():
    """Test ontodoc."""
    from pathlib import Path

    from ontopy.ontodoc2 import OntoDoc
    from ontopy import get_ontology
    import owlready2
    import owlready2.reasoning

    owlready2.reasoning.JAVA_MEMORY = 28000

    # emmo = get_ontology("https://w3id.org/emmo/1.0.0-rc1").load()
    emmo = get_ontology("../EMMO/emmo.ttl").load()
    # emmo.sync_reasoner(include_imported=True)

    # ontologies = emmo.get_imported_ontologies(True)
    # owlready2.sync_reasoner(ontologies)
