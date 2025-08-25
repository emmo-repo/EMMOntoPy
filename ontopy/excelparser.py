"""
Module from parsing an excelfile and creating an
ontology from it.

The excelfile is read by pandas and the pandas
dataframe should have column names:
prefLabel, altLabel, Elucidation, Comments, Examples,
subClassOf, Relations.

Note that correct case is mandatory.
"""

import os
from typing import Tuple, Union
import warnings

import pandas as pd
import numpy as np
import pyparsing
import defusedxml.ElementTree as ET

import ontopy
from ontopy import get_ontology
from ontopy.exceptions import ExcelError, NoSuchLabelError
from ontopy.exceptions import ReadCatalogError, LabelDefinitionError
from ontopy.utils import read_catalog, english
from ontopy.manchester import evaluate
import owlready2  # pylint: disable=C0411


def create_ontology_from_excel(  # pylint: disable=too-many-arguments, too-many-locals
    excelpath: str,
    *,
    concept_sheet_name: str = "Concepts",
    metadata_sheet_name: str = "Metadata",
    imports_sheet_name: str = "ImportedOntologies",
    dataproperties_sheet_name: str = "DataProperties",
    objectproperties_sheet_name: str = "ObjectProperties",
    annotationproperties_sheet_name: str = "AnnotationProperties",
    base_iri: str = "http://emmo.info/emmo/domain/onto#",
    base_iri_from_metadata: bool = True,
    imports: list = None,
    catalog: dict = None,
    force: bool = False,
    input_ontology: Union[ontopy.ontology.Ontology, None] = None,
) -> Tuple[ontopy.ontology.Ontology, dict, dict]:
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
        dataproperties_sheet_name: Name of sheet where data properties are
            defined. The second row of this sheet should contain column names
            that are supported. Currently these are 'prefLabel','altLabel',
            'Elucidation', 'Comments', 'Examples', 'subPropertyOf',
            'Domain', 'Range', 'dijointWith', 'equivalentTo'.
        annotationproperties_sheet_name: Name of sheet where annotation
            properties are defined. The second row of this sheet should contain
            column names that are supported. Currently these are 'prefLabel',
            'altLabel', 'Elucidation', 'Comments', 'Examples', 'subPropertyOf',
            'Domain', 'Range'.
        objectproperties_sheet_name: Name of sheet where object properties are
            defined.The second row of this sheet should contain column names
            that are supported. Currently these are 'prefLabel','altLabel',
            'Elucidation', 'Comments', 'Examples', 'subPropertyOf',
            'Domain', 'Range', 'inverseOf', 'dijointWith', 'equivalentTo'.
        base_iri: Base IRI of the new ontology.
        base_iri_from_metadata: Whether to use base IRI defined from metadata.
        imports: List of imported ontologies.
        catalog: Imported ontologies with (name, full path) key/value-pairs.
        force: Forcibly make an ontology by skipping concepts
            that are erroneously defined or other errors in the excel sheet.
        input_ontology: Ontology that should be updated.
            Default is None,
            which means that a completely new ontology is generated.
            If an input_ontology to be updated is provided,
            the metadata sheet in the excel sheet will not be considered.


    Returns:
        A tuple with the:

            * created ontology
            * associated catalog of ontology names and resolvable path as dict
            * a dictionary with lists of concepts that raise errors, with the
              following keys:

                - "already_defined": These are concepts (classes)
                    that are already in the
                    ontology, because they were already added in a
                    previous line of the excelfile/pandas dataframe, or because
                    it is already defined in an imported ontology with the same
                    base_iri as the newly created ontology.
                - "in_imported_ontologies": Concepts (classes)
                    that are defined in the
                    excel, but already exist in the imported ontologies.
                - "wrongly_defined": Concepts (classes) that are given an
                    invalid prefLabel (e.g. with a space in the name).
                - "missing_subClassOf": Concepts (classes) that are missing
                    parents. These concepts are added directly under owl:Thing.
                - "invalid_subClassOf": Concepts (classes) with invalidly
                    defined parents.
                    These concepts are added directly under owl:Thing.
                - "nonadded_concepts": List of all concepts (classes) that are
                    not added,
                    either because the prefLabel is invalid, or because the
                    concept has already been added once or already exists in an
                    imported ontology.
                - "obj_prop_already_defined": Object properties that are already
                    defined in the ontology.
                - "obj_prop_in_imported_ontologies": Object properties that are
                    defined in the excel, but already exist in the imported
                    ontologies.
                - "obj_prop_wrongly_defined": Object properties that are given
                    an invalid prefLabel (e.g. with a space in the name).
                - "obj_prop_missing_subPropertyOf": Object properties that are
                    missing parents.
                - "obj_prop_invalid_subPropertyOf": Object properties with
                    invalidly defined parents.
                - "obj_prop_nonadded_entities": List of all object properties
                    that are not added, either because the prefLabel is invalid,
                    or because the concept has already been added once or
                    already exists in an imported ontology.
                - "obj_prop_errors_in_properties": Object properties with
                    invalidly defined properties.
                - "obj_prop_errors_in_range": Object properties with invalidly
                    defined range.
                - "obj_prop_errors_in_domain": Object properties with invalidly
                    defined domain.
                - "annot_prop_already_defined": Annotation properties that are
                    already defined in the ontology.
                - "annot_prop_in_imported_ontologies":  Annotation properties
                    that
                    are defined in the excel, but already exist in the imported
                    ontologies.
                - "annot_prop_wrongly_defined": Annotation properties that are
                    given an invalid prefLabel (e.g. with a space in the name).
                - "annot_prop_missing_subPropertyOf": Annotation properties that
                    are missing parents.
                - "annot_prop_invalid_subPropertyOf": Annotation properties with
                    invalidly defined parents.
                - "annot_prop_nonadded_entities": List of all annotation
                    properties that are not added, either because the prefLabel
                    is invalid, or because the concept has already been added
                    once or already exists in an imported ontology.
                - "annot_prop_errors_in_properties": Annotation properties with
                    invalidly defined properties.
                - "data_prop_already_defined": Data properties that are already
                    defined in the ontology.
                - "data_prop_in_imported_ontologies": Data properties that are
                    defined in the excel, but already exist in the imported
                    ontologies.
                - "data_prop_wrongly_defined":  Data properties that are given
                    an invalid prefLabel (e.g. with a space in the name).
                - "data_prop_missing_subPropertyOf": Data properties that are
                    missing parents.
                - "data_prop_invalid_subPropertyOf": Data properties with
                    invalidly defined parents.
                - "data_prop_nonadded_entities": List of all data properties
                    that are not added, either because the prefLabel is invalid,
                    or because the concept has already been added once or
                    already exists in an imported ontology.
                - "data_prop_errors_in_properties": Data properties with
                    invalidly defined properties.
                - "data_prop_errors_in_range": Data properties with invalidly
                    defined range.
                - "data_prop_errors_in_domain": Data properties with invalidly
                    defined domain.

    """
    web_protocol = "http://", "https://", "ftp://"

    def _relative_to_absolute_paths(path):
        if isinstance(path, str):
            if not path.startswith(web_protocol):
                path = os.path.dirname(excelpath) + "/" + str(path)
        return path

    try:
        imports = pd.read_excel(
            excelpath, sheet_name=imports_sheet_name, skiprows=[1]
        )
    except ValueError:
        imports = pd.DataFrame()
    else:
        # Strip leading and trailing white spaces in paths
        imports.replace(r"^\s+", "", regex=True).replace(
            r"\s+$", "", regex=True
        )
        # Set empty strings to nan
        imports = imports.replace(r"^\s*$", np.nan, regex=True)
        if "Imported ontologies" in imports.columns:
            imports["Imported ontologies"] = imports[
                "Imported ontologies"
            ].apply(_relative_to_absolute_paths)

    # Read datafile TODO: Some magic to identify the header row
    conceptdata = pd.read_excel(
        excelpath, sheet_name=concept_sheet_name, skiprows=[0, 2]
    )
    try:
        objectproperties = pd.read_excel(
            excelpath, sheet_name=objectproperties_sheet_name, skiprows=[0, 2]
        )
        if "prefLabel" not in objectproperties.columns:
            warnings.warn(
                "The 'prefLabel' column is missing in "
                f"{objectproperties_sheet_name}. "
                "New object properties will not be added to the ontology."
            )
            objectproperties = None
    except ValueError:
        warnings.warn(
            f"No sheet named {objectproperties_sheet_name} found "
            f"in {excelpath}. "
            "New object properties will not be added to the ontology."
        )
        objectproperties = None
    try:
        annotationproperties = pd.read_excel(
            excelpath,
            sheet_name=annotationproperties_sheet_name,
            skiprows=[0, 2],
        )
        if "prefLabel" not in annotationproperties.columns:
            warnings.warn(
                "The 'prefLabel' column is missing in "
                f"{annotationproperties_sheet_name}. "
                "New annotation properties will not be added to the ontology."
            )
            annotationproperties = None
    except ValueError:
        warnings.warn(
            f"No sheet named {annotationproperties_sheet_name} "
            f"found in {excelpath}. "
            "New annotation properties will not be added to the ontology."
        )
        annotationproperties = None

    try:
        dataproperties = pd.read_excel(
            excelpath, sheet_name=dataproperties_sheet_name, skiprows=[0, 2]
        )
        if "prefLabel" not in dataproperties.columns:
            warnings.warn(
                "The 'prefLabel' column is missing in "
                f"{dataproperties_sheet_name}. "
                "New data properties will not be added to the ontology."
            )
            dataproperties = None
    except ValueError:
        warnings.warn(
            f"No sheet named {dataproperties_sheet_name} found in {excelpath}. "
            "New data properties will not be added to the ontology."
        )
        dataproperties = None

    metadata = pd.read_excel(excelpath, sheet_name=metadata_sheet_name)
    return create_ontology_from_pandas(
        data=conceptdata,
        objectproperties=objectproperties,
        dataproperties=dataproperties,
        annotationproperties=annotationproperties,
        metadata=metadata,
        imports=imports,
        base_iri=base_iri,
        base_iri_from_metadata=base_iri_from_metadata,
        catalog=catalog,
        force=force,
        input_ontology=input_ontology,
    )


def create_ontology_from_pandas(  # pylint:disable=too-many-locals,too-many-branches,too-many-statements,too-many-arguments, too-many-positional-arguments
    data: pd.DataFrame,
    objectproperties: pd.DataFrame,
    annotationproperties: pd.DataFrame,
    dataproperties: pd.DataFrame,
    metadata: pd.DataFrame,
    imports: pd.DataFrame,
    base_iri: str = "http://emmo.info/emmo/domain/onto#",
    base_iri_from_metadata: bool = True,
    catalog: dict = None,
    force: bool = False,
    input_ontology: Union[ontopy.ontology.Ontology, None] = None,
) -> Tuple[ontopy.ontology.Ontology, dict]:
    """
    Create an ontology from a pandas DataFrame.

    Check 'create_ontology_from_excel' for complete documentation.
    """
    # Get ontology to which new concepts should be added
    if input_ontology:
        onto = input_ontology
        catalog = {}
        # Since we will remove newly created python_name added
        # by owlready2 in the triples, we keep track of those
        # that come from the input ontology
        pyname_triples_to_keep = list(
            onto.get_unabbreviated_triples(
                predicate="http://www.lesfleursdunormal.fr/static/_downloads/"
                "owlready_ontology.owl#python_name"
            )
        )
    else:  # Create new ontology
        onto, catalog = get_metadata_from_dataframe(
            metadata, base_iri, imports=imports
        )

        # Set given or default base_iri if base_iri_from_metadata is False.
        if not base_iri_from_metadata:
            onto.base_iri = base_iri
    # onto.sync_python_names()
    # prefLabel, label, and altLabel
    # are default label annotations
    onto.set_default_label_annotations()
    # Add object properties
    if objectproperties is not None:
        objectproperties = _clean_dataframe(objectproperties)
        (
            onto,
            objectproperties_with_errors,
            added_objprop_indices,
        ) = _add_entities(
            onto=onto,
            data=objectproperties,
            entitytype=owlready2.ObjectPropertyClass,
            force=force,
        )

    if annotationproperties is not None:
        annotationproperties = _clean_dataframe(annotationproperties)
        (
            onto,
            annotationproperties_with_errors,
            added_annotprop_indices,
        ) = _add_entities(
            onto=onto,
            data=annotationproperties,
            entitytype=owlready2.AnnotationPropertyClass,
            force=force,
        )

    if dataproperties is not None:
        dataproperties = _clean_dataframe(dataproperties)
        (
            onto,
            dataproperties_with_errors,
            added_dataprop_indices,
        ) = _add_entities(
            onto=onto,
            data=dataproperties,
            entitytype=owlready2.DataPropertyClass,
            force=force,
        )
    onto.sync_attributes(
        name_policy="uuid", name_prefix="EMMO_", class_docstring="elucidation"
    )
    # Clean up data frame with new concepts
    data = _clean_dataframe(data)
    # Add entities
    onto, entities_with_errors, added_concept_indices = _add_entities(
        onto=onto, data=data, entitytype=owlready2.ThingClass, force=force
    )

    # Add entity properties in a second loop
    for index in added_concept_indices:
        row = data.loc[index]
        properties = row["Relations"]
        if properties == "nan":
            properties = None
        if isinstance(properties, str):
            try:
                entity = onto.get_by_label(row["prefLabel"].strip())
            except NoSuchLabelError:
                pass
            props = properties.split(";")
            for prop in props:
                try:
                    entity.is_a.append(evaluate(onto, prop.strip()))
                except pyparsing.ParseException as exc:
                    warnings.warn(
                        # This is currently not tested
                        f"Error in Property assignment for: '{entity}'. "
                        f"Property to be Evaluated: '{prop}'. "
                        f"{exc}"
                    )
                    entities_with_errors["errors_in_properties"].append(
                        entity.name
                    )
                except NoSuchLabelError as exc:
                    msg = (
                        f"Error in Property assignment for: {entity}. "
                        f"Property to be Evaluated: {prop}. "
                        f"{exc}"
                    )
                    if force is True:
                        warnings.warn(msg)
                        entities_with_errors["errors_in_properties"].append(
                            entity.name
                        )
                    else:
                        raise ExcelError(msg) from exc

    # Add range and domain for object properties
    if objectproperties is not None:
        onto, objectproperties_with_errors = _add_range_domain(
            onto=onto,
            properties=objectproperties,
            added_prop_indices=added_objprop_indices,
            properties_with_errors=objectproperties_with_errors,
            force=force,
        )
        for key, value in objectproperties_with_errors.items():
            entities_with_errors["obj_prop_" + key] = value
    # Add range and domain for annotation properties
    if annotationproperties is not None:
        onto, annotationproperties_with_errors = _add_range_domain(
            onto=onto,
            properties=annotationproperties,
            added_prop_indices=added_annotprop_indices,
            properties_with_errors=annotationproperties_with_errors,
            force=force,
        )
        for key, value in annotationproperties_with_errors.items():
            entities_with_errors["annot_prop_" + key] = value

    # Add range and domain for data properties
    if dataproperties is not None:
        onto, dataproperties_with_errors = _add_range_domain(
            onto=onto,
            properties=dataproperties,
            added_prop_indices=added_dataprop_indices,
            properties_with_errors=dataproperties_with_errors,
            force=force,
        )
        for key, value in dataproperties_with_errors.items():
            entities_with_errors["data_prop_" + key] = value

    # Synchronise Python attributes to ontology
    onto.sync_attributes(
        name_policy="uuid", name_prefix="EMMO_", class_docstring="elucidation"
    )
    onto.dir_label = False
    entities_with_errors = {
        key: set(value) for key, value in entities_with_errors.items()
    }

    # Remove triples with predicate 'python_name' added by owlready2
    onto._del_data_triple_spod(  # pylint: disable=protected-access
        p=onto._abbreviate(  # pylint: disable=protected-access
            "http://www.lesfleursdunormal.fr/static/_downloads/"
            "owlready_ontology.owl#python_name"
        )
    )

    # Add back the triples python name triples that were in the input_ontology.
    if input_ontology:
        for triple in pyname_triples_to_keep:
            onto._add_data_triple_spod(  # pylint: disable=protected-access
                s=triple[0], p=triple[1], o=triple[2]
            )

    return onto, catalog, entities_with_errors


def get_metadata_from_dataframe(  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    metadata: pd.DataFrame,
    base_iri: str,
    base_iri_from_metadata: bool = True,
    imports: pd.DataFrame = None,
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
    for _, row in imports.iterrows():
        # for location in imports:
        location = row["Imported ontologies"]
        if not pd.isna(location) and location not in locations:
            imported = onto.world.get_ontology(location).load()
            onto.imported_ontologies.append(imported)
            catalog[imported.base_iri.rstrip("#/")] = location
            try:
                cat = read_catalog(location.rsplit("/", 1)[0])
                catalog.update(cat)
            except (ReadCatalogError, ET.ParseError):  # Issue 840
                warnings.warn(f"Catalog for {imported} not found.")
            locations.add(location)
        # set defined prefix
        if not pd.isna(row["prefix"]):
            # set prefix for all ontologies with same 'base_iri_root'
            if not pd.isna(row["base_iri_root"]):
                onto.set_common_prefix(
                    iri_base=row["base_iri_root"], prefix=row["prefix"]
                )
            # If base_root not given, set prefix only to top ontology
            else:
                imported.prefix = row["prefix"]

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
    *,
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


def _clean_dataframe(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Remove lines with empty prefLabel,
    convert all data to strings, remove spaces, and finally remove
    additional rows with 0-length prefLabel.
    """
    data = data[data["prefLabel"].notna()]
    data = data.astype(str)
    data["prefLabel"] = data["prefLabel"].str.strip()
    data = data[data["prefLabel"].str.len() > 0]
    data.reset_index(drop=True, inplace=True)
    return data


