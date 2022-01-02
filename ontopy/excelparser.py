"""
Module from parsing an excelfile and creating an
ontology from it.

The excelfile is read by pandas and the pandas
dataframe should have column names:
prefLabel, altLabel, Elucidation, Comments, Examples,
subClassOf, Relations.

Note that correct case is mandatory.
"""
import sys
import warnings
from typing import Tuple, Union
import pyparsing
import pandas as pd
import ontopy
from ontopy import get_ontology
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
    force: bool = False,
) -> Tuple[ontopy.ontology.Ontology, dict]:
    """
    Creates an ontology from an excelfile.

    Catalog is dict of imported ontologies with key name and value path.
    """
    # Read datafile TODO: Some magic to identify the header row
    conceptdata = pd.read_excel(
        excelpath, sheet_name=concept_sheet_name, skiprows=[0, 2]
    )
    metadata = pd.read_excel(excelpath, sheet_name=metadata_sheet_name)
    return create_ontology_from_pandas(
        conceptdata,
        metadata,
        base_iri,
        base_iri_from_metadata,
        catalog,
        force=force,
    )


def create_ontology_from_pandas(  # pylint:disable=too-many-locals,too-many-branches,too-many-statements,too-many-arguments
    data: pd.DataFrame,
    metadata: pd.DataFrame,
    base_iri: str = "http://emmo.info/emmo/domain/onto#",
    base_iri_from_metadata: bool = True,
    catalog: dict = None,
    force: bool = False,
) -> Tuple[ontopy.ontology.Ontology, dict]:
    """
    Create an ontology from a pandas DataFrame.
    """

    # Remove Concepts without prefLabel and make all to string
    data = data[data["prefLabel"].notna()]
    data = data.astype({"prefLabel": "str"})

    # Make new ontology
    onto, catalog = get_metadata_from_dataframe(metadata, base_iri)

    # base_iri from metadata if it exists and base_iri_from_metadata
    if not base_iri_from_metadata:
        onto.base_iri = base_iri

    onto.sync_python_names()
    with onto:
        # loop through the rows until no more are added
        new_loop = True
        final_loop = False
        while new_loop:
            number_of_added_classes = 0
            for _, row in data.iterrows():
                name = row["prefLabel"].strip()
                try:
                    if isinstance(
                        onto.get_by_label(name), owlready2.ThingClass
                    ):
                        continue
                except NoSuchLabelError:
                    pass

                parent_names = str(row["subClassOf"]).split(";")
                try:
                    parents = [
                        onto.get_by_label(pn.strip(" ")) for pn in parent_names
                    ]

                except (NoSuchLabelError, ValueError) as err:
                    if force is True:
                        if final_loop is True:
                            warnings.warn(
                                "Invalid name for at least one of the parents:"
                                f" {err}"
                            )
                        else:
                            continue
                    else:
                        print("ERROR:", err)
                        print("Have you forgotten to add imported ontologies?")
                        sys.exit(1)

                    if final_loop is True:
                        parents = owlready2.Thing

                        warnings.warn(
                            "At least one of the defined parents is missing. "
                            f"Concept: {name}; Defined parents: {parent_names}"
                        )
                        new_loop = False
                    else:
                        continue

                concept = onto.new_entity(name, parents)
                # Add elucidation
                _add_literal(
                    row, concept.elucidation, "Elucidation", only_one=True
                )

                # Add examples
                _add_literal(row, concept.example, "Examples", expected=False)

                # Add comments
                _add_literal(row, concept.comment, "Comments", expected=False)

                # Add altLAbels
                _add_literal(row, concept.altLabel, "altLabel", expected=False)

                number_of_added_classes += 1

            if number_of_added_classes == 0:
                final_loop = True

    # Add properties in a second loop
    for _, row in data.iterrows():
        properties = row["Relations"]
        if isinstance(properties, str):
            try:
                concept = onto.get_by_label(row["prefLabel"].strip())
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
                except NoSuchLabelError as err:
                    if force is True:
                        pass
                    else:
                        print("ERROR:", err)
                        sys.exit(1)

    # Synchronise Python attributes to ontology
    onto.sync_attributes(
        name_policy="uuid", name_prefix="EMMO_", class_docstring="elucidation"
    )
    onto.dir_label = False
    return onto, catalog


