#!/usr/bin/env python3
import sys
import os
import json

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology

#emmo = get_ontology()
#emmo.load()

# If false, read from cached json file (much faster...)
load_emmo = False


def setmodules(onto, modules):
    """Update the dict `modules` with key-value pairs, where each key is
    the IRIs of ontology `onto` and all its imported sub-ontologies and
    the corresponding values the IRIs of the ontologies they import."""
    for o in onto.imported_ontologies:
        if onto.base_iri in modules:
            modules[onto.base_iri].add(o.base_iri)
        else:
            modules[onto.base_iri] = set([o.base_iri])
        if o.base_iri not in modules:
            modules[o.base_iri] = set()
        setmodules(o, modules)


def getname(iri):
    """Returns the name part of an iri."""
    return os.path.basename(os.path.splitext(iri)[0])


if load_emmo:
    emmo = get_ontology('http://emmo.info/emmo/1.0.0-alpha')
    emmo.load()

    modules = {}
    setmodules(emmo, modules)
    modules = {k: list(v) for k, v in modules.items()}
    with open('emmo-modules.json', 'wt') as f:
        json.dump(modules, f, indent=4)
else:
    with open('emmo-modules.json', 'rt') as f:
        modules = json.load(f)


# Plot module dependencies
from graphviz import Digraph

base = 'http://emmo.info/'
topurl = base + 'emmo.owl#'
clusters = set(k.split('/')[3] for k in modules if k != topurl)

dot = Digraph(comment='EMMO module dependencies')
dot.attr(rankdir='TB')
dot.node_attr.update(style='filled', fillcolor='lightblue', shape='box',
                     edgecolor='blue')
dot.edge_attr.update(arrowtail='open', dir='back')
dot.node('emmo', nodeURL=topurl)
for i, cluster in enumerate(clusters):
    nodes = [k for k in modules if k.startswith(base + cluster)]
    with dot.subgraph(name='cluster%d' % i) as c:
        c.attr(label=cluster, labeljust='c', fontsize='20',
               style='filled', fillcolor='lightgray')
        print('cluster:', cluster)
        for node in nodes:
            print('  -', getname(node))
            c.node(getname(node), nodeURL=node)

for module, deps in modules.items():
    for dep in deps:
        dot.edge(getname(dep), getname(module))
dot.render('emmo-modules', format='pdf', view=False)
dot.render('emmo-modules', format='png', view=False)
