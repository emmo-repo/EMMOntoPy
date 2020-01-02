# -*- coding: utf-8 -*-
"""
A module for documenting ontologies.
"""
import os
import re
import time
import warnings
import shlex
import subprocess
from textwrap import dedent
from tempfile import NamedTemporaryFile

import yaml
import owlready2

from .utils import asstring, camelsplit
from .ontograph import get_figsize


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
    _markdown_style = dict(
        sep='\n',
        figwidth='{{ width={width:.0f}px }}',
        figure='![{caption}]({path}){figwidth}\n',
        header='\n{:#<{level}} {label}',
        link='[{name}]({lowerurl})',
        point='  - {point}\n',
        points='\n\n{points}\n',
        annotation='**{key}:** {value}\n',
        substitutions=[],
    )
    # Extra style settings for markdown+tex (e.g. pdf generation with pandoc)
    _markdown_tex_extra_style = dict(
        substitutions=[
            # logic/math symbols
            ('\u2200', r'$\\forall$'),
            ('\u2203', r'$\\exists$'),
            ('\u2227', r'$\\land$'),
            ('\u2228', r'$\\lor$'),
            # uppercase greek letters
            ('\u0391', r'$\\Upalpha$'),
            ('\u0392', r'$\\Upbeta$'),
            ('\u0393', r'$\\Upgamma$'),
            ('\u0394', r'$\\Updelta$'),
            ('\u0395', r'$\\Upepsilon$'),
            ('\u0396', r'$\\Upzeta$'),
            ('\u0397', r'$\\Upeta$'),
            ('\u0398', r'$\\Uptheta$'),
            ('\u0399', r'$\\Upiota$'),
            ('\u039a', r'$\\Upkappa$'),
            ('\u039b', r'$\\Uplambda$'),
            ('\u039c', r'$\\Upmu$'),
            ('\u039d', r'$\\Upnu$'),
            ('\u039e', r'$\\Upxi$'),
            ('\u039f', r'$\\Upomekron$'),
            ('\u03a0', r'$\\Uppi$'),
            ('\u03a1', r'$\\Uprho$'),
            ('\u03a3', r'$\\Upsigma$'),  # no \u0302
            ('\u03a4', r'$\\Uptau$'),
            ('\u03a5', r'$\\Upupsilon$'),
            ('\u03a6', r'$\\Upvarphi$'),
            ('\u03a7', r'$\\Upchi$'),
            ('\u03a8', r'$\\Uppsi$'),
            ('\u03a9', r'$\\Upomega$'),
            # lowercase greek letters
            ('\u03b1', r'$\\upalpha$'),
            ('\u03b2', r'$\\upbeta$'),
            ('\u03b3', r'$\\upgamma$'),
            ('\u03b4', r'$\\updelta$'),
            ('\u03b5', r'$\\upepsilon$'),
            ('\u03b6', r'$\\upzeta$'),
            ('\u03b7', r'$\\upeta$'),
            ('\u03b8', r'$\\uptheta$'),
            ('\u03b9', r'$\\upiota$'),
            ('\u03ba', r'$\\upkappa$'),
            ('\u03bb', r'$\\uplambda$'),
            ('\u03bc', r'$\\upmu$'),
            ('\u03bd', r'$\\upnu$'),
            ('\u03be', r'$\\upxi$'),
            ('\u03bf', r'$\\upomicron$'),
            ('\u03c0', r'$\\uppi$'),
            ('\u03c1', r'$\\uprho$'),
            ('\u03c2', r'$\\upvarsigma$'),
            ('\u03c3', r'$\\upsigma$'),
            ('\u03c4', r'$\\uptau$'),
            ('\u03c5', r'$\\upupsilon$'),
            ('\u03c6', r'$\\upvarphi$'),
            ('\u03c7', r'$\\upchi$'),
            ('\u03c8', r'$\\uppsi$'),
            ('\u03c9', r'$\\upomega$'),
            # acutes, accents, etc...
            ('\u03ae', r"$\\acute{\\upeta}$"),
            ('\u1e17', r"$\\acute{\\bar{\\mathrm{e}}}$"),
            ('\u03ac', r"$\\acute{\\upalpha}$"),
            ('\u00e1', r"$\\acute{\\mathrm{a}}$"),
            ('\u03cc', r"$\\acute{\\upomicron}$"),
            ('\u014d', r"$\\bar{\\mathrm{o}}$"),
        ],
    )
    _html_style = dict(
        sep='<p>\n',
        figwidth='width="{width:.0f}"',
        figure='<img src="{path}" alt="{caption}"{figwidth}>',
        header='<h{level} id="{lowerlabel}">{label}</h{level}>',
        link='<a href="{lowerurl}">{name}</a>',
        point='      <li>{point}</li>\n',
        points='    <ul>\n      {points}\n    </ul>\n',
        annotation='  <dd><strong>{key}:</strong>\n{value}  </dd>\n',
        substitutions=[
            (r'\n\n', r'<p>'),
            (r'\n', r'<br>\n'),
            (r'&', r"&#8210;"),
            (r'<p>', r'<p>\n\n'),
            (r'\u2018([^\u2019]*)\u2019', r'<q>\1</q>'),
            (r'\u2019', r"'"),
            (r'\u2260', r"&ne;"),
            (r'\u2264', r"&le;"),
            (r'\u2265', r"&ge;"),
            (r'\u226A', r"&x226A;"),
            (r'\u226B', r"&x226B;"),
            (r'"Y$', r""),  # strange noice added by owlready2
        ],
    )

    def __init__(self, onto, style='markdown'):
        if isinstance(style, str):
            if style == 'markdown_tex':
                style = self._markdown_style.copy()
                style.update(self._markdown_tex_extra_style)
            else:
                style = getattr(self, '_%s_style' % style)
        self.onto = onto
        self.style = style

    def get_default_template(self):
        """Returns default template."""
        title = os.path.splitext(os.path.basename(self.onto.base_iri))[0]
        irilink = self.style.get('link', '{name}').format(
            name=self.onto.base_iri, url=self.onto.base_iri,
            lowerurl=self.onto.base_iri)
        s = dedent('''\
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
        ''').format(ontology=self.onto, title=title, irilink=irilink)
        return s

    def get_header(self, label, header_level=1):
        """Returns `label` formatted as a header of given level."""
        header_style = self.style.get('header', '{label}\n')
        return header_style.format(
            '', level=header_level, label=label, lowerlabel=label.lower())

    def get_figure(self, path, caption='', width=None):
        """Returns a formatted insert-figure-directive."""
        figwidth_style = self.style.get('figwidth', '')
        figure_style = self.style.get('figure', '')
        figwidth = figwidth_style.format(width=width) if width else ''
        return figure_style.format(path=path, caption=caption,
                                   figwidth=figwidth)

    def itemdoc(self, item, header_level=3):
        """Returns documentation of `item`.

        Parameters
        ----------
        item : obj | label
            The class, individual or relation to document.
        header_level : int
            Header level. Defaults to 3.
        """
        onto = self.onto
        if isinstance(item, str):
            item = self.onto.get_by_label(item)

        header_style = self.style.get('header', '{label}\n')
        link_style = self.style.get('link', '{name}')
        point_style = self.style.get('point', '{point}')
        points_style = self.style.get('points', '{points}')
        annotation_style = self.style.get('annotation', '{key}: {value}\n')
        substitutions = self.style.get('substitutions', [])

        # Logical "sorting" of annotations
        order = dict(definition='00', axiom='01', theorem='02',
                     elucidation='03', domain='04', range='05', example='06')

        doc = []

        # Header
        label = item.label.first()
        doc.append(header_style.format(
            '', level=header_level, label=label, lowerlabel=label.lower()))

        # Add iri
        doc.append(annotation_style.format(
            key='IRI', value=asstring(item.iri, link_style), ontology=onto))

        # Add annotations
        if isinstance(item, owlready2.Thing):
            annotations = item.get_individual_annotations()
        else:
            annotations = item.get_annotations()
        for key in sorted(annotations.keys(),
                          key=lambda key: order.get(key, key)):
            for value in annotations[key]:
                for reg, sub in substitutions:
                    value = re.sub(reg, sub, value)
                doc.append(annotation_style.format(
                    key=key.capitalize(), value=value))

        # ...add relations from is_a
        points = []
        nonProp = (owlready2.ThingClass,  # owlready2.Restriction,
                   owlready2.And, owlready2.Or, owlready2.Not)
        for p in item.is_a:
            if (isinstance(p, nonProp) or
                (isinstance(item, owlready2.PropertyClass) and
                 isinstance(p, owlready2.PropertyClass))):
                points.append(point_style.format(
                    point='is_a ' + asstring(p, link_style), ontology=onto))
            else:
                points.append(point_style.format(
                    point=asstring(p, link_style), ontology=onto))

        # ...add equivalent_to relations
        for e in item.equivalent_to:
            points.append(point_style.format(
                point='equivalent_to ' + asstring(e, link_style)))

        # ...add disjoint_with relations
        if hasattr(item, 'disjoints'):
            for d in item.disjoints():
                s = ', '.join(asstring(e, link_style) for e in d)
                points.append(point_style.format(
                    point='disjoint_width ' + s, ontology=onto))

        # ...add disjoint_unions
        if hasattr(item, 'disjoint_unions'):
            for u in item.disjoint_unions:
                s = ', '.join(asstring(e, link_style) for e in u)
                points.append(point_style.format(
                    point='disjoint_union_of ' + s, ontology=onto))

        # ...add inverse_of relations
        if hasattr(item, 'inverse_property') and item.inverse_property:
            points.append(point_style.format(
                point='inverse_of ' + asstring(
                    item.inverse_property, link_style)))

        # ...add domain restrictions
        for d in getattr(item, 'domain', ()):
            points.append(point_style.format(
                point='domain ' + asstring(d, link_style)))

        # ...add range restrictions
        for d in getattr(item, 'range', ()):
            points.append(point_style.format(
                point='range ' + asstring(d, link_style)))

        # Add relations
        if points:
            value = points_style.format(
                points=''.join(points), ontology=onto)
            doc.append(annotation_style.format(
                key='Relations', value=value, ontology=onto))

        # Instances (individuals)
        if hasattr(item, 'instances'):
            points = []
            for e in [i for i in item.instances() if item in i.is_instance_of]:
                points.append(point_style.format(
                    point=asstring(e, link_style), ontology=onto))
            if points:
                value = points_style.format(
                    points=''.join(points), ontology=onto)
                doc.append(annotation_style.format(
                    key='Individuals', value=value, ontology=onto))

        return '\n'.join(doc)

    def itemsdoc(self, items, header_level=3):
        """Returns documentation of `items`."""
        sep_style = self.style.get('sep', '\n')
        doc = []
        for item in items:
            doc.append(self.itemdoc(item, header_level))
            doc.append(sep_style.format(ontology=self.onto))
        return '\n'.join(doc)


