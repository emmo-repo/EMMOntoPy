"""Test Ontology class methods."""

from ontopy import get_ontology
from ontopy.testutils import ontodir

animal = get_ontology(ontodir / "mammal.ttl").load()


# if True:
def test_find():
    """Test find() method."""
    m1 = (animal.chasing, animal.prefLabel, "chasing")
    for domain in "ontology", "imported", "world":
        assert m1 in animal.find("chas", domain=domain)
        assert m1 in animal.find("chas", domain=domain, regex=True)
        assert m1 in animal.find("chas", domain=domain, case_sensitive=True)
        assert m1 in animal.find(
            "chas", domain=domain, regex=True, case_sensitive=True
        )

        assert m1 in animal.find("Chas", domain=domain)
        assert m1 in animal.find("Chas", domain=domain, regex=True)
        assert m1 not in animal.find("Chas", domain=domain, case_sensitive=True)
        assert m1 not in animal.find(
            "Chas", domain=domain, regex=True, case_sensitive=True
        )
