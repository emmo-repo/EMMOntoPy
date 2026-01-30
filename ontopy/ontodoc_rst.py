"""
A module for documenting ontologies.
"""

# pylint: disable=fixme,too-many-lines,no-member,too-many-instance-attributes
# pylint: disable=invalid-name
# pylint: disable=line-too-long # SHOULD BE REMOVED LATER, because of templates
from curses import raw
import html
import re
import time
import warnings
from pathlib import Path
from typing import TYPE_CHECKING
import shutil
from urllib.request import urlopen
from urllib.parse import urlparse

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

# Standard IRIs for the built‑in annotation properties
ANNOTATION_RANK = {
    "prefLabel": "http://www.w3.org/2004/02/skos/core#prefLabel",
    "altLabel": "http://www.w3.org/2004/02/skos/core#altLabel",
    "label": "http://www.w3.org/2000/01/rdf-schema#label",
    "elucidation": "https://w3id.org/emmo"
    "#EMMO_967080e5_2f42_4eb2_a3a9_c58143e835f9",
    #"comment": "http://www.w3.org/2000/01/rdf-schema#comment",
    "example": "http://www.w3.org/2004/02/skos/core#example",
    "seeAlso": "http://www.w3.org/2000/01/rdf-schema#seeAlso",
    "isDefinedBy": "http://www.w3.org/2000/01/rdf-schema#isDefinedBy",
}

# Annotations that should render as admonitions
CALLOUTS = {
    # admonition type -> (directive, optional title)
    "note":        ("note", None),
    "comment":     ("note", None),       # treat rdfs:comment as a note (optional)
    "scopenote":   ("note", None),
    "example":     ("admonition", "Example"),
    "tip":         ("tip", None),
    "caution":     ("caution", None),
    "warning":     ("warning", None),
    "important":   ("important", None),
    "danger":      ("danger", None),
    "error":       ("error", None),
}

 


def _get_annotation_rank(onto: Ontology):
    # Resolve IRIs → AnnotationProperty instances (in defined order)
    # Not all IRIs may be present in the ontology
    priorities = [
        onto[iri] for iri in ANNOTATION_RANK.values() if onto[iri] is not None
    ]

    def rank(prop):
        # Exact match for the first three anchors
        if prop in priorities[:3]:

            return priorities.index(prop)

        # Otherwise find the earliest anchor among its ancestors
        ancestors = set(prop.ancestors())
        for idx, anchor in enumerate(priorities[3:], start=3):
            if anchor in ancestors:
                return idx

        # Anything else falls to the bottom
        return len(priorities)

    all_props = list(onto.annotation_properties(imported=True))
    return sorted(all_props, key=rank)


