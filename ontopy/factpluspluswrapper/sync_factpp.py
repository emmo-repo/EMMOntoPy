from collections import defaultdict
from collections.abc import Sequence

import rdflib
from rdflib import URIRef, RDF, RDFS, OWL

import owlready2
from owlready2 import World, Ontology, CURRENT_NAMESPACES
from owlready2.reasoning import (
    _apply_reasoning_results, _apply_inferred_obj_relations,
    _INFERRENCES_ONTOLOGY)

from ontopy.factpluspluswrapper.factppgraph import FaCTPPGraph


OWL_2_TYPE = {
    RDFS.subClassOf:        'class',
    RDFS.subPropertyOf:     'property',
    RDF.type:               'individual',
    OWL.equivalentClass:    'class',
    OWL.equivalentProperty: 'property',
}


def sync_reasoner_factpp(ontology_or_world=None, infer_property_values=False,
                         debug=1):
    """Run FaCT++ reasoner and load the inferred relations back into
    the owlready2 triplestore.

    Parameters
    ----------
    ontology_or_world : None | Ontology instance | World instance | list
        Identifies the world to run the reasoner over.
    infer_property_values : bool
        Whether to also infer property values.
    debug : bool
        Whether to print debug info to standard output.
    """
    if isinstance(ontology_or_world, World):
        world = ontology_or_world
    elif isinstance(ontology_or_world, Ontology):
        world = ontology_or_world.world
    elif isinstance(ontology_or_world, Sequence):
        world = ontology_or_world[0].world
    else:
        world = owlready2.default_world

    if isinstance(ontology_or_world, Ontology):
        ontology = ontology_or_world
    elif CURRENT_NAMESPACES.get():
        ontology = CURRENT_NAMESPACES.get()[-1].ontology
    else:
        ontology = world.get_ontology(_INFERRENCES_ONTOLOGY)

    locked = world.graph.has_write_lock()
    if locked:
        world.graph.release_write_lock()  # Not needed during reasoning

    try:
        print('*** Prepare graph')
        # Exclude owl:imports because they are not needed and can
        # cause trouble when loading the inferred ontology
        g1 = rdflib.Graph()
        for s, p, o in world.as_rdflib_graph().triples((None, None, None)):
            if p != OWL.imports:
                g1.add((s, p, o))

        print('*** Run FaCT++ reasoner (and postprocess)')
        g2 = FaCTPPGraph(g1).inferred_graph()

        print('*** Load inferred ontology')
        # Check all rdfs:subClassOf relations in the inferred graph and add
        # them to the world if they are missing
        new_parents = defaultdict(list)
        new_equivs = defaultdict(list)
        entity_2_type = {}

        for s, p, o in g2.triples((None, None, None)):
            if (isinstance(s, URIRef) and
                    p in OWL_2_TYPE and
                    isinstance(o, URIRef)):
                s_storid = ontology._abbreviate(str(s), False)
                p_storid = ontology._abbreviate(str(p), False)
                o_storid = ontology._abbreviate(str(o), False)
                if (s_storid is not None and
                        p_storid is not None and
                        o_storid is not None):
                    if p in (RDFS.subClassOf, RDFS.subPropertyOf, RDF.type):
                        new_parents[s_storid].append(o_storid)
                        entity_2_type[s_storid] = OWL_2_TYPE[p]
                    else:
                        new_equivs[s_storid].append(o_storid)
                        entity_2_type[s_storid] = OWL_2_TYPE[p]

        if infer_property_values:
            inferred_obj_relations = []
            # Hmm, does FaCT++ infer any property values?
            # If not, remove the `infer_property_values` keyword argument.
            raise NotImplementedError

    finally:
        if locked:
            world.graph.acquire_write_lock()  # re-lock when applying results

    print('*** Applying reasoning results')
    _apply_reasoning_results(world, ontology, debug, new_parents, new_equivs,
                             entity_2_type)
    if infer_property_values:
        _apply_inferred_obj_relations(world, ontology, debug,
                                      inferred_obj_relations)
