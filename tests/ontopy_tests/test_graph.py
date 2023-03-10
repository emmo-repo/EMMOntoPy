from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
    from pathlib import Path

    from ontopy.ontology import Ontology


def test_graph(testonto: "Ontology", tmpdir: "Path") -> None:
    """Testing OntoGraph on a small ontology

    Two relations in addition to isA are used,
    one that has a default style and one that does not.
    This should give one warning, and with the defined filterwarnings
    the test should pass also when running `pytest -Werror`

    Parameters:
        testonto: A local fixture from the root `conftest.py`.
            Return a local ontology used for testing.
        tmpdir: A built in pytest fixture to get a function-scoped
            temporary directory'
    """
    import owlready2
    from ontopy.graph import OntoGraph

    with testonto:
        # Add a relation that does not have a default style in OntoGraph
        class hasSpecialRelation(owlready2.ObjectProperty):
            """New special relation"""

            domain = list(testonto.classes())
            range = list(testonto.classes())

        class NewSpecialClass(owlready2.Thing):
            """New class"""

        # Add a relation that has a default style
        class hasProperty(owlready2.ObjectProperty):
            """hasProperty relation"""

            domain = list(testonto.classes())
            range = list(testonto.classes())

        class NewSpecialPropertyClass(owlready2.Thing):
            """New property class"""

        class NewSpecialPartClass(owlready2.Thing):
            """New class"""

        class hasPartRenamed(owlready2.ObjectProperty):
            """Renamed property class"""

            domain = list(testonto.classes())
            range = list(testonto.classes())
            altLabel = "hasPart"

    testonto.sync_attributes()

    testonto.TestClass.hasSpecialRelation.append(testonto.NewSpecialClass)
    testonto.TestClass.hasProperty.append(testonto.NewSpecialPropertyClass)
    testonto.TestClass.hasPartRenamed.append(testonto.NewSpecialPartClass)

    with pytest.warns() as record:
        graph = OntoGraph(
            testonto,
            testonto.TestClass,
            relations="all",
            addnodes=True,
            edgelabels=None,
        )
        assert str(record[0].message) == (
            "Style not defined for relation hasSpecialRelation. "
            "Resorting to default style."
        )
    graph.add_legend()
    graph.save(tmpdir / "testonto.png")


def test_emmo_graphs(emmo: "Ontology", tmpdir: "Path") -> None:
    """Testing OntoGraph on various aspects of EMMO.

    Parameters:
        testonto: A local fixture from the root `conftest.py`.
            Return a local ontology used for testing.
        tmpdir: A built in pytest fixture to get a function-scoped
            temporary directory'
    """
    import owlready2
    from ontopy.graph import OntoGraph

    graph = OntoGraph(
        emmo,
        emmo.hasPart,
        leafs=("mereological", "semiotical", "causal"),
    )
    graph.save(tmpdir / "hasPart.svg")

    graph = OntoGraph(
        emmo, emmo.Matter, relations="all", addnodes=True, edgelabels=None
    )
    graph.save(tmpdir / "Matter.png")

    graph = OntoGraph(
        emmo,
        emmo.ElementaryParticle,
        relations="all",
        addnodes=True,
        edgelabels=None,
    )
    graph.save(tmpdir / "ElementaryParticle.png")

    graph = OntoGraph(
        emmo,
        emmo.SIBaseUnit,
        relations="all",
        addnodes=True,
        edgelabels=True,
        addconstructs=False,
        graph_attr={"rankdir": "RL"},
    )
    graph.add_legend()
    graph.save(tmpdir / "SIBaseUnit.png")

    graph = OntoGraph(emmo, emmo.EMMORelation, relations="all", edgelabels=None)
    graph.save(tmpdir / "EMMORelation.png")

    graph = OntoGraph(
        emmo,
        emmo.Quantity,
        leafs=[emmo.DerivedQuantity, emmo.BaseQuantity, emmo.PhysicalConstant],
        relations="all",
        edgelabels=None,
        addnodes=True,
        addconstructs=True,
        graph_attr={"rankdir": "RL"},
    )
    graph.add_legend()
    graph.save(tmpdir / "Quantity.svg")

    # Used for figures

    graph = OntoGraph(emmo)
    graph.add_legend("all")
    graph.save(tmpdir / "legend.png")

    graph = OntoGraph(
        emmo, emmo.EMMO, leafs=[emmo.Perspective, emmo.Elementary]
    )
    graph.save(tmpdir / "top.png")

    leafs = set()
    for s in emmo.Perspective.subclasses():
        leafs.update(s.subclasses())
    graph = OntoGraph(emmo, emmo.Perspective, leafs=leafs, parents=1)
    graph.save(tmpdir / "Perspectives.png")

    leafs = {
        emmo.Interpreter,
        emmo.Conventional,
        emmo.Icon,
        emmo.Observation,
        emmo.Object,
    }
    hidden = {
        emmo.SIUnitSymbol,
        emmo.SpecialUnit,
        emmo.Manufacturing,
        emmo.Engineered,
        emmo.PhysicalPhenomenon,
    }
    semiotic = emmo.get_branch(emmo.Holistic, leafs=leafs.union(hidden))
    semiotic.difference_update(hidden)
    graph = OntoGraph(emmo)
    graph.add_entities(semiotic, relations="all", edgelabels=False)
    graph.save(tmpdir / "Semiotic.png")
    graph.add_legend()
    graph.save(tmpdir / "Semiotic+legend.png")

    legend = OntoGraph(emmo)
    legend.add_legend(graph.get_relations())
    legend.save(tmpdir / "Semiotic-legend.png")

    # Measurement
    leafs = {emmo.Object}

    hidden = {
        emmo.SIUnitSymbol,
        emmo.SpecialUnit,
        emmo.Manufacturing,
        emmo.Engineered,
        emmo.PhysicalPhenomenon,
        emmo.Icon,
        emmo.Interpretant,
        emmo.Index,
        emmo.Subjective,
        emmo.NominalProperty,
        emmo.ConventionalQuantitativeProperty,
        emmo.ModelledQuantitativeProperty,
        emmo.Theorization,
        emmo.Experiment,
        emmo.Theory,
        emmo.Variable,
    }
    semiotic = emmo.get_branch(emmo.Holistic, leafs=leafs.union(hidden))
    semiotic.difference_update(hidden)
    graph = OntoGraph(emmo)
    graph.add_entities(semiotic, relations="all", edgelabels=False)
    graph.add_legend()
    graph.save(tmpdir / "measurement.png")

    # Reductionistic perspective
    graph = OntoGraph(
        emmo,
        emmo.Reductionistic,
        relations="all",
        addnodes=False,
        leafs=[
            emmo.Quantity,
            emmo.String,
            emmo.PrefixedUnit,
            emmo.SymbolicConstruct,
            emmo.Matter,
        ],
        parents=2,
        edgelabels=None,
    )
    graph.add_legend()
    graph.save(tmpdir / "Reductionistic.png")