from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
    from ontopy.ontology import Ontology


def test_descendants(emmo: "Ontology", repo_dir: "Path") -> None:
    from ontopy import get_ontology
    from ontopy.utils import LabelDefinitionError

    ontopath = repo_dir / "tests" / "testonto" / "testontology.ttl"

    onto = get_ontology(ontopath).load()

    # Test that default gives one generation
    assert onto.get_descendants(onto.Tree) == {
        onto.EvergreenTree,
        onto.DesiduousTree,
    }
    assert onto.get_descendants(onto.Tree, generations=1) == {
        onto.EvergreenTree,
        onto.DesiduousTree,
    }
    # Test that asking for 0 generations returns empty set
    assert onto.get_descendants(onto.Tree, generations=0) == set()
    # Check that more than one generation works
    assert onto.get_descendants(onto.Tree, generations=2) == {
        onto.EvergreenTree,
        onto.DesiduousTree,
        onto.Avocado,
        onto.Spruce,
    }
    # Check that no error is generated if one of the subclasses do not have enough children for all given generations
    assert onto.get_descendants(onto.Tree, generations=3) == {
        onto.EvergreenTree,
        onto.DesiduousTree,
        onto.Avocado,
        onto.Spruce,
        onto.EngelmannSpruce,
        onto.NorwaySpruce,
    }
    assert onto.get_descendants(onto.Tree, generations=4) == {
        onto.EvergreenTree,
        onto.DesiduousTree,
        onto.Avocado,
        onto.Spruce,
        onto.EngelmannSpruce,
        onto.NorwaySpruce,
    }
    # Check that descendants of a list is returned correctly
    assert onto.get_descendants([onto.Tree, onto.NaturalDye]) == {
        onto.EvergreenTree,
        onto.DesiduousTree,
        onto.Avocado,
        onto.ShingledHedgehogMushroom,
    }
    # Check that common descendants within the number of generations are found
    # With all descentants if number of generations not given
    assert onto.get_descendants(
        [onto.Tree, onto.NaturalDye], common=True, generations=2
    ) == {onto.Avocado}
    assert (
        onto.get_descendants(
            [onto.Tree, onto.NaturalDye], common=True, generations=1
        )
        == set()
    )
    assert onto.get_descendants([onto.Tree, onto.NaturalDye], common=True) == {
        onto.Avocado
    }
