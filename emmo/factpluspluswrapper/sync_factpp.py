import tempfile

from rdflib import OWL, RDFS

from owlready2 import World, Ontology, CURRENT_NAMESPACES
from owlready2.reasoning import _INFERRENCES_ONTOLOGY

from .owlapi_interface import OwlApiInterface


def sync_reasoner_factpp(x=None, infer_property_values=False, debug=1, keep_tmp_file=False):
    """
    """
    if isinstance(x, World):
        world = x
    elif isinstance(x, Ontology):
        world = x.world
    elif isinstance(x, list):
        world = x[0].world
    else:
        world = owlready2.default_world

    locked = world.graph.has_write_lock()
    if locked:
        world.graph.release_write_lock() # Not needed during reasoning

    try:

        #if isinstance(x, Ontology):
        #    ontology = x
        #elif CURRENT_NAMESPACES.get():
        #    ontology = CURRENT_NAMESPACES.get()[-1].ontology
        #else:
        #    ontology = world.get_ontology(_INFERRENCES_ONTOLOGY)

        #f = tempfile.NamedTemporaryFile("wb", delete=False)
        #if isinstance(x, list):
        #    for o in x:
        #        o.save(f, format="ntriples", commit=False)
        #else:
        #    world.save(f, format="ntriples")
        #f.close()

        print('*** start reasoning')
        g1 = world.as_rdflib_graph()

        # Remove owl:imports since they may cause problem when loading
        # the reasoned ontology
        for t in g1.triples((None, OWL.imports, None)):
            g1.remove(t)

        interface = OwlApiInterface()
        g2 = interface.reason(g1)

        print('*** start diffing')
        #both, only_g1, only_g2 = graph_diff(g1, g2)
        s1 = set(g1.triples((None, RDFS.subClassOf, None)))
        s2 = set(g2.triples((None, RDFS.subClassOf, None)))

        with open('diff.txt', 'wt') as f:
            from emmo.graph import getlabel
            for s, p, o in s2.difference(s1):
                #olabel = getlabel(world[str(o)])
                #f.write('%-40s owl:subClassOf  %s\n' % (
                #    getlabel(world[str(s)]), olabel if olabel != 'None' else o))
                f.write('%-60s owl:subClassOf %s\n' % (s, o))

        g1.serialize('g1.ttl', format='turtle')
        g2.serialize('g2.ttl', format='turtle')


        print('*** done diffing')


    finally:
        if locked:
            world.graph.acquire_write_lock() # re-lock when applying results
