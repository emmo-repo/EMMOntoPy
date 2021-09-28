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

import dlite

from step2_define_metadata import DLiteAtoms


# Example for importing structure from the MaterialsProject.
# See https://materialsproject.org/docs/api for instructions for getting
# personal access.
# Not used in the current demo
#
#     from pymatgen.ext.matproj import MPRester
#     with MPRester('USER_API_KEY') as m:
#         structure = m.get_structure_by_material_id('mp-2018')
#


# Load atom structure from cif file
at = ase.io.read('../vertical/Al-Fe4Al13.cif')

# convert atom structure to a DLiteAtoms object
atoms = dlite.objectfactory(at, cls=DLiteAtoms, instanceid='atoms_Al-Fe4Al13')


# Create a new collection for data instances
coll = dlite.Collection('usercase_appdata')
coll.add('Atoms', atoms.dlite_meta)
coll.add('atoms', atoms.dlite_inst)
coll.save('json', 'usercase_appdata.json', 'mode=w')
