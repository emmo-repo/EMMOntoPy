from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
    from ontopy.ontology import Ontology


def test_descendants(emmo: "Ontology", repo_dir: "Path") -> None:
    from ontopy import get_ontology
    from ontopy.utils import LabelDefinitionError

    ontopath = repo_dir / "tests" / "testonto" / "testontology.ttl"

    onto = get_ontology(ontopath).load()

    # Test that default gives all descendants.
    assert onto.get_descendants(onto.Tree) == {
        onto.EvergreenTree,
        onto.DesiduousTree,
        onto.Avocado,
        onto.Spruce,
        onto.EngelmannSpruce,
        onto.NorwaySpruce,
    }

    # Test that asking for 0 generations returns empty set
    assert onto.get_descendants(onto.Tree, generations=0) == set()

    # Check that number of generations are returned correctly
    assert onto.get_descendants(onto.Tree, generations=1) == {
        onto.EvergreenTree,
        onto.DesiduousTree,
    }

    assert onto.get_descendants(onto.Tree, generations=2) == {
        onto.EvergreenTree,
        onto.DesiduousTree,
        onto.Avocado,
        onto.Spruce,
    }
    # Check that no error is generated if one of the subclasses do
    # not have enough children for all given generations
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
        onto.Spruce,
        onto.EngelmannSpruce,
        onto.NorwaySpruce,
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


def test_ancestors(emmo: "Ontology", repo_dir: "Path") -> None:
    from ontopy import get_ontology
    from ontopy.utils import LabelDefinitionError

    ontopath = repo_dir / "tests" / "testonto" / "testontology.ttl"

    onto = get_ontology(ontopath).load()

    # Test that default gives all ancestors.
    assert onto.get_ancestors(onto.NorwaySpruce) == {
        onto.Spruce,
        onto.Tree,
        onto.EvergreenTree,
        onto.Thing,
    }

    # Test that asking for 0 generations returns empty set
    assert onto.get_ancestors(onto.NorwaySpruce, generations=0) == set()

    # Check that number of generations are returned correctly
    assert onto.get_ancestors(onto.NorwaySpruce, generations=2) == {
        onto.Spruce,
        onto.EvergreenTree,
    }

    assert onto.get_ancestors(onto.NorwaySpruce, generations=1) == {
        onto.Spruce,
    }
    # Check that no error is generated if one of the classes do
    # not have enough parents for all given generations
    assert onto.get_ancestors(onto.NorwaySpruce, generations=10) == (
        onto.get_ancestors(onto.NorwaySpruce)
    )

    # Check that ancestors of a list is returned correctly
    assert onto.get_ancestors([onto.NorwaySpruce, onto.Avocado]) == {
        onto.Tree,
        onto.EvergreenTree,
        onto.Spruce,
        onto.NaturalDye,
        onto.Thing,
    }
    # Check that classes up to closest common ancestor are returned

    assert onto.get_ancestors(
        [onto.NorwaySpruce, onto.Avocado], closest=True
    ) == {
        onto.EvergreenTree,
        onto.Spruce,
    }

    with pytest.raises(ValueError):
        onto.get_ancestors(onto.NorwaySpruce, closest=True, generations=4)

    # Test strict == False
    assert onto.get_ancestors(
        [onto.NorwaySpruce, onto.Avocado],
        closest=True,
        strict=False,
    ) == {
        onto.EvergreenTree,
        onto.Spruce,
        onto.NorwaySpruce,
        onto.Avocado,
    }
