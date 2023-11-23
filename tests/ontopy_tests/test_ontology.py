from pathlib import Path

from ontopy import get_ontology


thisdir = Path(__file__).resolve().parent

onto = get_ontology(thisdir.parent / "testonto" / "testonto.ttl").load()

onto2 = onto.copy()

assert len(list(onto2.classes())) == len(list(onto.classes()))
assert len(list(onto2.classes(True))) == len(list(onto.classes(True)))
