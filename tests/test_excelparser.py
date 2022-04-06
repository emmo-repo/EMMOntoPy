"""Test the Excel parser module."""
from typing import TYPE_CHECKING

from ontopy import get_ontology
from ontopy.excelparser import create_ontology_from_excel

if TYPE_CHECKING:
    from pathlib import Path


def test_excelparser(repo_dir: "Path") -> None:
    """Basic test for creating an ontology from an Excel file."""
    ontopath = (
        repo_dir / "tests" / "testonto" / "excelparser" / "fromexcelonto.ttl"
    )

    onto = get_ontology(str(ontopath)).load()
    xlspath = repo_dir / "tests" / "testonto" / "excelparser" / "onto.xlsx"
    ontology, catalog, errors = create_ontology_from_excel(xlspath, force=True)
    print(errors)
    assert onto == ontology
