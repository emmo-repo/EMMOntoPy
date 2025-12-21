
def test_annotate_source():
    from ontopy import get_ontology
    from ontopy.ontology import _has_unabbreviated_triple
    from ontopy.testutils import ontodir
    from ontopy.utils import annotate_source

    testonto = get_ontology(ontodir / "testonto.ttl").load()

    assert not _has_unabbreviated_triple(
        testonto,
        "http://emmo.info/models#testclass",
        "http://www.w3.org/2000/01/rdf-schema#isDefinedBy",
        "http://emmo.info/models#",
    )

    annotate_source(testonto, imported=False)
    assert not _has_unabbreviated_triple(
        testonto,
        "http://emmo.info/models#testclass",
        "http://www.w3.org/2000/01/rdf-schema#isDefinedBy",
        "http://emmo.info/models#",
    )

    annotate_source(testonto, imported=True)
    assert _has_unabbreviated_triple(
        testonto,
        "http://emmo.info/models#testclass",
        "http://www.w3.org/2000/01/rdf-schema#isDefinedBy",
        "http://emmo.info/models#",
    )


def test_rename_iris():
    from ontopy import get_ontology
    from ontopy.testutils import ontodir
    from ontopy.ontology import (
        _get_unabbreviated_triples,
        _has_unabbreviated_triple,
    )
    from ontopy.utils import rename_iris

    testonto = get_ontology(ontodir / "testonto.ttl").load()

    assert "http://emmo.info/models#TestClass" not in testonto
    assert not _has_unabbreviated_triple(
        testonto,
        "http://emmo.info/models#TestClass",
        "http://www.w3.org/2004/02/skos/core#exactMatch",
        "http://emmo.info/models#testclass",
    )

    rename_iris(testonto)
    assert "http://emmo.info/models#TestClass" in testonto
    assert _has_unabbreviated_triple(
        testonto,
        "http://emmo.info/models#TestClass",
        "http://www.w3.org/2004/02/skos/core#exactMatch",
        "http://emmo.info/models#testclass",
        'http://www.w3.org/2001/XMLSchema#anyURI',
    )


def test_rename_ontologies():
    from ontopy import get_ontology
    from ontopy.testutils import ontodir
    from ontopy.ontology import (
        _get_unabbreviated_triples,
        _has_unabbreviated_triple,
    )
    from ontopy.utils import rename_ontology

    onto = get_ontology(ontodir / "ani.ttl").load()
    onto.iri = onto.base_iri.rstrip("/#")
    assert onto.base_iri == "https://w3id.org/emmo/domain/ani/"
    assert onto.iri == "https://w3id.org/emmo/domain/ani"
    assert onto.metadata.versionIRI == ["https://w3id.org/emmo/domain/ani/0.1"]
    assert {o.base_iri for o in onto.get_imported_ontologies(True)} == {
        "https://w3id.org/emmo/domain/animal#",
        "https://w3id.org/emmo/domain/animal/birds#",
        "https://w3id.org/emmo/domain/animal/vertebrates#",
        "https://w3id.org/emmo/domain/mammal#",
    }
    assert {o.metadata.versionIRI[0] for o in onto.get_imported_ontologies(True)} == {
        "https://w3id.org/emmo/domain/animal/0.1",
        "https://w3id.org/emmo/domain/animal/0.1/birds",
        "https://w3id.org/emmo/domain/animal/0.1/vertebrates",
        "https://w3id.org/emmo/domain/mammal/0.1",
    }

    rename_ontology(onto, "/emmo/domain/", "/emmo/application/")
    assert onto.base_iri == "https://w3id.org/emmo/application/ani/"
    assert onto.iri == "https://w3id.org/emmo/application/ani"
    assert onto.metadata.versionIRI == ["https://w3id.org/emmo/application/ani/0.1"]
    assert {o.base_iri for o in onto.get_imported_ontologies(True)} == {
        "https://w3id.org/emmo/application/animal#",
        "https://w3id.org/emmo/application/animal/birds#",
        "https://w3id.org/emmo/application/animal/vertebrates#",
        "https://w3id.org/emmo/application/mammal#",
    }
    assert {o.metadata.versionIRI[0] for o in onto.get_imported_ontologies(True)} == {
        "https://w3id.org/emmo/application/animal/0.1",
        "https://w3id.org/emmo/application/animal/0.1/birds",
        "https://w3id.org/emmo/application/animal/0.1/vertebrates",
        "https://w3id.org/emmo/application/mammal/0.1",
    }

    rename_ontology(onto, "/0.1", "/0.2")
    assert onto.base_iri == "https://w3id.org/emmo/application/ani/"
    assert onto.iri == "https://w3id.org/emmo/application/ani"
    assert onto.metadata.versionIRI == ["https://w3id.org/emmo/application/ani/0.2"]
    assert {o.base_iri for o in onto.get_imported_ontologies(True)} == {
        "https://w3id.org/emmo/application/animal#",
        "https://w3id.org/emmo/application/animal/birds#",
        "https://w3id.org/emmo/application/animal/vertebrates#",
        "https://w3id.org/emmo/application/mammal#",
    }
    assert {o.metadata.versionIRI[0] for o in onto.get_imported_ontologies(True)} == {
        "https://w3id.org/emmo/application/animal/0.2",
        "https://w3id.org/emmo/application/animal/0.2/birds",
        "https://w3id.org/emmo/application/animal/0.2/vertebrates",
        "https://w3id.org/emmo/application/mammal/0.2",
    }


def test_preferred_language():
    from ontopy import get_ontology
    from ontopy.testutils import ontodir
    from ontopy.utils import get_preferred_language

    onto = get_ontology(ontodir / "animal" / "vertebrates.ttl").load()
    pl = onto.Vertebrate.prefLabel
    assert get_preferred_language(pl) == "Vertebrate"
    assert get_preferred_language(pl, "en") == "Vertebrate"
    assert get_preferred_language(pl, "no") == "Virveldyr"
    assert get_preferred_language(pl, "it") == "Vertebrate"


def test_datatype_class():
    from ontopy.utils import get_datatype_class

    Datatype = get_datatype_class()
    assert "Datatype" in repr(Datatype)
