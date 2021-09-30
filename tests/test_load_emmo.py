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

    assert EMMO_inferred == get_emmo(None)
    assert EMMO != EMMO_inferred

    EMMO_inferred.new_entity('HydrogenAtom', EMMO_inferred.Atom)
    EMMO_inferred.sync_attributes()
    assert EMMO_inferred != get_emmo(None)

