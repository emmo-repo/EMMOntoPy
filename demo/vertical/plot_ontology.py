#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plots the user case ontology created with the script `define_ontology.py`.
"""
from emmo import World


# Load usercase ontology from sqlite3 database
world = World(filename='demo.sqlite3')
onto = world.get_ontology('http://www.emmc.info/emmc-csa/demo#')
onto.load()

classes = set(onto.classes())


# Visualise new classes (classes from emmo gets a red border)
graph = onto.get_graph(entities=classes, relations='all',
                       edgelabels=False, addnodes=True, addconstructs=False,
                       excluded_nodes=['SquareLengthDimension'],
                       graph_attr={'rankdir': 'RL'})
graph.add_legend()
graph.save('demo.svg')


# Visualise units and quantities
entities = [c for c in classes
            if issubclass(c, (onto.MeasurementUnit, onto.Quantity))]
graph = onto.get_graph(entities=entities, relations='all',
                       edgelabels=False, addnodes=True, addconstructs=False,
                       graph_attr={'rankdir': 'RL'})
graph.add_legend()
graph.save('units+properties.svg')


# Visualise Material branch
graph = onto.get_graph(root=onto.Material, relations='all',
                       edgelabels=False, addnodes=False, addconstructs=False)
graph.add_legend()
graph.save('materials.svg')


# Material and properties
entities = [c for c in classes if issubclass(c, onto.Material)]
graph = onto.get_graph(entities=entities, relations='all',
                       edgelabels=False, addnodes=True, addconstructs=False,
                       graph_attr={'rankdir': 'RL'})
graph.add_legend()
graph.save('materials+properties.svg')
