from ontopy import get_ontology


# Loading emmo-inferred where everything is sqashed into one ontology
emmo = get_ontology().load()
assert emmo[emmo.Atom.name] == emmo.Atom
assert emmo[emmo.Atom.iri] == emmo.Atom

# Load an ontology with imported sub-ontologies
onto = get_ontology(
    "https://raw.githubusercontent.com/BIG-MAP/BattINFO/master/battinfo.ttl"
).load()
assert onto.Electrolyte.prefLabel.first() == "Electrolyte"
