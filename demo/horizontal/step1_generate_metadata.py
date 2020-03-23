#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Step 1 - Generate metadata from ontology
----------------------------------------
This step takes the ontology from the vertical case and generates
metadata from it.

Here we use DLite as metadata framework, which is a SOFT
implementation in C.  Other frameworks, like CUDS, could equally well
have been used, but the metadata structure would have been different.

This generator maps OWL classes to dlite metadata entities which are
placed into a collection.  OWL class properties are mapped into
relations between the entities in the collection. The only relations
that are treated especially are `has_property` and `is_property_for`,
that are mapped into properties of the generated metadata entities.

The generated  metadata is finally serialised into a JSON file.
"""
import os

from emmo import get_ontology
from emmo2meta import EMMO2Meta


# Load our ontology from the vertical case
ontopath = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'vertical', 'usercase_ontology.owl'))
onto = get_ontology(ontopath)
onto.load()


# hmm, the base iri has cnanged... - bug in owlready2?
onto.base_iri = 'http://www.emmc.info/emmc-csa/demo#'


# Generate metadata and store it in a JSON file
#
# This does not include all of EMMO, but only the new classes,
# bonded_atom and all classes that these relates to.
classes = list(onto.classes()) + [
    onto.BondedAtom, onto.Integer, onto.Real, onto.String]
e = EMMO2Meta(ontology=onto, classes=classes, collid='usercase_ontology')
e.save('json', 'usercase_metadata.json', 'mode=w')

print('Generated metadata for the usercase ontology:')
print('  %d instances' % e.coll.count())
print('  %d relations' % len(list(e.coll.relations())))
