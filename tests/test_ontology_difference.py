"""Test the Ontology.difference() methode"""


if True:
    from pathlib import Path
    from ontopy import get_ontology

    repo_dir = Path(__file__).resolve().parent.parent
    onto_dir = repo_dir / "tests" / "testonto"
    print(repo_dir)

    testonto = get_ontology(onto_dir / "testonto.ttl").load()
    testontowi = get_ontology(onto_dir / "testonto_w_individual.ttl").load()

    diff = testonto.difference(testontowi)
    diffwi = testontowi.difference(testonto)
    assert not diff.intersection(diffwi)

    triple1 = (
        "http://emmo.info/testonto#testindividual",
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
        "http://www.w3.org/2002/07/owl#NamedIndividual",
    )
    assert triple1 in diffwi
    assert triple1 not in diff
