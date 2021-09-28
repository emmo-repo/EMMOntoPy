from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from ontopy.ontology import Ontology


def test_graph2(emmo: "Ontology", tmpdir: "Path") -> None:
    import os

    from ontopy.graph import OntoGraph

    os.chdir(tmpdir)

    graph = OntoGraph(emmo, emmo.hasPart, leafs=('mereotopological', 'semiotical',
                                            'connected'))
    graph.save('hasPart.svg')


    graph = OntoGraph(emmo, emmo.Matter, relations='all', addnodes=True,
                edgelabels=None)
    graph.save('Matter.png')

    graph = OntoGraph(emmo, emmo.ElementaryParticle, relations='all', addnodes=True,
                edgelabels=None)
    graph.save('ElementaryParticle.png')

    graph = OntoGraph(emmo, emmo.SIBaseUnit, relations='all', addnodes=True,
                edgelabels=True,
                addconstructs=False, graph_attr={'rankdir': 'RL'})
    graph.add_legend()
    graph.save('SIBaseUnit.png')

    graph = OntoGraph(emmo, emmo.EMMORelation, relations='all', edgelabels=None)
    graph.save('EMMORelation.png')

    graph = OntoGraph(emmo, emmo.Quantity,
                leafs=[emmo.DerivedQuantity, emmo.BaseQuantity,
                        emmo.PhysicalConstant],
                relations='all', edgelabels=None, addnodes=True,
                addconstructs=True, graph_attr={'rankdir': 'RL'})
    graph.add_legend()
    graph.save('Quantity.svg')


    # Used for figures

    graph = OntoGraph(emmo)
    graph.add_legend('all')
    graph.save('legend.png')


    graph = OntoGraph(emmo, emmo.EMMO, leafs=[emmo.Perspective, emmo.Elementary])
    graph.save('top.png')


    leafs = set()
    for s in emmo.Perspective.subclasses():
        leafs.update(s.subclasses())
    graph = OntoGraph(emmo, emmo.Perspective, leafs=leafs, parents=1)
    graph.save('Perspectives.png')


    leafs = {emmo.Interpreter, emmo.Conventional, emmo.Icon, emmo.Observation,
            emmo.Object}
    hidden = {emmo.SIUnitSymbol, emmo.SpecialUnit, emmo.Manufacturing,
            emmo.Engineered, emmo.PhysicalPhenomenon}
    semiotic = emmo.get_branch(emmo.Holistic, leafs=leafs.union(hidden))
    semiotic.difference_update(hidden)
    graph = OntoGraph(emmo)
    graph.add_entities(semiotic, relations='all', edgelabels=False)
    graph.save('Semiotic.png')
    graph.add_legend()
    graph.save('Semiotic+legend.png')

    legend = OntoGraph(emmo)
    legend.add_legend(graph.get_relations())
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
    graph = OntoGraph(emmo)
    graph.add_entities(semiotic, relations='all', edgelabels=False)
    graph.add_legend()
    graph.save('measurement.png')


    # Reductionistic perspective
    graph = OntoGraph(emmo, emmo.Reductionistic, relations='all', addnodes=False,
                leafs=[emmo.Quantity, emmo.String, emmo.PrefixedUnit,
                        emmo.SymbolicComposition, emmo.Matter],
                parents=2,
                edgelabels=None)
    graph.add_legend()
    graph.save('Reductionistic.png')
