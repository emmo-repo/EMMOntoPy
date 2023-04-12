from pathlib import Path

from ontopy import get_ontology


thisdir = Path(__file__).resolve().parent

onto = get_ontology(
    thisdir / "test_excelparser/imported_onto/ontology.ttl"
).load()
assert "TestClass2" in dir(onto)

onto.dir_imported = False
assert "TestClass2" not in dir(onto)
assert "testclass" not in dir(onto)

onto.dir_imported = True
onto.dir_name = True
assert "TestClass2" in dir(onto)
assert "testclass" in dir(onto)
assert "testclass2" in dir(onto)
