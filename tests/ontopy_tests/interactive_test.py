# Please keep this file as a script that can be run interactive with
# "ipython -i"
from pathlib import Path

from .conftest import get_triples, has_triple
from ontopy import get_ontology

thisdir = Path(__file__).resolve().parent

path = thisdir / ".." / "testonto" / "testonto.ttl"
onto = get_ontology(path).load()

emmopath = thisdir / ".." / "testonto" / "emmo" / "emmo-squashed.ttl"

emmo = get_ontology(emmopath).load()
