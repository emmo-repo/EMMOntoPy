from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from pathlib import Path


# def test_metadata() -> None:
if True:
    from pathlib import Path
    from ontopy import get_ontology

    repo_dir = Path(__file__).resolve().parent.parent
    testonto = get_ontology(
        str(repo_dir / "tests" / "testonto" / "testonto.ttl")
    ).load()

    expected_keys = set(
        [
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "http://www.w3.org/2002/07/owl#imports",
            "http://www.w3.org/2002/07/owl#versionIRI",
            "http://purl.org/dc/terms/contributor",
            "http://purl.org/dc/terms/creator",
            testonto.metadata.namespace.hasFormat,
            "http://purl.org/dc/terms/publisher",
            testonto.metadata.namespace.homepage,
            # testonto.metadata.namespace.comment,
            # testonto.metadata.namespace.versionInfo,
            "http://purl.org/dc/terms/abstract",
            testonto.metadata.namespace.alternative,
            testonto.metadata.namespace.created,
            "http://purl.org/dc/terms/license",
            "http://purl.org/dc/terms/title",
            testonto.metadata.namespace.status,
            testonto.metadata.namespace.preferredNamespacePrefix,
            testonto.metadata.namespace.preferredNamespaceUri,
            "http://emmo.info/testonto#EMMO_1246b120_abbe_4840_b0f8_3e4348b24a17",
        ]
    )

    print(set(testonto.metadata.keys()).difference(expected_keys))
    assert set(testonto.metadata.keys()) == set(
        [
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "http://www.w3.org/2002/07/owl#imports",
            "http://www.w3.org/2002/07/owl#versionIRI",
            "http://purl.org/dc/terms/contributor",
            "http://purl.org/dc/terms/creator",
            testonto.metadata.namespace.hasFormat,
            "http://purl.org/dc/terms/publisher",
            testonto.metadata.namespace.homepage,
            "http://purl.org/dc/terms/comment",
            "http://www.w3.org/2002/07/owl#versionInfo",
            "http://purl.org/dc/terms/abstract",
            "http://purl.org/dc/terms/alternative",
            testonto.metadata.namespace.created,
            "http://iurl.org/dc/terms/title",
            "http://purl.org/ontology/bibo/status",
            "http://purl.org/vocab/vann/preferredNamespacePrefix",
            "http://purl.org/vocab/vann/preferredNamespaceUri",
            "http://emmo.info/testonto#EMMO_1246b120_abbe_4840_b0f8_3e4348b24a17",
        ]
    )

    assert testonto.metadata.items() == []
