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
from ontopy import World, get_ontology
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
) -> Tuple[ontopy.Ontology, dict]:
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

    # Make new ontology
    world = World()
    onto = world.get_ontology(base_iri)

    onto, catalog = get_metadata_from_dataframe(metadata, onto)

    # base_iri from metadata if it exists and base_iri_from_metadata
    if not base_iri_from_metadata:
        onto.base_iri = base_iri

    # have to decide how to add metadata and imports etc.
    # base_iri to be added from excel (maybe also possibly argument?)
    # onto = world.get_ontology(base_iri)

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
                        parents = owlready2.ThingClass

                        warnings.warn(
                            "Missing at least one of the defined parents. "
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

                altlabels = row["altLabel"]
                if isinstance(altlabels, str):
                    altlabel_list = altlabels.split(";")
                    for altlabel in altlabel_list:
                        concept.altLabel.append(english(altlabel))

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

    onto, catalog = get_metadata_from_dataframe(metadata, onto)
    # Synchronise Python attributes to ontology
    onto.sync_attributes(
        name_policy="uuid", name_prefix="EMMO_", class_docstring="elucidation"
    )
    onto.dir_label = False

    return onto, catalog


# To test: with and without ontology as input
def get_metadata_from_dataframe(  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    metadata: pd.DataFrame,
    onto: owlready2.Ontology = None,
    base_iri_from_metadata: bool = True,
    catalog: dict = None,
) -> Tuple[owlready2.Ontology, dict]:
    """
    Populate ontology with metada from pd.DataFrame
    """

    if onto is None:
        onto = get_ontology()

    # base_iri from metadata if it exists and base_iri_from_metadata
    if base_iri_from_metadata:
        try:
            base_iris = _parse_metadata_string(metadata, "Ontology IRI")
            if len(base_iris) > 1:
                warnings.warn(
                    "More than one Ontology IRI given. " "The first was chosen."
                )
            base_iri = base_iris[0] + "#"
            onto.base_iri = base_iri
        except (TypeError, ValueError, AttributeError):
            pass

    # Get imported ontologies from metadata
    try:
        imported_ontology_paths = _parse_metadata_string(
            metadata, "Imported ontologies"
        )
    except (TypeError, ValueError, AttributeError):
        imported_ontology_paths = []
    # Add imported ontologies
    catalog = {} if catalog is None else catalog
    for path in imported_ontology_paths:
        imported = onto.world.get_ontology(path).load()
        onto.imported_ontologies.append(imported)
        catalog[imported.base_iri.rstrip("/")] = path

    # Add title
    try:
        titles = _parse_metadata_string(metadata, "Title")
        if len(titles) > 1:
            warnings.warn(
                "More than one title is given. " "The first was chosen."
            )
        onto.metadata.title.append(english(titles[0]))
    except (TypeError, ValueError, AttributeError):
        pass

    # Add versionINFO
    try:
        version_infos = _parse_metadata_string(
            metadata, "Ontology version Info"
        )
        if len(version_infos) > 1:
            warnings.warn(
                "More than one versionINFO is given. " "The first was chosen."
            )
        onto.metadata.versionInfo.append(english(version_infos[0]))
    except (TypeError, ValueError, AttributeError):
        pass

    # Add versionINFO
    try:
        licenses = _parse_metadata_string(metadata, "License")
        if len(licenses) > 1:
            warnings.warn(
                "More than one license is given. " "The first was chosen."
            )
        onto.metadata.license.append(english(licenses[0]))
    except (TypeError, ValueError, AttributeError):
        pass

    # Add authors
    try:
        authors = _parse_metadata_string(metadata, "Author")
        for author in authors:
            onto.metadata.creator.append(english(author))
    except (TypeError, ValueError, AttributeError):
        warnings.warn("No authors or creators added.")

    # Add contributors
    try:
        contributors = _parse_metadata_string(metadata, "Contributor")
        for contributor in contributors:
            onto.metadata.contributor.append(english(contributor))
    except (TypeError, ValueError, AttributeError):
        warnings.warn("No contributors added.")

    return onto, catalog


def _parse_metadata_string(metadata: pd.DataFrame, name: str) -> list:
    """Helper function to make list ouf strings from ';'-delimited
    strings in one string.
    """
    return metadata.loc[metadata["Metadata name"] == name]["Value"].item().split(";")
