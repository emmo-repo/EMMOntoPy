#!/usr/bin/env python3
import sys
import os

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology

from emmo.graph import (OntoGraph, plot_modules, get_module_dependencies,
                        check_module_dependencies)


emmo = get_ontology()
emmo.load()

g = OntoGraph(emmo, emmo.MaterialState, relations='all', addnodes=True,
              edgelabels=None)
g.save('MaterialState.png')

g = OntoGraph(emmo, emmo.ElementaryParticle, relations='all', addnodes=True,
              edgelabels=None)
g.save('ElementaryParticle.png')

g = OntoGraph(emmo, emmo.SIBaseUnit, relations='all', addnodes=True,
              edgelabels=True)
g.save('SIBaseUnit.png')

g = OntoGraph(emmo, emmo.EMMORelation, relations='all', edgelabels=None)
g.save('EMMORelation.png')

g = OntoGraph(emmo, emmo.Quantity,
              leafs=[emmo.DerivedQuantity, emmo.BaseQuantity,
                     emmo.PhysicalConstant],
              relations='all', edgelabels=None, addnodes=True,
              addconstructs=True)
g.save('Quantity.svg')

g = OntoGraph(emmo, emmo.EMMO, leafs=[emmo.Perspective, emmo.Elementary],
              relations='isA', edgelabels=None, addnodes=False,
              addconstructs=False)
g.save('top.svg')


leafs = set()
for s in emmo.Perspective.subclasses():
    leafs.update(s.subclasses())
g = OntoGraph(emmo, emmo.Perspective, leafs=leafs, parents=1,
              relations='isA', edgelabels=None, addnodes=False,
              addconstructs=False)
g.save('Perspectives.svg')
