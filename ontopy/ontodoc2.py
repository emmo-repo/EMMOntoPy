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

import rdflib
from rdflib import DCTERMS, URIRef

from ontopy.ontology import Ontology
from ontopy.utils import asstring, camelsplit, get_label, get_format

import owlready2

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Iterable, Optional, Union

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
        ontology: "Optional[Ontology]" = None,
        entities: "Optional[Iterable[Entity]]" = None,
        title: "Optional[str]" = None,
    ) -> None:
        self.ontology = ontology
        self.title = title
        self.graph = (
            ontology.world.as_rdflib_graph() if ontology else rdflib.Graph()
        )
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
        for entity in ontology.get_entities(imported=imported):
            self.add_entity(entity)

    def get_header(self) -> str:
        """Return a the reStructuredText header as a string."""
        if self.title:
            title = self.title
        elif self.ontology:
            iri = self.ontology.base_iri.rstrip("#/")
            title = self.graph.value(URIRef(iri), DCTERMS.title)
        else:
            title = ""

        return f"""

{title}
{'='*len(title)}

"""

    def get_refdoc(
        self,
        subsections="classes,object_properties,data_properties,annotation_properties,individuals,datatypes",
    ):
        """Return reference documentation of all module entities.

        `subsections` is a comma-separated list of subsections to
        return documentation for.
        """
        maps = {
            "classes": self.classes,
            "object_properties": self.object_properties,
            "data_properties": self.data_properties,
            "annotation_properties": self.annotation_properties,
            "individuals": self.individuals,
            "datatypes": self.datatypes,
        }
        lines = []

        for subsection in subsections.split(","):
            if maps[subsection]:
                lines.extend(
                    [
                        subsection.replace("_", " ").title(),
                        "-" * len(subsection),
                        "",
                    ]
                )
            for entity in sorted(maps[subsection], key=lambda e: get_label(e)):
                label = str(get_label(entity))
                lines.extend(
                    [
                        ".. raw:: html",
                        "",
                        f'   <div id="{entity.name}"></div>',
                        "",
                        label,
                        "-" * len(label),
                        "",
                        f"* {entity.iri}",
                        "",
                        ".. raw:: html",
                        "",
                        '  <table class="element-table">',
                    ]
                )
                for key, value in entity.get_annotations():
                    lines.extend(
                        [
                            "  <tr>",
                            f'  <td class="element-table-key"><span class="element-table-key">{key.title()}</span></td>',
                            f'  <td class="element-table-value">{value}</td>',
                            "  </tr>",
                        ]
                    )
                lines.extend(
                    [
                        "  </table>",
                        "",
                    ]
                )
        return "\n".join(lines)


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
        ontologies: "Iterable[Ontology]" = (),
        imported: bool = False,
    ) -> None:
        if ontologies:
            for onto in ontologies:
                self.add_ontology(onto, imported=imported)

        if entities:
            for entity in entities:
                self.add_entity(entity)