def _add_entities(
    # pylint: disable=too-many-statements,too-many-branches, too-many-locals
    onto: ontopy.ontology.Ontology,
    data: pd.DataFrame,
    entitytype: Union[
        owlready2.ThingClass,
        owlready2.AnnotationPropertyClass,
        owlready2.ObjectPropertyClass,
        owlready2.DataPropertyClass,
    ],
    force: bool = False,
) -> Tuple[ontopy.ontology.Ontology, dict, list]:
    """Add entities to ontology.
    Returns ontology, dictionary with lists of entities that raise errors,
    and a list with indices of added rows."""
    labels = set(data["prefLabel"])
    for altlabel in data["altLabel"].str.strip():
        if not altlabel == "nan":
            labels.update(altlabel.split(";"))
    # Find column name depending on entitytype
    rowheader = "entity_type_not_set"
    if entitytype is owlready2.ThingClass:
        rowheader = "subClassOf"
    # If entitytype is a subclass of owlready2.PropertyClass
    elif entitytype in [
        owlready2.AnnotationPropertyClass,
        owlready2.ObjectPropertyClass,
        owlready2.DataPropertyClass,
    ]:
        rowheader = "subPropertyOf"
    else:
        raise TypeError(f"Unexpected `entitytype`: {entitytype!r}")

    # Dictionary with lists of entities that raise errors
    entities_with_errors = {
        "already_defined": [],
        "in_imported_ontologies": [],
        "wrongly_defined": [],
        f"missing_{rowheader}": [],
        f"invalid_{rowheader}": [],
        "nonadded_entities": [],
        "errors_in_properties": [],
    }

    with onto:
        remaining_rows = set(range(len(data)))
        all_added_rows = []
        while remaining_rows:
            added_rows = set()
            for index in remaining_rows:
                row = data.loc[index]
                name = row["prefLabel"]
                # Check if entity is already in ontology
                try:
                    onto.get_by_label(name)
                    if onto.base_iri in [
                        a.namespace.base_iri
                        for a in onto.get_by_label_all(name)
                    ]:
                        if not force:
                            raise ExcelError(
                                f'Concept "{name}" already in ontology'
                            )
                        warnings.warn(
                            f'Ignoring concept "{name}" since it is already in '
                            "the ontology."
                        )
                        entities_with_errors["already_defined"].append(name)
                        continue
                    entities_with_errors["in_imported_ontologies"].append(name)
                except (ValueError, TypeError) as err:
                    warnings.warn(
                        f'Ignoring concept "{name}". '
                        f'The following error was raised: "{err}"'
                    )
                    entities_with_errors["wrongly_defined"].append(name)
                    continue
                except NoSuchLabelError:
                    pass

                # Find parents
                if entitytype is owlready2.ThingClass:
                    rowheader = "subClassOf"
                # If entitytype is a subclass of owlready2.PropertyClass
                elif entitytype in [
                    owlready2.AnnotationPropertyClass,
                    owlready2.ObjectPropertyClass,
                    owlready2.DataPropertyClass,
                ]:
                    rowheader = "subPropertyOf"

                (
                    parents,
                    invalid_parent,
                    entities_with_errors,
                ) = _make_entity_list(
                    onto,
                    row,
                    rowheader,
                    force,
                    entities_with_errors,
                    name,
                    labels,
                )
                if invalid_parent:
                    continue
                if not parents:
                    if entitytype == owlready2.ThingClass:
                        parents = [owlready2.Thing]
                    elif entitytype == owlready2.AnnotationPropertyClass:
                        parents = [owlready2.AnnotationProperty]
                    elif entitytype == owlready2.ObjectPropertyClass:
                        parents = [owlready2.ObjectProperty]
                    elif entitytype == owlready2.DataPropertyClass:
                        parents = [owlready2.DataProperty]

                # Add entity
                try:
                    entity = onto.new_entity(
                        name, parents, entitytype=entitytype
                    )
                except LabelDefinitionError:
                    entities_with_errors["wrongly_defined"].append(name)
                    continue
                added_rows.add(index)
                # Add elucidation
                try:
                    _add_literal(
                        row,
                        entity.elucidation,
                        "Elucidation",
                        only_one=True,
                    )
                except AttributeError as err:
                    if force:
                        _add_literal(
                            row,
                            entity.comment,
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
                        row, entity.example, "Examples", expected=False
                    )
                except AttributeError:
                    if force:
                        warnings.warn(
                            "Not able to add examples. "
                            "Did you forget to import an ontology?."
                        )

                # Add comments
                _add_literal(row, entity.comment, "Comments", expected=False)

                # Add altLabels
                try:
                    _add_literal(
                        row, entity.altLabel, "altLabel", expected=False
                    )
                except AttributeError as err:
                    if force is True:
                        _add_literal(
                            row,
                            entity.label,
                            "altLabel",
                            expected=False,
                        )
                        warnings.warn("altLabel added as rdfs.label.")
                    else:
                        raise ExcelError(
                            f"Not able to add altLabels. " f"{err}."
                        ) from err
                # Add other annotations if any

                if not (
                    pd.isna(row["Other annotations"])
                    or row["Other annotations"] == ""
                    or row["Other annotations"] == "nan"
                ):
                    for annotation in row["Other annotations"].split(";"):
                        key, value = annotation.split("=", 1)
                        entity[key.strip(" ")] = english(value.strip(" "))

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
                    entities_with_errors["nonadded_concepts"] = unadded
                else:
                    raise ExcelError(
                        f"Not able to add the following concepts: {unadded}."
                    )
            all_added_rows.extend(added_rows)

    return onto, entities_with_errors, all_added_rows


