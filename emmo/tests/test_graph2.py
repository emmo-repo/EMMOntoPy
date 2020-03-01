#!/usr/bin/env python3
import sys
import os

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology

emmo = get_ontology()
emmo.load()


from emmo.graph import OntoGraph
g = OntoGraph(emmo, emmo.MaterialState, relations='all', addnodes=True,
              edgelabels=None)
g.save('MaterialState.png')

g = OntoGraph(emmo, emmo.ElementaryParticle, relations='all', addnodes=True,
              edgelabels=None)
g.save('ElementaryParticle.png')

g = OntoGraph(emmo, emmo.SIBaseUnit, relations='all', addnodes=True,
              edgelabels=True)
g.save('SIBaseUnit.png')
