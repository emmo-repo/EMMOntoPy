#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plots the user case ontology created with the script `define_ontology.py`.
"""
from emmo import get_ontology


# Load usercase ontology

# Create a new ontology with out extensions that imports EMMO
onto = get_ontology('usercase_ontology.owl')
onto.load()
#onto.base_iri = 'http://www.emmc.info/emmc-csa/demo#'


#
# Visualise our new EMMO-based ontology
# =====================================

# Update the uml-style to generate
del onto._uml_style['class']['shape']
del onto._uml_style['defined_class']['shape']


# Save graph with our new classes
graph = onto.get_dot_graph(list(onto.classes()), relations=True,
                           style='uml', constraint=None)
graph.write_svg('usercase_ontology.svg')


# Categories of classes
units = [c for c in onto.classes() if issubclass(c, onto.SIUnit)]
properties = [c for c in onto.classes()
              if issubclass(c, onto.Property) and c not in units]
leaf_prop = [c for c in properties if len(c.descendants()) == 1]
materials = [c for c in onto.classes() if issubclass(c, (
    onto.Subatomic, onto.Atomic, onto.Mesoscopic, onto.Continuum,
    onto.Boundary, onto.Engineered))]
subdimensional = [c for c in onto.classes() if issubclass(c, (
    onto.Point, onto.Line, onto.Plane, onto.EuclideanSpace))]
types = [onto.Integer, onto.Real, onto.String]

# Update the uml-stype to generate
onto._uml_style['graph']['rankdir'] = 'BT'

# Units and properties
#graph = onto.get_dot_graph([onto.SI_unit] + leaf_prop, relations=True,
graph = onto.get_dot_graph([onto.SIUnit] + properties, relations=True,
                           style='uml', constraint=None)
graph.write_svg('units+properties.svg')

# Types and properties
graph = onto.get_dot_graph(types + leaf_prop, relations=True, style='uml',
                           constraint=None)
graph.write_svg('types+properties.svg')

# Properties and materials
items = [
    onto.PhysicalQuantity, onto.BondedAtom] + materials + subdimensional
graph = onto.get_dot_graph(items, relations=True, style='uml', constraint=None)
graph.write_svg('properties+materials.svg')

# Material
#items = [onto.atomic, onto.continuum, onto.boundary]
items = [onto.State] + materials
leafs = ['Elementary', 'Symbolic', 'Subatomic', 'StandaloneAtom']
graph = onto.get_dot_graph(items, leafs=leafs, relations=True,
                           parents=False, style='uml')
graph.write_svg('materials.svg')

# Also include the parents of our new classes (this graph becomes
# rather large...)
parents = {e.mro()[1] for e in onto.classes()}
classes = list(parents.union(onto.classes()))  # + [onto.Space]
onto._uml_style['graph']['rankdir'] = 'RL'
graph = onto.get_dot_graph(classes, relations=True, style='uml',
                           edgelabels=True)
graph.write_svg('usercase_ontology-parents.svg')