# Helper function for adding range and domain to properties
def _add_range_domain(
    onto: owlready2.Ontology,
    properties: pd.DataFrame,
    added_prop_indices: list,
    properties_with_errors: dict,
    force: bool = False,
) -> Tuple[owlready2.Ontology, dict]:
    """Add range and domain to properties.

    Arguments:
        onto: ontology with properties already added,
        properties: properties to whcih range and domain are to be added,
        added_prop_indices: indices in properties dataframe describing
            properties that have been added,
        properties_with_errors: dictionary to store properties with errors,
        force: if True, will skip properties with errors and add them to
            the dictionary. If False errors will cause eception.

    Returns:
        onto: ontology with range and domain added to properties,
        properties_with_errors: dictionary with properties with errors.
    """
    # check if both 'Ranges' and 'Domains' columns are present in dataframe
    if (
        "Ranges" not in properties.columns
        or "Domains" not in properties.columns
    ):
        return onto, properties_with_errors

    properties_with_errors["errors_in_range"] = []
    properties_with_errors["errors_in_domain"] = []
    for index in added_prop_indices:
        row = properties.loc[index]
        try:
            prop = onto.get_by_label(row["prefLabel"].strip())
        except NoSuchLabelError:
            pass
        if row["Ranges"] != "nan":
            try:
                prop.range = [onto.get_by_label(row["Ranges"].strip())]
            except NoSuchLabelError as exc:
                msg = (
                    f"Error in range assignment for: {prop}. "
                    f"Range to be Evaluated: {row['Ranges']}. "
                    f"{exc}"
                )
                if force is True:
                    warnings.warn(msg)
                    properties_with_errors["errors_in_range"].append(prop.name)
                else:
                    raise ExcelError(msg) from exc
        if row["Domains"] != "nan":
            try:
                prop.domain = [onto.get_by_label(row["Domains"].strip())]
            except NoSuchLabelError as exc:
                msg = (
                    f"Error in domain assignment for: {prop}. "
                    f"Domain to be Evaluated: {row['Domains']}. "
                    f"{exc}"
                )
                if force is True:
                    warnings.warn(msg)
                    properties_with_errors["errors_in_domain"].append(prop.name)
                else:
                    raise ExcelError(msg) from exc
    return onto, properties_with_errors


