from emmo import get_ontology


emmo = get_ontology(
    'https://raw.githubusercontent.com/emmo-repo/EMMO/v1.0.0/emmo.owl')
emmo.load()
