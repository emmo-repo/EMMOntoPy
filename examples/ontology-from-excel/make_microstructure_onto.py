from ontopy import World, get_ontology
from ontopy.utils import NoSuchLabelError, write_catalog
from ontopy.manchester import evaluate
import owlready2

import pyparsing

import pandas as pd
import os
import numpy as np


def en(s):
    """Returns `s` as an English location string."""
    return owlready2.locstr(s, lang="en")


world = World()
chemistry_ontology_path = (
    "https://raw.githubusercontent.com/emmo-repo/"
    "emmo-repo.github.io/master/versions/"
    "1.0.0-beta/emmo-inferred-chemistry2.ttl"
)

chemistry = world.get_ontology(chemistry_ontology_path).load()

catalog = {chemistry.base_iri.rstrip("/"): chemistry_ontology_path}


# Create new ontology
onto = world.get_ontology("http://emmo.info/emmo/domain/onto#")
onto.base_iri = "http://emmo.info/emmo/domain/onto#"
onto.imported_ontologies.append(chemistry)
onto.sync_python_names()


# Read datafile
data = pd.read_excel("onto.xlsx", skiprows=1)


with onto:
    # loop through the rows until no more are added
    new_loop = True
    final_loop = False
    while new_loop:
        number_of_added_classes = 0
        for index, row in data.iterrows():
            name = row["Concept (prefLabel)"]
            try:
                if isinstance(onto.get_by_label(name), owlready2.ThingClass):
                    continue
            except NoSuchLabelError:
                pass

            parent_names = str(row["subClassOf"]).split(";")

            try:
                parents = [onto.get_by_label(pn) for pn in parent_names]
            except NoSuchLabelError:
                if final_loop == True:
                    parents = onto.EMMO
                    print("--------------------------------")
                    print("At least one of the defined parents do not exist")
                    print("Concept:", name, "; Defined parents", parent_names)
                    print("--------------------------------")
                    new_loop = False
                else:
                    continue

            Concept = onto.new_entity(name, parents)

            elucidation = row["Elucidation (definition intended for humans)"]
            if isinstance(elucidation, str):
                Concept.elucidation.append(en(elucidation))

            example = row["Example"]
            if isinstance(example, str):
                Concept.example.append(en(example))

            number_of_added_classes += 1

        if number_of_added_classes == 0:
            final_loop = True


# Add properties in a second loop
for index, row in data.iterrows():
    properties = row["Properties"]
    if isinstance(properties, str):
        Concept = onto.get_by_label(row["Concept (prefLabel)"])
        props = properties.split(";")
        for p in props:
            try:
                r = evaluate(onto, p)
                Concept.is_a.append(r)
            except pyparsing.ParseException as err:
                print("*******************************************")
                print("Error in Property assignment for:", Concept)
                print("Property to be Evaluated: ", p)
                print(err)
                print("*******************************************")


version = "0.1"

onto.metadata.title.append(en("microstructureonto"))
onto.metadata.creator.append(en("Sylvain Gouttebroze"))
onto.metadata.creator.append(en("Jesper Friis"))
onto.metadata.creator.append(en("Francesca Lønstad Bleken"))
onto.metadata.contributor.append(en("SINTEF"))
onto.metadata.publisher.append(en("EMMC ASBL???"))
onto.metadata.license.append(
    en("https://creativecommons.org/licenses/by/4.0/legalcode")
)
onto.metadata.versionInfo.append(en(version))
onto.metadata.comment.append(
    en(
        "The EMMO requires FacT++ reasoner plugin in order to visualize all "
        "inferences and class hierarchy (ctrl+R hotkey in Protege)."
    )
)
onto.metadata.comment.append(
    en(
        "This ontology is generated with EMMOntoPy using data from a dedicated"
        "Excel sheet developed by the domain experts."
    )
)

# Synchronise Python attributes to ontology
onto.sync_attributes(
    name_policy="uuid", name_prefix="EMMO_", class_docstring="elucidation"
)
onto.dir_label = False

write_catalog(catalog, output="catalog-v001.xml")

"""
# Hack to ensure that we import using versionURI
# FIXME: included this in sync_attributes()
d = {o.base_iri.rstrip('/#'): o.get_version(as_iri=True)
     for o in onto.imported_ontologies}
for abbrev_iri in onto.world._get_obj_triples_sp_o(
        onto.storid, owlready2.owl_imports):
    iri = onto._unabbreviate(abbrev_iri)
    version_iri = d[iri]
    onto._del_obj_triple_spo(
        onto.storid,
        owlready2.owl_imports,
        abbrev_iri)
    onto._add_obj_triple_spo(
        onto.storid,
        owlready2.owl_imports,
        onto._abbreviate(version_iri))
"""

# Save new ontology as turtle
onto.save(
    os.path.join("microstructureonto.ttl"), format="turtle", overwrite=True
)
