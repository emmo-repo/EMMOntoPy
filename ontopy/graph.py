# -*- coding: utf-8 -*-
"""
A module for visualising ontologies using graphviz.
"""
# pylint: disable=fixme,too-many-lines
import os
import re
import tempfile
import warnings
from typing import Optional, TYPE_CHECKING
import defusedxml.ElementTree as ET
import owlready2
import graphviz

from ontopy.utils import asstring, get_label
from ontopy.ontology import Ontology
from ontopy.utils import EMMOntoPyException

if TYPE_CHECKING:
    from ipywidgets.widgets.widget_templates import GridspecLayout


typenames = (
    owlready2.class_construct._restriction_type_2_label  # pylint: disable=protected-access
)


# Literal for `root` arguments
ALL = 1

_default_style = {
    "graphtype": "Digraph",
    "graph": {
        "rankdir": "BT",
        "fontsize": "8",
        # 'fontname': 'Bitstream Vera Sans', 'splines': 'ortho',
    },
    "class": {
        "style": "filled",
        "fillcolor": "#ffffcc",
    },
    "root": {"penwidth": "2"},
    "leaf": {"penwidth": "2"},
    "defined_class": {
        "style": "filled",
        "fillcolor": "#ffc880",
    },
    "class_construct": {
        "style": "filled",
        "fillcolor": "gray",
    },
    "individual": {
        "shape": "diamond",
        "style": "filled",
        "fillcolor": "#874b82",
        "fontcolor": "white",
    },
    "object_property": {
        "shape": "box",
        "style": "filled",
        "fillcolor": "#0079ba",
        "fontcolor": "white",
    },
    "data_property": {
        "shape": "box",
        "style": "filled",
        "fillcolor": "green",
    },
    "annotation_property": {
        "shape": "box",
        "style": "filled",
        "fillcolor": "orange",
    },
    "parent_node": {
        "style": "filled",
        "fillcolor": "lightgray",
    },
    "added_node": {
        "color": "red",
    },
    "isA": {"arrowhead": "empty"},
    "not": {"color": "gray", "style": "dotted"},
    "equivalent_to": {"color": "green3"},
    "disjoint_with": {"color": "red", "constraint": "false"},
    "inverse_of": {
        "color": "orange",
    },
    "default_relation": {"color": "olivedrab", "constraint": "false"},
    "relations": {
        "disconnected": {
            "color": "red",
            "style": "dotted",
            "arrowhead": "odot",
        },
        "hasPart": {"color": "blue"},
        "hasProperPart": {"color": "blue", "style": "dashed"},
        "hasMember": {"color": "blue", "style": "dotted"},
        "hasParticipant": {"color": "red"},
        "hasProperParticipant": {"color": "red", "style": "dashed"},
        "hasSpatialPart": {"color": "darkgreen"},
        "hasSpatialDirectPart": {"color": "darkgreen", "style": "dashed"},
        "hasTemporalPart": {"color": "magenta"},
        "hasTemporalDirectPart": {"color": "magenta", "style": "dashed"},
        "hasReferenceUnit": {"color": "darkgreen", "style": "dashed"},
        "hasSign": {"color": "orange"},
        "hasConvention": {"color": "orange", "style": "dashed"},
        "hasProperty": {"color": "orange", "style": "dotted"},
    },
    "inverse": {"arrowhead": "inv"},
    "default_dataprop": {"color": "green", "constraint": "false"},
    "node": {},
    "edge": {},
}


def cytoscape_style(style=None):  # pylint: disable=too-many-branches
    """Get list of color, style and fills."""
    if not style:
        style = _default_style
    colours = {}
    styles = {}
    fill = {}
    for key, value in style.items():
        if isinstance(value, dict):
            if "color" in value:
                colours[key] = value["color"]
            else:
                colours[key] = "black"
            if "style" in value:
                styles[key] = value["style"]
            else:
                styles[key] = "solid"
            if "arrowhead" in value:
                if value["arrowhead"] == "empty":
                    fill[key] = "hollow"
            else:
                fill[key] = "filled"

    for key, value in style.get("relations", {}).items():
        if isinstance(value, dict):
            if "color" in value:
                colours[key] = value["color"]
            else:
                colours[key] = "black"
            if "style" in value:
                styles[key] = value["style"]
            else:
                styles[key] = "solid"
            if "arrowhead" in value:
                if value["arrowhead"] == "empty":
                    fill[key] = "hollow"
            else:
                fill[key] = "filled"
    return [colours, styles, fill]


