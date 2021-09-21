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
            self._base_iri = URIRef(self.asserted_base_iri() + '-inferred')
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
            self._namespaces[''] = self.base_iri
        return self._namespaces

    def asserted_base_iri(self):
        """Returns the base iri or the original graph."""
        return URIRef(dict(self.graph.namespaces()).get('', '').rstrip('#/'))

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
        for s, p, o in self.graph.triples(
                (self.asserted_base_iri(), None, None)):
            if p == OWL.versionIRI:
                version = o.rsplit('/', 1)[-1]
                o = URIRef('%s/%s' % (base, version))
            inferred.add((base, p, o))

    def set_namespace(self):
        """Override namespace of inferred graph with the namespace of the
        original graph.
        """
        inferred = self.inferred
        for k, v in self.namespaces.items():
            inferred.namespace_manager.bind(k, v, override=True, replace=True)

    def clean_base(self):
        """Remove all relations `s? a owl:Ontology` where `s?` is not
        `base_iri`.
        """
        inferred = self.inferred
        for s, p, o in inferred.triples((None, RDF.type, OWL.Ontology)):
            inferred.remove((s, p, o))
        inferred.add((self.base_iri, RDF.type, OWL.Ontology))

    def remove_nothing_is_nothing(self):
        """Remove superfluid relation in inferred graph:

            owl:Nothing rdfs:subClassOf owl:Nothing
        """
        t = OWL.Nothing, RDFS.subClassOf, OWL.Nothing
        inferred = self.inferred
        if t in inferred:
            inferred.remove(t)

    def clean_ancestors(self):
        """Remove redundant rdfs:subClassOf relations in inferred graph."""
        inferred = self.inferred
        for s in inferred.subjects(RDF.type, OWL.Class):
            if isinstance(s, URIRef):
                parents = set(p for p in inferred.objects(s, RDFS.subClassOf)
                              if isinstance(p, URIRef))
                if len(parents) > 1:
                    for parent in parents:
                        ancestors = set(inferred.transitive_objects(
                            parent, RDFS.subClassOf))
                        for p in parents:
                            if p != parent and p in ancestors:
                                t = s, RDFS.subClassOf, p
                                if t in inferred:
                                    inferred.remove(t)
