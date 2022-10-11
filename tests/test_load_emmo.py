def test_load_emmo() -> None:
    """Test loading EMMO.

    EMMO is also loaded in the `emmo` fixture.
    I.e., the fixture acts as a "test" as well, in this regard.
    """
    from emmopy import get_emmo

    EMMO_inferred = get_emmo()
    EMMO_inferred_again = get_emmo(None)
    EMMO = get_emmo(inferred=False)

    assert EMMO_inferred
    assert EMMO_inferred_again
    assert EMMO

    assert EMMO_inferred == EMMO_inferred_again
    assert EMMO != EMMO_inferred

    EMMO_inferred.new_entity("HydrogenAtom", EMMO_inferred.Atom)
    EMMO_inferred.sync_attributes()
    assert EMMO_inferred != EMMO_inferred_again

    EMMO_inferred2 = get_emmo()
    EMMO_inferred2.Atom.comment.append("New triple")
    assert EMMO_inferred2 != EMMO_inferred_again
