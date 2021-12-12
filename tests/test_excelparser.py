from ontopy import get_ontology
from ontopy.excelparser import create_ontology_from_excel
from ontopy.utils import write_catalog


def test_excelparser(repo_dir: "Path") -> None:
    ontopath = (
        repo_dir / "tests" / "testonto" / "excelparser" / "fromexcelonto.ttl"
    )
    onto = get_ontology(str(ontopath)).load()
    xlspath = repo_dir / "tests" / "testonto" / "excelparser" / "onto.xlsx"
    ontology, catalog = create_ontology_from_excel(xlspath)
    assert onto == ontology


if __name__ == "__main__":
    test_excelparser()
