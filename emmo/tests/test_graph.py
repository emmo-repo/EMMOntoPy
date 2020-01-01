#!/usr/bin/env python3
import sys
import os

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology


emmo = get_ontology()
emmo.load()

#graph = emmo.get_dot_graph(relations=True, style='uml')
#graph.write_svg('graph-noreason.svg')
#graph.write_pdf('graph-noreason.pdf')
#emmo.sync_reasoner()

#graph = emmo.get_dot_graph(relations=True, style='uml')
graph = emmo.get_dot_graph(relations='is_a', style='uml')
graph.write_svg('taxonomy.svg')
graph.write_pdf('taxonomy.pdf')

entity_graph = emmo.get_dot_graph('EMMO')
entity_graph.write_svg('taxonomy2.svg')

substrate_graph = emmo.get_dot_graph('Item', relations=True,
                                     leafs=('Physical'), parents='Item',
                                     style='uml')
substrate_graph.write_svg('merotopology_graph.svg')

property_graph = emmo.get_dot_graph('Property')
property_graph.write_svg('property_graph.svg')

#relations_graph = emmo.get_dot_relations_graph(relations=True)
#relations_graph.write_pdf('relation_graph.pdf')


# Update the default style
emmo._default_style['graph']['rankdir'] = 'BT'

#relations_graph = emmo.get_dot_relations_graph()
relations_graph = emmo.get_dot_graph('EMMORelation')
relations_graph.write_pdf('relation_graph.pdf')
relations_graph.write_png('relation_graph.png')
