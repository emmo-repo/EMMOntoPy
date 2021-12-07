#!/usr/bin/env python3
"""
Module from parsing an excelfile and creating an
ontology from it.

The excelfile is read by pandas and the pandas
dataframe should have column names:
[
"""
import warnings
from typing import Tuple
import pyparsing
import pandas as pd
from ontopy import World
from ontopy.utils import NoSuchLabelError
from ontopy.manchester import evaluate
import owlready2  # pylint: disable=C0411


def english(string):
    """Returns `string` as an English location string."""
    return owlready2.locstr(string, lang="en")


def create_ontology_from_excel(  # pylint: disable=too-many-arguments
    excelpath: str,
    concept_sheet_name: str = "Concepts",
    metadata_sheet_name: str = "Metadata",
    base_iri: str = "http://emmo.info/emmo/domain/onto#",
    base_iri_from_metadata: bool = True,
    catalog: dict = None,
) -> (owlready2.Ontology, dict):
    """
    Creates an ontology from an excelfile.

    catalog is dict of imported ontologies with key name and value path
    """
    # Read datafile TODO: Some magic to identify the header row
    conceptdata = pd.read_excel(
        excelpath, sheet_name=concept_sheet_name, skiprows=[0, 2]
    )
    metadata = pd.read_excel(excelpath, sheet_name=metadata_sheet_name)
    return create_ontology_from_pandas(
        conceptdata, metadata, base_iri, base_iri_from_metadata, catalog
    )


def create_ontology_from_pandas(  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    data: pd.DataFrame,
    metadata: pd.DataFrame,
    base_iri: str = "http://emmo.info/emmo/domain/onto#",
    base_iri_from_metadata: bool = True,
    catalog: dict = None,
) -> Tuple[owlready2.Ontology, dict]:
    """
    Create an ontology from a pandas DataFrame
    """

    # Remove Concepts without prefLabel and make all to string
    data = data[data["prefLabel"].notna()]
    data = data.astype({"prefLabel": "str"})

    # base_iri from metadata if it exists and base_iri_from_metadata
    if base_iri_from_metadata:
        try:
            base_iri = (
                metadata.loc[metadata["Metadata name"] == "Ontology IRI"][
                    "Value"
                ].item()
                + "#"
            )
        except (TypeError, ValueError):
            pass

    # Make new ontology and import ontologies
    world = World()

    # have to decide how to add metadata and imports etc.
    # base_iri to be added from excel (maybe also possibly argument?)
    onto = world.get_ontology(base_iri)
    onto.base_iri = base_iri

    # Get imported ontologies from metadata
    try:
        imported_ontology_paths = (
            metadata.loc[metadata["Metadata name"] == "Imported ontologies"][
                "Value"
            ]
            .item()
            .split(";")
        )
    except (TypeError, ValueError, AttributeError):
        imported_ontology_paths = []
    # Add imported ontologies
    catalog = {} if catalog is None else catalog
    for path in imported_ontology_paths:
        imported = world.get_ontology(path).load()
        onto.imported_ontologies.append(imported)
        catalog[imported.base_iri.rstrip("/")] = path

    onto.sync_python_names()
    with onto:
        # loop through the rows until no more are added
        new_loop = True
        final_loop = False
        while new_loop:
            number_of_added_classes = 0
            for _, row in data.iterrows():
                name = row["prefLabel"]
                try:
                    if isinstance(
                        onto.get_by_label(name), owlready2.ThingClass
                    ):
                        continue
                except NoSuchLabelError:
                    pass

                parent_names = str(row["subClassOf"]).split(";")

                try:
                    parents = [onto.get_by_label(pn) for pn in parent_names]
                except NoSuchLabelError:
                    if final_loop is True:
                        parents = onto.EMMO

                        warnings.warn(
                            "At least one of the defined parents do not exist. "
                            f"Concept: {name}; Defined parents: {parent_names}"
                        )
                        new_loop = False
                    else:
                        continue

                concept = onto.new_entity(name, parents)

                elucidation = row["Elucidation"]
                if isinstance(elucidation, str):
                    concept.elucidation.append(english(elucidation))

                examples = row["Examples"]
                if isinstance(examples, str):
                    example_list = examples.split(";")
                    for example in example_list:
                        concept.example.append(english(example))

                comments = row["Comments"]
                if isinstance(comments, str):
                    comment_list = comments.split(";")
                    for comment in comment_list:
                        concept.comment.append(english(comment))

                number_of_added_classes += 1

            if number_of_added_classes == 0:
                final_loop = True

    # Add properties in a second loop
    for _, row in data.iterrows():
        properties = row["Relations"]
        if isinstance(properties, str):
            try:
                concept = onto.get_by_label(row["prefLabel"])
            except NoSuchLabelError:
                pass
            props = properties.split(";")
            for prop in props:
                try:
                    concept.is_a.append(evaluate(onto, prop))
                except pyparsing.ParseException as err:
                    warnings.warn(
                        f"Error in Property assignment for: {concept}. "
                        f"Property to be Evaluated: {prop}. "
                        f"Error is {err}."
                    )
    return Tuple[onto, catalog]
