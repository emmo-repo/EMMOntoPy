#!/usr/bin/env python3
import sys
import os

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology  # noqa: E402, F401
from emmo.graph import OntoGraph  # noqa: E402, F401

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


g = OntoGraph(emmo, emmo.Matter, relations='all', addnodes=True,
              edgelabels=None)
g.save('Matter.png')

g = OntoGraph(emmo, emmo.ElementaryParticle, relations='all', addnodes=True,
              edgelabels=None)
g.save('ElementaryParticle.png')

g = OntoGraph(emmo, emmo.SIBaseUnit, relations='all', addnodes=True,
              edgelabels=True,
              addconstructs=False, graph_attr={'rankdir': 'RL'})
g.add_legend()
g.save('SIBaseUnit.png')

g = OntoGraph(emmo, emmo.EMMORelation, relations='all', edgelabels=None)
g.save('EMMORelation.png')

g = OntoGraph(emmo, emmo.Quantity,
              leafs=[emmo.DerivedQuantity, emmo.BaseQuantity,
                     emmo.PhysicalConstant],
              relations='all', edgelabels=None, addnodes=True,
              addconstructs=True, graph_attr={'rankdir': 'RL'})
g.add_legend()
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


# Measurement
leafs = {emmo.Object}

hidden = {emmo.SIUnitSymbol, emmo.SpecialUnit, emmo.Manufacturing,
          emmo.Engineered, emmo.PhysicalPhenomenon,
          emmo.Icon, emmo.Interpretant, emmo.Index,
          emmo.SubjectiveProperty,
          emmo.NominalProperty,
          emmo.ConventionalQuantitativeProperty,
          emmo.ModelledQuantitativeProperty,
          emmo.Theorization, emmo.Experiment, emmo.Theory, emmo.Variable}
semiotic = emmo.get_branch(emmo.Holistic, leafs=leafs.union(hidden))
semiotic.difference_update(hidden)
g = OntoGraph(emmo)
g.add_entities(semiotic, relations='all', edgelabels=False)
g.add_legend()
g.save('measurement.png')



# Reductionistic perspective
g = OntoGraph(emmo, emmo.Reductionistic, relations='all', addnodes=False,
              leafs=[emmo.Quantity, emmo.String, emmo.PrefixedUnit,
                     emmo.SymbolicComposition, emmo.Matter],
              parents=2,
              #entities=[emmo.Symbolic],
              edgelabels=None)
g.add_legend()
g.save('Reductionistic.png')
