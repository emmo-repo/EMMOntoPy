from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test_load(repo_dir: "Path", testonto: "Ontology") -> None:
    from ontopy import get_ontology

    # Check that the defaults works
    emmo = get_ontology("emmo").load()  # ttl format
    assert emmo.Atom.prefLabel.first() == "Atom"

    emmo = get_ontology("emmo-inferred").load()
    assert emmo.Atom.prefLabel.first() == "Atom"

    emmo = get_ontology("emmo-development").load()  # ttl format
    assert emmo.Atom.prefLabel.first() == "Atom"

    emmo = get_ontology(
        "https://emmo-repo.github.io/latest-stable/" "emmo-inferred.owl"
    ).load()  # owl format
    assert emmo.Atom.prefLabel.first() == "Atom"

    # Load a local ontology with catalog
    assert testonto.TestClass.prefLabel.first() == "TestClass"

    # Use catalog file when downloading from web
    onto = get_ontology(
        "https://raw.githubusercontent.com/BIG-MAP/BattINFO/master/"
        "battinfo.ttl"
    ).load()
    assert onto.Electrolyte.prefLabel.first() == "Electrolyte"


def test_load_rdfs() -> None:
    from ontopy import get_ontology

    # Test loading non-EMMO-based ontologies rdf and rdfs
    rdf_onto = get_ontology(
        "https://www.w3.org/1999/02/22-rdf-syntax-ns.ttl"
    ).load(emmo_based=False)
    rdfs_onto = get_ontology("https://www.w3.org/2000/01/rdf-schema.ttl").load(
        emmo_based=False
    )
    rdfs_onto.Class  # Needed to initialize rdfs_onto
    assert type(rdf_onto.HTML).iri == rdfs_onto.Datatype.iri
