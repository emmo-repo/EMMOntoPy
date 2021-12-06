from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
    from pathlib import Path


def test_get_version(repo_dir: "Path") -> None:
    """Test get_version function in ontology"""
    from ontopy import get_ontology

    ontopath = repo_dir / "tests" / "testonto"
    testonto = get_ontology(str(ontopath) + "/testonto.ttl").load()
    assert (
        testonto.get_version(as_iri=True) == "http://emmo.info/testonto/0.1.0"
    )
    assert testonto.get_version() == "0.1.0"

    testonto_noVersionIRI = get_ontology(
        str(ontopath) + "/testonto_noVersionIRI.ttl"
    ).load()
    assert testonto_noVersionIRI.get_version() == "v0.1.0"
    with pytest.raises(TypeError):
        testonto_noVersionIRI.get_version(as_iri=True)
    testonto_noVersionIRI_noVersionInfo = get_ontology(
        str(ontopath) + "/testonto_noVersionIRI_noVersionInfo.ttl"
    ).load()
    with pytest.raises(TypeError):
        testonto_noVersionIRI_noVersionInfo.get_version()
