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

import yaml
import owlready2

from ontopy.utils import asstring, camelsplit, get_label, get_format

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Iterable, Union

    from ontopy import Ontology

    Cls: Type[owlready2.Thing]
    Property: Type[owlready2.Property]
    Individual: owlready2.Thing


class OntoDoc:
    """Class for documentating ontologies.

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
