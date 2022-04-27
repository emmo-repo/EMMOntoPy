import ontopy.utils as utils
from testutils import get_triples, has_triple


def test_annotate_source(onto):
    assert not has_triple(
        onto,
        "http://emmo.info/models#testclass",
        "http://www.w3.org/2000/01/rdf-schema#isDefinedBy",
        "http://emmo.info/models#",
    )

    utils.annotate_source(onto, imported=False)
    assert not has_triple(
        onto,
        "http://emmo.info/models#testclass",
        "http://www.w3.org/2000/01/rdf-schema#isDefinedBy",
        "http://emmo.info/models#",
    )

    utils.annotate_source(onto, imported=True)
    assert has_triple(
        onto,
        "http://emmo.info/models#testclass",
        "http://www.w3.org/2000/01/rdf-schema#isDefinedBy",
        "http://emmo.info/models#",
    )


def test_rename_iris(onto):
    assert not has_triple(onto, s="http://emmo.info/models#TestClass")
    utils.rename_iris(onto)
    assert has_triple(onto, s="http://emmo.info/models#TestClass")
    assert has_triple(
        onto,
        "http://emmo.info/models#TestClass",
        "http://www.w3.org/2004/02/skos/core#exactMatch",
        "http://emmo.info/models#testclass",
    )