def _extract_all_annotations(value_list, lang="en"):
    """Extract text values, prioritizing a language (default: en)."""
    result = []
    for elem in value_list:
        if isinstance(elem, str):
            result.append(elem)
        elif hasattr(elem, "lang") and elem.lang == lang:
            result.append(elem)
    return result


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

        # All navigation IDs added by the ontology. Used to warn about
        # dublicated IDs
        self.navids = set()

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

    def get_title(self) -> str:
        """Return a module title."""
        iri = self.ontology.base_iri.rstrip("#/")
        if self.title:
            title = self.title
        elif self.ontology:
            title = self.graph.value(URIRef(iri), DCTERMS.title)
        if not title:
            title = iri.rsplit("/", 1)[-1]
        return title

    def get_header(self) -> str:
        """Return a the reStructuredText header as a string."""
        heading = f"Module: {self.get_title()}"
        return f"""

{heading.title()}
{'='*len(heading)}

"""

    def get_refdoc(
        self,
        subsections: str = "all",
        header: bool = True,
    ) -> str:
        # pylint: disable=too-many-branches,too-many-locals,too-many-statements
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

        annotations_ranked = _get_annotation_rank(self.ontology)

        def add_header(name):
            """Help function to add header row to table."""
            clsname = f"element-table-{name.lower().replace(' ', '-')}"
            lines.extend(
                [
                    "  <tr>",
                    f'    <th class="{clsname}" colspan="2">{name}</th>',
                    "  </tr>",
                ]
            )

        def _get_links(item, key):
            """Get HTML links for a list of entitities that
            can be fetched from the ontology as keys."""
            links = []
            for ent in item[key]:
                full_iri = ent.iri
                try:
                    val = ent.prefLabel.get_lang("en")[0]
                except (IndexError, AttributeError):
                    val = ent
                links.append(_html_links(full_iri, display_text=val))

            return links

        def _linkify_manchester(text: str, onto) -> str:
            """
            Convert manchester notation as string to HTML links.
            """

            def _replace(match):
                word = match.group(0)
                try:
                    full = onto[word].iri
                    return _html_links(full, word)
                except (KeyError, AttributeError):
                    return word

            return re.sub(r"\w+", _replace, text)

        def _html_links(full_iri, display_text):
            """Create the HTML code so that links lead to
            the correct fragment in the same document if possibe,
            otherwise link to the full IRI"""
            fragment_iri = full_iri.split("#")[-1]
            return (
                f"<a href='#{fragment_iri}' "
                f'onclick="'
                f"if(!document.getElementById('{fragment_iri}'))"
                f"{{window.location.href='{full_iri}'; return false;}}"
                f'">'
                f"{display_text}</a>"
            )

        def _add_table_row(rst, key, value):
            try:
                key = get_preferred_label(key)
            except AttributeError:
                key = key
            rst += "  <tr>\n"
            rst += f'    <td class="element-table-key"><span class="element-table-key">{key}</span></td>\n'
            rst += '    <td class="element-table-value">'
            rst += value
            rst += "</td>\n"
            rst += "  </tr>\n"
            return rst

        def add_keyvalue(
            key, value, iri=None, escape=True, htmllink=True, show_figure=True
        ):
            """Help function for adding a key-value row to table.

            Arguments:
                key: Key to show in the table.
                value: Value to show in the table.
                iri: IRI to link to, if value does not have attribute .iri.
                htmllink: Whether to add html link to value.
                show_figure: Whether to show figure in value column.

            """
            if not isinstance(value, list):
                values = [value]
            else:
                values = value
                #value = _html_links(value.iri, get_label(value))
            
            strval = ""
            count=0
            for value in values:
                if count>0 and not key=="Restrictions":
                        strval += ", "
                count+=1
                
                if show_figure and re.match(
                    r"^https?://[a-zA-Z0-9.+?@/_-]+\.(png|jpg|jpeg|svg|gif)$",
                    asstring(value, ontology=self.ontology),
                ):
                    strval+= f'<img src="{value}">'
                elif hasattr(value, "iri"):
                    strval+= _html_links(value.iri, get_label(value))
                elif iri:
                    strval+= _html_links(iri, value)
                elif key == "Restrictions":
                    strval+= "<li>" + _linkify_manchester(
                        asstring(value),
                        self.ontology,
                    ) + "</li>"
                else: # Check what this else is for
                    #if escape:  # Not documented what this is
                    strval+= html.escape(str(value))
                    strval = strval.replace("\n", "<br>")
            
            # Build a self-contained snippet to prevent table misalignment
            if key == "Restrictions":
                strval =  f"<div class=\"restriction-list\"><ul>{strval}</ul></div>"
 
            lines.extend(
                [
                    "  <tr>",
                    '    <td class="element-table-key">'
                    f'<span class="element-table-key">'
                    f"{key}</span></td>",
                    f'    <td class="element-table-value">{strval}</td>',
                    "  </tr>",
                ]
            )

        for subsection in subsections.split(","):
            if maps[subsection]:
                moduletitle = self.get_title().lower().replace(" ", "-")
                anchor = f"{moduletitle}-{subsection.replace('_', '-')}"
                lines.extend(
                    [
                        "",
                        f".. _{anchor}:",
                        "",
                        subsection.replace("_", " ").title(),
                        "-" * len(subsection),
                        "",
                    ]
                )
            for entity in sorted(maps[subsection], key=get_label):
                label = get_label(entity)
                navid = navid2 = ""
                if entity.name in self.navids:
                    warnings.warn(f"duplicated entity names: {entity.name}")
                else:
                    self.navids.add(entity.name)
                    navid = f'   <div id="{entity.name}"></div>'
                if hasattr(entity, "prefLabel"):
                    preflabel = str(entity.prefLabel.first())
                    if preflabel != entity.name:
                        if preflabel in self.navids:
                            warnings.warn(f"duplicated prefLabel: {preflabel}")
                        else:
                            self.navids.add(preflabel)
                            navid2 = f'   <div id="{preflabel}"></div>'

                lines.extend(
                    [
                        ".. raw:: html",
                        "",
                        navid,
                        navid2,
                        "",
                        f"{label}",
                        "^" * len(label),
                        "",
                        ".. raw:: html",
                        "",
                        '  <table class="element-table">',
                    ]
                )
                add_keyvalue("IRI", entity.iri)
                if hasattr(entity, "get_annotations") or hasattr(entity, "get_individual_annotations"):
                    add_header("Annotations")
                    annotations = {  # pylint: disable=protected-access
                        a: a._get_values_for_class(  # pylint: disable=protected-access
                            entity
                        )
                        for a in annotations_ranked
                        if a._get_values_for_class(  # pylint: disable=protected-access
                            entity
                        )
                    }

                    long_annotations = [
                        "http://www.w3.org/2004/02/skos/core#example",
                        "https://w3id.org/emmo#"
                        "EMMO_c7b62dd7_063a_4c2a_8504_42f7264ba83f",
                        "https://w3id.org/emmo#EMMO_967080e5_2f42_4eb2_a3a9_c58143e835f9",
                        "https://w3id.org/emmo#EMMO_31252f35_c767_4b97_a877_1235076c3e13",
                        "https://w3id.org/emmo#EMMO_70fe84ff_99b6_4206_a9fc_9a8931836d84"


                    ]
                    
                    table_annotations = {key: value for key, value in annotations.items() if get_label(key) not in CALLOUTS.keys()}

                    for key, item in table_annotations.items():
                        if key.iri not in long_annotations:
                            add_keyvalue(get_label(key), table_annotations[key])
                        else:
                            add_keyvalue(get_label(key), item)
                
                    # Fetch parents (all direct superclasses)
                    parents = [
                        ent
                        for ent in entity.is_a
                        if (
                            isinstance(ent, owlready2.ThingClass)
                            or isinstance(ent, owlready2.PropertyClass)
                        )
                    ]

                    # Fetch direct subclasses
                    subclasses = (list(entity.subclasses()) if isinstance(entity, owlready2.ThingClass) else [])

                    # Fetch OWL restrictions (object property + someValuesFrom)
                    restrictions = [restriction for restriction in entity.is_a if isinstance(restriction, owlready2.Restriction)]

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
                        # Add SubclassOf
                        add_keyvalue("Subclass Of", parents)
                        # Add Subclasses if any
                        if subclasses:
                            add_keyvalue("Subclasses", subclasses)
                    
                        # Add Restrictions if any
                        if restrictions:
                            add_keyvalue("Restrictions", restrictions)

                    lines.extend(["  </table>", ""])

                    # raw html block content (indented)
                    lines.extend([
                        "  </table>",
                        "",   # end of indented raw content
                        "",   # blank line after raw directive block
                    ]) 
                    callout_annotations = {key: value for key, value in annotations.items() if get_label(key) in CALLOUTS.keys()}

                    def _indent(block: str, n: int = 3) -> str:
                        pad = " " * n
                        return "\n".join((pad + ln) if ln.strip() else "" for ln in block.splitlines())


                    for key, item in callout_annotations.items():
                        directive, title = CALLOUTS[get_label(key)]
                        lines.extend([f".. {directive}::" + (f" {title}" if title else "") + "\n\n"])
                        content = _extract_all_annotations(item)
                        content = "\n\n".join(content)
                        content = _indent(content, n=3)
                        lines.extend([content, ""])

                    lines.extend(["\n"])      # blank line between callouts

        lines = "\n".join(lines)
        
        return lines


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
        included_ontologies = {}
        for onto in ontologies:
            if isinstance(onto, (str, Path)):
                onto = get_ontology(onto).load()
            elif not isinstance(onto, Ontology):
                raise TypeError(
                    "expected ontology as an IRI, Path or Ontology object, "
                    f"got: {onto}"
                )
            if onto.base_iri not in included_ontologies:
                included_ontologies[onto.base_iri] = onto

        # Indirectly included ontologies (imported)
        if imported:
            for onto in list(included_ontologies.values()):
                for o in onto.get_imported_ontologies(recursive=recursive):
                    if o.base_iri not in included_ontologies:
                        included_ontologies[o.base_iri] = o

        # Module documentations
        for onto in included_ontologies.values():
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
        authors = sorted(md.graph.objects(URIRef(iri), DCTERMS.creator))
        license = md.graph.value(URIRef(iri), DCTERMS.license, default=None)
        release = md.graph.value(URIRef(iri), OWL.versionInfo, default="1.0")

        # FIXME: If authors are URIs, extract their names from the URI
        author = (
            ", ".join(
                a.value if hasattr(a, "value") else str(a) for a in authors
            )
            if authors
            else "<AUTHOR>"
        )
        copyright = license if license else f"{time.strftime('%Y')}, {author}"
        # pylint: disable=line-too-long
        content = f"""\
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

# Pygments styles are Sphinx settings (not theme options)
pygments_style = "friendly"
pygments_dark_style = "lightbulb"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"

html_theme_options = {{
    # Remove left sidebar content (primary sidebar)
    "primary_sidebar_items": [],

    # Navigation depth (only matters if you show a nav in the sidebar)
    "show_nav_level": 2,

    # Disable right "On this page" TOC everywhere
    "show_toc_level": 0,
    "secondary_sidebar_items": [],

    # Navbar
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["navbar-icon-links", "theme-switcher", "search-button"],

    # Icon links (Font Awesome 6 classes)
    "icon_links": [
        {{
            "name": "GitHub",
            "url": "https://github.com/emmo-repo/domain-{md.ontology.name.lower()}",
            "icon": "fa-brands fa-github",
        }},
        {{
            "name": "Ontology Homepage",
            "url": "{iri}",
            "icon": "fa-solid fa-globe",
        }},
    ],

    "show_prev_next": False,
    "footer_start": ["copyright"],
    "footer_center": ["sphinx-version"],
}}

html_static_path = ["_static"]
html_title = "Domain {md.ontology.name.capitalize()} Ontology"
html_css_files = ["custom.css"]

# html_sidebars keys are docname globs. Apply everywhere unless you truly want per-page overrides.
html_sidebars = {{
    "{md.ontology.name.lower()}": ["search-field.html", "page-toc.html", "edit-this-page.html"],
}}
"""

        if not conffile:
            conffile = Path(docfile).with_name("conf.py")
        if not overwrite and conffile.exists():
            warnings.warn(f"conf.py file already exists: {conffile}")
            return

        conffile.write_text(content, encoding="utf8")

    def copy_css_file(
        self,
        source: str | Path = (
            "https://raw.githubusercontent.com/"
            "emmo-repo/EMMOntoPy/refs/heads/flb/issue916/"
            "ontopy/ontokit/templates/custom.css"
        ),
    ) -> Path:
        """
        Copy a custom CSS file into the Sphinx HTML static directory.

        The source may be:
          - a URL (http/https),
          - an absolute local path,
          - a relative local path.

        Parameters
        ----------
        source : str or pathlib.Path, optional
            Location of the CSS file to copy.

        Returns
        -------
        pathlib.Path
            Path to the copied CSS file.
        """
        static_dir = Path("build") / "_static"
        static_dir.mkdir(parents=True, exist_ok=True)

        destination = static_dir / "custom.css"
        # Remove existing file if it exists
        # if destination.exists():
        #    destination.unlink()

        # URL source
        # if source.startswith(("http://", "https://")):
        if urlparse(str(source)).scheme in ("http", "https"):
            with urlopen(source) as response, open(destination, "wb") as f:
                shutil.copyfileobj(response, f)
        # Local path source
        else:
            source_path = Path(source)
            if not source_path.exists():
                raise FileNotFoundError(f"CSS source not found: {source_path}")
            shutil.copyfile(source_path, destination)

        print(f"Copied CSS file to: {destination}")
        return destination
