#!/usr/bin/env python3
import sys
import os

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo.graph import NestedAttrDict


#n = NestedAttrDict()
n = NestedAttrDict(a=1, b=NestedAttrDict(c=3, d=4))
