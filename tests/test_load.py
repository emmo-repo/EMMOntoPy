from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from pathlib import Path


def test_load() -> None:
    # if True:
    from pathlib import Path
    from ontopy import get_ontology

    repo_dir = Path(__file__).resolve().parent.parent
    testonto = get_ontology(
        str(repo_dir / "tests" / "testonto" / "testonto.ttl")
    ).load()

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
        "https://emmo-repo.github.io/emmo-inferred.ttl"
    ).load()  # owl format
    assert str(emmo.Atom.prefLabel.first()) == "Atom"

    # Load a local ontology with catalog
    assert str(testonto.TestClass.prefLabel.first()) == "TestClass"

    # Use catalog file when downloading from web
    # This is tested in test_get_by_label in which some additional tests
    # are performed on labels.

    with pytest.raises(
        EMMOntoPyException,
        match="'URL error', <HTTPError 404: 'Not Found'>, 'http://emmo.info/non-existing/ontology'",
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
