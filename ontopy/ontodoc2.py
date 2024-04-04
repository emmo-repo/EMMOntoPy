# -*- coding: utf-8 -*-
"""
A module for documenting ontologies.
"""
# pylint: disable=fixme,too-many-lines,no-member
import os
import re
import time
import warnings
import shlex
import shutil
import subprocess  # nosec
from textwrap import dedent
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import TYPE_CHECKING

from rdflib import DCTERMS

import yaml
import owlready2

from ontopy.utils import asstring, camelsplit, get_label, get_format

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Iterable, Union

    from ontopy import Ontology

    Cls: Type[owlready2.Thing]
    Property: Type[owlready2.Property]
    Individual: owlready2.Thing  # also datatype
    Entity: Union[Cls, Property, Individual]


class ModuleDocumentation:
    """Class for documentating a module in an ontology.

    Arguments:
        ontology: Ontology to include in the generated documentation.
            All entities in this ontology will be included.
        entities: Explicit listing of entities (classes, properties,
            individuals, datatypes) to document.  Normally not needed.
        title: Header title.  Be default it is inferred from title of
    """

    def __init__(
        self,
        ontology: "Ontology" = None,
        entities: "Iterable[Entity]" = None,
    ) -> None:
        self.ontology = ontology

        if title:
            self.title = title
        elif ontology:
            titleid = ontology._abbreviate(DCTERMS.title)
            _, _, title = ontology.get_triples(ontology.storid, titleid)[0]
            if title.endswith("@en"):  # fixme: should work for all languages
                title = title[:-3].strip("'\"")
            self.title = title

        self.classes = set()
        self.object_properties = set()
        self.data_properties = set()
        self.annotation_properties = set()
        self.datatypes = set()
        self.individuals = set()

        if ontology:
            self.add_ontology(ontology)

        if entities:
            for entity in entities:
                self.add_entity(entity)

    def add_entity(self, entity: "Entity") -> None:
        """Add `entity` (class, property, individual, datatype) to list of
        entities to document.
        """
        if isinstance(entity, owlready2.ThingClass):
            self.classes.add(entity)
        elif isinstance(entity, owlready2.ObjectPropertyClass):
            self.object_properties.add(entity)
        elif isinstance(entity, owlready2.DataPropertyClass):
            self.object_properties.add(entity)
        elif isinstance(entity, owlready2.AnnotationPropertyClass):
            self.object_properties.add(entity)
        elif isinstance(entity, owlready2.Thing):
            if (
                hasattr(entity.__class__, "iri")
                and entity.__class__.iri
                == "http://www.w3.org/2000/01/rdf-schema#Datatype"
            ):
                self.datatypes.add(entity)
            else:
                self.individuals.add(entity)

    def add_ontology(
        self, ontology: "Ontology", imported: bool = False
    ) -> None:
        """Add ontology to documentation."""
        for entity in onto.get_entities(imported=imported):
            self.add_entity(entity)

    def write_header(self) -> str:
        """Return a the reStructuredText header as a string."""
        return f"""
==========
References
==========

{self.title}
================

"""


class OntologyDocumentation:
    """Documentation for an ontology with a common namespace.

    Arguments:
        ontologies: Ontologies to include in the generated documentation.
            All entities in these ontologies will be included.
        entities: Explicit listing of entities (classes, properties,
            individuals) to document.
        imported: Whether to recursively include imported ontologies.

    """

    def __init__(
        self,
        ontologies: "Iterable[Ontology]" = None,
        entities: "Iterable[Union[Cls, Property, Individual]]" = None,
        imported: bool = False,
    ) -> None:
        if ontologies:
            for onto in ontologies:
                self.add_ontology(onto, imported=imported)

        if entities:
            for entity in entities:
                self.add_entity(entity)

        self.classes = set()
        self.object_properties = set()
        self.data_properties = set()
        self.annotation_properties = set()
        self.datatypes = set()
        self.individuals = set()

    def add_entity(self, entity: "Union[Cls, Property, Individual]") -> None:
        """Add `entity` (class, property, individual) to list of entities to
        document."""
        if isinstance(entity, owlready2.ThingClass):
            self.classes.add(entity)
        elif isinstance(entity, owlready2.ObjectPropertyClass):
            self.object_properties.add(entity)
        elif isinstance(entity, owlready2.DataPropertyClass):
            self.object_properties.add(entity)
        elif isinstance(entity, owlready2.AnnotationPropertyClass):
            self.object_properties.add(entity)
        elif isinstance(entity, owlready2.Thing):
            if (
                hasattr(entity.__class__, "iri")
                and entity.__class__.iri
                == "http://www.w3.org/2000/01/rdf-schema#Datatype"
            ):
                self.datatypes.add(entity)
            else:
                self.individuals.add(entity)

    def add_ontology(self, onto: "Ontology", imported: bool = False) -> None:
        """Add ontology `onto` to documentation."""
        for entity in onto.get_entities(imported=imported):
            self.add_entity(entity)

    def write_header(self):
        """ """
