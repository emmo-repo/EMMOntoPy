import pytest


def test_get_version() -> None:
    """Test get_version function in ontology"""
    from ontopy import get_ontology

    testonto = get_ontology("testonto/testonto.ttl").load()
    assert (
        testonto.get_version(as_iri=True) == "http://emmo.info/testonto/0.1.0"
    )
    assert testonto.get_version() == "0.1.0"

    testonto_noVersionIRI = get_ontology(
        "testonto/testonto_noVersionIRI.ttl"
    ).load()
    assert testonto_noVersionIRI.get_version() == "v0.1.0"
    with pytest.raises(TypeError):
        testonto_noVersionIRI.get_version(as_iri=True)
    testonto_noVersionIRI_noVersionInfo = get_ontology(
        "testonto/testonto_noVersionIRI_noVersionInfo.ttl"
    ).load()
    with pytest.raises(TypeError):
        testonto_noVersionIRI_noVersionInfo.get_version()