class OntoGraph:  # pylint: disable=too-many-instance-attributes
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
    edgelabels : None | bool | dict
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

    def __init__(  # pylint: disable=too-many-arguments,too-many-locals
        self,
        ontology,
        root=None,
        leafs=None,
        entities=None,
        relations="isA",
        style=None,
        edgelabels=None,
        addnodes=False,
        addconstructs=False,
        included_namespaces=(),
        included_ontologies=(),
        parents=0,
        excluded_nodes=None,
        graph=None,
        imported=False,
        **kwargs,
    ):
        if style is None or style == "default":
            style = _default_style

        if graph is None:
            graphtype = style.get("graphtype", "Digraph")
            dotcls = getattr(graphviz, graphtype)
            graph_attr = kwargs.pop("graph_attr", {})
            for key, value in style.get("graph", {}).items():
                graph_attr.setdefault(key, value)
            self.dot = dotcls(graph_attr=graph_attr, **kwargs)
            self.nodes = set()
            self.edges = set()
        else:
            if ontology != graph.ontology:
                raise ValueError(
                    "the same ontology must be used when extending a graph"
                )
            self.dot = graph.dot.copy()
            self.nodes = graph.nodes.copy()
            self.edges = graph.edges.copy()

        self.ontology = ontology
        self.relations = set(
            [relations] if isinstance(relations, str) else relations
        )
        self.style = style
        self.edgelabels = edgelabels
        self.addnodes = addnodes
        self.addconstructs = addconstructs
        self.excluded_nodes = set(excluded_nodes) if excluded_nodes else set()
        self.imported = imported

        if root == ALL:
            self.add_entities(
                relations=relations,
                edgelabels=edgelabels,
                addnodes=addnodes,
                addconstructs=addconstructs,
            )
        elif root:
            self.add_branch(
                root,
                leafs,
                relations=relations,
                edgelabels=edgelabels,
                addnodes=addnodes,
                addconstructs=addconstructs,
                included_namespaces=included_namespaces,
                included_ontologies=included_ontologies,
            )
            if parents:
                self.add_parents(
                    root,
                    levels=parents,
                    relations=relations,
                    edgelabels=edgelabels,
                    addnodes=addnodes,
                    addconstructs=addconstructs,
                )

        if entities:
            self.add_entities(
                entities=entities,
                relations=relations,
                edgelabels=edgelabels,
                addnodes=addnodes,
                addconstructs=addconstructs,
            )

    def add_entities(  # pylint: disable=too-many-arguments
        self,
        entities=None,
        relations="isA",
        edgelabels=None,
        addnodes=False,
        addconstructs=False,
        nodeattrs=None,
        **attrs,
    ):
        """Adds a sequence of entities to the graph.  If `entities` is None,
        all classes are added to the graph.

        `nodeattrs` is a dict mapping node names to are attributes for
        dedicated nodes.
        """
        if entities is None:
            entities = self.ontology.classes(imported=self.imported)
        self.add_nodes(entities, nodeattrs=nodeattrs, **attrs)
        self.add_edges(
            relations=relations,
            edgelabels=edgelabels,
            addnodes=addnodes,
            addconstructs=addconstructs,
            **attrs,
        )

    def add_branch(  # pylint: disable=too-many-arguments,too-many-locals
        self,
        root,
        leafs=None,
        include_leafs=True,
        strict_leafs=False,
        exclude=None,
        relations="isA",
        edgelabels=None,
        addnodes=False,
        addconstructs=False,
        included_namespaces=(),
        included_ontologies=(),
        include_parents="closest",
        **attrs,
    ):
        """Adds branch under `root` ending at any entiry included in the
        sequence `leafs`.  If `include_leafs` is true, leafs classes are
        also included."""
        if leafs is None:
            leafs = ()

        classes = self.ontology.get_branch(
            root=root,
            leafs=leafs,
            include_leafs=include_leafs,
            strict_leafs=strict_leafs,
            exclude=exclude,
        )

        classes = filter_classes(
            classes,
            included_namespaces=included_namespaces,
            included_ontologies=included_ontologies,
        )

        nodeattrs = {}
        nodeattrs[get_label(root)] = self.style.get("root", {})
        for leaf in leafs:
            nodeattrs[get_label(leaf)] = self.style.get("leaf", {})

        self.add_entities(
            entities=classes,
            relations=relations,
            edgelabels=edgelabels,
            addnodes=addnodes,
            addconstructs=addconstructs,
            nodeattrs=nodeattrs,
            **attrs,
        )

        parents = self.ontology.get_ancestors(
            classes, include=include_parents, strict=True
        )
        if parents:
            for parent in parents:
                nodeattrs[get_label(parent)] = self.style.get("parent_node", {})
            self.add_entities(
                entities=parents,
                relations=relations,
                edgelabels=edgelabels,
                addnodes=addnodes,
                addconstructs=addconstructs,
                nodeattrs=nodeattrs,
                **attrs,
            )

    def add_parents(  # pylint: disable=too-many-arguments
        self,
        name,
        levels=1,
        relations="isA",
        edgelabels=None,
        addnodes=False,
        addconstructs=False,
        **attrs,
    ):
        """Add `levels` levels of strict parents of entity `name`."""

        def addparents(entity, nodes, parents):
            if nodes > 0:
                for parent in entity.get_parents(strict=True):
                    parents.add(parent)
                    addparents(parent, nodes - 1, parents)

        entity = self.ontology[name] if isinstance(name, str) else name
        parents = set()
        addparents(entity, levels, parents)
        self.add_entities(
            entities=parents,
            relations=relations,
            edgelabels=edgelabels,
            addnodes=addnodes,
            addconstructs=addconstructs,
            **attrs,
        )

    def add_node(self, name, nodeattrs=None, **attrs):
        """Add node with given name. `attrs` are graphviz node attributes."""
        entity = self.ontology[name] if isinstance(name, str) else name
        label = get_label(entity)
        if label not in self.nodes.union(self.excluded_nodes):
            kwargs = self.get_node_attrs(
                entity, nodeattrs=nodeattrs, attrs=attrs
            )
            if hasattr(entity, "iri"):
                kwargs.setdefault("URL", entity.iri)
            self.dot.node(label, label=label, **kwargs)
            self.nodes.add(label)

    def add_nodes(self, names, nodeattrs, **attrs):
        """Add nodes with given names. `attrs` are graphviz node attributes."""
        for name in names:
            self.add_node(name, nodeattrs=nodeattrs, **attrs)

    def add_edge(self, subject, predicate, obj, edgelabel=None, **attrs):
        """Add edge corresponding for ``(subject, predicate, object)``
        triplet."""
        subject = subject if isinstance(subject, str) else get_label(subject)
        predicate = (
            predicate if isinstance(predicate, str) else get_label(predicate)
        )
        obj = obj if isinstance(obj, str) else get_label(obj)
        if subject in self.excluded_nodes or obj in self.excluded_nodes:
            return
        if not isinstance(subject, str) or not isinstance(obj, str):
            raise TypeError("`subject` and `object` must be strings")
        if subject not in self.nodes:
            raise RuntimeError(f'`subject` "{subject}" must have been added')
        if obj not in self.nodes:
            raise RuntimeError(f'`object` "{obj}" must have been added')
        key = (subject, predicate, obj)
        if key not in self.edges:
            if edgelabel is None:
                edgelabel = self.edgelabels

            label = None
            if edgelabel is None:
                tokens = predicate.split()
                if len(tokens) == 2 and tokens[1] in ("some", "only"):
                    label = tokens[1]
                elif len(tokens) == 3 and tokens[1] in (
                    "exactly",
                    "min",
                    "max",
                ):
                    label = f"{tokens[1]} {tokens[2]}"
            elif isinstance(edgelabel, str):
                label = edgelabel
            elif isinstance(edgelabel, dict):
                label = edgelabel.get(predicate, predicate)
            elif edgelabel:
                label = predicate

            kwargs = self.get_edge_attrs(predicate, attrs=attrs)
            self.dot.edge(subject, obj, label=label, **kwargs)
            self.edges.add(key)

    def add_source_edges(  # pylint: disable=too-many-arguments,too-many-branches
        self,
        source,
        relations=None,
        edgelabels=None,
        addnodes=None,
        addconstructs=None,
        **attrs,
    ):
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
            self.addconstructs if addconstructs is None else addconstructs
        )

        entity = self.ontology[source] if isinstance(source, str) else source
        label = get_label(entity)
        for relation in entity.is_a:
            # isA
            if isinstance(
                relation, (owlready2.ThingClass, owlready2.ObjectPropertyClass)
            ):
                if "all" in relations or "isA" in relations:
                    rlabel = get_label(relation)
                    # FIXME - we actually want to include individuals...
                    if isinstance(entity, owlready2.Thing):
                        continue
                    if relation not in entity.get_parents(strict=True):
                        continue
                    if not self.add_missing_node(relation, addnodes=addnodes):
                        continue
                    self.add_edge(
                        subject=label,
                        predicate="isA",
                        obj=rlabel,
                        edgelabel=edgelabels,
                        **attrs,
                    )

            # restriction
            elif isinstance(relation, owlready2.Restriction):
                rname = get_label(relation.property)
                if "all" in relations or rname in relations:
                    rlabel = f"{rname} {typenames[relation.type]}"
                    if isinstance(relation.value, owlready2.ThingClass):
                        obj = get_label(relation.value)
                        if not self.add_missing_node(relation.value, addnodes):
                            continue
                    elif (
                        isinstance(relation.value, owlready2.ClassConstruct)
                        and self.addconstructs
                    ):
                        obj = self.add_class_construct(relation.value)
                    else:
                        continue
                    pred = asstring(relation, exclude_object=True)
                    self.add_edge(
                        label, pred, obj, edgelabel=edgelabels, **attrs
                    )

            # inverse
            if isinstance(relation, owlready2.Inverse):
                if "all" in relations or "inverse" in relations:
                    rlabel = get_label(relation)
                    if not self.add_missing_node(relation, addnodes=addnodes):
                        continue
                    if relation not in entity.get_parents(strict=True):
                        continue
                    self.add_edge(
                        subject=label,
                        predicate="inverse",
                        obj=rlabel,
                        edgelabel=edgelabels,
                        **attrs,
                    )

    def add_edges(  # pylint: disable=too-many-arguments
        self,
        sources=None,
        relations=None,
        edgelabels=None,
        addnodes=None,
        addconstructs=None,
        **attrs,
    ):
        """Adds all relations originating from entities `sources` who's type
        are listed in `relations`.  If `sources` is None, edges are added
        between all current nodes."""
        if sources is None:
            sources = self.nodes
        for source in sources.copy():
            self.add_source_edges(
                source,
                relations=relations,
                edgelabels=edgelabels,
                addnodes=addnodes,
                addconstructs=addconstructs,
                **attrs,
            )

    def add_missing_node(self, name, addnodes=None):
        """Checks if `name` corresponds to a missing node and add it if
        `addnodes` is true.

        Returns true if the node exists or is added, false otherwise."""
        addnodes = self.addnodes if addnodes is None else addnodes
        entity = self.ontology[name] if isinstance(name, str) else name
        label = get_label(entity)
        if label not in self.nodes:
            if addnodes:
                self.add_node(entity, **self.style.get("added_node", {}))
            else:
                return False
        return True

    def add_class_construct(self, construct):
        """Adds class construct and return its label."""
        self.add_node(construct, **self.style.get("class_construct", {}))
        label = get_label(construct)
        if isinstance(construct, owlready2.Or):
            for cls in construct.Classes:
                clslabel = get_label(cls)
                if clslabel not in self.nodes and self.addnodes:
                    self.add_node(cls)
                if clslabel in self.nodes:
                    self.add_edge(get_label(cls), "isA", label)
        elif isinstance(construct, owlready2.And):
            for cls in construct.Classes:
                clslabel = get_label(cls)
                if clslabel not in self.nodes and self.addnodes:
                    self.add_node(cls)
                if clslabel in self.nodes:
                    self.add_edge(label, "isA", get_label(cls))
        elif isinstance(construct, owlready2.Not):
            clslabel = get_label(construct.Class)
            if clslabel not in self.nodes and self.addnodes:
                self.add_node(construct.Class)
            if clslabel in self.nodes:
                self.add_edge(clslabel, "not", label)
        # Neither and nor inverse constructs are
        return label

    def get_node_attrs(self, name, nodeattrs, attrs):
        """Returns attributes for node or edge `name`.  `attrs` overrides
        the default style."""
        entity = self.ontology[name] if isinstance(name, str) else name
        label = get_label(entity)
        # class
        if isinstance(entity, owlready2.ThingClass):
            if self.ontology.is_defined(entity):
                kwargs = self.style.get("defined_class", {})
            else:
                kwargs = self.style.get("class", {})
        # class construct
        elif isinstance(entity, owlready2.ClassConstruct):
            kwargs = self.style.get("class_construct", {})
        # individual
        elif isinstance(entity, owlready2.Thing):
            kwargs = self.style.get("individual", {})
        # object property
        elif isinstance(entity, owlready2.ObjectPropertyClass):
            kwargs = self.style.get("object_property", {})
        # data property
        elif isinstance(entity, owlready2.DataPropertyClass):
            kwargs = self.style.get("data_property", {})
        # annotation property
        elif isinstance(entity, owlready2.AnnotationPropertyClass):
            kwargs = self.style.get("annotation_property", {})
        else:
            raise TypeError(f"Unknown entity type: {entity!r}")
        kwargs = kwargs.copy()
        kwargs.update(self.style.get("nodes", {}).get(label, {}))
        if nodeattrs:
            kwargs.update(nodeattrs.get(label, {}))
        kwargs.update(attrs)
        return kwargs

    def get_edge_attrs(self, predicate, attrs):
        """Returns attributes for node or edge `name`.  `attrs` overrides
        the default style."""
        # given type
        types = ("isA", "equivalent_to", "disjoint_with", "inverse_of")
        if predicate in types:
            kwargs = self.style.get(predicate, {}).copy()
        else:
            kwargs = {}
            name = predicate.split(None, 1)[0]
            match = re.match(r"Inverse\((.*)\)", name)
            if match:
                (name,) = match.groups()
                attrs = attrs.copy()
                for key, value in self.style.get("inverse", {}).items():
                    attrs.setdefault(key, value)
            if not isinstance(name, str) or name in self.ontology:
                entity = self.ontology[name] if isinstance(name, str) else name
                relations = self.style.get("relations", {})
                rels = set(
                    self.ontology[_] for _ in relations if _ in self.ontology
                )
                for relation in entity.mro():
                    if relation in rels:
                        rattrs = (
                            relations[get_label(relation)]
                            if relation in rels
                            else {}
                        )
                        break
                else:
                    warnings.warn(
                        f"Style not defined for relation {name}. "
                        "Resorting to default style."
                    )
                    rattrs = self.style.get("default_relation", {})
                # object property
                if isinstance(
                    entity,
                    (owlready2.ObjectPropertyClass, owlready2.ObjectProperty),
                ):
                    kwargs = self.style.get("default_relation", {}).copy()
                    kwargs.update(rattrs)
                # data property
                elif isinstance(
                    entity,
                    (owlready2.DataPropertyClass, owlready2.DataProperty),
                ):
                    kwargs = self.style.get("default_dataprop", {}).copy()
                    kwargs.update(rattrs)
                else:
                    raise TypeError(f"Unknown entity type: {entity!r}")
        kwargs.update(self.style.get("edges", {}).get(predicate, {}))
        kwargs.update(attrs)
        return kwargs

    def add_legend(self, relations=None):
        """Adds legend for specified relations to the graph.

        If `relations` is "all", the legend will contain all relations
        that are defined in the style.  By default the legend will
        only contain relations that are currently included in the
        graph.

        Hence, you usually want to call add_legend() as the last method
        before saving or displaying.
        """
        rels = self.style.get("relations", {})
        if relations is None:
            relations = self.get_relations(sort=True)
        elif relations == "all":
            relations = ["isA"] + list(rels.keys()) + ["inverse"]
        elif isinstance(relations, str):
            relations = relations.split(",")

        nrelations = len(relations)
        if nrelations == 0:
            return

        table = (
            '<<table border="0" cellpadding="2" cellspacing="0" cellborder="0">'
        )
        label1 = [table]
        label2 = [table]
        for index, relation in enumerate(relations):
            label1.append(
                f'<tr><td align="right" port="i{index}">{relation}</td></tr>'
            )
            label2.append(f'<tr><td port="i{index}">&nbsp;</td></tr>')
        label1.append("</table>>")
        label2.append("</table>>")
        self.dot.node("key1", label="\n".join(label1), shape="plaintext")
        self.dot.node("key2", label="\n".join(label2), shape="plaintext")

        rankdir = self.dot.graph_attr.get("rankdir", "TB")
        constraint = "false" if rankdir in ("TB", "BT") else "true"
        inv = rankdir in ("BT",)

        for index in range(nrelations):
            relation = (
                relations[nrelations - 1 - index] if inv else relations[index]
            )
            if relation == "inverse":
                kwargs = self.style.get("inverse", {}).copy()
            else:
                kwargs = self.get_edge_attrs(relation, {}).copy()
            kwargs["constraint"] = constraint
            with self.dot.subgraph(name=f"sub{index}") as subgraph:
                subgraph.attr(rank="same")
                if rankdir in ("BT", "LR"):
                    self.dot.edge(
                        f"key1:i{index}:e", f"key2:i{index}:w", **kwargs
                    )
                else:
                    self.dot.edge(
                        f"key2:i{index}:w", f"key1:i{index}:e", **kwargs
                    )

    def get_relations(self, sort=True):
        """Returns a set of relations in current graph.  If `sort` is true,
        a sorted list is returned."""
        relations = set()
        for _, predicate, _ in self.edges:
            if predicate.startswith("Inverse"):
                relations.add("inverse")
                match = re.match(r"Inverse\((.+)\)", predicate)
                if match is None:
                    raise ValueError(
                        "Could unexpectedly not find the inverse relation "
                        f"just added in: {predicate}"
                    )
                relations.add(match.groups()[0])
            else:
                relations.add(predicate.split(None, 1)[0])

        # Sort, but place 'isA' first and 'inverse' last
        if sort:
            start, end = [], []
            if "isA" in relations:
                relations.remove("isA")
                start.append("isA")
            if "inverse" in relations:
                relations.remove("inverse")
                end.append("inverse")
            relations = start + sorted(relations) + end

        return relations

    def save(self, filename, fmt=None, **kwargs):
        """Saves graph to `filename`.  If format is not given, it is
        inferred from `filename`."""
        base, ext = os.path.splitext(filename)
        if fmt is None:
            fmt = ext.lstrip(".")
        kwargs.setdefault("cleanup", True)
        if fmt in ("graphviz", "gv"):
            if "dictionary" in kwargs:
                self.dot.save(filename, dictionary=kwargs["dictionary"])
            else:
                self.dot.save(filename)
        else:
            fmt = kwargs.pop("format", fmt)
            self.dot.render(base, format=fmt, **kwargs)

    def view(self):
        """Shows the graph in a viewer."""
        self.dot.view(cleanup=True)

    def get_figsize(self):
        """Returns the default figure size (width, height) in points."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = os.path.join(tmpdir, "graph.svg")
            self.save(tmpfile)
            xml = ET.parse(tmpfile)
            svg = xml.getroot()
            width = svg.attrib["width"]
            height = svg.attrib["height"]
            if not width.endswith("pt"):
                # ensure that units are in points
                raise ValueError(
                    "The width attribute should always be given in 'pt', "
                    f"but it is: {width}"
                )

            def asfloat(string):
                return float(re.match(r"^[\d.]+", string).group())

        return asfloat(width), asfloat(height)


def filter_classes(classes, included_namespaces=(), included_ontologies=()):
    """Filter out classes whos namespace is not in `included_namespaces`
    or whos ontology name is not in one of the ontologies in
    `included_ontologies`.

    `classes` should be a sequence of classes.
    """
    filtered = set(classes)
    if included_namespaces:
        filtered = set(
            c for c in filtered if c.namespace.name in included_namespaces
        )
    if included_ontologies:
        filtered = set(
            c
            for c in filtered
            if c.namespace.ontology.name in included_ontologies
        )
    return filtered


def get_module_dependencies(iri_or_onto, strip_base=None):
    """Reads `iri_or_onto` and returns a dict mapping ontology names to a
    list of ontologies that they depends on.

    If `strip_base` is true, the base IRI is stripped from ontology
    names.  If it is a string, it lstrip'ped from the base iri.
    """
    from ontopy.ontology import (  # pylint: disable=import-outside-toplevel
        get_ontology,
    )

    if isinstance(iri_or_onto, str):
        onto = get_ontology(iri_or_onto)
        onto.load()
    else:
        onto = iri_or_onto

    modules = {onto.base_iri: set()}

    def strip(base_iri):
        if isinstance(strip_base, str):
            return base_iri.lstrip(strip_base)
        if strip_base:
            return base_iri.strip(onto.base_iri)
        return base_iri

    visited = set()

    def setmodules(onto):
        for imported_onto in onto.imported_ontologies:
            if onto.base_iri in modules:
                modules[strip(onto.base_iri)].add(strip(imported_onto.base_iri))
            else:
                modules[strip(onto.base_iri)] = set(
                    [strip(imported_onto.base_iri)]
                )
            if imported_onto.base_iri not in modules:
                modules[strip(imported_onto.base_iri)] = set()
            if imported_onto not in visited:
                visited.add(imported_onto)
                setmodules(imported_onto)

    setmodules(onto)
    return modules


def plot_modules(  # pylint: disable=too-many-arguments
    src,
    filename=None,
    fmt=None,
    show=False,
    strip_base=None,
    ignore_redundant=True,
):
    """Plot module dependency graph for `src` and return a graph object.

    Here `src` may be an IRI, a path the the ontology or a dict returned by
    get_module_dependencies().

    If `filename` is given, write the graph to this file.

    If `fmt` is None, the output format is inferred from `filename`.

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

    dot = graphviz.Digraph(comment="Module dependencies")
    dot.attr(rankdir="TB")
    dot.node_attr.update(
        style="filled", fillcolor="lightblue", shape="box", edgecolor="blue"
    )
    dot.edge_attr.update(arrowtail="open", dir="back")

    for iri in modules.keys():
        iriname = iri.split(":", 1)[1]
        dot.node(iriname, label=iri, URL=iri)

    for iri, deps in modules.items():
        for dep in deps:
            iriname = iri.split(":", 1)[1]
            depname = dep.split(":", 1)[1]
            dot.edge(depname, iriname)

    if filename:
        base, ext = os.path.splitext(filename)
        if fmt is None:
            fmt = ext.lstrip(".")
        dot.render(base, format=fmt, view=False, cleanup=True)

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
        for dependency in modules[iri]:
            if dependency != excl:
                deps.add(dependency)
                deps.update(get_deps(dependency))
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
        print("** Warning: Redundant module dependency:")
        for iri, dep in redundant:
            print(f"{iri} -> {dep}")

    return mods


