#!/usr/bin/env python3
import sys
import os

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology, World  # noqa: E402, F401

import owlready2  # noqa: E402, F401


emmodir = os.path.join(thisdir, '..', '..', '..', 'EMMO')
owlready2.set_log_level(0)


# Load latest stable EMMO
emmo = get_ontology('emmo')
emmo.load()


# Load emmo-inferred
world = World()
inferred = world.get_ontology()
inferred.load()


# Load local EMMO
if os.path.exists(os.path.join(emmodir, 'emmo.owl')):
    world2 = World()
    local = world2.get_ontology(os.path.join(emmodir, 'emmo.owl'))
    local.load(catalog_file=True)
