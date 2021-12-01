#!/usr/bin/env python3
"""
Module from parsing an excelfile and creating an
ontology from it.

The excelfile is read by pandas and the pandas
dataframe should have column names:
[
"""
import argparse
import sys
import pyparsing
import pandas as pd
from ontopy import World
from ontopy.utils import NoSuchLabelError
from ontopy.manchester import evaluate
import owlready2  # pylint: disable=C0411


def english(string):
    """Returns `string` as an English location string."""
    return owlready2.locstr(string, lang="en")

def create_ontology_from_excel(excelpath: str, sheet_name: str = "Concepts", base_iri: str =
                               "http://emmo.info/emmo/domain/onto#" ) -> pd.DataFrame:
    # Read datafile
    dataframe = pd.read_excel(excelpath, sheet_name=sheet_name, skiprows=[0, 2])
    # Some magic to identify the header row
    return create_ontology_from_pandas(dataframe, base_iri)


def create_ontology_from_pandas(data: pd.DataFrame, base_iri: str =
                                "http://emmo.info/emmo/domain/onto#" ) -> owlready2.Ontology:

    # Make new ontology and import ontologies
    world = World()

    # have to decide how to add metadata and imports etc.
    # base_iri to be added from excel (maybe also possibly argument?)
    onto = world.get_ontology("http://emmo.info/emmo/domain/onto#")
    onto.base_iri = "http://emmo.info/emmo/domain/onto#"

    # imported ontologies to be added from excel
    catalog = {}
    imported_ontology_paths = [
        (
            "https://raw.githubusercontent.com/emmo-repo/"
            "emmo-repo.github.io/master/versions/"
            "1.0.0-beta/emmo-inferred-chemistry2.ttl"
        )
    ]

    # Add imported ontologies
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

                        # make warning!
                        print("--------------------------------")
                        print(
                            "At least one of the defined parents do not exist"
                        )
                        print(
                            "Concept:", name, "; Defined parents", parent_names
                        )
                        print("--------------------------------")
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
        properties = row["Properties"]
        if isinstance(properties, str):
            concept = onto.get_by_label(row["Concept (prefLabel)"])
            props = properties.split(";")
            for prop in props:
                try:
                    concept.is_a.append(evaluate(onto, prop))
                except pyparsing.ParseException as err:
                    # make warning!
                    print("*******************************************")
                    print("Error in Property assignment for:", concept)
                    print("Property to be Evaluated: ", prop)
                    print(err)
                    print("*******************************************")

    return onto
