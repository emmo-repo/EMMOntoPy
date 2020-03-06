#!/usr/bin/env python3
import sys
import os

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology

from emmo.graph import (OntoGraph, plot_modules, get_module_dependencies,
                        check_module_dependencies)

emmo = get_ontology()
emmo.load()


iri = 'http://emmo.info/emmo/1.0.0-alpha'
modules = get_module_dependencies(iri)
plot_modules(iri, filename='modules.png', modules=modules)
check_module_dependencies(modules)
