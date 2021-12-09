"""
Module from parsing an excelfile and creating an
ontology from it.

The excelfile is read by pandas and the pandas
dataframe should have column names:
prefLabel, altLabel, Elucidation, Comments, Examples,
subClassOf, Relations.

Note that correct case is mandatory.
"""
import warnings
from typing import Tuple
import pyparsing
import pandas as pd
import ontopy
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
) -> Tuple[ontopy.ontology.Ontology, dict]:
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
) -> Tuple[ontopy.ontology.Ontology, dict]:
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
                        parents = owlready2.Thing

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
) -> Tuple[ontopy.ontology.Ontology, dict]:
    """
    Populate ontology with metada from pd.DataFrame
    """

    if onto is None:
        onto = get_ontology()

    # base_iri from metadata if it exists and base_iri_from_metadata
    if base_iri_from_metadata:
        try:
            base_iris = _parse_data_string(
                metadata, "Ontology IRI", metadata=True
            )
            if len(base_iris) > 1:
                warnings.warn(
                    "More than one Ontology IRI given. The first was chosen."
                )
            base_iri = base_iris[0] + "#"
            onto.base_iri = base_iri
        except (TypeError, ValueError, AttributeError):
            pass

    # Get imported ontologies from metadata
    try:
        imported_ontology_paths = _parse_data_string(
            metadata,
            "Imported ontologies",
            metadata=True,
        )
    except (TypeError, ValueError, AttributeError):
        imported_ontology_paths = []
    # Add imported ontologies
    catalog = {} if catalog is None else catalog
    for path in imported_ontology_paths:
        imported = onto.world.get_ontology(path).load()
        onto.imported_ontologies.append(imported)
        catalog[imported.base_iri.rstrip("/")] = path

    with onto:
        # Add title
        _add_data(
            metadata, onto.metadata.title, "Title", metadata=True, only_one=True
        )

        # Add license
        _add_data(metadata, onto.metadata.license, "License", metadata=True)

        # Add authors onto.metadata.author does not work!
        _add_data(metadata, onto.metadata.contributor, "Author", metadata=True)

        # Add contributors
        _add_data(
            metadata, onto.metadata.contributor, "Contributor", metadata=True
        )

        # Add versionInfo
        _add_data(
            metadata,
            onto.metadata.versionInfo,
            "Ontology version Info",
            metadata=True,
            only_one=True,
        )

    return onto, catalog


def _parse_data_string(
    data: pd.DataFrame, name: str, metadata: bool = False
) -> list:
    """Helper function to make list ouf strings from ';'-delimited
    strings in one string.
    """

    if metadata is True:
        values = data.loc[data["Metadata name"] == name]["Value"].item()
        if not pd.isna(values):
            return str(values).split(";")
    return values.split(";")


def _add_data(  # onto: ontopy.ontology.Ontology,
    data: pd.DataFrame,
    destination: owlready2.prop.IndividualValueList,  # Check this for metadata
    name: str,
    metadata: bool = False,
    only_one: bool = False,
) -> None:
    try:
        name_list = _parse_data_string(data, name, metadata=metadata)
        if only_one is True and len(name_list) > 1:
            warnings.warn(
                f"More than one {name} is given. The first was chosen."
            )
            destination.append(english(name_list[0]))
        else:
            destination.extend([english(nm) for nm in name_list])
    except (TypeError, ValueError, AttributeError):
        warnings.warn(f"No {name} added.")
