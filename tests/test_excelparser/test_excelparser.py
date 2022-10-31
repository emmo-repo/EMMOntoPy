"""Test the Excel parser module."""
from typing import TYPE_CHECKING

from ontopy import get_ontology
from ontopy.excelparser import create_ontology_from_excel

if TYPE_CHECKING:
    from pathlib import Path


def test_excelparser(repo_dir: "Path") -> None:
    """Basic test for creating an ontology from an Excel file."""
    ontopath = repo_dir / "tests" / "test_excelparser" / "fromexcelonto.ttl"

    onto = get_ontology(str(ontopath)).load()
    xlspath = repo_dir / "tests" / "test_excelparser" / "onto.xlsx"
    ontology, catalog, errors = create_ontology_from_excel(xlspath, force=True)
    assert onto == ontology

    assert errors["already_defined"] == {"Atom", "Pattern"}
    assert errors["in_imported_ontologies"] == {"Atom"}
    assert errors["wrongly_defined"] == {"Temporal Boundary"}
    assert errors["missing_parents"] == {"SpatioTemporalBoundary"}
    assert errors["invalid_parents"] == {
        "TemporalPattern",
        "SubSubgrainBoundary",
        "SubgrainBoundary",
    }
    assert errors["nonadded_concepts"] == {
        "Atom",
        "Pattern",
        "Temporal Boundary",
    }
