#!/usr/bin/env python3
import sys
import os

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology  # noqa: E402, F401

# Load a local ontology with catalog
testonto = os.path.join(os.path.dirname(__file__), 'testonto', 'testonto.ttl')
o = get_ontology(testonto).load()
assert o.TestClass.prefLabel.first() == 'TestClass'

assert o.models.SpecialTestClass.prefLabel.first() == 'SpecielTestClass'
assert o.models.SpecialTestClass.namespace.name == 'models'

assert o.testonto.SpecialTestClass.prefLabel.first() == 'SpecialTestClass'
assert o.testonto.SpecialTestClass.namespace.name == 'testonto'

assert o.get_by_label('SpecialTestClass', namespace = 'models').namespace.name == 'models'



