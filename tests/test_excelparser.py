from ontopy import get_ontology
from ontopy.excelparser import create_ontology_from_excel
from ontopy.utils import write_catalog

onto = get_ontology("testonto/excelparser/fromexcelonto.ttl").load()


def test_excelparser():
    ontology, catalog = create_ontology_from_excel(
        "testonto/excelparser/onto.xlsx"
    )
    assert onto == ontology


if __name__ == "__main__":
    test_excelparser()
