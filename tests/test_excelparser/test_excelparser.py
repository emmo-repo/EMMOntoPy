"""Test the Excel parser module."""
import pytest
from typing import TYPE_CHECKING

from ontopy import get_ontology
from ontopy.excelparser import create_ontology_from_excel
from ontopy.utils import NoSuchLabelError

if TYPE_CHECKING:
    from pathlib import Path


def test_excelparser(repo_dir: "Path") -> None:
    """Basic test for creating an ontology from an Excel file."""
    ontopath = (
        repo_dir
        / "tests"
        / "test_excelparser"
        / "result_ontology"
        / "fromexcelonto.ttl"
    )

    onto = get_ontology(str(ontopath)).load()
    xlspath = repo_dir / "tests" / "test_excelparser" / "onto.xlsx"
    update_xlspath = (
        repo_dir / "tests" / "test_excelparser" / "onto_update.xlsx"
    )
    ontology, catalog, errors = create_ontology_from_excel(xlspath, force=True)
    print("--------------------------")
    print(list(onto.object_properties()))
    print("--------------------------")
    print(list(ontology.object_properties()))
    print("--------------------------")
    ontology.save("test.ttl", format="ttl")
    assert onto == ontology

    assert errors["already_defined"] == {"Pattern"}
    assert errors["in_imported_ontologies"] == {"Atom"}
    assert errors["wrongly_defined"] == {"Temporal Boundary"}
    assert errors["missing_parents"] == {"SpatioTemporalBoundary"}
    assert errors["invalid_parents"] == {
        "TemporalPattern",
        "SubSubgrainBoundary",
        "SubgrainBoundary",
    }
    assert errors["nonadded_concepts"] == {
        "Pattern",
        "Temporal Boundary",
    }

    assert len(ontology.get_by_label_all("Atom")) == 2
    onto_length = len(list(onto.get_entities()))
    with pytest.raises(NoSuchLabelError):
        onto.ATotallyNewPattern

    updated_onto, _, _ = create_ontology_from_excel(
        update_xlspath, force=True, input_ontology=ontology
    )
    assert updated_onto.ATotallyNewPattern
    assert updated_onto.Pattern.iri == onto.Pattern.iri
    assert len(list(onto.classes())) + 1 == len(list(updated_onto.classes()))
