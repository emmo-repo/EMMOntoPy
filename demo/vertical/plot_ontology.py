#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plots the user case ontology created with the script `define_ontology.py`."""
from emmo import get_ontology


# Load EMMO

# Create a new ontology with out extensions that imports EMMO
onto = get_ontology('usercase_ontology.owl')
onto.load()
#onto.base_iri = 'http://www.emmc.info/emmc-csa/demo#'


#
# Visualise our new EMMO-based ontology
# =====================================

# Update the uml-stype to generate
del onto._uml_style['class']['shape']
del onto._uml_style['defined_class']['shape']


# Save graph with our new classes
graph = onto.get_dot_graph(list(onto.classes()), relations=True,
                           style='uml', constraint=None)
graph.write_svg('usercase_ontology.svg')


# Categories of classes
units = [c for c in onto.classes() if issubclass(c, onto.SI_unit)]
properties = [c for c in onto.classes()
              if issubclass(c, onto.property) and not c in units]
leaf_prop = [c for c in properties if len(c.descendants()) == 1]
materials = [c for c in onto.classes() if issubclass(c, (
    onto.subatomic, onto.atomic, onto.mesoscopic, onto.continuum))]
subdimensional = [c for c in onto.classes() if issubclass(c, (
    onto.point, onto.line, onto.surface, onto.volume))]
types = [onto.integer, onto.real, onto.string]

# Update the uml-stype to generate
onto._uml_style['graph']['rankdir'] = 'BT'

# Units and properties
#graph = onto.get_dot_graph([onto.SI_unit] + leaf_prop, relations=True,
graph = onto.get_dot_graph([onto.SI_unit] + properties, relations=True,
                           style='uml', constraint=None)
graph.write_svg('units+properties.svg')

# Types and properties
graph = onto.get_dot_graph(types + leaf_prop, relations=True, style='uml',
                           constraint=None)
graph.write_svg('types+properties.svg')

# Properties and materials
items = [
    onto.physical_quantity, onto['e-bonded_atom']] + materials + subdimensional
graph = onto.get_dot_graph(items, relations=True, style='uml', constraint=None)
graph.write_svg('properties+materials.svg')

# Material
#items = [onto.atomic, onto.continuum, onto.boundary]
items = [onto.state] + materials
leafs = ['elementary', 'symbolic', 'subatomic', 'standalone_atom']
graph = onto.get_dot_graph(items, leafs=leafs, relations=True,
                           parents=False, style='uml')
graph.write_svg('materials.svg')

# Also include the parents of our new classes (this graph becomes
# rather large...)
parents = {e.mro()[1] for e in onto.classes()}
classes = list(parents.union(onto.classes())) + [onto.space]
onto._uml_style['graph']['rankdir'] = 'RL'
graph = onto.get_dot_graph(classes, relations=True, style='uml',
                            edgelabels=True)
graph.write_svg('usercase_ontology-parents.svg')
