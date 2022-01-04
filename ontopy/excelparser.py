"""
Module from parsing an excelfile and creating an
ontology from it.

The excelfile is read by pandas and the pandas
dataframe should have column names:
prefLabel, altLabel, Elucidation, Comments, Examples,
subClassOf, Relations.

Note that correct case is mandatory.
"""
from typing import Tuple, Union, Sequence
import warnings

import pandas as pd
import pyparsing

import ontopy
from ontopy import get_ontology
from ontopy.utils import EMMOntoPyException, NoSuchLabelError
from ontopy.manchester import evaluate
import owlready2  # pylint: disable=C0411


class ExcelError(EMMOntoPyException):
    """Raised on errors in Excel file."""


def english(string):
    """Returns `string` as an English location string."""
    return owlready2.locstr(string, lang="en")


def create_ontology_from_excel(  # pylint: disable=too-many-arguments
    excelpath: str,
    concept_sheet_name: str = "Concepts",
    metadata_sheet_name: str = "Metadata",
    imports_sheet_name: str = "ImportedOntologies",
    base_iri: str = "http://emmo.info/emmo/domain/onto#",
    base_iri_from_metadata: bool = True,
    imports: list = None,
    catalog: dict = None,
    force: bool = False,
) -> Tuple[ontopy.ontology.Ontology, dict]:
    """
    Creates an ontology from an excelfile.

    Catalog is dict of imported ontologies with key name and value path.
    """
    # Get imported ontologies from optional "Imports" sheet
    if not imports:
        imports = []
    try:
        imports_frame = pd.read_excel(
            excelpath, sheet_name=imports_sheet_name, skiprows=[1]
        )
    except ValueError:
        pass
    else:
        imports.extend(imports_frame["Imported ontologies"].to_list())

    # Read datafile TODO: Some magic to identify the header row
    conceptdata = pd.read_excel(
        excelpath, sheet_name=concept_sheet_name, skiprows=[0, 2]
    )
    metadata = pd.read_excel(excelpath, sheet_name=metadata_sheet_name)
    return create_ontology_from_pandas(
        data=conceptdata,
        metadata=metadata,
        imports=imports,
        base_iri=base_iri,
        base_iri_from_metadata=base_iri_from_metadata,
        catalog=catalog,
        force=force,
    )


def create_ontology_from_pandas(  # pylint:disable=too-many-locals,too-many-branches,too-many-statements,too-many-arguments
    data: pd.DataFrame,
    metadata: pd.DataFrame,
    imports: list,
    base_iri: str = "http://emmo.info/emmo/domain/onto#",
    base_iri_from_metadata: bool = True,
    catalog: dict = None,
    force: bool = False,
) -> Tuple[ontopy.ontology.Ontology, dict]:
    """
    Create an ontology from a pandas DataFrame.
    """

    # Remove Concepts without prefLabel and make all to string
    # data[
    #    data['prefLabel'].apply(lambda x: x.notna())
    # ]
    # df['cars'].apply(lambda x: "i" in x) &
    # df['age'].apply(lambda x: int(x)<2)
    #  ]
    data = data[data["prefLabel"].notna()]
    data = data.astype({"prefLabel": "str"})
    data["prefLabel"] = data["prefLabel"].str.strip()
    data = data[data["prefLabel"].str.len() > 0]
    data.reset_index(drop=True, inplace=True)

    # Make new ontology
    onto, catalog = get_metadata_from_dataframe(
        metadata, base_iri, imports=imports
    )
    # base_iri from metadata if it exists and base_iri_from_metadata
    if not base_iri_from_metadata:
        onto.base_iri = base_iri

    onto.sync_python_names()
    with onto:
        remaining_rows = set(range(len(data)))
        while remaining_rows:
            added_rows = set()
            for index in remaining_rows:
                row = data.loc[index]
                name = row["prefLabel"]
                try:
                    onto.get_by_label(name)
                except (ValueError, TypeError) as err:
                    warnings.warn(
                        f'Ignoring concept "{name}". '
                        f'The following error was raised: "{err}"'
                    )
                    continue
                except NoSuchLabelError:
                    pass

                if name in onto:
                    if not force:
                        raise ExcelError(
                            f'Concept "{name}" already in ontology'
                        )
                    warnings.warn(
                        f'Ignoring concept "{name}" since it is already in '
                        "the ontology."
                    )
                    # What to do if we want to add info to this concept?
                    # Should that be not allowed?
                    # If it should be allowed the index has to be added to
                    # added_rows
                    continue

                if pd.isna(row["subClassOf"]):
                    if not force:
                        raise ExcelError(f"{row[0]} has no subClassOf")
                    parent_names = []  # Should be "owl:Thing"
                else:
                    parent_names = str(row["subClassOf"]).split(";")

                parents = []
                for parent_name in parent_names:
                    print(parent_name)
                    try:
                        parent = onto.get_by_label(parent_name.strip())
                    except NoSuchLabelError as exc:
                        if force:
                            warnings.warn(
                                f'Invalid parents for "{name}": {parent_name}'
                            )
                            continue
                        raise ExcelError(
                            f'Invalid parents for "{name}": {exc}\n'
                            "Have you forgotten an imported ontology?"
                        ) from exc
                    else:
                        parents.append(parent)
                if not parents:
                    parents = [owlready2.Thing]

                concept = onto.new_entity(name, parents)
                added_rows.add(index)

                # Add elucidation
                _add_literal(
                    row,
                    concept.elucidation,
                    "Elucidation",
                    only_one=True,
                )

                # Add examples
                _add_literal(row, concept.example, "Examples", expected=False)

                # Add comments
                _add_literal(row, concept.comment, "Comments", expected=False)

                # Add altLabels
                _add_literal(row, concept.altLabel, "altLabel", expected=False)
            remaining_rows.difference_update(added_rows)

            # Detect infinite loop...
            if not added_rows and remaining_rows:
                unadded = [data.loc[i].prefLabel for i in remaining_rows]
                if force:
                    warnings.warn(
                        f"Not able to add the following concepts: {unadded}."
                        " Will continue without these."
                    )
                    remaining_rows = False
                else:
                    raise ExcelError(
                        f"Not able to add the following concepts: {unadded}."
                    )

    # Add properties in a second loop
    for index in added_rows:
        row = data.loc[index]
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
                except pyparsing.ParseException as exc:
                    warnings.warn(
                        f"Error in Property assignment for: {concept}. "
                        f"Property to be Evaluated: {prop}. "
                        f"Error is {exc}."
                    )
                except NoSuchLabelError as exc:
                    if force is True:
                        pass
                    else:
                        raise ExcelError(exc) from exc

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
    imports: Sequence = (),
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
        except (TypeError, ValueError, AttributeError, IndexError):
            pass

    # Create new ontology
    onto = get_ontology(base_iri)

    # Add imported ontologies
    catalog = {} if catalog is None else catalog
    locations = set()
    for location in imports:
        if not pd.isna(location) and location not in locations:
            imported = onto.world.get_ontology(location).load()
            onto.imported_ontologies.append(imported)
            catalog[imported.base_iri.rstrip("#/")] = location
            locations.add(location)

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
    return []


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
