"""
A module for documenting ontologies.
"""

# pylint: disable=fixme,too-many-lines,no-member,too-many-instance-attributes
import html
import re
import time
import warnings
from pathlib import Path
from typing import TYPE_CHECKING

import rdflib
from rdflib import DCTERMS, OWL, URIRef

from ontopy.ontology import Ontology, get_ontology
from ontopy.utils import asstring, get_label

import owlready2  # pylint: disable=wrong-import-order

if TYPE_CHECKING:
    from typing import Iterable, Optional, Type, Union

    Cls = Type[owlready2.Thing]
    Property = Type[owlready2.Property]
    Individual = owlready2.Thing  # also datatype
    Entity = Union[Cls, Property, Individual]


class ModuleDocumentation:
    """Class for documentating a module in an ontology.

    Arguments:
        ontology: Ontology to include in the generated documentation.
            All entities in this ontology will be included.
        entities: Explicit listing of entities (classes, properties,
            individuals, datatypes) to document.  Normally not needed.
        title: Header title.  Be default it is inferred from title of
        iri_regex: A regular expression that the IRI of documented entities
            should match.
    """

    def __init__(
        self,
        ontology: "Optional[Ontology]" = None,
        entities: "Optional[Iterable[Entity]]" = None,
        title: "Optional[str]" = None,
        iri_regex: "Optional[str]" = None,
    ) -> None:
        self.ontology = ontology
        self.title = title
        self.iri_regex = iri_regex
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
        if self.iri_regex and not re.match(self.iri_regex, entity.iri):
            return

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
        iri = self.ontology.base_iri.rstrip("#/")
        if self.title:
            title = self.title
        elif self.ontology:
            title = self.graph.value(URIRef(iri), DCTERMS.title)
        if not title:
            title = iri.rsplit("/", 1)[-1]

        heading = f"Module: {title}"
        return f"""

{heading.title()}
{'='*len(heading)}

"""

    def get_refdoc(
        self,
        subsections: str = "all",
        header: bool = True,
    ) -> str:
        # pylint: disable=too-many-branches
        """Return reference documentation of all module entities.

        Arguments:
            subsections: Comma-separated list of subsections to include in
                the returned documentation.  Valid subsection names are:
                  - classes
                  - object_properties
                  - data_properties
                  - annotation_properties
                  - individuals
                  - datatypes
                If "all", all subsections will be documented.
            header: Whether to also include the header in the returned
                documentation.

        Returns:
            String with reference documentation.
        """
        # pylint: disable=too-many-nested-blocks
        if subsections == "all":
            subsections = (
                "classes,object_properties,data_properties,"
                "annotation_properties,individuals,datatypes"
            )

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

        def add_header(name):
            clsname = f"element-table-{name.lower().replace(' ', '-')}"
            lines.extend(
                [
                    "  <tr>",
                    f'    <th class="{clsname}" rowspac="2">{name}</th>',
                    "  </tr>",
                ]
            )

        def add_keyvalue(key, value, escape=True, htmllink=True):
            """Help function for adding a key-value row to table."""
            if escape:
                value = html.escape(str(value))
            if htmllink:
                value = re.sub(
                    r"(https?://[^\s]+)", r'<a href="\1">\1</a>', value
                )
            value = value.replace("\n", "<br>")
            lines.extend(
                [
                    "  <tr>",
                    '    <td class="element-table-key">'
                    f'<span class="element-table-key">'
                    f"{key.title()}</span></td>",
                    f'    <td class="element-table-value">{value}</td>',
                    "  </tr>",
                ]
            )

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
            for entity in sorted(maps[subsection], key=get_label):
                label = get_label(entity)
                lines.extend(
                    [
                        ".. raw:: html",
                        "",
                        f'   <div id="{entity.name}"></div>',
                        "",
                        f"{label}",
                        "-" * len(label),
                        "",
                        ".. raw:: html",
                        "",
                        '  <table class="element-table">',
                    ]
                )
                add_keyvalue("IRI", entity.iri)
                if hasattr(entity, "get_annotations"):
                    add_header("Annotatins")
                    for key, value in entity.get_annotations().items():
                        if isinstance(value, list):
                            for val in value:
                                add_keyvalue(key, val)
                        else:
                            add_keyvalue(key, value)
                if entity.is_a or entity.equivalent_to:
                    add_header("Formal description")
                    for r in entity.equivalent_to:

                        # FIXME: Skip restrictions with value None to work
                        # around bug in Owlready2 that doesn't handle custom
                        # datatypes in restrictions correctly...
                        if hasattr(r, "value") and r.value is None:
                            continue

                        add_keyvalue(
                            "Equivalent To",
                            asstring(
                                r,
                                link='<a href="{iri}">{label}</a>',
                                ontology=self.ontology,
                            ),
                            escape=False,
                            htmllink=False,
                        )
                    for r in entity.is_a:
                        add_keyvalue(
                            "Subclass Of",
                            asstring(
                                r,
                                link='<a href="{iri}">{label}</a>',
                                ontology=self.ontology,
                            ),
                            escape=False,
                            htmllink=False,
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
        iri_regex: A regular expression that the IRI of documented entities
            should match.
    """

    def __init__(
        self,
        ontologies: "Iterable[Ontology]",
        imported: bool = True,
        recursive: bool = False,
        iri_regex: "Optional[str]" = None,
    ) -> None:
        if isinstance(ontologies, (Ontology, str, Path)):
            ontologies = [ontologies]

        if recursive:
            imported = True

        self.iri_regex = iri_regex
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
            for onto in included_ontologies[:]:
                for o in onto.get_imported_ontologies(recursive=recursive):
                    if o not in included_ontologies:
                        included_ontologies.append(o)

        # Module documentations
        for onto in included_ontologies:
            self.module_documentations.append(
                ModuleDocumentation(onto, iri_regex=iri_regex)
            )

    def get_header(self) -> str:
        """Return a the reStructuredText header as a string."""
        return """
==========
References
==========
"""

    def get_refdoc(self, header: bool = True, subsections: str = "all") -> str:
        """Return reference documentation of all module entities.

        Arguments:
            header: Whether to also include the header in the returned
                documentation.
            subsections: Comma-separated list of subsections to include in
                the returned documentation. See ModuleDocumentation.get_refdoc()
                for more info.

        Returns:
            String with reference documentation.
        """
        moduledocs = []
        if header:
            moduledocs.append(self.get_header())
        moduledocs.extend(
            md.get_refdoc(subsections=subsections)
            for md in self.module_documentations
            if md.nonempty()
        )
        return "\n".join(moduledocs)

    def top_ontology(self) -> Ontology:
        """Return the top-level ontology."""
        return self.module_documentations[0].ontology

    def write_refdoc(self, docfile=None, subsections="all"):
        """Write reference documentation to disk.

        Arguments:
            docfile: Name of file to write to. Defaults to the name of
                the top ontology with extension `.rst`.
            subsections: Comma-separated list of subsections to include in
                the returned documentation. See ModuleDocumentation.get_refdoc()
                for more info.
        """
        if not docfile:
            docfile = self.top_ontology().name + ".rst"
        Path(docfile).write_text(
            self.get_refdoc(subsections=subsections), encoding="utf8"
        )

    def write_index_template(
        self, indexfile="index.rst", docfile=None, overwrite=False
    ):
        """Write a basic template index.rst file to disk.

        Arguments:
            indexfile: Name of index file to write.
            docfile: Name of generated documentation file.  If not given,
                the name of the top ontology will be used.
            overwrite: Whether to overwrite an existing file.
        """
        docname = Path(docfile).stem if docfile else self.top_ontology().name
        content = f"""
.. toctree::
   :includehidden:
   :hidden:

   Reference Index <{docname}>

"""
        outpath = Path(indexfile)
        if not overwrite and outpath.exists():
            warnings.warn(f"index.rst file already exists: {outpath}")
            return

        outpath.write_text(content, encoding="utf8")

    def write_conf_template(
        self, conffile="conf.py", docfile=None, overwrite=False
    ):
        """Write basic template sphinx conf.py file to disk.

        Arguments:
            conffile: Name of configuration file to write.
            docfile: Name of generated documentation file.  If not given,
                the name of the top ontology will be used.
            overwrite: Whether to overwrite an existing file.
        """
        # pylint: disable=redefined-builtin
        md = self.module_documentations[0]

        iri = md.ontology.base_iri.rstrip("#/")
        authors = list(md.graph.objects(URIRef(iri), DCTERMS.creator))
        license = md.graph.value(URIRef(iri), DCTERMS.license, default=None)
        release = md.graph.value(URIRef(iri), OWL.versionInfo, default="1.0")

        author = ", ".join(str(authors)) if authors else "<AUTHOR>"
        copyright = license if license else f"{time.strftime('%Y')}, {author}"

        content = f"""
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = '{md.ontology.name}'
copyright = '{copyright}'
author = '{author}'
release = '{release}'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
"""
        if not conffile:
            conffile = Path(docfile).with_name("conf.py")
        if overwrite and conffile.exists():
            warnings.warn(f"conf.py file already exists: {conffile}")
            return

        conffile.write_text(content, encoding="utf8")
