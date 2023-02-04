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

from ontopy.utils import asstring, camelsplit, get_label
from ontopy.graph import OntoGraph, filter_classes

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Iterable, Union


class OntoDoc:
    """A class for helping documentating ontologies.

    Parameters
    ----------
    onto : Ontology instance
        The ontology that should be documented.
    style : dict | "html" | "markdown" | "markdown_tex"
        A dict defining the following template strings (and substitutions):

        :header: Formats an header.
            Substitutions: {level}, {label}
        :link: Formats a link.
           Substitutions: {name}
        :point: Formats a point (list item).
           Substitutions: {point}, {ontology}
        :points: Formats a list of points.  Used within annotations.
           Substitutions: {points}, {ontology}
        :annotation: Formats an annotation.
            Substitutions: {key}, {value}, {ontology}
        :substitutions: list of ``(regex, sub)`` pairs for substituting
            annotation values.
    """

    _markdown_style = {
        "sep": "\n",
        "figwidth": "{{ width={width:.0f}px }}",
        "figure": "![{caption}]({path}){figwidth}\n",
        "header": "\n{:#<{level}} {label}",
        "link": "[{name}]({lowerurl})",
        "point": "  - {point}\n",
        "points": "\n\n{points}\n",
        "annotation": "**{key}:** {value}\n",
        "substitutions": [],
    }
    # Extra style settings for markdown+tex (e.g. pdf generation with pandoc)
    _markdown_tex_extra_style = {
        "substitutions": [
            # logic/math symbols
            ("\u2200", r"$\\forall$"),
            ("\u2203", r"$\\exists$"),
            ("\u2206", r"$\\nabla$"),
            ("\u2227", r"$\\land$"),
            ("\u2228", r"$\\lor$"),
            ("\u2207", r"$\\nabla$"),
            ("\u2212", r"-"),
            ("->", r"$\\rightarrow$"),
            # uppercase greek letters
            ("\u0391", r"$\\Upalpha$"),
            ("\u0392", r"$\\Upbeta$"),
            ("\u0393", r"$\\Upgamma$"),
            ("\u0394", r"$\\Updelta$"),
            ("\u0395", r"$\\Upepsilon$"),
            ("\u0396", r"$\\Upzeta$"),
            ("\u0397", r"$\\Upeta$"),
            ("\u0398", r"$\\Uptheta$"),
            ("\u0399", r"$\\Upiota$"),
            ("\u039a", r"$\\Upkappa$"),
            ("\u039b", r"$\\Uplambda$"),
            ("\u039c", r"$\\Upmu$"),
            ("\u039d", r"$\\Upnu$"),
            ("\u039e", r"$\\Upxi$"),
            ("\u039f", r"$\\Upomekron$"),
            ("\u03a0", r"$\\Uppi$"),
            ("\u03a1", r"$\\Uprho$"),
            ("\u03a3", r"$\\Upsigma$"),  # no \u0302
            ("\u03a4", r"$\\Uptau$"),
            ("\u03a5", r"$\\Upupsilon$"),
            ("\u03a6", r"$\\Upvarphi$"),
            ("\u03a7", r"$\\Upchi$"),
            ("\u03a8", r"$\\Uppsi$"),
            ("\u03a9", r"$\\Upomega$"),
            # lowercase greek letters
            ("\u03b1", r"$\\upalpha$"),
            ("\u03b2", r"$\\upbeta$"),
            ("\u03b3", r"$\\upgamma$"),
            ("\u03b4", r"$\\updelta$"),
            ("\u03b5", r"$\\upepsilon$"),
            ("\u03b6", r"$\\upzeta$"),
            ("\u03b7", r"$\\upeta$"),
            ("\u03b8", r"$\\uptheta$"),
            ("\u03b9", r"$\\upiota$"),
            ("\u03ba", r"$\\upkappa$"),
            ("\u03bb", r"$\\uplambda$"),
            ("\u03bc", r"$\\upmu$"),
            ("\u03bd", r"$\\upnu$"),
            ("\u03be", r"$\\upxi$"),
            ("\u03bf", r"o"),  # no \upomicron
            ("\u03c0", r"$\\uppi$"),
            ("\u03c1", r"$\\uprho$"),
            ("\u03c2", r"$\\upvarsigma$"),
            ("\u03c3", r"$\\upsigma$"),
            ("\u03c4", r"$\\uptau$"),
            ("\u03c5", r"$\\upupsilon$"),
            ("\u03c6", r"$\\upvarphi$"),
            ("\u03c7", r"$\\upchi$"),
            ("\u03c8", r"$\\uppsi$"),
            ("\u03c9", r"$\\upomega$"),
            # acutes, accents, etc...
            ("\u03ae", r"$\\acute{\\upeta}$"),
            ("\u1e17", r"$\\acute{\\bar{\\mathrm{e}}}$"),
            ("\u03ac", r"$\\acute{\\upalpha}$"),
            ("\u00e1", r"$\\acute{\\mathrm{a}}$"),
            ("\u03cc", r"$\\acute{o}$"),  # no \upomicron
            ("\u014d", r"$\\bar{\\mathrm{o}}$"),
            ("\u1f45", r"$\\acute{o}$"),  # no \omicron
        ],
    }
    _html_style = {
        "sep": "<p>\n",
        "figwidth": 'width="{width:.0f}"',
        "figure": '<img src="{path}" alt="{caption}"{figwidth}>',
        "header": '<h{level} id="{lowerlabel}">{label}</h{level}>',
        "link": '<a href="{lowerurl}">{name}</a>',
        "point": "      <li>{point}</li>\n",
        "points": "    <ul>\n      {points}\n    </ul>\n",
        "annotation": "  <dd><strong>{key}:</strong>\n{value}  </dd>\n",
        "substitutions": [
            (r"&", r"&#8210;"),
            (r"<p>", r"<p>\n\n"),
            (r"\u2018([^\u2019]*)\u2019", r"<q>\1</q>"),
            (r"\u2019", r"'"),
            (r"\u2260", r"&ne;"),
            (r"\u2264", r"&le;"),
            (r"\u2265", r"&ge;"),
            (r"\u226A", r"&x226A;"),
            (r"\u226B", r"&x226B;"),
            (r'"Y$', r""),  # strange noice added by owlready2
        ],
    }

    def __init__(self, onto, style="markdown"):
        if isinstance(style, str):
            if style == "markdown_tex":
                style = self._markdown_style.copy()
                style.update(self._markdown_tex_extra_style)
            else:
                style = getattr(self, f"_{style}_style")
        self.onto = onto
        self.style = style
        self.url_regex = re.compile(r"https?:\/\/[^\s ]+")

    def get_default_template(self):
        """Returns default template."""
        title = os.path.splitext(
            os.path.basename(self.onto.base_iri.rstrip("/#"))
        )[0]
        irilink = self.style.get("link", "{name}").format(
            name=self.onto.base_iri,
            url=self.onto.base_iri,
            lowerurl=self.onto.base_iri,
        )
        template = dedent(
            """\
        %HEADER {title}
        Documentation of {irilink}

        %HEADER Relations level=2
        %ALL object_properties

        %HEADER Classes level=2
        %ALL classes

        %HEADER Individuals level=2
        %ALL individuals

        %HEADER Appendix               level=1
        %HEADER "Relation taxonomies"  level=2
        %ALLFIG object_properties

        %HEADER "Class taxonomies"     level=2
        %ALLFIG classes
        """
        ).format(ontology=self.onto, title=title, irilink=irilink)
        return template

    def get_header(self, label, header_level=1):
        """Returns `label` formatted as a header of given level."""
        header_style = self.style.get("header", "{label}\n")
        return header_style.format(
            "", level=header_level, label=label, lowerlabel=label.lower()
        )

    def get_figure(self, path, caption="", width=None):
        """Returns a formatted insert-figure-directive."""
        figwidth_style = self.style.get("figwidth", "")
        figure_style = self.style.get("figure", "")
        figwidth = figwidth_style.format(width=width) if width else ""
        return figure_style.format(
            path=path, caption=caption, figwidth=figwidth
        )

    def itemdoc(
        self, item, header_level=3, show_disjoints=False
    ):  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
        """Returns documentation of `item`.

        Parameters
        ----------
        item : obj | label
            The class, individual or relation to document.
        header_level : int
            Header level. Defaults to 3.
        show_disjoints : Bool
            Whether to show `disjoint_with` relations.
        """
        onto = self.onto
        if isinstance(item, str):
            item = self.onto.get_by_label(item)

        header_style = self.style.get("header", "{label}\n")
        link_style = self.style.get("link", "{name}")
        point_style = self.style.get("point", "{point}")
        points_style = self.style.get("points", "{points}")
        annotation_style = self.style.get("annotation", "{key}: {value}\n")
        substitutions = self.style.get("substitutions", [])

        # Logical "sorting" of annotations
        order = {
            "definition": "00",
            "axiom": "01",
            "theorem": "02",
            "elucidation": "03",
            "domain": "04",
            "range": "05",
            "example": "06",
        }

        doc = []

        # Header
        label = get_label(item)
        doc.append(
            header_style.format(
                "", level=header_level, label=label, lowerlabel=label.lower()
            )
        )

        # Add warning about missing prefLabel
        if not hasattr(item, "prefLabel") or not item.prefLabel.first():
            doc.append(
                annotation_style.format(
                    key="Warning", value="Missing prefLabel"
                )
            )

        # Add iri
        doc.append(
            annotation_style.format(
                key="IRI", value=asstring(item.iri, link_style), ontology=onto
            )
        )

        # Add annotations
        if isinstance(item, owlready2.Thing):
            annotations = item.get_individual_annotations()
        else:
            annotations = item.get_annotations()

        for key in sorted(
            annotations.keys(), key=lambda key: order.get(key, key)
        ):
            for value in annotations[key]:
                value = str(value)
                if self.url_regex.match(value):
                    doc.append(
                        annotation_style.format(
                            key=key, value=asstring(value, link_style)
                        )
                    )
                else:
                    for reg, sub in substitutions:
                        value = re.sub(reg, sub, value)
                    doc.append(annotation_style.format(key=key, value=value))

        # ...add relations from is_a
        points = []
        non_prop = (
            owlready2.ThingClass,  # owlready2.Restriction,
            owlready2.And,
            owlready2.Or,
            owlready2.Not,
        )
        for prop in item.is_a:
            if isinstance(prop, non_prop) or (
                isinstance(item, owlready2.PropertyClass)
                and isinstance(prop, owlready2.PropertyClass)
            ):
                points.append(
                    point_style.format(
                        point="is_a " + asstring(prop, link_style),
                        ontology=onto,
                    )
                )
            else:
                points.append(
                    point_style.format(
                        point=asstring(prop, link_style), ontology=onto
                    )
                )

        # ...add equivalent_to relations
        for entity in item.equivalent_to:
            points.append(
                point_style.format(
                    point="equivalent_to " + asstring(entity, link_style)
                )
            )

        # ...add disjoint_with relations
        if show_disjoints and hasattr(item, "disjoint_with"):
            subjects = set(item.disjoint_with(reduce=True))
            points.append(
                point_style.format(
                    point="disjoint_with "
                    + ", ".join(asstring(_, link_style) for _ in subjects),
                    ontology=onto,
                )
            )

        # ...add disjoint_unions
        if hasattr(item, "disjoint_unions"):
            for unions in item.disjoint_unions:
                string = ", ".join(asstring(_, link_style) for _ in unions)
                points.append(
                    point_style.format(
                        point=f"disjoint_union_of {string}", ontology=onto
                    )
                )

        # ...add inverse_of relations
        if hasattr(item, "inverse_property") and item.inverse_property:
            points.append(
                point_style.format(
                    point="inverse_of "
                    + asstring(item.inverse_property, link_style)
                )
            )

        # ...add domain restrictions
        for domain in getattr(item, "domain", ()):
            points.append(
                point_style.format(
                    point=f"domain {asstring(domain, link_style)}"
                )
            )

        # ...add range restrictions
        for restriction in getattr(item, "range", ()):
            points.append(
                point_style.format(
                    point=f"range {asstring(restriction, link_style)}"
                )
            )

        # Add points (from is_a)
        if points:
            value = points_style.format(points="".join(points), ontology=onto)
            doc.append(
                annotation_style.format(
                    key="Subclass of", value=value, ontology=onto
                )
            )

        # Instances (individuals)
        if hasattr(item, "instances"):
            points = []

            for instance in item.instances():
                if isinstance(instance.is_instance_of, property):
                    warnings.warn(
                        f'Ignoring instance "{instance}" which is both and '
                        "indivudual and class. Ontodoc does not support "
                        "punning at the present moment."
                    )
                    continue
                if item in instance.is_instance_of:
                    points.append(
                        point_style.format(
                            point=asstring(instance, link_style),
                            ontology=onto,
                        )
                    )
                if points:
                    value = points_style.format(
                        points="".join(points), ontology=onto
                    )
                    doc.append(
                        annotation_style.format(
                            key="Individuals", value=value, ontology=onto
                        )
                    )

        return "\n".join(doc)

    def itemsdoc(self, items, header_level=3):
        """Returns documentation of `items`."""
        sep_style = self.style.get("sep", "\n")
        doc = []
        for item in items:
            doc.append(self.itemdoc(item, header_level))
            doc.append(sep_style.format(ontology=self.onto))
        return "\n".join(doc)


