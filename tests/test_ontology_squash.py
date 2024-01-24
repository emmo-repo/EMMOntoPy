"""Test the Ontology.save(squash=True, ...)"""


def test_ontology_squash():
    import re
    from pathlib import Path
    from ontopy import get_ontology

    repo_dir = Path(__file__).resolve().parent.parent
    onto_dir = repo_dir / "tests" / "testonto"
    out_dir = repo_dir / "tests" / "output"

    testonto = get_ontology(onto_dir / "testonto.ttl").load()

    testonto.save(out_dir / "testonto_squash.ttl", squash=True)

    with open(out_dir / "testonto_squash.ttl", "r") as f:
        txt = f.read()

    s = re.findall(r".* a owl:Ontology", txt)
    assert len(s) == 1
    assert s[0].startswith("<http://emmo.info/testonto>")
    assert len(re.findall(r"owl:imports", txt)) == 0
