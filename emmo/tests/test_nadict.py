#!/usr/bin/env python3
import sys
import os

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo.nadict import NADict  # noqa: E402, F401


n = NADict(a=1, b=NADict(c=3, d=4))

assert n.a == 1
assert n.b.c == 3
assert n.b.d == 4
assert n['b.c'] == 3
