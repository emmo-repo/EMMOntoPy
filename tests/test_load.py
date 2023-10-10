from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test_load(repo_dir: "Path", testonto: "Ontology") -> None:
    import pytest

    from ontopy import get_ontology
    from ontopy.ontology import EMMOntoPyException

    # Check that the defaults works
    emmo = get_ontology("emmo").load()  # ttl format
    assert str(emmo.Atom.prefLabel.first()) == "Atom"

    emmo = get_ontology("emmo-inferred").load()
    assert str(emmo.Atom.prefLabel.first()) == "Atom"

    emmo = get_ontology("emmo-development").load()  # ttl format
    assert str(emmo.Atom.prefLabel.first()) == "Atom"

    emmo = get_ontology(
        "https://emmo-repo.github.io/latest-stable/" "emmo-inferred.owl"
    ).load()  # owl format
    assert str(emmo.Atom.prefLabel.first()) == "Atom"

    # Load a local ontology with catalog
    assert str(testonto.TestClass.prefLabel.first()) == "TestClass"

    # Use catalog file when downloading from web
    onto = get_ontology(
        "https://raw.githubusercontent.com/BIG-MAP/BattINFO/master/"
        "battinfo.ttl"
    ).load()
    assert str(onto.Electrolyte.prefLabel.first()) == "Electrolyte"

    with pytest.raises(
        EMMOntoPyException,
        match="'URL error', <HTTPError 404: 'Not Found'>, 'http://emmo.info/non-existing/ontology'"
        # match="HTTP Error 404: https://emmo.info/non-existing/ontology: Not Found",
    ):
        get_ontology("http://emmo.info/non-existing/ontology#").load()

    # test loading of ontologies that only import subparts of emmo
    # with url to raw on github specified in catalog-file
    onto = get_ontology(
        "https://raw.githubusercontent.com/emmo-repo/"
        "datamodel-ontology/master/datamodel.ttl"
    ).load()
    assert onto.DataModel


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
