from pathlib import Path

import pytest


def abbreviate(onto, iri, must_exist=True):
    """Returns existing Owlready2 storid for `iri`."""
    if iri is None:
        return None
    abbreviater = getattr(onto, "_abbreviate")
    storid = abbreviater(iri, create_if_missing=False)
    if storid is None and must_exist:
        raise ValueError(f"no such IRI in ontology: {iri}")
    return storid


def get_triples(onto, s=None, p=None, o=None) -> list:
    """Returns a list of triples matching spo."""
    return [
        (
            onto._unabbreviate(s_) if isinstance(s_, int) and s_ > 0 else s_,
            onto._unabbreviate(p_) if isinstance(p_, int) and p_ > 0 else p_,
            onto._unabbreviate(o_) if isinstance(o_, int) and o_ > 0 else o_,
        )
        for s_, p_, o_, d in onto._get_triples_spod_spod(
            abbreviate(onto, s),
            abbreviate(onto, p),
            abbreviate(onto, o, False) or o,
            None,
        )
    ]


def has_triple(onto, s=None, p=None, o=None) -> bool:
    """Returns true if ontology `onto` contains the given triple.

    None may be used as a wildcard for of `s`, `p` or `o`.
    """
    try:
        return bool(get_triples(onto, s, p, o))
    except ValueError:
        return False


@pytest.fixture
def onto() -> "ontopy.Ontology":
    """Test ontology."""
    from ontopy import get_ontology

    url = Path(__file__).parent.parent / "testonto" / "testonto.ttl"
    onto = get_ontology(url).load()
    return onto
