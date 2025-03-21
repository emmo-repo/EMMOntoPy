from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from pathlib import Path


def test_metadata() -> None:
    from pathlib import Path
    from ontopy import get_ontology

    repo_dir = Path(__file__).resolve().parent.parent
    testonto = get_ontology(
        str(repo_dir / "tests" / "testonto" / "testonto.ttl")
    ).load()

    expected_keys = set(
        [
            "http://purl.org/vocab/vann/preferredNamespacePrefix",
            "http://purl.org/vocab/vann/preferredNamespaceUri",
            "http://purl.org/dc/terms/created",
            "http://purl.org/dc/terms/alternative",
            "http://purl.org/ontology/bibo/status",
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "http://www.w3.org/2000/01/rdf-schema#comment",
            "http://purl.org/dc/terms/abstract",
            "http://purl.org/dc/terms/license",
            "http://purl.org/dc/terms/title",
            "http://emmo.info/testonto#EMMO_1246b120_abbe_4840_b0f8_3e4348b24a17",
            "http://www.w3.org/2002/07/owl#versionIRI",
            "http://www.w3.org/2002/07/owl#imports",
            "http://purl.org/dc/terms/contributor",
            "http://www.w3.org/2002/07/owl#versionInfo",
            "http://purl.org/dc/terms/creator",
            "http://purl.org/dc/terms/hasFormat",
            "http://xmlns.com/foaf/0.1/homepage",
        ]
    )

    # versionInfo and comment are not defined in the ontology
    # but are still available predefined in owlready2
    assert set(testonto.metadata.keys()) == expected_keys

    items_dict = dict(testonto.metadata.items())

    assert set(items_dict.keys()) == set(testonto.metadata.keys())

    assert testonto.metadata["http://purl.org/dc/terms/title"] == [
        "The test ontology (TESTONTO)"
    ]
    assert testonto.metadata.title == ["The test ontology (TESTONTO)"]

    assert testonto.metadata.creator == [
        "https://orcid.org/0000-0001-8869-3718",
        "http://emmo.info/testonto#JesperFriis",
    ]

    assert testonto.metadata.versionInfo == ["0.2.0"]
