#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 3 - load atom structure and represent it using our metadata framework
--------------------------------------------------------------------------
In this step we uses the Atomistic Simulation Environment (ASE) to load
a atomistic Al-Fe4Al13 interface structure from a cif file and
represents it using the metadata defined in step 2.
"""
import ase
import ase.io
from ase.spacegroup import Spacegroup

import dlite

from step2_define_metadata import DLiteAtoms



# Load atom structure from cif file and convert it to a DLiteAtoms object
at = ase.io.read('../vertical/Al-Fe4Al13.cif')
atoms = dlite.objectfactory(at, cls=DLiteAtoms, instanceid='atoms_Al-Fe4Al13')


# Create a new collection for data instances
coll = dlite.Collection('usercase_appdata')
coll.add('Atoms', atoms.dlite_meta)
coll.add('atoms', atoms.dlite_inst)
coll.save('json', 'usercase_appdata.json', 'mode=w')
