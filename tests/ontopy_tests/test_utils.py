import ontopy.utils as utils
from utilities import get_triples, has_triple


def test_annotate_source(testonto: "Ontology"):
    assert not has_triple(
        testonto,
        "http://emmo.info/models#testclass",
        "http://www.w3.org/2000/01/rdf-schema#isDefinedBy",
        "http://emmo.info/models#",
    )

    utils.annotate_source(testonto, imported=False)
    assert not has_triple(
        testonto,
        "http://emmo.info/models#testclass",
        "http://www.w3.org/2000/01/rdf-schema#isDefinedBy",
        "http://emmo.info/models#",
    )

    utils.annotate_source(testonto, imported=True)
    assert has_triple(
        testonto,
        "http://emmo.info/models#testclass",
        "http://www.w3.org/2000/01/rdf-schema#isDefinedBy",
        "http://emmo.info/models#",
    )


def test_rename_iris(testonto: "Ontology"):
    assert not has_triple(testonto, s="http://emmo.info/models#TestClass")
    utils.rename_iris(testonto)
    assert has_triple(testonto, s="http://emmo.info/models#TestClass")
    assert has_triple(
        testonto,
        "http://emmo.info/models#TestClass",
        "http://www.w3.org/2004/02/skos/core#exactMatch",
        "http://emmo.info/models#testclass",
    )
