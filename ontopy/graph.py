# -*- coding: utf-8 -*-
"""
A module for visualising ontologies using graphviz.
"""
import os
import re
import tempfile
import xml.etree.ElementTree as ET

import owlready2
import graphviz

from ontopy.utils import asstring, get_label
from ontopy.ontology import get_ontology

typenames = owlready2.class_construct._restriction_type_2_label


# Literal for `root` arguments
ALL = 1

_default_style = {
    'graphtype': 'Digraph',
    'graph': {
        'rankdir': 'BT', 'fontsize': '8',
        # 'fontname': 'Bitstream Vera Sans', 'splines': 'ortho',
    },
    'class': {
        'style': 'filled',
        'fillcolor': '#ffffcc',
    },
    'root': {'penwidth': '2'},
    'leaf': {'penwidth': '2'},
    'defined_class': {
        'style': 'filled',
        'fillcolor': '#ffc880',
    },
    'class_construct': {
        'style': 'filled',
        'fillcolor': 'gray',
    },
    'individual': {
        'shape': 'diamond',
        'style': 'filled',
        'fillcolor': '#874b82',
        'fontcolor': 'white',
    },
    'object_property': {
        'shape': 'box',
        'style': 'filled',
        'fillcolor': '#0079ba',
        'fontcolor': 'white',
    },
    'data_property': {
        'shape': 'box',
        'style': 'filled',
        'fillcolor': 'green',
    },
    'annotation_property': {
        'shape': 'box',
        'style': 'filled',
        'fillcolor': 'orange',
    },
    'parent_node': {
        'style': 'filled',
        'fillcolor': 'lightgray',
    },
    'added_node': {
        'color': 'red',
    },
    'isA': {'arrowhead': 'empty'},
    'not': {'color': 'gray', 'style': 'dotted'},
    'equivalent_to': {'color': 'green3'},
    'disjoint_with': {'color': 'red', 'constraint': 'false'},
    'inverse_of': {'color': 'orange', },
    'default_relation': {'color': 'olivedrab', 'constraint': 'false'},
    'relations': {
        'disconnected': {'color': 'red', 'style': 'dotted',
                         'arrowhead': 'odot'},
        'hasPart': {'color': 'blue'},
        'hasProperPart': {'color': 'blue', 'style': 'dashed'},
        'hasParticipant': {'color': 'red'},
        'hasProperParticipant': {'color': 'red', 'style': 'dashed'},
        'hasSpatialPart': {'color': 'darkgreen'},
        'hasSpatialDirectPart': {'color': 'darkgreen', 'style': 'dashed'},
        'hasTemporalPart': {'color': 'magenta'},
        'hasTemporalDirectPart': {'color': 'magenta', 'style': 'dashed'},
        'hasReferenceUnit': {'color': 'darkgreen', 'style': 'dashed'},
        'hasSign': {'color': 'orange'},
        'hasConvention': {'color': 'orange', 'style': 'dashed'},
        'hasProperty': {'color': 'orange', 'style': 'dotted'},
    },
    'inverse': {'arrowhead': 'inv'},
    'default_dataprop': {'color': 'green', 'constraint': 'false'},
    'node': {},
    'edge': {},
}


def cytoscape_style(style=None):
    if not style:
        style = _default_style
    colours = {}
    styles = {}
    fill = {}
    for d in style.keys():
        if isinstance(style[d], dict):
            if 'color' in style[d].keys():
                colours[d] = style[d]['color']
            else:
                colours[d] = 'black'
            if 'style' in style[d].keys():
                styles[d] = style[d]['style']
            else:
                styles[d] = 'solid'
            if 'arrowhead' in style[d].keys():
                if style[d]['arrowhead'] == 'empty':
                    fill[d] = 'hollow'
            else:
                fill[d] = 'filled'

    for d in style['relations'].keys():
        if isinstance(style['relations'][d], dict):
            if 'color' in style['relations'][d].keys():
                colours[d] = style['relations'][d]['color']
            else:
                colours[d] = 'black'
            if 'style' in style['relations'][d].keys():
                styles[d] = style['relations'][d]['style']
            else:
                styles[d] = 'solid'
            if 'arrowhead' in style['relations'][d].keys():
                if style['relations'][d]['arrowhead'] == 'empty':
                    fill[d] = 'hollow'
            else:
                fill[d] = 'filled'
    return [colours, styles, fill]


