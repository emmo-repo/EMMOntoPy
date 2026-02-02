"""Test Ontology class methods."""

from ontopy import get_ontology
from ontopy.testutils import ontodir

animal = get_ontology(ontodir / "mammal.ttl").load()


def test_find():
    """Test find() method."""
    m1 = (animal.chasing, animal.prefLabel, "chasing")
    m2 = (animal.Mouse, animal.prefLabel, "Mouse")
    # for domain in "ontology", "imported", "world":
    assert m1 not in animal.find("chas", domain="ontology")
    assert m2 in animal.find("Mouse", domain="ontology")
    assert m2 in animal.find("Mouse", domain="ontology", regex=True)
    assert m2 in animal.find("Mouse", domain="ontology", case_sensitive=True)
    assert m2 in animal.find(
        "Mouse", domain="ontology", regex=True, case_sensitive=True
    )
    assert m2 not in animal.find(
        "mouse", domain="ontology", case_sensitive=True
    )
    assert m2 in animal.find("mouse", domain="ontology", case_sensitive=False)

    assert m1 in animal.find("chas", domain="imported", regex=True)
    assert m1 in animal.find("chas", domain="imported", case_sensitive=True)
    assert m1 in animal.find(
        "chas", domain="imported", regex=True, case_sensitive=True
    )

    assert m1 in animal.find("Chas", domain="imported")
    assert m1 in animal.find("Chas", domain="imported", regex=True)
    assert m1 not in animal.find("Chas", domain="imported", case_sensitive=True)
    assert m1 not in animal.find(
        "Chas", domain="imported", regex=True, case_sensitive=True
    )

    assert m2 not in animal.imported_ontologies[0].find(
        "mouse", domain="ontology"
    )
    assert m2 in animal.imported_ontologies[0].find(
        "mouse", domain="world", regex=True
    )


def test_get_iri():
    """Test get_iri() method."""
    assert animal.get_iri() == "https://w3id.org/emmo/domain/mammal"


def test__get_unabbreviated_triples():
    """Test _get_unabbreviated_triples()."""
    from ontopy.ontology import _get_unabbreviated_triples

    m = "https://w3id.org/emmo/domain/mammal#"
    a = "https://w3id.org/emmo/domain/animal#"
    skos = "http://www.w3.org/2004/02/skos/core#"

    assert list(
        _get_unabbreviated_triples(animal, predicate=a + "chasing")
    ) == [(m + "Tom", a + "chasing", m + "Jerry")]
    assert list(_get_unabbreviated_triples(animal, obj=m + "Jerry")) == [
        (m + "Tom", a + "chasing", m + "Jerry")
    ]

    triples = list(
        _get_unabbreviated_triples(animal, predicate=skos + "prefLabel")
    )
    assert len(triples) == 10

    triples = list(
        _get_unabbreviated_triples(
            animal, predicate=skos + "prefLabel", datatype="@en"
        )
    )
    assert len(triples) == 10

    triples = list(
        _get_unabbreviated_triples(animal.world, predicate=skos + "prefLabel")
    )
    assert len(triples) == 24

    assert list(
        _get_unabbreviated_triples(
            animal, predicate=skos + "prefLabel", obj="Cat"
        )
    ) == [(m + "Cat", skos + "prefLabel", '"Cat"@en')]
    assert list(
        _get_unabbreviated_triples(
            animal, predicate=skos + "prefLabel", obj="Cat", datatype="@en"
        )
    ) == [(m + "Cat", skos + "prefLabel", '"Cat"@en')]
    assert list(_get_unabbreviated_triples(animal, "no-match")) == []


def test__has_unabbreviated_triple():
    """Test _has_unabbreviated_triple()."""
    from ontopy.ontology import _has_unabbreviated_triple

    m = "https://w3id.org/emmo/domain/mammal#"
    a = "https://w3id.org/emmo/domain/animal#"
    skos = "http://www.w3.org/2004/02/skos/core#"

    assert _has_unabbreviated_triple(
        animal, m + "Tom", a + "chasing", m + "Jerry"
    )
    assert _has_unabbreviated_triple(
        animal, m + "Cat", skos + "prefLabel", "Cat"
    )
    assert _has_unabbreviated_triple(
        animal, m + "Cat", skos + "prefLabel", "Cat", "@en"
    )
    assert not _has_unabbreviated_triple(
        animal, m + "Cat", skos + "prefLabel", "Cat", "@no"
    )
    assert not _has_unabbreviated_triple(animal, "no-match")
