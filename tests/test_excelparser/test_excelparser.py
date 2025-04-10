"""Test the Excel parser module."""

from typing import TYPE_CHECKING

import pytest

from ontopy import get_ontology
from ontopy.excelparser import create_ontology_from_excel
from ontopy.utils import NoSuchLabelError

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.filterwarnings("ignore:Ignoring concept :UserWarning")
@pytest.mark.filterwarnings("ignore:Invalid parents for :UserWarning")
@pytest.mark.filterwarnings(
    "ignore:Not able to add the following concepts :UserWarning"
)
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
    # ontology.save("test.ttl") # used for printing new ontology when debugging
    assert onto == ontology
    assert errors.keys() == {
        "already_defined",
        "in_imported_ontologies",
        "wrongly_defined",
        "missing_subClassOf",
        "invalid_subClassOf",
        "nonadded_entities",
        "errors_in_properties",
        "nonadded_concepts",
        "obj_prop_already_defined",
        "obj_prop_in_imported_ontologies",
        "obj_prop_wrongly_defined",
        "obj_prop_missing_subPropertyOf",
        "obj_prop_invalid_subPropertyOf",
        "obj_prop_nonadded_entities",
        "obj_prop_errors_in_properties",
        "obj_prop_errors_in_range",
        "obj_prop_errors_in_domain",
        "annot_prop_already_defined",
        "annot_prop_in_imported_ontologies",
        "annot_prop_wrongly_defined",
        "annot_prop_missing_subPropertyOf",
        "annot_prop_invalid_subPropertyOf",
        "annot_prop_nonadded_entities",
        "annot_prop_errors_in_properties",
        "data_prop_already_defined",
        "data_prop_in_imported_ontologies",
        "data_prop_wrongly_defined",
        "data_prop_missing_subPropertyOf",
        "data_prop_invalid_subPropertyOf",
        "data_prop_nonadded_entities",
        "data_prop_errors_in_properties",
        "data_prop_errors_in_range",
        "data_prop_errors_in_domain",
    }
    assert errors["already_defined"] == {"SpecialPattern"}
    assert errors["in_imported_ontologies"] == {"Atom"}
    assert errors["wrongly_defined"] == {"Temporal Boundary"}
    assert errors["missing_subClassOf"] == {"SpatioTemporalBoundary"}
    assert errors["invalid_subClassOf"] == {
        "TemporalPattern",
        "SubSubgrainBoundary",
        "SubgrainBoundary",
    }
    assert errors["nonadded_concepts"] == {
        "SpecialPattern",
        "Temporal Boundary",
    }

    assert len(ontology.get_by_label_all("Atom")) == 2
    with pytest.raises(NoSuchLabelError):
        onto.ATotallyNewPattern

    updated_onto, _, _ = create_ontology_from_excel(
        update_xlspath, force=True, input_ontology=ontology
    )
    assert updated_onto.ATotallyNewPattern
    assert updated_onto.FinitePattern.iri == onto.FinitePattern.iri
    assert len(list(onto.classes())) + 1 == len(list(updated_onto.classes()))

    # check that the owlready2 generated python names are not in the triples
    assert (
        list(
            ontology.get_unabbreviated_triples(
                predicate="http://www.lesfleursdunormal.fr/static/_downloads/"
                "owlready_ontology.owl#python_name"
            )
        )
        == []
    )
    # check that the owlready2 generated python names are not in the triples
    assert (
        list(
            updated_onto.get_unabbreviated_triples(
                predicate="http://www.lesfleursdunormal.fr/static/_downloads/"
                "owlready_ontology.owl#python_name"
            )
        )
        == []
    )

    # Just to be sure that the method of getting the correct triples is OK
    assert (
        len(
            list(
                ontology.get_unabbreviated_triples(
                    predicate="http://www.w3.org/2000/01/rdf-schema#subClassOf"
                )
            )
        )
        > 1
    )


def test_excelparser_only_classes(repo_dir: "Path") -> None:
    """This loads the excelfile used and tests that the resulting ontology prior
    to version 0.5.2 in which only classes where considered, but with empty sheets
    for properties."""

    # Useful for debugging with ipython
    # if True:
    #    from pathlib import Path
    #    repo_dir = Path(__file__).resolve().parent.parent.parent

    ontopath = (
        repo_dir
        / "tests"
        / "test_excelparser"
        / "result_ontology"
        / "fromexcelonto_only_classes.ttl"
    )

    onto = get_ontology(str(ontopath)).load()
    xlspath = repo_dir / "tests" / "test_excelparser" / "onto_only_classes.xlsx"
    update_xlspath = (
        repo_dir
        / "tests"
        / "test_excelparser"
        / "onto_update_only_classes.xlsx"
    )
    ontology, catalog, errors = create_ontology_from_excel(xlspath, force=True)
    # Used for printing new ontology when debugging
    # ontology.save("test_only_classes.ttl")

    # Useful for debugging
    # print("-----  only in onto  -----")
    # print(onto.difference(ontology))

    assert onto == ontology
    assert errors["already_defined"] == {"SpecialPattern"}
    assert errors["in_imported_ontologies"] == {"Atom"}
    assert errors["wrongly_defined"] == {"Temporal Boundary"}
    assert errors["missing_subClassOf"] == {"SpatioTemporalBoundary"}
    assert errors["invalid_subClassOf"] == {
        "TemporalPattern",
        "SubSubgrainBoundary",
        "SubgrainBoundary",
    }
    assert errors["nonadded_concepts"] == {
        "SpecialPattern",
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
    assert updated_onto.FinitePattern.iri == onto.FinitePattern.iri
    assert len(list(onto.classes())) + 1 == len(list(updated_onto.classes()))
