#!/usr/bin/env python3
import sys
import os

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology
from emmo.graph import OntoGraph

# Create output directory
outdir = 'test_graph2'
if not os.path.exists(outdir):
    os.makedirs(outdir)
os.chdir(outdir)


emmo = get_ontology()
emmo.load()

g = OntoGraph(emmo, emmo.hasPart, leafs=('mereotopological', 'semiotical',
                                         'connected'))
g.save('hasPart.svg')

g.save('MaterialState.png')

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


# Used for figures

g = OntoGraph(emmo)
g.add_legend('all')
g.save('legend.png')


g = OntoGraph(emmo, emmo.EMMO, leafs=[emmo.Perspective, emmo.Elementary])
g.save('top.png')


leafs = set()
for s in emmo.Perspective.subclasses():
    leafs.update(s.subclasses())
g = OntoGraph(emmo, emmo.Perspective, leafs=leafs, parents=1)
g.save('Perspectives.png')


leafs = {emmo.Interpreter, emmo.Conventional, emmo.Icon, emmo.Observation,
         emmo.Object}
hidden = {emmo.SIUnitSymbol, emmo.SpecialUnit, emmo.Manufacturing,
          emmo.Engineered, emmo.PhysicalPhenomenon}
semiotic = emmo.get_branch(emmo.Holistic, leafs=leafs.union(hidden))
semiotic.difference_update(hidden)
g = OntoGraph(emmo)
g.add_entities(semiotic, relations='all', edgelabels=False)
g.save('Semiotic.png')
g.add_legend()
g.save('Semiotic+legend.png')


legend = OntoGraph(emmo)
legend.add_legend(g.get_relations())
legend.save('Semiotic-legend.png')
