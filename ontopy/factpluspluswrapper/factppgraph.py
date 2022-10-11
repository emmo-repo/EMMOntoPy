"""# `ontopy.factpluspluswrapper.factppgraph`"""
# pylint: disable=too-few-public-methods
from rdflib import URIRef, OWL, RDF, RDFS

from ontopy.factpluspluswrapper.owlapi_interface import OwlApiInterface


class FactPPError:
    """Postprocessing error after reasoning with FaCT++."""


class FaCTPPGraph:
    """Class for running the FaCT++ reasoner (using OwlApiInterface) and
    postprocessing the resulting inferred ontology.

    Parameters
    ----------
    graph : owlapi.Graph instance
        The graph to be inferred.
    """

    def __init__(self, graph):
        self.graph = graph
        self._inferred = None
        self._namespaces = None
        self._base_iri = None

    @property
    def inferred(self):
        """The current inferred graph."""
        if self._inferred is None:
            self._inferred = self.raw_inferred_graph()
        return self._inferred

    @property
    def base_iri(self):
        """Base iri of inferred ontology."""
        if self._base_iri is None:
            self._base_iri = URIRef(self.asserted_base_iri() + "-inferred")
        return self._base_iri

    @base_iri.setter
    def base_iri(self, value):
        """Assign inferred base iri."""
        self._base_iri = URIRef(value)

    @property
    def namespaces(self):
        """Namespaces defined in the original graph."""
        if self._namespaces is None:
            self._namespaces = dict(self.graph.namespaces()).copy()
            self._namespaces[""] = self.base_iri
        return self._namespaces

    def asserted_base_iri(self):
        """Returns the base iri or the original graph."""
        return URIRef(dict(self.graph.namespaces()).get("", "").rstrip("#/"))

    def raw_inferred_graph(self):
        """Returns the raw non-postprocessed inferred ontology as a rdflib
        graph."""
        return OwlApiInterface().reason(self.graph)

    def inferred_graph(self):
        """Returns the postprocessed inferred graph."""
        self.add_base_annotations()
        self.set_namespace()
        self.clean_base()
        self.remove_nothing_is_nothing()
        self.clean_ancestors()
        return self.inferred

    def add_base_annotations(self):
        """Copy base annotations from original graph to the inferred graph."""
        base = self.base_iri
        inferred = self.inferred
        for _, predicate, obj in self.graph.triples(
            (self.asserted_base_iri(), None, None)
        ):
            if predicate == OWL.versionIRI:
                version = obj.rsplit("/", 1)[-1]
                obj = URIRef(f"{base}/{version}")
            inferred.add((base, predicate, obj))

    def set_namespace(self):
        """Override namespace of inferred graph with the namespace of the
        original graph.
        """
        inferred = self.inferred
        for key, value in self.namespaces.items():
            inferred.namespace_manager.bind(
                key, value, override=True, replace=True
            )

    def clean_base(self):
        """Remove all relations `s? a owl:Ontology` where `s?` is not
        `base_iri`.
        """
        inferred = self.inferred
        for (
            subject,
            predicate,
            obj,
        ) in inferred.triples(  # pylint: disable=not-an-iterable
            (None, RDF.type, OWL.Ontology)
        ):
            inferred.remove((subject, predicate, obj))
        inferred.add((self.base_iri, RDF.type, OWL.Ontology))

    def remove_nothing_is_nothing(self):
        """Remove superfluid relation in inferred graph:

        owl:Nothing rdfs:subClassOf owl:Nothing
        """
        triple = OWL.Nothing, RDFS.subClassOf, OWL.Nothing
        inferred = self.inferred
        if triple in inferred:
            inferred.remove(triple)

    def clean_ancestors(self):
        """Remove redundant rdfs:subClassOf relations in inferred graph."""
        inferred = self.inferred
        for (  # pylint: disable=too-many-nested-blocks
            subject
        ) in inferred.subjects(RDF.type, OWL.Class):
            if isinstance(subject, URIRef):
                parents = set(
                    parent
                    for parent in inferred.objects(subject, RDFS.subClassOf)
                    if isinstance(parent, URIRef)
                )
                if len(parents) > 1:
                    for parent in parents:
                        ancestors = set(
                            inferred.transitive_objects(parent, RDFS.subClassOf)
                        )
                        for entity in parents:
                            if entity != parent and entity in ancestors:
                                triple = subject, RDFS.subClassOf, entity
                                if triple in inferred:
                                    inferred.remove(triple)
