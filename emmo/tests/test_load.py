#!/usr/bin/env python3
import sys
import os

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology  # noqa: E402, F401


# Check that the defaults works
emmo = get_ontology('emmo').load()  # owl format
assert emmo.Atom.prefLabel.first() == 'Atom'

emmo = get_ontology('emmo-inferred').load()
assert emmo.Atom.prefLabel.first() == 'Atom'

emmo = get_ontology('emmo-development').load()  # ttl format
assert emmo.Atom.prefLabel.first() == 'Atom'

# Load a local ontology with catalog
testonto = os.path.join(os.path.dirname(__file__), 'testonto', 'testonto.ttl')
o = get_ontology(testonto).load()
assert o.TestClass.prefLabel.first() == 'TestClass'


# Error in redirecting links on emmo.info, temporarily removed 01.07.2021
# Use catalog file when downloading from web
# o = get_ontology(
#    'https://raw.githubusercontent.com/BIG-MAP/BattINFO/master/'
#    'battinfo.ttl').load()
# assert o.Electrolyte.prefLabel.first() == 'Electrolyte'
