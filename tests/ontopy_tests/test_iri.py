import re
from pathlib import Path
import os

from ontopy import get_ontology


# if True:
def test_iri():
    thisdir = Path(__file__).resolve().parent
    ontodir = thisdir.parent / "testonto"
    outdir = thisdir.parent / "output"

    onto = get_ontology(ontodir / "testonto.ttl").load()
    onto.base_iri = "http://example.com/onto"
    onto.iri = "http://example.com/onto/testonto"
    if os.path.exists(outdir / "testonto.ttl"):
        os.remove(outdir / "testonto.ttl")
    onto.save(outdir / "testonto.ttl")

    # Load saved ontology and make sure that base_iri and iri are stored
    # correctly
    with open(outdir / "testonto.ttl", mode="r") as f:
        ttl = f.read()
    assert re.findall(r"@prefix : (\S+) \.", ttl) == [f"<{onto.base_iri}>"]
    assert re.findall(r"(\S+) a owl:Ontology", ttl) == [f"<{onto.iri}>"]
