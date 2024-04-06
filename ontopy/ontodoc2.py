# -*- coding: utf-8 -*-
"""
A module for documenting ontologies.
"""
# pylint: disable=fixme,too-many-lines,no-member
from pathlib import Path
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
        self.individuals = set()
        self.datatypes = set()

        if ontology:
            self.add_ontology(ontology)

        if entities:
            for entity in entities:
                self.add_entity(entity)

    def nonempty(self) -> bool:
        """Returns whether the module has any classes, properties, individuals
        or datatypes."""
        return (
            self.classes
            or self.object_properties
            or self.data_properties
            or self.annotation_properties
            or self.individuals
            or self.datatypes
        )

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
        if not title:
            title = self.ontology.name

        heading = f"Module: {title}"
        return f"""

{heading.title()}
{'='*len(heading)}

"""

    def get_refdoc(
        self,
        subsections: str = "classes,object_properties,data_properties,annotation_properties,individuals,datatypes",
        header: bool = True,
    ) -> str:
        """Return reference documentation of all module entities.

        Arguments:
            subsections: Comma-separated list of subsections to include in
                the returned documentation.
            header: Whether to also include the header in the returned
                documentation.

        Returns:
            String with reference documentation.
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

        if header:
            lines.append(self.get_header())

        for subsection in subsections.split(","):
            if maps[subsection]:
                lines.extend(
                    [
                        "-" * len(subsection),
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
                        f"{label}",
                        "-" * len(label),
                        "",
                        f"* {entity.iri}",
                        "",
                        ".. raw:: html",
                        "",
                    ]
                )
                if hasattr(entity, "get_annotations"):
                    lines.append('  <table class="element-table">')
                    for key, value in entity.get_annotations().items():
                        lines.extend(
                            [
                                "  <tr>",
                                f'  <td class="element-table-key"><span class="element-table-key">{key.title()}</span></td>',
                                f'  <td class="element-table-value">{value}</td>',
                                "  </tr>",
                            ]
                        )
                    lines.extend(["  </table>", ""])

        return "\n".join(lines)


class OntologyDocumentation:
    """Documentation for an ontology with a common namespace.

    Arguments:
        ontologies: Ontologies to include in the generated documentation.
            All entities in these ontologies will be included.
        imported: Whether to include imported ontologies.
        recursive: Whether to recursively import all imported ontologies.
            Implies `recursive=True`.
        iri_match: A regular expression that the `base_iri` of imported
            ontologies should match in order to be included.
    """

    def __init__(
        self,
        ontologies: "Iterable[Ontology]",
        imported: bool = True,
        recursive: bool = False,
        iri_match: "Optional[str]" = None,
    ) -> None:
        if isinstance(ontologies, (Ontology, str, Path)):
            ontologies = [ontologies]

        if recursive:
            imported = True

        self.module_documentations = []

        # Explicitly included ontologies
        included_ontologies = []
        for onto in ontologies:
            if isinstance(onto, (str, Path)):
                onto = get_ontology(onto).load()
            elif not isinstance(onto, Ontology):
                raise TypeError(
                    "expected ontology as an IRI, Path or Ontology object, "
                    f"got: {onto}"
                )
            if onto not in included_ontologies:
                included_ontologies.append(onto)

        # Indirectly included ontologies (imported)
        if imported:
            for onto in included_ontologies:
                ontos = onto.get_imported_ontologies(recursive=recursive)
                if iri_match:
                    ontos = [
                        o for o in ontos if re.match(iri_match, o.base_iri)
                    ]
                for o in ontos:
                    if o not in included_ontologies:
                        included_ontologies.append(o)

        # Module documentations
        for onto in included_ontologies:
            self.module_documentations.append(ModuleDocumentation(onto))

    def get_header(self) -> str:
        """Return a the reStructuredText header as a string."""
        return f"""
==========
References
==========
"""

    def get_refdoc(self, header: bool = True) -> str:
        """Return reference documentation of all module entities.

        Arguments:
            header: Whether to also include the header in the returned
                documentation.

        Returns:
            String with reference documentation.
        """
        moduledocs = []
        if header:
            moduledocs.append(self.get_header())
        moduledocs.extend(
            md.get_refdoc()
            for md in self.module_documentations
            if md.nonempty()
        )
        return "\n".join(moduledocs)
