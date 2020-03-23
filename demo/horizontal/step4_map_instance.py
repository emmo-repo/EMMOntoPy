#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 4 - map to common representation
-------------------------------------
maps it to a collection of instances of the metadata generated from the
ontology.


This script uses the Atomistic Simulation Environment (ASE) to load
a atomistic Al-Fe4Al13 interface structure from a cif file and
represents it using the same metadata framework as used in step 1.
"""
import dlite


def map_app2common(inst, metacoll, out_id=None):
    """Maps atom structure `inst` from our application representation
    (based on a not explicitly stated ontology) to the common
    EMMO-based representation in `metacoll`.

    Parameters
    ----------
    inst : Instance of http://sintef.no/meta/soft/0.1/Atoms
        Input atom structure.
    metacoll : Collection
        Collection of EMMO-based metadata generated from the ontology.
    out_id : None | string
        An optional id associated with the returned collection.

    Returns
    -------
    atcoll : Collection
        New collection with the atom structure represented as instances
        of metadata in `metacoll`.

    Notes
    -----
    We use lowercase and underscore notation for the individuals.
    """
    infodict = dict(inst.info)  # make dict out of the info field

    # Create new collection representing `inst` in our case ontology
    atcoll = dlite.Collection(out_id)

    # Get metadata from metacoll
    Crystal = metacoll['Crystal']
    UnitCell = metacoll['CrystalUnitCell']
    EBondedAtom = metacoll['BondedAtom']

    # Instanciate the structure
    crystal = Crystal([])
    crystal.spacegroup = infodict['spacegroup']
    atcoll.add('crystal', crystal)

    unit_cell = UnitCell([3, 3, 36])
    unit_cell.lattice_vector = inst.cell
    atcoll.add('unit_cell', unit_cell)
    atcoll.add_relation('crystal', 'hasSpatialDirectPart', 'unit_cell')

    for i in range(inst.natoms):
        label = 'atom%d' % i
        a = EBondedAtom([3])
        a.AtomicNumber = inst.numbers[i]
        a.Position = inst.positions[i]
        atcoll.add(label, a)
        atcoll.add_relation('unit_cell', 'hasSpatialDirectPart', label)

    return atcoll


# Load metadata collection from step 1
metacoll = dlite.Collection(
    'json://usercase_metadata.json?mode=r#usercase_ontology', True)

# Load dlite-representation of atoms structure from step 3
coll = dlite.Collection(
    'json://usercase_appdata.json?mode=r#usercase_appdata', False)
inst = coll.get('atoms')

# Do the mapping
new = map_app2common(inst, metacoll)


# Append the new atoms collection to the storage
new.save('json://usercase_data.json?mode=w')
