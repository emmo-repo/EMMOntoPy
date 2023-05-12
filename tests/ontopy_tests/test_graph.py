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

    with pytest.warns() as record:
        graph2 = OntoGraph(
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
    graph2.add_legend()
    graph2.save(tmpdir / "testonto2.png")


def test_emmo_graphs(emmo: "Ontology", tmpdir: "Path") -> None:
    """Testing OntoGraph on various aspects of EMMO.

    Parameters:
        testonto: A local fixture from the root `conftest.py`.
            Return a local ontology used for testing.
        tmpdir: A built in pytest fixture to get a function-scoped
            temporary directory'
    """
    import owlready2
    from ontopy.graph import OntoGraph, plot_modules
    from ontopy import get_ontology
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        graph = OntoGraph(
            emmo,
            emmo.hasPart,
            leaves=("mereological", "semiotical", "causal"),
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
            edgelabels=False,
            addconstructs=False,
            graph_attr={"rankdir": "RL"},
        )
        graph.add_legend()
        graph.save(tmpdir / "SIBaseUnit.png")

        graph = OntoGraph(
            emmo, emmo.EMMORelation, relations="all", edgelabels=None
        )
        graph.save(tmpdir / "EMMORelation.png")

        graph = OntoGraph(
            emmo,
            emmo.Quantity,
            leaves=[
                emmo.DerivedQuantity,
                emmo.BaseQuantity,
                emmo.PhysicalConstant,
            ],
            relations="all",
            edgelabels=True,
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
            emmo, emmo.EMMO, leaves=[emmo.Perspective, emmo.Elementary]
        )
        graph.save(tmpdir / "top.png")

        leaves = set()
        for s in emmo.Perspective.subclasses():
            leaves.update(s.subclasses())
        graph = OntoGraph(emmo, emmo.Perspective, leaves=leaves, parents=1)
        graph.save(tmpdir / "Perspectives.png")

        leaves = {
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
        semiotic = emmo.get_branch(emmo.Holistic, leaves=leaves.union(hidden))
        semiotic.difference_update(hidden)
        graph = OntoGraph(emmo)
        graph.add_entities(semiotic, relations="all", edgelabels=None)
        graph.save(tmpdir / "Semiotic.png")
        graph.add_legend()
        graph.save(tmpdir / "Semiotic+legend.png")

        legend = OntoGraph(emmo)
        legend.add_legend(graph.get_relations())
        legend.save(tmpdir / "Semiotic-legend.png")

        # Measurement
        leaves = {emmo.Object}

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
        semiotic = emmo.get_branch(emmo.Holistic, leaves=leaves.union(hidden))
        semiotic.difference_update(hidden)
        graph = OntoGraph(emmo)
        graph.add_entities(semiotic, relations="all", edgelabels=False)
        graph.add_legend()
        graph.save(tmpdir / "measurement.png", fmt="graphviz")
        print("reductionistc")
        # Reductionistic perspective
        graph = OntoGraph(
            emmo,
            emmo.Reductionistic,
            relations="all",
            addnodes=False,
            leaves=[
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

        # Reductionistic perspective, choose leaf_generations
        graph = OntoGraph(
            emmo,
            emmo.Reductionistic,
            relations="all",
            addnodes=False,
            parents=2,
            edgelabels=None,
        )
        graph.add_branch(
            emmo.Reductionistic,
            leaves=[
                emmo.Quantity,
                emmo.String,
                emmo.PrefixedUnit,
                emmo.SymbolicConstruct,
                emmo.Matter,
            ],
        )

        graph.add_legend()
        graph.save(tmpdir / "Reductionistic_addbranch.png")

        graph2 = OntoGraph(
            emmo,
            emmo.Reductionistic,
            relations="all",
            addnodes=False,
            # parents=2,
            edgelabels=None,
        )
        graph2.add_branch(
            emmo.Reductionistic,
            leaves=[
                emmo.Quantity,
                emmo.String,
                emmo.PrefixedUnit,
                emmo.SymbolicConstruct,
                emmo.Matter,
            ],
            include_parents=2,
        )

        graph2.add_legend()
        graph2.save(tmpdir / "Reductionistic_addbranch_2.png")

        # View modules

        onto = get_ontology(
            "https://raw.githubusercontent.com/emmo-repo/EMMO/1.0.0-beta4/emmo.ttl"
        ).load()
        plot_modules(onto, tmpdir / "modules.png", ignore_redundant=True)