def cytoscapegraph(
    graph: OntoGraph,
    onto: Optional[Ontology] = None,
    infobox: str = None,
    force: bool = False,
) -> "GridspecLayout":
    # pylint: disable=too-many-locals,too-many-statements
    """Returns and instance of icytoscape-figure for an
    instance Graph of OntoGraph, the accompanying ontology
    is required for mouse actions.
    Args:
            graph: graph generated with OntoGraph with edgelabels=True.
            onto: ontology to be used for mouse actions.
            infobox: "left" or "right". Placement of infbox with
                     respect to graph.
            force: force generate graph withour correct edgelabels.
    Returns:
            cytoscapewidget with graph and infobox to be visualized
            in jupyter lab.

    """
    # pylint: disable=import-error,import-outside-toplevel
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
    pydot_graph = nx.nx_pydot.from_pydot(dotplus)

    colours, styles, fill = cytoscape_style()

    data = cytoscape_data(pydot_graph)["elements"]
    for datum in data["edges"]:
        try:
            datum["data"]["label"] = (
                datum["data"]["label"].rsplit(" ", 1)[0].lstrip('"')
            )
        except KeyError as err:
            if not force:
                raise EMMOntoPyException(
                    "Edge label is not defined. Are you sure that the OntoGraph"
                    "instance you provided was generated with "
                    "´edgelabels=True´?"
                ) from err
            warnings.warn(
                "ARROWS WILL NOT BE DISPLAYED CORRECTLY. "
                "Edge label is not defined. Are you sure that the OntoGraph "
                "instance you provided was generated with ´edgelabels=True´?"
            )
            datum["data"]["label"] = ""

        lab = datum["data"]["label"].replace("Inverse(", "").rstrip(")")
        try:
            datum["data"]["colour"] = colours[lab]
        except KeyError:
            datum["data"]["colour"] = "black"
        try:
            datum["data"]["style"] = styles[lab]
        except KeyError:
            datum["data"]["style"] = "solid"
        if datum["data"]["label"].startswith("Inverse("):
            datum["data"]["targetarrow"] = "diamond"
            datum["data"]["sourcearrow"] = "none"
        else:
            datum["data"]["targetarrow"] = "triangle"
            datum["data"]["sourcearrow"] = "none"
        try:
            datum["data"]["fill"] = fill[lab]
        except KeyError:
            datum["data"]["fill"] = "filled"

    cytofig = ipycytoscape.CytoscapeWidget()
    cytofig.graph.add_graph_from_json(data, directed=True)

    cytofig.set_style(
        [
            {
                "selector": "node",
                "css": {
                    "content": "data(label)",
                    # "text-valign": "center",
                    # "color": "white",
                    # "text-outline-width": 2,
                    # "text-outline-color": "red",
                    "background-color": "blue",
                },
            },
            {"selector": "node:parent", "css": {"background-opacity": 0.333}},
            {
                "selector": "edge",
                "style": {
                    "width": 2,
                    "line-color": "data(colour)",
                    # "content": "data(label)"",
                    "line-style": "data(style)",
                },
            },
            {
                "selector": "edge.directed",
                "style": {
                    "curve-style": "bezier",
                    "target-arrow-shape": "data(targetarrow)",
                    "target-arrow-color": "data(colour)",
                    "target-arrow-fill": "data(fill)",
                    "mid-source-arrow-shape": "data(sourcearrow)",
                    "mid-source-arrow-color": "data(colour)",
                },
            },
            {
                "selector": "edge.multiple_edges",
                "style": {"curve-style": "bezier"},
            },
            {
                "selector": ":selected",
                "css": {
                    "background-color": "black",
                    "line-color": "black",
                    "target-arrow-color": "black",
                    "source-arrow-color": "black",
                    "text-outline-color": "black",
                },
            },
        ]
    )

    if onto is not None:
        out = Output(layout={"border": "1px solid black"})

        def log_clicks(node):
            with out:
                print((onto.get_by_label(node["data"]["label"])))
                parent = onto.get_by_label(node["data"]["label"]).get_parents()
                print(f"parents: {parent}")
                try:
                    elucidation = onto.get_by_label(
                        node["data"]["label"]
                    ).elucidation
                    print(f"elucidation: {elucidation[0]}")
                except (AttributeError, IndexError):
                    pass

                try:
                    annotations = onto.get_by_label(
                        node["data"]["label"]
                    ).annotations
                    for _ in annotations:
                        print(f"annotation: {_}")
                except AttributeError:
                    pass

                # Try does not work...
                try:
                    iri = onto.get_by_label(node["data"]["label"]).iri
                    print(f"iri: {iri}")
                except (AttributeError, IndexError):
                    pass
                try:
                    fig = node["data"]["label"]
                    if os.path.exists(Path(fig + ".png")):
                        display(Image(fig + ".png", width=100))
                    elif os.path.exists(Path(fig + ".jpg")):
                        display(Image(fig + ".jpg", width=100))
                except (AttributeError, IndexError):
                    pass
                out.clear_output(wait=True)

        def log_mouseovers(node):
            with out:
                print(onto.get_by_label(node["data"]["label"]))
                # print(f'mouseover: {pformat(node)}')
            out.clear_output(wait=True)

        cytofig.on("node", "click", log_clicks)
        cytofig.on("node", "mouseover", log_mouseovers)  # , remove=True)
        cytofig.on("node", "mouseout", out.clear_output(wait=True))
        grid = GridspecLayout(1, 3, height="400px")
        if infobox == "left":
            grid[0, 0] = out
            grid[0, 1:] = cytofig
        elif infobox == "right":
            grid[0, 0:-1] = cytofig
            grid[0, 2] = out
        else:
            return VBox([cytofig, out])
        return grid

    return cytofig