def get_metadata_from_dataframe(  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    metadata: pd.DataFrame,
    base_iri: str,
    base_iri_from_metadata: bool = True,
    catalog: dict = None,
) -> Tuple[ontopy.ontology.Ontology, dict]:
    """Create ontology with metadata from pd.DataFrame"""

    # base_iri from metadata if it exists and base_iri_from_metadata
    if base_iri_from_metadata:
        try:
            base_iris = _parse_literal(metadata, "Ontology IRI", metadata=True)
            if len(base_iris) > 1:
                warnings.warn(
                    "More than one Ontology IRI given. The first was chosen."
                )
            base_iri = base_iris[0] + "#"
        except (TypeError, ValueError, AttributeError):
            pass

    # Create new ontology
    onto = get_ontology(base_iri)

    # Get imported ontologies from metadata
    try:
        imported_ontology_paths = _parse_literal(
            metadata,
            "Imported ontologies",
            metadata=True,
        )
    except (TypeError, ValueError, AttributeError):
        imported_ontology_paths = []
    # IMPORTANT THIS SHOULD BE AN OPTION
    if len(onto.imported_ontologies) == 0:
        imported_ontology_paths = [
            "https://emmo-repo.github.io/versions/1.0.0-beta/emmo-inferred.ttl"
        ]

    # Add imported ontologies
    catalog = {} if catalog is None else catalog
    for path in imported_ontology_paths:
        imported = onto.world.get_ontology(path).load()
        onto.imported_ontologies.append(imported)
        catalog[imported.base_iri.rstrip("/")] = path

    print("===", onto.imported_ontologies)

    with onto:
        # Add title
        try:
            _add_literal(
                metadata,
                onto.metadata.title,
                "Title",
                metadata=True,
                only_one=True,
            )
        except AttributeError:
            pass

        # Add license
        try:
            _add_literal(
                metadata, onto.metadata.license, "License", metadata=True
            )
        except AttributeError:
            pass

        # Add authors/creators
        try:
            _add_literal(
                metadata, onto.metadata.creator, "Author", metadata=True
            )
        except AttributeError:
            pass

        # Add contributors
        try:
            _add_literal(
                metadata,
                onto.metadata.contributor,
                "Contributor",
                metadata=True,
            )
        except AttributeError:
            pass

        # Add versionInfo
        try:
            _add_literal(
                metadata,
                onto.metadata.versionInfo,
                "Ontology version Info",
                metadata=True,
                only_one=True,
            )
        except AttributeError:
            pass

    return onto, catalog


def _parse_literal(
    data: Union[pd.DataFrame, pd.Series],
    name: str,
    metadata: bool = False,
    sep: str = ";",
) -> list:
    """Helper function to make list ouf strings from ';'-delimited
    strings in one string.
    """

    if metadata is True:
        values = data.loc[data["Metadata name"] == name]["Value"].item()
    else:
        values = data[name]
    if not pd.isna(values):
        return str(values).split(sep)
    return values.split(sep)


def _add_literal(  # pylint: disable=too-many-arguments
    data: Union[pd.DataFrame, pd.Series],
    destination: owlready2.prop.IndividualValueList,  #
    name: str,
    metadata: bool = False,
    only_one: bool = False,
    sep: str = ";",
    expected: bool = True,
) -> None:
    """Append literal data to ontological entity."""
    try:
        name_list = _parse_literal(data, name, metadata=metadata, sep=sep)
        if only_one is True and len(name_list) > 1:
            warnings.warn(
                f"More than one {name} is given. The first was chosen."
            )
            destination.append(english(name_list[0]))
        else:
            destination.extend([english(nm) for nm in name_list])
    except (TypeError, ValueError, AttributeError):
        if expected:
            if metadata:
                warnings.warn(f"Missing metadata {name}")
            else:
                warnings.warn(f"{data[0]} has no {name}")
