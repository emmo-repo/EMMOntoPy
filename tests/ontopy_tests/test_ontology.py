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
