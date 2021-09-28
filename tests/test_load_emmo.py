def test_load_emmo() -> None:
    """Test loading EMMO.

    EMMO is also loaded in the `emmo` fixture.
    I.e., the fixture acts as a "test" as well, in this regard.
    """
    from emmopy import get_emmo

    EMMO_inferred = get_emmo()
    EMMO = get_emmo(inferred=False)

    assert EMMO_inferred
    assert EMMO

    assert EMMO_inferred.base_iri == get_emmo(None).base_iri

