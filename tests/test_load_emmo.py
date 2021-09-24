def test_load_emmo() -> None:
    """Add emmo to sys path"""
    import os
    import sys

    thisdir = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..')))
    from ontopy import get_ontology  # noqa: E402, F401
    from emmopy import get_emmo

    emmo = get_ontology()
    emmo.load()

    EMMO_inferred = get_emmo()
    EMMO = get_emmo(inferred=False)
    assert EMMO_inferred.base_iri == get_emmo(None).base_iri