class AttributeDict(dict):
    """A dict with attribute access.

    Note that methods like key() and update() may be overridden."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


class InvalidTemplateError(NameError):
    """Raised on errors in template files."""


def get_options(opts, **kwargs):
    """Returns a dict with options from the sequence `opts` with
    "name=value" pairs. Valid option names and default values are
    provided with the keyword arguments."""
    res = AttributeDict(kwargs)
    for opt in opts:
        if "=" not in opt:
            raise InvalidTemplateError(
                f'Missing "=" in template option: {opt!r}'
            )
        name, value = opt.split("=", 1)
        if name not in res:
            raise InvalidTemplateError(f"Invalid template option: {name!r}")
        res_type = type(res[name])
        res[name] = res_type(value)
    return res


class DocPP:  # pylint: disable=too-many-instance-attributes
    """Documentation pre-processor.

    It supports the following features:

      * Comment lines

            %% Comment line...

      * Insert header with given level

            %HEADER label [level=1]

      * Insert figure with optional caption and width. `filepath`
        should be relative to `basedir`.  If width is 0, no width will
        be specified.

            %FIGURE filepath [caption='' width=0px]

      * Include other markdown files.  Header levels may be up or down with
        `shift`

            %INCLUDE filepath [shift=0]

      * Insert generated documentation for ontology entity.  The header
        level may be set with `header_level`.

            %ENTITY name [header_level=3]

      * Insert generated documentation for ontology branch `name`.  Options:
          - header_level: Header level.
          - terminated: Whether to branch should be terminated at all branch
            names in the final document.
          - include_leafs: Whether to include leaf.

            %BRANCH name [header_level=3 terminated=1 include_leafs=0
                          namespaces='' ontologies='']

      * Insert generated figure of ontology branch `name`.  The figure
        is written to `path`.  The default path is `figdir`/`name`,
        where `figdir` is given at class initiation. It is recommended
        to exclude the file extension from `path`.  In this case, the
        default figformat will be used (and easily adjusted to the
        correct format required by the backend). `leafs` may be a comma-
        separated list of leaf node names.

            %BRANCHFIG name [path='' caption='' terminated=1 include_leafs=1
                             strict_leafs=1, width=0px leafs='' relations=all
                             edgelabels=0 namespaces='' ontologies='']

      * This is a combination of the %HEADER and %BRANCHFIG directives.

            %BRANCHHEAD name [level=2  path='' caption='' terminated=1
                              include_leafs=1 width=0px leafs='']

      * This is a combination of the %HEADER, %BRANCHFIG and %BRANCH
        directives. It inserts documentation of branch `name`, with a
        header followed by a figure and then documentation of each
        element.

            %BRANCHDOC name [level=2  path='' title='' caption='' terminated=1
                             strict_leafs=1 width=0px leafs='' relations='all'
                             rankdir='BT' legend=1 namespaces='' ontologies='']

      * Insert generated documentation for all entities of the given type.
        Valid values of `type` are: "classes", "individuals",
        "object_properties", "data_properties", "annotations_properties"

            %ALL type [header_level=3, namespaces='', ontologies='']

      * Insert generated figure of all entities of the given type.
        Valid values of `type` are: "classes", "object_properties" and
        "data_properties".

            %ALLFIG type

    Parameters
    ----------
    template : str
        Input template.
    ontodoc : OntoDoc instance
        Instance of OntoDoc
    basedir : str
        Base directory for including relative file paths.
    figdir : str
        Default directory to store generated figures.
    figformat : str
        Default format for generated figures.
    figscale : float
        Default scaling of generated figures.
    maxwidth : float
        Maximum figure width.  Figures larger than this will be rescaled.
    imported : bool
        Whether to include imported entities.
    """

    # FIXME - this class should be refractured:
    #   * Instead of rescan the entire document for each pre-processer
    #     directive, we should scan the source like by line and handle
    #     each directive as they occour.
    #   * The current implementation has a lot of dublicated code.
    #   * Instead of modifying the source in-place, we should copy to a
    #     result list. This will make good error reporting much easier.
    #   * Branch leaves are only looked up in the file witht the %BRANCH
    #     directive, not in all included files as expedted.

    def __init__(  # pylint: disable=too-many-arguments
        self,
        template,
        ontodoc,
        basedir=".",
        figdir="genfigs",
        figformat="png",
        figscale=1.0,
        maxwidth=None,
        imported=False,
    ):
        self.lines = template.split("\n")
        self.ontodoc = ontodoc
        self.basedir = basedir
        self.figdir = os.path.join(basedir, figdir)
        self.figformat = figformat
        self.figscale = figscale
        self.maxwidth = maxwidth
        self.imported = imported
        self._branch_cache = None
        self._processed = False  # Whether process() has been called

    def __str__(self):
        return self.get_buffer()

    def get_buffer(self):
        """Returns the current buffer."""
        return "\n".join(self.lines)

    def copy(self):
        """Returns a copy of self."""
        docpp = DocPP(
            "",
            self.ontodoc,
            self.basedir,
            figformat=self.figformat,
            figscale=self.figscale,
            maxwidth=self.maxwidth,
        )
        docpp.lines[:] = self.lines
        docpp.figdir = self.figdir
        return docpp

    def get_branches(self):
        """Returns a list with all branch names as specified with %BRANCH
        (in current and all included documents).  The returned value is
        cached for efficiency purposes and so that it is not lost after
        processing branches."""
        if self._branch_cache is None:
            names = []
            docpp = self.copy()
            docpp.process_includes()
            for line in docpp.lines:
                if line.startswith("%BRANCH"):
                    names.append(shlex.split(line)[1])
            self._branch_cache = names
        return self._branch_cache

    def shift_header_levels(self, shift):
        """Shift header level of all hashtag-headers in buffer.  Underline
        headers are ignored."""
        if not shift:
            return
        pat = re.compile("^#+ ")
        for i, line in enumerate(self.lines):
            match = pat.match(line)
            if match:
                if shift > 0:
                    self.lines[i] = "#" * shift + line
                elif shift < 0:
                    counter = match.end()
                    if shift > counter:
                        self.lines[i] = line.lstrip("# ")
                    else:
                        self.lines[i] = line[counter:]

    def process_comments(self):
        """Strips out comment lines starting with "%%"."""
        self.lines = [line for line in self.lines if not line.startswith("%%")]

    def process_headers(self):
        """Expand all %HEADER specifications."""
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith("%HEADER "):
                tokens = shlex.split(line)
                name = tokens[1]
                opts = get_options(tokens[2:], level=1)
                del self.lines[i]
                self.lines[i:i] = self.ontodoc.get_header(
                    name, int(opts.level)  # pylint: disable=no-member
                ).split("\n")

    def process_figures(self):
        """Expand all %FIGURE specifications."""
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith("%FIGURE "):
                tokens = shlex.split(line)
                path = tokens[1]
                opts = get_options(tokens[2:], caption="", width=0)
                del self.lines[i]
                self.lines[i:i] = self.ontodoc.get_figure(
                    os.path.join(self.basedir, path),
                    caption=opts.caption,  # pylint: disable=no-member
                    width=opts.width,  # pylint: disable=no-member
                ).split("\n")

    def process_entities(self):
        """Expand all %ENTITY specifications."""
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith("%ENTITY "):
                tokens = shlex.split(line)
                name = tokens[1]
                opts = get_options(tokens[2:], header_level=3)
                del self.lines[i]
                self.lines[i:i] = self.ontodoc.itemdoc(
                    name, int(opts.header_level)  # pylint: disable=no-member
                ).split("\n")

    def process_branches(self):
        """Expand all %BRANCH specifications."""
        onto = self.ontodoc.onto

        # Get all branch names in final document
        names = self.get_branches()
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith("%BRANCH "):
                tokens = shlex.split(line)
                name = tokens[1]
                opts = get_options(
                    tokens[2:],
                    header_level=3,
                    terminated=1,
                    include_leafs=0,
                    namespaces="",
                    ontologies="",
                )
                leafs = (
                    names if opts.terminated else ()
                )  # pylint: disable=no-member

                included_namespaces = (
                    opts.namespaces.split(",")
                    if opts.namespaces
                    else ()  # pylint: disable=no-member
                )
                included_ontologies = (
                    opts.ontologies.split(",")
                    if opts.ontologies
                    else ()  # pylint: disable=no-member
                )

                branch = filter_classes(
                    onto.get_branch(
                        name, leafs, opts.include_leafs
                    ),  # pylint: disable=no-member
                    included_namespaces=included_namespaces,
                    included_ontologies=included_ontologies,
                )

                del self.lines[i]
                self.lines[i:i] = self.ontodoc.itemsdoc(
                    branch, int(opts.header_level)  # pylint: disable=no-member
                ).split("\n")

    def _make_branchfig(  # pylint: disable=too-many-arguments,too-many-locals
        self,
        name: str,
        path: "Union[Path, str]",
        terminated: bool,
        include_leafs: bool,
        strict_leafs: bool,
        width: float,
        leafs: "Union[str, list[str]]",
        relations: str,
        edgelabels: str,
        rankdir: str,
        legend: bool,
        included_namespaces: "Iterable[str]",
        included_ontologies: "Iterable[str]",
    ) -> "tuple[str, list[str], float]":
        """Help method for process_branchfig().

        Args:
            name: name of branch root
            path: optional figure path name
            include_leafs: whether to include leafs
            strict_leafs: whether strictly exclude leafs descendants
            terminated: whether the graph should be terminated at leaf nodes
            width: optional figure width
            leafs: optional leafs node names for graph termination
            relations: comma-separated list of relations to include
            edgelabels: whether to include edgelabels
            rankdir: graph direction (BT, TB, RL, LR)
            legend: whether to add legend
            included_namespaces: sequence of names of namespaces to be included
            included_ontologies: sequence of names of ontologies to be included

        Returns:
            filepath: path to generated figure
            leafs: used list of leaf node names
            width: actual figure width

        """
        onto = self.ontodoc.onto
        if leafs:
            if isinstance(leafs, str):
                leafs = leafs.split(",")
        elif terminated:
            leafs = set(self.get_branches())
            leafs.discard(name)
        else:
            leafs = None
        if path:
            figdir = os.path.dirname(path)
            formatext = os.path.splitext(path)[1]
            if formatext:
                fmt = formatext.lstrip(".")
            else:
                fmt = self.figformat
                path += f".{fmt}"
        else:
            figdir = self.figdir
            fmt = self.figformat
            term = "T" if terminated else ""
            path = os.path.join(figdir, name + term) + f".{fmt}"

        # Create graph
        graph = OntoGraph(onto, graph_attr={"rankdir": rankdir})
        graph.add_branch(
            root=name,
            leafs=leafs,
            include_leafs=include_leafs,
            strict_leafs=strict_leafs,
            relations=relations,
            edgelabels=edgelabels,
            included_namespaces=included_namespaces,
            included_ontologies=included_ontologies,
        )
        if legend:
            graph.add_legend()

        if not width:
            figwidth, _ = graph.get_figsize()
            width = self.figscale * figwidth
            if self.maxwidth and width > self.maxwidth:
                width = self.maxwidth

        filepath = os.path.join(self.basedir, path)
        destdir = os.path.dirname(filepath)
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        graph.save(filepath, fmt=fmt)
        return filepath, leafs, width

    def process_branchfigs(self):
        """Process all %BRANCHFIG directives."""
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith("%BRANCHFIG "):
                tokens = shlex.split(line)
                name = tokens[1]
                opts = get_options(
                    tokens[2:],
                    path="",
                    caption="",
                    terminated=1,
                    include_leafs=1,
                    strict_leafs=1,
                    width=0,
                    leafs="",
                    relations="all",
                    edgelabels=0,
                    rankdir="BT",
                    legend=1,
                    namespaces="",
                    ontologies="",
                )

                included_namespaces = (
                    opts.namespaces.split(",")
                    if opts.namespaces
                    else ()  # pylint: disable=no-member
                )
                included_ontologies = (
                    opts.ontologies.split(",")
                    if opts.ontologies
                    else ()  # pylint: disable=no-member
                )

                filepath, _, width = self._make_branchfig(
                    name,
                    opts.path,  # pylint: disable=no-member
                    opts.terminated,  # pylint: disable=no-member
                    opts.include_leafs,  # pylint: disable=no-member
                    opts.strict_leafs,  # pylint: disable=no-member
                    opts.width,  # pylint: disable=no-member
                    opts.leafs,  # pylint: disable=no-member
                    opts.relations,  # pylint: disable=no-member
                    opts.edgelabels,  # pylint: disable=no-member
                    opts.rankdir,  # pylint: disable=no-member
                    opts.legend,  # pylint: disable=no-member
                    included_namespaces,
                    included_ontologies,
                )

                del self.lines[i]
                self.lines[i:i] = self.ontodoc.get_figure(
                    filepath,
                    caption=opts.caption,
                    width=width,  # pylint: disable=no-member
                ).split("\n")

    def process_branchdocs(self):  # pylint: disable=too-many-locals
        """Process all %BRANCHDOC and  %BRANCHEAD directives."""
        onto = self.ontodoc.onto
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith("%BRANCHDOC ") or line.startswith(
                "%BRANCHHEAD "
            ):
                with_branch = bool(line.startswith("%BRANCHDOC "))
                tokens = shlex.split(line)
                name = tokens[1]
                title = camelsplit(name)
                title = title[0].upper() + title[1:] + " branch"
                opts = get_options(
                    tokens[2:],
                    level=2,
                    path="",
                    title=title,
                    caption=title + ".",
                    terminated=1,
                    strict_leafs=1,
                    width=0,
                    leafs="",
                    relations="all",
                    edgelabels=0,
                    rankdir="BT",
                    legend=1,
                    namespaces="",
                    ontologies="",
                )

                included_namespaces = (
                    opts.namespaces.split(",")
                    if opts.namespaces
                    else ()  # pylint: disable=no-member
                )
                included_ontologies = (
                    opts.ontologies.split(",")
                    if opts.ontologies
                    else ()  # pylint: disable=no-member
                )

                include_leafs = 1
                filepath, leafs, width = self._make_branchfig(
                    name,
                    opts.path,  # pylint: disable=no-member
                    opts.terminated,  # pylint: disable=no-member
                    include_leafs,
                    opts.strict_leafs,  # pylint: disable=no-member
                    opts.width,  # pylint: disable=no-member
                    opts.leafs,  # pylint: disable=no-member
                    opts.relations,  # pylint: disable=no-member
                    opts.edgelabels,  # pylint: disable=no-member
                    opts.rankdir,  # pylint: disable=no-member
                    opts.legend,  # pylint: disable=no-member
                    included_namespaces,
                    included_ontologies,
                )

                sec = []
                sec.append(
                    self.ontodoc.get_header(opts.title, int(opts.level))
                )  # pylint: disable=no-member
                sec.append(
                    self.ontodoc.get_figure(
                        filepath,
                        caption=opts.caption,
                        width=width,  # pylint: disable=no-member
                    )
                )
                if with_branch:
                    include_leafs = 0
                    branch = filter_classes(
                        onto.get_branch(name, leafs, include_leafs),
                        included_namespaces=included_namespaces,
                        included_ontologies=included_ontologies,
                    )
                    sec.append(
                        self.ontodoc.itemsdoc(
                            branch, int(opts.level + 1)
                        )  # pylint: disable=no-member
                    )

                del self.lines[i]
                self.lines[i:i] = sec

    def process_alls(self):
        """Expand all %ALL specifications."""
        onto = self.ontodoc.onto
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith("%ALL "):
                tokens = shlex.split(line)
                token = tokens[1]
                opts = get_options(tokens[2:], header_level=3)
                if token == "classes":  # nosec
                    items = onto.classes(imported=self.imported)
                elif token in ("object_properties", "relations"):
                    items = onto.object_properties(imported=self.imported)
                elif token == "data_properties":  # nosec
                    items = onto.data_properties(imported=self.imported)
                elif token == "annotation_properties":  # nosec
                    items = onto.annotation_properties(imported=self.imported)
                elif token == "individuals":  # nosec
                    items = onto.individuals(imported=self.imported)
                else:
                    raise InvalidTemplateError(
                        f"Invalid argument to %%ALL: {token}"
                    )
                items = sorted(items, key=asstring)
                del self.lines[i]
                self.lines[i:i] = self.ontodoc.itemsdoc(
                    items, int(opts.header_level)  # pylint: disable=no-member
                ).split("\n")

    def process_allfig(self):  # pylint: disable=too-many-locals
        """Process all %ALLFIG directives."""
        onto = self.ontodoc.onto
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith("%ALLFIG "):
                tokens = shlex.split(line)
                token = tokens[1]
                opts = get_options(
                    tokens[2:],
                    path="",
                    level=3,
                    terminated=0,
                    include_leafs=1,
                    strict_leafs=1,
                    width=0,
                    leafs="",
                    relations="isA",
                    edgelabels=0,
                    rankdir="BT",
                    legend=1,
                    namespaces="",
                    ontologies="",
                )
                if token == "classes":  # nosec
                    roots = onto.get_root_classes(imported=self.imported)
                elif token in ("object_properties", "relations"):
                    roots = onto.get_root_object_properties(
                        imported=self.imported
                    )
                elif token == "data_properties":  # nosec
                    roots = onto.get_root_data_properties(
                        imported=self.imported
                    )
                else:
                    raise InvalidTemplateError(
                        f"Invalid argument to %%ALLFIG: {token}"
                    )

                included_namespaces = (
                    opts.namespaces.split(",")
                    if opts.namespaces
                    else ()  # pylint: disable=no-member
                )
                included_ontologies = (
                    opts.ontologies.split(",")
                    if opts.ontologies
                    else ()  # pylint: disable=no-member
                )

                sec = []
                for root in roots:
                    name = asstring(root)
                    filepath, _, width = self._make_branchfig(
                        name,
                        opts.path,  # pylint: disable=no-member
                        opts.terminated,  # pylint: disable=no-member
                        opts.include_leafs,  # pylint: disable=no-member
                        opts.strict_leafs,  # pylint: disable=no-member
                        opts.width,  # pylint: disable=no-member
                        opts.leafs,  # pylint: disable=no-member
                        opts.relations,  # pylint: disable=no-member
                        opts.edgelabels,  # pylint: disable=no-member
                        opts.rankdir,  # pylint: disable=no-member
                        opts.legend,  # pylint: disable=no-member
                        included_namespaces,
                        included_ontologies,
                    )
                    title = f"Taxonomy of {name}."
                    sec.append(
                        self.ontodoc.get_header(title, int(opts.level))
                    )  # pylint: disable=no-member
                    sec.extend(
                        self.ontodoc.get_figure(
                            filepath, caption=title, width=width
                        ).split("\n")
                    )

                del self.lines[i]
                self.lines[i:i] = sec

    def process_includes(self):
        """Process all %INCLUDE directives."""
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith("%INCLUDE "):
                tokens = shlex.split(line)
                filepath = tokens[1]
                opts = get_options(tokens[2:], shift=0)
                with open(
                    os.path.join(self.basedir, filepath), "rt", encoding="utf8"
                ) as handle:
                    docpp = DocPP(
                        handle.read(),
                        self.ontodoc,
                        basedir=os.path.dirname(filepath),
                        figformat=self.figformat,
                        figscale=self.figscale,
                        maxwidth=self.maxwidth,
                    )
                    docpp.figdir = self.figdir
                if opts.shift:  # pylint: disable=no-member
                    docpp.shift_header_levels(
                        int(opts.shift)
                    )  # pylint: disable=no-member
                docpp.process()
                del self.lines[i]
                self.lines[i:i] = docpp.lines

    def process(self):
        """Perform all pre-processing steps."""
        if not self._processed:
            self.process_comments()
            self.process_headers()
            self.process_figures()
            self.process_entities()
            self.process_branches()
            self.process_branchfigs()
            self.process_branchdocs()
            self.process_alls()
            self.process_allfig()
            self.process_includes()
            self._processed = True

    def write(  # pylint: disable=too-many-arguments
        self,
        outfile,
        fmt=None,
        pandoc_option_files=(),
        pandoc_options=(),
        genfile=None,
        verbose=True,
    ):
        """Writes documentation to `outfile`.

        Parameters
        ----------
        outfile : str
            File that the documentation is written to.
        fmt : str
            Output format.  If it is "md" or "simple-html",
            the built-in template generator is used.  Otherwise
            pandoc is used.  If not given, the format is inferred
            from the `outfile` name extension.
        pandoc_option_files : sequence
            Sequence with command line arguments provided to pandoc.
        pandoc_options : sequence
            Additional pandoc options overriding options read from
        `pandoc_option_files`.
        genfile : str
            Store temporary generated markdown input file to pandoc
            to this file (for debugging).
        verbose : bool
            Whether to show some messages when running pandoc.
        """
        self.process()
        content = self.get_buffer()

        substitutions = self.ontodoc.style.get("substitutions", [])
        for reg, sub in substitutions:
            content = re.sub(reg, sub, content)

        fmt = get_format(outfile, fmt)
        if fmt not in ("simple-html", "markdown", "md"):  # Run pandoc
            if not genfile:
                with NamedTemporaryFile(mode="w+t", suffix=".md") as temp_file:
                    temp_file.write(content)
                    temp_file.flush()
                    genfile = temp_file.name

                    run_pandoc(
                        genfile,
                        outfile,
                        fmt,
                        pandoc_option_files=pandoc_option_files,
                        pandoc_options=pandoc_options,
                        verbose=verbose,
                    )
            else:
                with open(genfile, "wt") as handle:
                    handle.write(content)

                run_pandoc(
                    genfile,
                    outfile,
                    fmt,
                    pandoc_option_files=pandoc_option_files,
                    pandoc_options=pandoc_options,
                    verbose=verbose,
                )
        else:
            if verbose:
                print("Writing:", outfile)
            with open(outfile, "wt") as handle:
                handle.write(content)


def load_pandoc_option_file(yamlfile):
    """Loads pandoc options from `yamlfile` and return a list with
    corresponding pandoc command line arguments."""
    with open(yamlfile) as handle:
        pandoc_options = yaml.safe_load(handle)
    options = pandoc_options.pop("input-files", [])
    variables = pandoc_options.pop("variables", {})

    for key, value in pandoc_options.items():
        if isinstance(value, bool):
            if value:
                options.append(f"--{key}")
        else:
            options.append(f"--{key}={value}")

    for key, value in variables.items():
        if key == "date" and value == "now":
            value = time.strftime("%B %d, %Y")
        options.append(f"--variable={key}:{value}")

    return options


def append_pandoc_options(options, updates):
    """Append `updates` to pandoc options `options`.

    Parameters
    ----------
    options : sequence
        Sequence with initial Pandoc options.
    updates : sequence of str
        Sequence of strings of the form "--longoption=value", where
        ``longoption`` is a valid pandoc long option and ``value`` is the
        new value.  The "=value" part is optional.

        Strings of the form "no-longoption" will filter out "--longoption"
        from `options`.

    Returns
    -------
    new_options : list
        Updated pandoc options.
    """
    # Valid pandoc options starting with "--no-XXX"
    no_options = set("no-highlight")

    if not updates:
        return list(options)

    curated_updates = {}
    for update in updates:
        key, sep, value = update.partition("=")
        curated_updates[key.lstrip("-")] = value if sep else None
        filter_out = set(
            _
            for _ in curated_updates
            if _.startswith("no-") and _ not in no_options
        )
        _filter_out = set(f"--{_[3:]}" for _ in filter_out)
        new_options = [
            opt for opt in options if opt.partition("=")[0] not in _filter_out
        ]
        new_options.extend(
            [
                f"--{key}" if value is None else f"--{key}={value}"
                for key, value in curated_updates.items()
                if key not in filter_out
            ]
        )
    return new_options


def run_pandoc(  # pylint: disable=too-many-arguments
    genfile,
    outfile,
    fmt,
    pandoc_option_files=(),
    pandoc_options=(),
    verbose=True,
):
    """Runs pandoc.

    Parameters
    ----------
    genfile : str
        Name of markdown input file.
    outfile : str
        Output file name.
    fmt : str
        Output format.
    pandoc_option_files : sequence
        List of files with additional pandoc options.  Default is to read
        "pandoc-options.yaml" and "pandoc-FORMAT-options.yml", where
        `FORMAT` is the output format.
    pandoc_options : sequence
        Additional pandoc options overriding options read from
        `pandoc_option_files`.
    verbose : bool
        Whether to print the pandoc command before execution.

    Raises
    ------
    subprocess.CalledProcessError
        If the pandoc process returns with non-zero status.  The `returncode`
        attribute will hold the exit code.
    """
    # Create pandoc argument list
    args = [genfile]
    files = ["pandoc-options.yaml", f"pandoc-{fmt}-options.yaml"]
    if pandoc_option_files:
        files = pandoc_option_files
    for fname in files:
        if os.path.exists(fname):
            args.extend(load_pandoc_option_file(fname))
        else:
            warnings.warn(f"missing pandoc option file: {fname}")

    # Update pandoc argument list
    args = append_pandoc_options(args, pandoc_options)

    # pdf output requires a special attention...
    if fmt == "pdf":
        pdf_engine = "pdflatex"
        for arg in args:
            if arg.startswith("--pdf-engine"):
                pdf_engine = arg.split("=", 1)[1]
                break
        with TemporaryDirectory() as tmpdir:
            run_pandoc_pdf(tmpdir, pdf_engine, outfile, args, verbose=verbose)
    else:
        args.append(f"--output={outfile}")
        cmd = ["pandoc"] + args
        if verbose:
            print()
            print("* Executing command:")
            print(" ".join(shlex.quote(_) for _ in cmd))
        subprocess.check_call(cmd)  # nosec


def run_pandoc_pdf(latex_dir, pdf_engine, outfile, args, verbose=True):
    """Run pandoc for pdf generation."""
    basename = os.path.join(
        latex_dir, os.path.splitext(os.path.basename(outfile))[0]
    )

    # Run pandoc
    texfile = basename + ".tex"
    args.append(f"--output={texfile}")
    cmd = ["pandoc"] + args
    if verbose:
        print()
        print("* Executing commands:")
        print(" ".join(shlex.quote(s) for s in cmd))
    subprocess.check_call(cmd)  # nosec

    # Fixing tex output
    texfile2 = basename + "2.tex"
    with open(texfile, "rt") as handle:
        content = handle.read().replace(r"\$\Uptheta\$", r"$\Uptheta$")
    with open(texfile2, "wt") as handle:
        handle.write(content)

    # Run latex
    pdffile = basename + "2.pdf"
    cmd = [
        pdf_engine,
        texfile2,
        "-halt-on-error",
        f"-output-directory={latex_dir}",
    ]
    if verbose:
        print()
        print(" ".join(shlex.quote(s) for s in cmd))
    output = subprocess.check_output(cmd, timeout=60)  # nosec
    output = subprocess.check_output(cmd, timeout=60)  # nosec

    # Workaround for non-working "-output-directory" latex option
    if not os.path.exists(pdffile):
        if os.path.exists(os.path.basename(pdffile)):
            pdffile = os.path.basename(pdffile)
            for ext in "aux", "out", "toc", "log":
                filename = os.path.splitext(pdffile)[0] + "." + ext
                if os.path.exists(filename):
                    os.remove(filename)
        else:
            print()
            print(output)
            print()
            raise RuntimeError("latex did not produce pdf file: " + pdffile)

    # Copy pdffile
    if not os.path.exists(outfile) or not os.path.samefile(pdffile, outfile):
        if verbose:
            print()
            print(f"move {pdffile} to {outfile}")
        shutil.move(pdffile, outfile)


def get_format(outfile, fmt=None):
    """Infer format from outfile and format."""
    if fmt is None:
        fmt = os.path.splitext(outfile)[1]
    if not fmt:
        fmt = "html"
    if fmt.startswith("."):
        fmt = fmt[1:]
    return fmt


def get_style(fmt):
    """Infer style from output format."""
    if fmt == "simple-html":
        style = "html"
    elif fmt in ("tex", "latex", "pdf"):
        style = "markdown_tex"
    else:
        style = "markdown"
    return style


def get_figformat(fmt):
    """Infer preferred figure format from output format."""
    if fmt == "pdf":
        figformat = "pdf"  # XXX
    elif "html" in fmt:
        figformat = "svg"
    else:
        figformat = "png"
    return figformat


def get_maxwidth(fmt):
    """Infer preferred max figure width from output format."""
    if fmt == "pdf":
        maxwidth = 668
    else:
        maxwidth = 1024
    return maxwidth


def get_docpp(  # pylint: disable=too-many-arguments
    ontodoc,
    infile,
    figdir="genfigs",
    figformat="png",
    maxwidth=None,
    imported=False,
):
    """Read `infile` and return a new docpp instance."""
    if infile:
        with open(infile, "rt") as handle:
            template = handle.read()
        basedir = os.path.dirname(infile)
    else:
        template = ontodoc.get_default_template()
        basedir = "."

    docpp = DocPP(
        template,
        ontodoc,
        basedir=basedir,
        figdir=figdir,
        figformat=figformat,
        maxwidth=maxwidth,
        imported=imported,
    )

    return docpp