class OntoGraph:
    """Class for visualising an ontology.

    Parameters
    ----------
    ontology : ontopy.Ontology instance
        Ontology to visualize.
    root : None | graph.ALL | string | owlready2.ThingClass instance
        Name or owlready2 entity of root node to plot subgraph
        below.  If `root` is `graph.ALL`, all classes will be included
        in the subgraph.
    leafs : None | sequence
        A sequence of leaf node names for generating sub-graphs.
    entities : None | sequence
        A sequence of entities to add to the graph.
    relations : "all" | str | None | sequence
        Sequence of relations to visualise.  If "all", means to include
        all relations.
    style : None | dict | "default"
        A dict mapping the name of the different graphical elements
        to dicts of dot graph attributes. Supported graphical elements
        include:
          - graphtype : "Digraph" | "Graph"
          - graph : graph attributes (G)
          - class : nodes for classes (N)
          - root : additional attributes for root nodes (N)
          - leaf : additional attributes for leaf nodes (N)
          - defined_class : nodes for defined classes (N)
          - class_construct : nodes for class constructs (N)
          - individual : nodes for invididuals (N)
          - object_property : nodes for object properties (N)
          - data_property : nodes for data properties (N)
          - annotation_property : nodes for annotation properties (N)
          - added_node : nodes added because `addnodes` is true (N)
          - isA : edges for isA relations (E)
          - not : edges for not class constructs (E)
          - equivalent_to : edges for equivalent_to relations (E)
          - disjoint_with : edges for disjoint_with relations (E)
          - inverse_of : edges for inverse_of relations (E)
          - default_relation : default edges relations and restrictions (E)
          - relations : dict of styles for different relations (E)
          - inverse : default edges for inverse relations (E)
          - default_dataprop : default edges for data properties (E)
          - nodes : attribute for individual nodes (N)
          - edges : attribute for individual edges (E)
        If style is None or "default", the default style is used.
        See https://www.graphviz.org/doc/info/attrs.html
    edgelabels : bool | dict
        Whether to add labels to the edges of the generated graph.
        It is also possible to provide a dict mapping the
        full labels (with cardinality stripped off for restrictions)
        to some abbriviations.
    addnodes : bool
        Whether to add missing target nodes in relations.
    addconstructs : bool
        Whether to add nodes representing class constructs.
    included_namespaces : sequence
        In combination with `root`, only include classes with one of
        the listed namespaces.  If empty (the default), nothing is
        excluded.
    included_ontologies : sequence
        In combination with `root`, only include classes defined in
        one of the listed ontologies.  If empty (default), nothing is
        excluded.
    parents : int
        Include `parents` levels of parents.
    excluded_nodes : None | sequence
        Sequence of labels of nodes to exclude.
    graph : None | pydot.Dot instance
        Graphviz Digraph object to plot into.  If None, a new graph object
        is created using the keyword arguments.
    imported : bool
        Whether to include imported classes if `entities` is None.
    kwargs :
        Passed to graphviz.Digraph.
    """

    def __init__(self, ontology, root=None, leafs=None, entities=None,
                 relations='isA', style=None, edgelabels=True,
                 addnodes=False, addconstructs=False,
                 included_namespaces=(), included_ontologies=(),
                 parents=0, excluded_nodes=None, graph=None,
                 imported=False, **kwargs):
        if style is None or style == 'default':
            style = _default_style

        if graph is None:
            graphtype = style.get('graphtype', 'Digraph')
            dotcls = getattr(graphviz, graphtype)
            graph_attr = kwargs.pop('graph_attr', {})
            for k, v in style.get('graph', {}).items():
                graph_attr.setdefault(k, v)
            self.dot = dotcls(graph_attr=graph_attr, **kwargs)
            self.nodes = set()
            self.edges = set()
        else:
            if ontology != graph.ontology:
                ValueError(
                    'the same ontology must be used when extending a graph')
            self.dot = graph.dot.copy()
            self.nodes = graph.nodes.copy()
            self.edges = graph.edges.copy()

        self.ontology = ontology
        self.relations = set(
            [relations] if isinstance(relations, str) else relations)
        self.style = style
        self.edgelabels = edgelabels
        self.addnodes = addnodes
        self.addconstructs = addconstructs
        self.excluded_nodes = set(excluded_nodes) if excluded_nodes else set()
        self.imported = imported

        if root == ALL:
            self.add_entities(
                relations=relations, edgelabels=edgelabels,
                addnodes=addnodes, addconstructs=addconstructs)
        elif root:
            self.add_branch(
                root, leafs,
                relations=relations, edgelabels=edgelabels,
                addnodes=addnodes, addconstructs=addconstructs,
                included_namespaces=included_namespaces,
                included_ontologies=included_ontologies,
            )
            if parents:
                self.add_parents(
                    root, levels=parents,
                    relations=relations, edgelabels=edgelabels,
                    addnodes=addnodes, addconstructs=addconstructs,
                )

        if entities:
            self.add_entities(entities=entities, relations=relations,
                              edgelabels=edgelabels, addnodes=addnodes,
                              addconstructs=addconstructs)

    def add_entities(self, entities=None, relations='isA', edgelabels=True,
                     addnodes=False, addconstructs=False,
                     nodeattrs=None, **attrs):
        """Adds a sequence of entities to the graph.  If `entities` is None,
        all classes are added to the graph.

        `nodeattrs` is a dict mapping node names to are attributes for
        dedicated nodes.
        """
        if entities is None:
            entities = self.ontology.classes(imported=self.imported)
        self.add_nodes(entities, nodeattrs=nodeattrs, **attrs)
        self.add_edges(
            relations=relations, edgelabels=edgelabels,
            addnodes=addnodes, addconstructs=addconstructs, **attrs)

    def add_branch(self, root, leafs=None, include_leafs=True,
                   strict_leafs=False, exclude=None, relations='isA',
                   edgelabels=True, addnodes=False, addconstructs=False,
                   included_namespaces=(), included_ontologies=(),
                   include_parents='closest', **attrs):
        """Adds branch under `root` ending at any entiry included in the
        sequence `leafs`.  If `include_leafs` is true, leafs classes are
        also included."""
        if leafs is None:
            leafs = ()

        classes = self.ontology.get_branch(
            root=root, leafs=leafs, include_leafs=include_leafs,
            strict_leafs=strict_leafs, exclude=exclude)

        classes = filter_classes(
            classes,
            included_namespaces=included_namespaces,
            included_ontologies=included_ontologies)

        nodeattrs = {}
        nodeattrs[get_label(root)] = self.style.get('root', {})
        for leaf in leafs:
            nodeattrs[get_label(leaf)] = self.style.get('leaf', {})

        self.add_entities(
            entities=classes,
            relations=relations, edgelabels=edgelabels,
            addnodes=addnodes, addconstructs=addconstructs,
            nodeattrs=nodeattrs, **attrs)

        parents = self.ontology.get_ancestors(classes, include=include_parents,
                                              strict=True)
        if parents:
            for parent in parents:
                nodeattrs[
                        get_label(parent)] = self.style.get('parent_node', {})
            self.add_entities(
                entities=parents,
                relations=relations, edgelabels=edgelabels,
                addnodes=addnodes, addconstructs=addconstructs,
                nodeattrs=nodeattrs, **attrs)

    def add_parents(self, name, levels=1, relations='isA',
                    edgelabels=None, addnodes=False, addconstructs=False,
                    **attrs):
        """Add `levels` levels of strict parents of entity `name`."""
        def addparents(e, n, s):
            if n > 0:
                for p in e.get_parents(strict=True):
                    s.add(p)
                    addparents(p, n - 1, s)
        e = self.ontology[name] if isinstance(name, str) else name
        parents = set()
        addparents(e, levels, parents)
        self.add_entities(
            entities=parents,
            relations=relations, edgelabels=edgelabels,
            addnodes=addnodes, addconstructs=addconstructs, **attrs)

    def add_node(self, name, nodeattrs=None, **attrs):
        """Add node with given name. `attrs` are graphviz node attributes."""
        e = self.ontology[name] if isinstance(name, str) else name
        label = get_label(e)
        if label not in self.nodes.union(self.excluded_nodes):
            kw = self.get_node_attrs(e, nodeattrs=nodeattrs, attrs=attrs)
            if hasattr(e, 'iri'):
                kw.setdefault('URL', e.iri)
            self.dot.node(label, label=label, **kw)
            self.nodes.add(label)

    def add_nodes(self, names, nodeattrs, **attrs):
        """Add nodes with given names. `attrs` are graphviz node attributes."""
        for name in names:
            self.add_node(name, nodeattrs=nodeattrs, **attrs)

    def add_edge(self, subject, predicate, object, edgelabel=None, **attrs):
        """Add edge corresponding for ``(subject, predicate, object)``
        triplet."""
        subject = subject if isinstance(subject, str) else get_label(subject)
        predicate = predicate if isinstance(predicate, str) else get_label(
            predicate)
        object = object if isinstance(object, str) else get_label(object)
        if subject in self.excluded_nodes or object in self.excluded_nodes:
            return
        if not isinstance(subject, str) or not isinstance(object, str):
            raise TypeError('`subject` and `object` must be strings')
        if subject not in self.nodes:
            raise RuntimeError('`subject` "%s" must have been added' % subject)
        if object not in self.nodes:
            raise RuntimeError('`object` "%s" must have been added' % object)
        key = (subject, predicate, object)
        if key not in self.edges:
            if edgelabel is None:
                edgelabel = self.edgelabels

            if isinstance(edgelabel, str):
                label = edgelabel
            if isinstance(edgelabel, dict):
                label = edgelabel.get(predicate, predicate)
            elif edgelabel:
                label = predicate
            else:
                label = None

            kw = self.get_edge_attrs(predicate, attrs=attrs)
            self.dot.edge(subject, object, label=label, **kw)
            self.edges.add(key)

    def add_source_edges(self, source, relations=None, edgelabels=None,
                         addnodes=None, addconstructs=None, **attrs):
        """Adds all relations originating from entity `source` who's type
        are listed in `relations`."""
        if relations is None:
            relations = self.relations
        elif isinstance(relations, str):
            relations = set([relations])
        else:
            relations = set(relations)

        edgelabels = self.edgelabels if edgelabels is None else edgelabels
        addconstructs = (
            self.addconstructs if addconstructs is None else addconstructs)

        e = self.ontology[source] if isinstance(source, str) else source
        label = get_label(e)
        for r in e.is_a:

            # isA
            if isinstance(r, (owlready2.ThingClass,
                              owlready2.ObjectPropertyClass)):
                if 'all' in relations or 'isA' in relations:
                    rlabel = get_label(r)
                    # FIXME - we actually want to include individuals...
                    if isinstance(e, owlready2.Thing):
                        continue
                    if r not in e.get_parents(strict=True):
                        continue
                    if not self.add_missing_node(r, addnodes=addnodes):
                        continue
                    self.add_edge(
                        subject=label, predicate='isA', object=rlabel,
                        edgelabel=edgelabels, **attrs)

            # restriction
            elif isinstance(r, owlready2.Restriction):
                rname = get_label(r.property)
                if 'all' in relations or rname in relations:
                    rlabel = '%s %s' % (rname, typenames[r.type])
                    if isinstance(r.value, owlready2.ThingClass):
                        obj = get_label(r.value)
                        if not self.add_missing_node(r.value, addnodes):
                            continue
                    elif (isinstance(r.value, owlready2.ClassConstruct) and
                          self.addconstructs):
                        obj = self.add_class_construct(r.value)
                    else:
                        continue
                    pred = asstring(r, exclude_object=True)
                    self.add_edge(label, pred, obj, edgelabel=edgelabels,
                                  **attrs)

            # inverse
            if isinstance(r, owlready2.Inverse):
                if 'all' in relations or 'inverse' in relations:
                    rlabel = get_label(r)
                    if not self.add_missing_node(r, addnodes=addnodes):
                        continue
                    if r not in e.get_parents(strict=True):
                        continue
                    self.add_edge(
                        subject=label, predicate='inverse', object=rlabel,
                        edgelabel=edgelabels, **attrs)

    def add_edges(self, sources=None, relations=None, edgelabels=None,
                  addnodes=None, addconstructs=None, **attrs):
        """Adds all relations originating from entities `sources` who's type
        are listed in `relations`.  If `sources` is None, edges are added
        between all current nodes."""
        if sources is None:
            sources = self.nodes
        for source in sources.copy():
            self.add_source_edges(
                source, relations=relations, edgelabels=edgelabels,
                addnodes=addnodes, addconstructs=addconstructs, **attrs)

    def add_missing_node(self, name, addnodes=None):
        """Checks if `name` corresponds to a missing node and add it if
        `addnodes` is true.

        Returns true if the node exists or is added, false otherwise."""
        addnodes = self.addnodes if addnodes is None else addnodes
        e = self.ontology[name] if isinstance(name, str) else name
        label = get_label(e)
        if label not in self.nodes:
            if addnodes:
                self.add_node(e, **self.style.get('added_node', {}))
            else:
                return False
        return True

    def add_class_construct(self, c):
        """Adds class construct `c` and return its label."""
        self.add_node(c, **self.style.get('class_construct', {}))
        label = get_label(c)
        if isinstance(c, owlready2.Or):
            for cls in c.Classes:
                clslabel = get_label(cls)
                if clslabel not in self.nodes and self.addnodes:
                    self.add_node(cls)
                if clslabel in self.nodes:
                    self.add_edge(get_label(cls), 'isA', label)
        elif isinstance(c, owlready2.And):
            for cls in c.Classes:
                clslabel = get_label(cls)
                if clslabel not in self.nodes and self.addnodes:
                    self.add_node(cls)
                if clslabel in self.nodes:
                    self.add_edge(label, 'isA', get_label(cls))
        elif isinstance(c, owlready2.Not):
            clslabel = get_label(c.Class)
            if clslabel not in self.nodes and self.addnodes:
                self.add_node(c.Class)
            if clslabel in self.nodes:
                self.add_edge(clslabel, 'not', label)
        # Neither and nor inverse constructs are
        return label

    def get_node_attrs(self, name, nodeattrs, attrs):
        """Returns attributes for node or edge `name`.  `attrs` overrides
        the default style."""
        e = self.ontology[name] if isinstance(name, str) else name
        label = get_label(e)
        # class
        if isinstance(e, owlready2.ThingClass):
            if self.ontology.is_defined(e):
                kw = self.style.get('defined_class', {})
            else:
                kw = self.style.get('class', {})
        # class construct
        elif isinstance(e, owlready2.ClassConstruct):
            kw = self.style.get('class_construct', {})
        # individual
        elif isinstance(e, owlready2.Thing):
            kw = self.style.get('individual', {})
        # object property
        elif isinstance(e, owlready2.ObjectPropertyClass):
            kw = self.style.get('object_property', {})
        # data property
        elif isinstance(e, owlready2.DataPropertyClass):
            kw = self.style.get('data_property', {})
        # annotation property
        elif isinstance(e, owlready2.AnnotationPropertyClass):
            kw = self.style.get('annotation_property', {})
        else:
            raise TypeError('Unknown entity type: %r' % e)
        kw = kw.copy()
        kw.update(self.style.get('nodes', {}).get(label, {}))
        if nodeattrs:
            kw.update(nodeattrs.get(label, {}))
        kw.update(attrs)
        return kw

    def get_edge_attrs(self, predicate, attrs):
        """Returns attributes for node or edge `name`.  `attrs` overrides
        the default style."""
        # given type
        types = ('isA', 'equivalent_to', 'disjoint_with', 'inverse_of')
        if predicate in types:
            kw = self.style.get(predicate, {}).copy()
        else:
            kw = {}
            name = predicate.split(None, 1)[0]
            m = re.match(r'Inverse\((.*)\)', name)
            if m:
                name, = m.groups()
                attrs = attrs.copy()
                for k, v in self.style.get('inverse', {}).items():
                    attrs.setdefault(k, v)
            if not isinstance(name, str) or name in self.ontology:
                e = self.ontology[name] if isinstance(name, str) else name
                relations = self.style.get('relations', {})
                rels = set(self.ontology[r] for r in relations.keys()
                           if r in self.ontology)
                for r in e.mro():
                    if r in rels:
                        break
                rattrs = relations[get_label(r)] if r in rels else {}
                # object property
                if isinstance(e, (owlready2.ObjectPropertyClass,
                                  owlready2.ObjectProperty)):
                    kw = self.style.get('default_relation', {}).copy()
                    kw.update(rattrs)
                # data property
                elif isinstance(e, (owlready2.DataPropertyClass,
                                    owlready2.DataProperty)):
                    kw = self.style.get('default_dataprop', {}).copy()
                    kw.update(rattrs)
                else:
                    raise TypeError('Unknown entity type: %r' % e)
        kw.update(self.style.get('edges', {}).get(predicate, {}))
        kw.update(attrs)
        return kw

    def add_legend(self, relations=None):
        """Adds legend for specified relations to the graph.

        If `relations` is "all", the legend will contain all relations
        that are defined in the style.  By default the legend will
        only contain relations that are currently included in the
        graph.

        Hence, you usually want to call add_legend() as the last method
        before saving or displaying.
        """
        rels = self.style.get('relations', {})
        if relations is None:
            relations = self.get_relations(sort=True)
        elif relations == 'all':
            relations = ['isA'] + list(rels.keys()) + ['inverse']
        elif isinstance(relations, str):
            relations = relations.split(',')

        n = len(relations)
        if n == 0:
            return

        t = ('<<table border="0" cellpadding="2" cellspacing="0" '
             'cellborder="0">')
        label1 = [t]
        label2 = [t]
        for i, r in enumerate(relations):
            label1.append(
                '<tr><td align="right" port="i%d">%s</td></tr>' % (i, r))
            label2.append('<tr><td port="i%d">&nbsp;</td></tr>' % i)
        label1.append('</table>>')
        label2.append('</table>>')
        self.dot.node('key1', label='\n'.join(label1), shape='plaintext')
        self.dot.node('key2', label='\n'.join(label2), shape='plaintext')

        rankdir = self.dot.graph_attr.get('rankdir', 'TB')
        constraint = 'false' if rankdir in ('TB', 'BT') else 'true'
        inv = True if rankdir in ('BT', ) else False

        for i in range(n):
            r = relations[n - 1 - i] if inv else relations[i]
            if r == 'inverse':
                kw = self.style.get('inverse', {}).copy()
            else:
                kw = self.get_edge_attrs(r, {}).copy()
            kw['constraint'] = constraint
            with self.dot.subgraph(name='sub%d' % i) as s:
                s.attr(rank='same')
                if rankdir in ('BT', 'LR'):
                    self.dot.edge('key1:i%d:e' % i, 'key2:i%d:w' % i, **kw)
                else:
                    self.dot.edge('key2:i%d:w' % i, 'key1:i%d:e' % i, **kw)

    def get_relations(self, sort=True):
        """Returns a set of relations in current graph.  If `sort` is true,
        a sorted list is returned."""
        relations = set()
        for s, p, o in self.edges:
            if p.startswith('Inverse'):
                relations.add('inverse')
                m = re.match(r'Inverse\((.+)\)', p)
                assert m
                relations.add(m.groups()[0])
            else:
                relations.add(p.split(None, 1)[0])

        # Sort, but place 'isA' first and 'inverse' last
        if sort:
            start, end = [], []
            if 'isA' in relations:
                relations.remove('isA')
                start.append('isA')
            if 'inverse' in relations:
                relations.remove('inverse')
                end.append('inverse')
            relations = start + sorted(relations) + end

        return relations

    def save(self, filename, format=None, **kwargs):
        """Saves graph to `filename`.  If format is not given, it is
        inferred from `filename`."""
        base, ext = os.path.splitext(filename)
        if format is None:
            format = ext.lstrip('.')
        kwargs.setdefault('cleanup', True)
        if format in ('graphviz', 'gv'):
            if 'dictionary' in kwargs:
                self.dot.save(filename, dictionary=kwargs['dictionary'])
            else:
                self.dot.save(filename)
        else:
            self.dot.render(base, format=format, **kwargs)

    def view(self):
        """Shows the graph in a viewer."""
        self.dot.view(cleanup=True)

    def get_figsize(self):
        """Returns the default figure size (width, height) in points."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = os.path.join(tmpdir, 'graph.svg')
            self.save(tmpfile)
            xml = ET.parse(tmpfile)
            svg = xml.getroot()
            width = svg.attrib['width']
            height = svg.attrib['height']
            assert width.endswith('pt')  # ensure that units are in points

            def asfloat(s):
                return float(re.match(r'^[\d.]+', s).group())
        return asfloat(width), asfloat(height)


def filter_classes(classes, included_namespaces=(), included_ontologies=()):
    """Filter out classes whos namespace is not in `included_namespaces`
    or whos ontology name is not in one of the ontologies in
    `included_ontologies`.

    `classes` should be a sequence of classes.
    """
    filtered = set(classes)
    if included_namespaces:
        filtered = set(c for c in filtered
                       if c.namespace.name in included_namespaces)
    if included_ontologies:
        filtered = set(c for c in filtered
                       if c.namespace.ontology.name in included_ontologies)
    return filtered


def get_module_dependencies(iri_or_onto, strip_base=None):
    """Reads `iri_or_onto` and returns a dict mapping ontology names to a
    list of ontologies that they depends on.

    If `strip_base` is true, the base IRI is stripped from ontology
    names.  If it is a string, it lstrip'ped from the base iri.
    """
    if isinstance(iri_or_onto, str):
        onto = get_ontology(iri_or_onto)
        onto.load()
    else:
        onto = iri_or_onto

    modules = {onto.base_iri: set()}

    def strip(base_iri):
        if isinstance(strip_base, str):
            return base_iri.lstrip(strip_base)
        elif strip_base:
            return base_iri.strip(onto.base_iri)
        else:
            return base_iri

    visited = set()

    def setmodules(onto):
        for o in onto.imported_ontologies:
            if onto.base_iri in modules:
                modules[strip(onto.base_iri)].add(strip(o.base_iri))
            else:
                modules[strip(onto.base_iri)] = set([strip(o.base_iri)])
            if o.base_iri not in modules:
                modules[strip(o.base_iri)] = set()
            if o not in visited:
                visited.add(o)
                setmodules(o)

    setmodules(onto)
    return modules


def plot_modules(src, filename=None, format=None, show=False,
                 strip_base=None, ignore_redundant=True):
    """Plot module dependency graph for `src` and return a graph object.

    Here `src` may be an IRI, a path the the ontology or a dict returned by
    get_module_dependencies().

    If `filename` is given, write the graph to this file.

    If `format` is None, the output format is inferred from `filename`.

    If `show` is true, the graph is displayed.

    `strip_base` is passed on to get_module_dependencies() if `src` is not
    a dict.

    If `ignore_redundant` is true, redundant dependencies are not plotted.
    """
    if isinstance(src, dict):
        modules = src
    else:
        modules = get_module_dependencies(src, strip_base=strip_base)

    if ignore_redundant:
        modules = check_module_dependencies(modules, verbose=False)

    dot = graphviz.Digraph(comment='Module dependencies')
    dot.attr(rankdir='TB')
    dot.node_attr.update(style='filled', fillcolor='lightblue', shape='box',
                         edgecolor='blue')
    dot.edge_attr.update(arrowtail='open', dir='back')

    for iri in modules.keys():
        iriname = iri.split(':', 1)[1]
        dot.node(iriname, label=iri, URL=iri)

    for iri, deps in modules.items():
        for dep in deps:
            iriname = iri.split(':', 1)[1]
            depname = dep.split(':', 1)[1]
            dot.edge(depname, iriname)

    if filename:
        base, ext = os.path.splitext(filename)
        if format is None:
            format = ext.lstrip('.')
        dot.render(base, format=format, view=False, cleanup=True)

    if show:
        dot.view(cleanup=True)

    return dot


def check_module_dependencies(modules, verbose=True):
    """Check module dependencies and return a copy of modules with
    redundant dependencies removed.

    If `verbose` is true, warnings are printed for each module that

    If `modules` is given, it should be a dict returned by
    get_module_dependencies().
    """
    visited = set()

    def get_deps(iri, excl=None):
        """Returns a set with all dependencies of `iri`, excluding `excl` and
        its dependencies."""
        if iri in visited:
            return set()
        visited.add(iri)
        deps = set()
        for d in modules[iri]:
            if d != excl:
                deps.add(d)
                deps.update(get_deps(d))
        return deps

    mods = {}
    redundant = []
    for iri, deps in modules.items():
        if not deps:
            mods[iri] = set()
        for dep in deps:
            if dep in get_deps(iri, dep):
                redundant.append((iri, dep))
            elif iri in mods:
                mods[iri].add(dep)
            else:
                mods[iri] = set([dep])

    if redundant and verbose:
        print('** Warning: Redundant module dependency:')
        for iri, dep in redundant:
            print('%s -> %s' % (iri, dep))

    return mods


def cytoscapegraph(graph, onto=None, infobox=None, style=None):
    """Returns and instance of icytoscape-figure for an
    instance Graph of OntoGraph, the accomanying ontology
    is required for mouse actions"""

    from ipywidgets import Output, VBox, GridspecLayout
    from IPython.display import display, Image
    from pathlib import Path
    import networkx as nx
    import pydotplus
    import ipycytoscape
    from networkx.readwrite.json_graph import cytoscape_data
    # Define the styles, this has to be aligned with the graphviz values
    dotplus = pydotplus.graph_from_dot_data(graph.dot.source)
    # if graph doesn't have multiedges, use dotplus.set_strict(true)
    G = nx.nx_pydot.from_pydot(dotplus)

    colours, styles, fill = cytoscape_style()

    data = cytoscape_data(G)['elements']
    for d in data['edges']:
        d['data']['label'] = d['data']['label'].rsplit(' ', 1)[0].lstrip('"')
        lab = d['data']['label'].replace('Inverse(', '').rstrip(')')
        try:
            d['data']['colour'] = colours[lab]
        except KeyError:
            d['data']['colour'] = 'black'
        try:
            d['data']['style'] = styles[lab]
        except KeyError:
            d['data']['style'] = 'solid'
        if d['data']['label'].startswith('Inverse('):
            d['data']['targetarrow'] = 'diamond'
            d['data']['sourcearrow'] = 'none'
        else:
            d['data']['targetarrow'] = 'triangle'
            d['data']['sourcearrow'] = 'none'
        try:
            d['data']['fill'] = fill[lab]
        except KeyError:
            d['data']['fill'] = 'filled'

    cytofig = ipycytoscape.CytoscapeWidget()
    cytofig.graph.add_graph_from_json(data, directed=True)

    cytofig.set_style([
        {
            'selector': 'node',
            'css': {
                'content': 'data(label)',
                # 'text-valign': 'center',
                # 'color': 'white',
                # 'text-outline-width': 2,
                # 'text-outline-color': 'red',
                'background-color': 'blue'
            },
        },
        {
            'selector': 'node:parent',
            'css': {'background-opacity': 0.333}
        },
        {
            'selector': 'edge',
            'style': {'width': 2,
                      'line-color': 'data(colour)',
                      # 'content': 'data(label)',
                      'line-style': 'data(style)'}
        },
        {
            'selector': 'edge.directed',
            'style': {
                'curve-style': 'bezier',
                'target-arrow-shape': 'data(targetarrow)',
                'target-arrow-color': 'data(colour)',
                'target-arrow-fill': 'data(fill)',
                'mid-source-arrow-shape': 'data(sourcearrow)',
                'mid-source-arrow-color': 'data(colour)'
            },
        },
        {
            'selector': 'edge.multiple_edges',
            'style': {'curve-style': 'bezier'}
        },
        {
            'selector': ':selected',
            'css': {
                'background-color': 'black',
                'line-color': 'black',
                'target-arrow-color': 'black',
                'source-arrow-color': 'black',
                'text-outline-color': 'black'
            },
        },
    ])

    if onto is not None:
        out = Output(layout={'border': '1px solid black'})

        def log_clicks(node):
            with out:
                print((onto.get_by_label(node["data"]["label"])))
                p = onto.get_by_label(node["data"]["label"]).get_parents()
                print(f'parents: {p}')
                try:
                    elucidation = onto.get_by_label(
                        node["data"]["label"]).elucidation
                    print(f'elucidation: {elucidation[0]}')
                except (AttributeError, IndexError):
                    pass

                try:
                    annotations = onto.get_by_label(
                        node["data"]["label"]).annotations
                    for e in annotations:
                        print(f'annotation: {e}')
                except AttributeError:
                    pass

                # Try does not work...
                try:
                    iri = onto.get_by_label(
                            node["data"]["label"]).iri
                    print(f'iri: {iri}')
                except Exception:
                    pass
                try:
                    fig = node["data"]["label"]
                    if os.path.exists(Path(fig+'.png')):
                        display(Image(fig+'.png', width=100))
                    elif os.path.exists(Path(fig+'.jpg')):
                        display(Image(fig+'.jpg', width=100))
                except Exception:  # FIXME: make this more specific
                    pass
                out.clear_output(wait=True)

        def log_mouseovers(node):
            with out:
                print(onto.get_by_label(node["data"]["label"]))
                # print(f'mouseover: {pformat(node)}')
            out.clear_output(wait=True)

        cytofig.on('node', 'click', log_clicks)
        cytofig.on('node', 'mouseover', log_mouseovers)  # , remove=True)
        cytofig.on('node', 'mouseout', out.clear_output(wait=True))
        grid = GridspecLayout(1, 3, height='400px')
        if infobox == 'left':
            grid[0, 0] = out
            grid[0, 1:] = cytofig
        elif infobox == 'right':
            grid[0, 0:-1] = cytofig
            grid[0, 2] = out
        else:
            return VBox([cytofig, out])
        return grid

    return cytofig
