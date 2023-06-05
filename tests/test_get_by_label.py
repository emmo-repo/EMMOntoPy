import pytest

from ontopy import get_ontology
from ontopy.ontology import NoSuchLabelError


# Loading emmo-inferred where everything is sqashed into one ontology
emmo = get_ontology().load()
assert emmo[emmo.Atom.name] == emmo.Atom
assert emmo[emmo.Atom.iri] == emmo.Atom

# Load an ontology with imported sub-ontologies
onto = get_ontology(
    "https://raw.githubusercontent.com/BIG-MAP/BattINFO/master/battinfo.ttl"
).load()
assert onto.Electrolyte.prefLabel.en.first() == "Electrolyte"


# Check colon_in_name argument
onto.Atom.altLabel.append("Element:X")
with pytest.raises(NoSuchLabelError):
    onto.get_by_label("Element:X")

assert onto.get_by_label("Element:X", colon_in_label=True) == onto.Atom