class attrdict(dict):
    """A dict with attribute access.

    Note that methods like key() and update() may be overridden."""
    def __init__(self, *args, **kwargs):
        super(attrdict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class InvalidTemplateError(NameError):
    """Raised on errors in template files."""


def get_options(opts, **kw):
    """Returns a dict with options from the sequence `opts` with
    "name=value" pairs. Valid option names and default values are
    provided with the keyword arguments."""
    d = attrdict(kw)
    for opt in opts:
        if '=' not in opt:
            raise InvalidTemplateError('Missing "=" in template option: %r' %
                                       opt)
        name, value = opt.split('=', 1)
        if name not in d:
            raise InvalidTemplateError('Invalid template option: %r' % name)
        t = type(d[name])
        d[name] = t(value)
    return d


class DocPP:
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

            %BRANCH name [header_level=3 terminated=1 include_leafs=0]

      * Insert generated figure of ontology branch `name`.  The figure
        is written to `path`.  The default path is `figdir`/`name`,
        where `figdir` is given at class initiation. It is recommended
        to exclude the file extension from `path`.  In this case, the
        default figformat will be used (and easily adjusted to the
        correct format required by the backend). `leafs` may be a comma-
        separated list of leaf node names.

            %BRANCHFIG name [path='' caption='' terminated=1 include_leafs=1
                             width=0px leafs='']

      * This is a combination of the %HEADER and %BRANCHFIG directives.

            %BRANCHHEAD name [level=2  path='' caption='' terminated=1
                              include_leafs=1 width=0px leafs='']

      * This is a combination of the %HEADER, %BRANCHFIG and %BRANCH
        directives. It inserts documentation of branch `name`, with a
        header followed by a figure and then documentation of each
        element.

            %BRANCHDOC name [level=2  path='' caption='' terminated=1
                             include_leafs=1 width=0px leafs='']

      * Insert generated documentation for all entities of the given type.
        Valid values of `type` are: "classes", "individuals",
        "object_properties", "data_properties", "annotations_properties"

            %ALL type [header_level=3]

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

    """

    # FIXME - this class should be refractured:
    #   * Instead of rescan the entire document for each pre-processer
    #     directive, we should scan the source like by line and handle
    #     each directive as they occour.  The current implementation has
    #     a lot of dublicated code.
    #   * Instead of modifying the source in-place, we should copy to a
    #     result list. This will make good error reporting much easier.
    #   * Branch leaves are only looked up in the file witht the %BRANCH
    #     directive, not in all included files as expedted.

    def __init__(self, template, ontodoc, basedir='.', figdir='genfigs',
                 figformat='png', figscale=1.0, maxwidth=None):
        self.lines = template.split('\n')
        self.ontodoc = ontodoc
        self.basedir = basedir
        self.figdir = os.path.join(basedir, figdir)
        self.figformat = figformat
        self.figscale = figscale
        self.maxwidth = maxwidth
        self._branch_cache = None
        self._processed = False  # Whether process() has been called

    def __str__(self):
        return self.get_buffer()

    def get_buffer(self):
        """Returns the current buffer."""
        return '\n'.join(self.lines)

    def copy(self):
        """Returns a copy of self."""
        docpp = DocPP('', self.ontodoc, self.basedir, figformat=self.figformat,
                      figscale=self.figscale, maxwidth=self.maxwidth)
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
                if line.startswith('%BRANCH'):
                    names.append(shlex.split(line)[1])
            self._branch_cache = names
        return self._branch_cache

    def shift_header_levels(self, shift):
        """Shift header level of all hashtag-headers in buffer.  Underline
        headers are ignored."""
        if not shift:
            return
        pat = re.compile('^#+ ')
        for i, line in enumerate(self.lines):
            m = pat.match(line)
            if m:
                if shift > 0:
                    self.lines[i] = '#' * shift + line
                elif shift < 0:
                    n = m.end()
                    if shift > n:
                        self.lines[i] = line.lstrip('# ')
                    else:
                        self.lines[i] = line[n:]

    def process_comments(self):
        """Strips out comment lines starting with "%%"."""
        self.lines = [line for line in self.lines if not line.startswith('%%')]

    def process_headers(self):
        """Expand all %HEADER specifications."""
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith('%HEADER '):
                tokens = shlex.split(line)
                name = tokens[1]
                opts = get_options(tokens[2:], level=1)
                del self.lines[i]
                self.lines[i: i] = self.ontodoc.get_header(
                    name, int(opts.level)).split('\n')

    def process_figures(self):
        """Expand all %FIGURE specifications."""
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith('%FIGURE '):
                tokens = shlex.split(line)
                path = tokens[1]
                opts = get_options(tokens[2:], caption='', width=0)
                del self.lines[i]
                self.lines[i: i] = self.ontodoc.get_figure(
                    os.path.join(self.basedir, path),
                    caption=opts.caption, width=opts.width).split('\n')

    def process_entities(self):
        """Expand all %ENTITY specifications."""
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith('%ENTITY '):
                tokens = shlex.split(line)
                name = tokens[1]
                opts = get_options(tokens[2:], header_level=3)
                del self.lines[i]
                self.lines[i: i] = self.ontodoc.itemdoc(
                    name, int(opts.header_level)).split('\n')

    def process_branches(self):
        """Expand all %BRANCH specifications."""
        # Get all branch names in final document
        names = self.get_branches()
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith('%BRANCH '):
                tokens = shlex.split(line)
                name = tokens[1]
                opts = get_options(tokens[2:], header_level=3, terminated=1,
                                   include_leafs=0)
                leafs = names if opts.terminated else ()
                branch = self.ontodoc.onto.get_branch(name, leafs,
                                                      opts.include_leafs)
                del self.lines[i]
                self.lines[i: i] = self.ontodoc.itemsdoc(
                    branch, int(opts.header_level)).split('\n')

    def _make_branchfig(self, name, path, style, terminated, width, leafs):
        """Help method for process_branchfig().

        Args:
            name: name of branch root
            path: optional figure path name
            style: optional graph style
            terminated: whether the graph should be terminated at leaf nodes
            width: optional figure width
            leafs: optional leafs node names for graph termination

        Returns:
            filepath: path to generated figure
            leafs: used list of leaf node names
            width: actual figure width
        """
        onto = self.ontodoc.onto
        if leafs:
            if isinstance(leafs, str):
                leafs = leafs.split(',')
        elif terminated:
            leafs = set(self.get_branches())
            leafs.discard(name)
        else:
            leafs = None
        graph = onto.get_dot_graph(name, relations=True,
                                   leafs=leafs, style=style)
        if not width:
            figwidth, figheight = get_figsize(graph)
            width = self.figscale * figwidth
            if self.maxwidth and width > self.maxwidth:
                width = self.maxwidth

        # Set node URLs. Hmm, shouldn't that be done in ontograph.py?
        for node in graph.get_nodes():
            node.set_URL(onto[node.get_name()].iri)
            node.set_target("_top")

        # Add extra border to leafs nodes
        roots = set(asstring(r) for r in onto.get_roots())
        for leaf in set(self.get_branches()).difference(roots):
            nodes = graph.get_node(asstring(leaf))
            for node in nodes:
                node.set_penwidth(3)

        # Change root nodes to double octagons
        for root in roots:
            nodes = graph.get_node(asstring(root))
            for node in nodes:
                node.set_shape('doubleoctagon')

        if path:
            figdir = os.path.dirname(path)
            formatext = os.path.splitext(path)[1]
            if formatext:
                format = formatext.lstrip('.')
            else:
                format = self.figformat
                path += '.' + format
        else:
            figdir = self.figdir
            format = self.figformat
            term = 'T' if terminated else ''
            path = os.path.join(figdir, name + term) + '.' + format

        filepath = os.path.join(self.basedir, path)
        destdir = os.path.dirname(filepath)
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        writer = getattr(graph, 'write_' + format)
        writer(filepath)
        return filepath, leafs, width

    def process_branchfigs(self):
        """Process all %BRANCHFIG directives."""
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith('%BRANCHFIG '):
                tokens = shlex.split(line)
                name = tokens[1]
                opts = get_options(tokens[2:], path='', caption='',
                                   terminated=1, width=0, style='default',
                                   leafs='')
                filepath, leafs, width = self._make_branchfig(
                    name, opts.path, opts.style, opts.terminated, opts.width,
                    opts.leafs)

                del self.lines[i]
                self.lines[i: i] = self.ontodoc.get_figure(
                    filepath, caption=opts.caption, width=width).split('\n')

    def process_branchdocs(self):
        """Process all %BRANCHDOC and  %BRANCHEAD directives."""
        onto = self.ontodoc.onto
        for i, line in reversed(list(enumerate(self.lines))):
            if (line.startswith('%BRANCHDOC ') or
                    line.startswith('%BRANCHHEAD ')):
                with_branch = True if line.startswith('%BRANCHDOC ') else False
                tokens = shlex.split(line)
                name = tokens[1]
                title = camelsplit(name)
                title = title[0].upper() + title[1:] + ' branch'
                opts = get_options(tokens[2:], level=2, path='', title=title,
                                   caption=title + '.', terminated=1,
                                   include_leafs=0, width=0, style='default',
                                   leafs='')

                filepath, leafs, width = self._make_branchfig(
                    name, opts.path, opts.style, opts.terminated, opts.width,
                    opts.leafs)

                sec = []
                sec.append(
                    self.ontodoc.get_header(opts.title, int(opts.level)))
                sec.append(
                    self.ontodoc.get_figure(filepath, caption=opts.caption,
                                            width=width))
                if with_branch:
                    branch = onto.get_branch(name, leafs, opts.include_leafs)
                    sec.append(
                        self.ontodoc.itemsdoc(branch, int(opts.level + 1)))

                del self.lines[i]
                self.lines[i: i] = sec

    def process_alls(self):
        """Expand all %ALL specifications."""
        onto = self.ontodoc.onto
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith('%ALL '):
                tokens = shlex.split(line)
                type = tokens[1]
                opts = get_options(tokens[2:], header_level=3)
                if type == 'classes':
                    items = onto.classes()
                elif type in ('object_properties', 'relations'):
                    items = onto.object_properties()
                elif type == 'data_properties':
                    items = onto.data_properties()
                elif type == 'annotation_properties':
                    items = onto.annotation_properties()
                elif type == 'individuals':
                    items = onto.individuals()
                else:
                    raise InvalidTemplateError(
                        'Invalid argument to %%ALL: %s' % type)
                items = sorted(items, key=lambda x: asstring(x))
                del self.lines[i]
                self.lines[i: i] = self.ontodoc.itemsdoc(
                    items, int(opts.header_level)).split('\n')

    def process_allfig(self):
        """Process all %ALLFIG directives."""
        onto = self.ontodoc.onto
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith('%ALLFIG '):
                tokens = shlex.split(line)
                type = tokens[1]
                opts = get_options(tokens[2:], path='', level=3,
                                   terminated=0, width=0, style='default',
                                   leafs='')
                if type == 'classes':
                    roots = onto.get_root_classes()
                elif type in ('object_properties', 'relations'):
                    roots = onto.get_root_object_properties()
                elif type == 'data_properties':
                    roots = onto.get_root_data_properties()
                else:
                    raise InvalidTemplateError(
                        'Invalid argument to %%ALL: %s' % type)

                sec = []
                for root in roots:
                    name = asstring(root)
                    filepath, leafs, width = self._make_branchfig(
                        name, opts.path, opts.style, opts.terminated,
                        opts.width, opts.leafs)
                    title = 'Taxonomy of %s.' % name
                    sec.append(
                        self.ontodoc.get_header(title, int(opts.level)))
                    caption = 'Taxonomy of %s.' % name
                    sec.extend(self.ontodoc.get_figure(
                        filepath, caption=caption, width=width).split('\n'))

                del self.lines[i]
                self.lines[i: i] = sec

    def process_includes(self):
        """Process all %INCLUDE directives."""
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith('%INCLUDE '):
                tokens = shlex.split(line)
                filepath = tokens[1]
                opts = get_options(tokens[2:], shift=0)
                with open(os.path.join(self.basedir, filepath), 'rt') as f:
                    docpp = DocPP(
                        f.read(), self.ontodoc,
                        basedir=os.path.dirname(filepath),
                        figformat=self.figformat, figscale=self.figscale,
                        maxwidth=self.maxwidth)
                    docpp.figdir = self.figdir
                if opts.shift:
                    docpp.shift_header_levels(int(opts.shift))
                docpp.process()
                del self.lines[i]
                self.lines[i: i] = docpp.lines

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

    def write(self, outfile, format=None, pandoc_args=None, genfile=None,
              verbose=True):
        """Writes documentation to `outfile`.

        Parameters
        ----------
        outfile : str
            File that the documentation is written to.
        format : str
            Output format.  If it is "md" or "simple-html",
            the built-in template generator is used.  Otherwise
            pandoc is used.  If not given, the format is inferred
            from the `outfile` name extension.
        pandoc_args : sequence
            Sequence with command line arguments provided to pandoc.
        genfile : str
            Store temporary generated markdown input file to pandoc
            to this file (for debugging).
        verbose : bool
            Whether to show some messages when running pandoc.
        """
        self.process()
        content = self.get_buffer()
        format = get_format(outfile, format)
        if format not in ('simple-html', 'markdown', 'md'):  # Run pandoc
            if not genfile:
                f = NamedTemporaryFile(mode='w+t', suffix='.md')
                f.write(content)
                f.flush()
                genfile = f.name
            else:
                with open(genfile, 'wt') as f:
                    f.write(content)
            run_pandoc(genfile, outfile, format, pandoc_args=pandoc_args,
                       verbose=verbose)
        else:
            if verbose:
                print('Writing:', outfile)
            with open(outfile, 'wt') as f:
                f.write(content)


def load_pandoc_options(yamlfile):
    """Loads pandoc options from `yamlfile` and return a list with
    corresponding pandoc command line arguments."""
    with open(yamlfile) as f:
        d = yaml.safe_load(f)
    args = d.pop('input-files', [])
    variables = d.pop('variables', {})

    for k, v in d.items():
        if isinstance(v, bool):
            if v:
                args.append('--%s' % k)
        else:
            args.append('--%s=%s' % (k, v))

    for k, v in variables.items():
        if k == 'date' and v == 'now':
            v = time.strftime('%B %d, %Y')
        args.append('--variable=%s:%s' % (k, v))

    return args


def run_pandoc(genfile, outfile, format, pandoc_args=[], verbose=True):
    """Runs pandoc.

    Parameters
    ----------
    genfile : str
        Name of markdown input file.
    outfile : str
        Output file name.
    format : str
        Output format.
    pandoc_args : sequence
        List of files with additional pandoc options.
    verbose : bool
        Whether to print the pandoc command before execution.
    """
    # Create pandoc argument list
    args = [genfile]
    files = ['pandoc-args.yaml', 'pandoc-%s-args.yaml' % format]
    if pandoc_args:
        files.extend(pandoc_args)
    for fname in files:
        if os.path.exists(fname):
            args.extend(load_pandoc_options(fname))
        else:
            warnings.warn('missing pandoc option file: %s' % fname)
    args.append('--output=%s' % outfile)

    # Run pandoc
    cmd = ['pandoc'] + args
    if verbose:
        print()
        print('* Executing command:')
        print(' '.join(shlex.quote(s) for s in cmd))
    subprocess.check_call(cmd)


def get_format(outfile, format=None):
    """Infer format from outfile and format."""
    if format is None:
        format = os.path.splitext(outfile)[1]
    if not format:
        format = 'html'
    if format.startswith('.'):
        format = format[1:]
    return format


def get_style(format):
    """Infer style from output format."""
    if format == 'simple-html':
        style = 'html'
    elif format in ('tex', 'latex', 'pdf'):
        style = 'markdown_tex'
    else:
        style = 'markdown'
    return style


def get_figformat(format):
    """Infer preferred figure format from output format."""
    if format == 'pdf':
        figformat = 'pdf'
    elif 'html' in format:
        figformat = 'svg'
    else:
        figformat = 'png'
    return figformat


def get_maxwidth(format):
    """Infer preferred max figure width from output format."""
    if format == 'pdf':
        maxwidth = 668
    else:
        maxwidth = 1024
    return maxwidth


def get_docpp(ontodoc, infile, figdir='genfigs', figformat='png',
              maxwidth=None):
    """Read `infile` and return a new docpp instance."""
    if infile:
        with open(infile, 'rt') as f:
            template = f.read()
        basedir = os.path.dirname(infile)
    else:
        template = ontodoc.get_default_template()
        basedir = '.'

    docpp = DocPP(template, ontodoc, basedir=basedir, figdir=figdir,
                  figformat=figformat, maxwidth=maxwidth)

    return docpp
