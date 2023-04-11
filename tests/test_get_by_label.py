from ontopy import get_ontology


emmo = get_ontology().load()
assert emmo[emmo.Atom.name] == emmo.Atom
assert emmo[emmo.Atom.iri] == emmo.Atom
