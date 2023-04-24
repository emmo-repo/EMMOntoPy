from pathlib import Path

from ontopy import get_ontology


thisdir = Path(__file__).resolve().parent

onto = get_ontology(
    thisdir / "test_excelparser/imported_onto/ontology.ttl"
).load()
onto.dir_imported = False
onto.dir_preflabel = False
onto.dir_label = False
onto.dir_name = False
assert "TestClass2" not in dir(onto)

onto.dir_imported = True
onto.dir_preflabel = True
assert onto._dir_imported
assert onto.TestClass2
assert "TestClass2" in dir(onto)
assert "testclass" not in dir(onto)
assert "testclass2" not in dir(onto)

onto.dir_name = True
assert "TestClass2" in dir(onto)
assert "testclass" in dir(onto)
assert "testclass2" in dir(onto)
