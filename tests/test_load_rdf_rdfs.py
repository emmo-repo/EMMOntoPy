from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test_load(repo_dir: "Path") -> None:
    from ontopy import get_ontology

    # Test loading of non-EMMO-based ontologies rdf and rdfs
    rdf_onto = get_ontology(
        'https://www.w3.org/1999/02/22-rdf-syntax-ns.ttl').load(
            EMMObased=False)
    rdfs_onto = get_ontology(
        'https://www.w3.org/2000/01/rdf-schema.ttl').load(
            EMMObased=False)
    rdfs_onto.Class #  Needed to initialize rdfs_onto
    assert type(rdf_onto.HTML).iri == rdfs_onto.Datatype.iri