def _make_entity_list(  # pylint: disable=too-many-arguments, too-many-positional-arguments
    onto: owlready2.Ontology,
    row: pd.Series,
    rowheader: str,
    force: bool,
    entities_with_errors: dict,
    label: str,
    valid_labels: list,
):
    """Help function to create a list of entities
    from a pd.DataFrame wcich is a str."""
    if row[rowheader] == "nan":
        if not force:
            raise ExcelError(f"{row[0]} has no {rowheader}")
        name_list = []
        entities_with_errors[f"missing_{rowheader}"].append(label)
    else:
        name_list = str(row[rowheader]).split(";")
    concepts = []
    invalid_concept = False
    for name in name_list:
        try:
            concept = onto.get_by_label(name.strip())
        except (NoSuchLabelError, ValueError) as exc:
            if name not in valid_labels:
                if force:
                    warnings.warn(
                        f'Invalid {rowheader} for "{label}": ' f'"{name}".'
                    )
                    entities_with_errors[f"invalid_{rowheader}"].append(label)
                    break
                raise ExcelError(
                    f'Invalid {rowheader} for "{label}": {exc}\n'
                    "Have you forgotten an imported ontology?"
                ) from exc
            invalid_concept = True
            break
        else:
            concepts.append(concept)

    return concepts, invalid_concept, entities_with_errors
