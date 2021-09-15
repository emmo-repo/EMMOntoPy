def test_load() -> None:
    import sys
    import os

    # Add emmo to sys path
    thisdir = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..')))
    from ontopy import get_ontology  # noqa: E402, F401


    # Check that the defaults works
    emmo = get_ontology('emmo').load()  # ttl format
    assert emmo.Atom.prefLabel.first() == 'Atom'

    emmo = get_ontology('emmo-inferred').load()
    assert emmo.Atom.prefLabel.first() == 'Atom'

    emmo = get_ontology('emmo-development').load()  # ttl format
    assert emmo.Atom.prefLabel.first() == 'Atom'

    emmo = get_ontology('https://emmo-repo.github.io/latest-stable/'
                        'emmo-inferred.owl').load()  # owl format
    assert emmo.Atom.prefLabel.first() == 'Atom'


    # Load a local ontology with catalog
    testonto = os.path.join(os.path.dirname(__file__), 'testonto', 'testonto.ttl')
    o = get_ontology(testonto).load()
    assert o.TestClass.prefLabel.first() == 'TestClass'


    # Use catalog file when downloading from web
    o = get_ontology(
        'https://raw.githubusercontent.com/BIG-MAP/BattINFO/master/'
        'battinfo.ttl').load()
    assert o.Electrolyte.prefLabel.first() == 'Electrolyte'
