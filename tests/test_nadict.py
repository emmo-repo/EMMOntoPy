def test_nadict() -> None:
    from ontopy.nadict import NADict

    nadict = NADict(a=1, b=NADict(c=3, d=4))

    assert nadict.a == 1
    assert nadict.b.c == 3
    assert nadict.b.d == 4
    assert nadict['b.c'] == 3
