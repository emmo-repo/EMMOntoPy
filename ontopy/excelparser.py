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
    Creates an ontology from an Excel-file.

    Arguments:
        excelpath: Path to Excel workbook.
        concept_sheet_name: Name of sheet where concepts are defined.
            The second row of this sheet should contain column names that are
            supported. Currently these are 'prefLabel','altLabel',
            'Elucidation', 'Comments', 'Examples', 'subClassOf', 'Relations'.
            Multiple entries are separated with ';'.
        metadata_sheet_name: Name of sheet where metadata are defined.
            The first row contains column names 'Metadata name' and 'Value'
            Supported 'Metadata names' are: 'Ontology IRI',
            'Ontology vesion IRI', 'Ontology version Info', 'Title',
            'Abstract', 'License', 'Comment', 'Author', 'Contributor'.
            Multiple entries are separated with a semi-colon (`;`).
        imports_sheet_name: Name of sheet where imported ontologies are
            defined.
            Column name is 'Imported ontologies'.
            Fully resolvable URL or path to imported ontologies provided one
            per row.
        base_iri: Base IRI of the new ontology.
        base_iri_from_metadata: Whether to use base IRI defined from metadata.
        imports: List of imported ontologies.
        catalog: Imported ontologies with (name, full path) key/value-pairs.
        force: Forcibly make an ontology by skipping concepts with a prefLabel
            that is erroneously defined.

    Returns:
        A tuple of the created ontology and the associated catalog of ontology
        names and resolvable path as dict.


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

    # Remove lines with empty prefLabel
    data = data[data["prefLabel"].notna()]
    # Convert all data to string, remove spaces, and finally remove
    # additional rows with empty prefLabel.
    data = data.astype(str)
    data["prefLabel"] = data["prefLabel"].str.strip()
    data = data[data["prefLabel"].str.len() > 0]
    data.reset_index(drop=True, inplace=True)

    # Make new ontology
    onto, catalog = get_metadata_from_dataframe(
        metadata, base_iri, imports=imports
    )

    # Set given or default base_iri if base_iri_from_metadata is False.
    if not base_iri_from_metadata:
        onto.base_iri = base_iri

    labels = set(data["prefLabel"])
    for altlabel in data["altLabel"].str.strip():
        if not altlabel == "nan":
            labels.update(altlabel.split(";"))

    # Dictionary with lists of concepts that raise errors
    concepts_with_errors = {
        "already_defined": [],
        "in_imported_ontologies": [],
        "wrongly_defined": [],
        "missing_parents": [],
        "invalid_parents": [],
        "nonadded_concepts": [],
    }

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
                    if not force:
                        raise ExcelError(
                            f'Concept "{name}" already in ontology'
                        )
                    warnings.warn(
                        f'Ignoring concept "{name}" since it is already in '
                        "the ontology."
                    )
                    concepts_with_errors["already_defined"].append(name)
                    # What to do if we want to add info to this concept?
                    # Should that be not allowed?
                    # If it should be allowed the index has to be added to
                    # added_rows
                    continue
                except (ValueError, TypeError) as err:
                    warnings.warn(
                        f'Ignoring concept "{name}". '
                        f'The following error was raised: "{err}"'
                    )
                    concepts_with_errors["wrongly_defined"].append(name)
                    continue
                except NoSuchLabelError:
                    pass

                if pd.isna(row["subClassOf"]):
                    if not force:
                        raise ExcelError(f"{row[0]} has no subClassOf")
                    parent_names = []  # Should be "owl:Thing"
                    concepts_with_errors["missing_parents"].append(name)
                else:
                    parent_names = str(row["subClassOf"]).split(";")

                parents = []
                invalid_parent = False
                for parent_name in parent_names:
                    try:
                        parent = onto.get_by_label(parent_name.strip())
                    except (NoSuchLabelError, ValueError) as exc:
                        if parent_name not in labels:
                            if force:
                                warnings.warn(
                                    f'Invalid parents for "{name}": '
                                    f'"{parent_name}".'
                                )
                                concepts_with_errors["invalid_parents"].append(
                                    name
                                )
                                break
                            raise ExcelError(
                                f'Invalid parents for "{name}": {exc}\n'
                                "Have you forgotten an imported ontology?"
                            ) from exc
                        invalid_parent = True
                        break
                    else:
                        parents.append(parent)

                if invalid_parent:
                    continue

                if not parents:
                    parents = [owlready2.Thing]

                concept = onto.new_entity(name, parents)
                added_rows.add(index)
                # Add elucidation
                try:
                    _add_literal(
                        row,
                        concept.elucidation,
                        "Elucidation",
                        only_one=True,
                    )
                except AttributeError as err:
                    if force:
                        _add_literal(
                            row,
                            concept.comment,
                            "Elucidation",
                            only_one=True,
                        )
                        warnings.warn("Elucidation added as comment.")
                    else:
                        raise ExcelError(
                            f"Not able to add elucidations. {err}."
                        ) from err

                # Add examples
                try:
                    _add_literal(
                        row, concept.example, "Examples", expected=False
                    )
                except AttributeError:
                    if force:
                        warnings.warn(
                            "Not able to add examples. "
                            "Did you forget to import an ontology?."
                        )

                # Add comments
                _add_literal(row, concept.comment, "Comments", expected=False)

                # Add altLabels
                try:
                    _add_literal(
                        row, concept.altLabel, "altLabel", expected=False
                    )
                except AttributeError as err:
                    if force is True:
                        _add_literal(
                            row,
                            concept.label,
                            "altLabel",
                            expected=False,
                        )
                        warnings.warn("altLabel added as rdfs.label.")
                    else:
                        raise ExcelError(
                            f"Not able to add altLabels. " f"{err}."
                        ) from err

            remaining_rows.difference_update(added_rows)

            # Detect infinite loop...
            if not added_rows and remaining_rows:
                unadded = [data.loc[i].prefLabel for i in remaining_rows]
                if force is True:
                    warnings.warn(
                        f"Not able to add the following concepts: {unadded}."
                        " Will continue without these."
                    )
                    remaining_rows = False
                    concepts_with_errors["nonadded_concepts"] = unadded
                else:
                    raise ExcelError(
                        f"Not able to add the following concepts: {unadded}."
                    )

    # Add properties in a second loop

    for index in added_rows:
        row = data.loc[index]
        properties = row["Relations"]
        if properties == "nan":
            properties = None
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
                    concepts_with_errors["errors_in_properties"].append(name)
                except NoSuchLabelError as exc:
                    msg = (
                        f"Error in Property assignment for: {concept}. "
                        f"Property to be Evaluated: {prop}. "
                        f"Error is {exc}."
                    )
                    if force is True:
                        warnings.warn(msg)
                        concepts_with_errors["errors_in_properties"].append(
                            name
                        )
                    else:
                        raise ExcelError(msg) from exc

    # Synchronise Python attributes to ontology
    onto.sync_attributes(
        name_policy="uuid", name_prefix="EMMO_", class_docstring="elucidation"
    )
    onto.dir_label = False
    concepts_with_errors = {
        key: set(value) for key, value in concepts_with_errors.items()
    }
    return onto, catalog, concepts_with_errors


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
    if not (pd.isna(values) or values == "nan"):
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
