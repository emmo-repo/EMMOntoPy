#!/usr/bin/env python3
import sys
import os

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology

emmo = get_ontology()
emmo.load()
# emmo.sync_reasoner()


H = emmo.Atom(label='H')
e = emmo.Electron(label='e')
p = emmo.Proton(label='p')
v = emmo.Vacuum(label='v')

H.has_spatial_direct_part = [e, p, v]


print()
print("Atom")
print([s for s in dir(emmo.Atom) if not s.startswith('_')])


print()
print("H")
print([s for s in dir(H) if not s.startswith('_')])
