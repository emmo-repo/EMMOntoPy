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
# pylint: disable=import-error,invalid-name
import dlite


def map_app2common(instance, meta_collection, out_id=None):
    """Maps atom structure `instance` from our application representation
    (based on a not explicitly stated ontology) to the common
    EMMO-based representation in `meta_collection`.

    Parameters
    ----------
    instance : Instance of http://sintef.no/meta/soft/0.1/Atoms
        Input atom structure.
    meta_collection : Collection
        Collection of EMMO-based metadata generated from the ontology.
    out_id : None | string
        An optional id associated with the returned collection.

    Returns
    -------
    atcoll : Collection
        New collection with the atom structure represented as instances
        of metadata in `meta_collection`.

    Notes
    -----
    We use lowercase and underscore notation for the individuals.
    """
    infodict = dict(instance.info)  # make dict out of the info field

    # Create new collection representing `instance` in our case ontology
    atcoll = dlite.Collection(out_id)

    # Get metadata from meta_collection
    Crystal = meta_collection["Crystal"]
    UnitCell = meta_collection["CrystalUnitCell"]
    EBondedAtom = meta_collection["BondedAtom"]

    # Instanciate the structure
    crystal = Crystal([])
    crystal.spacegroup = infodict["spacegroup"]
    atcoll.add("crystal", crystal)

    unit_cell = UnitCell([3, 3, 36])
    unit_cell.lattice_vector = inst.cell
    atcoll.add("unit_cell", unit_cell)
    atcoll.add_relation("crystal", "hasSpatialDirectPart", "unit_cell")

    for index in range(instance.natoms):
        label = f"atom{index}"
        atom = EBondedAtom([3])
        atom.AtomicNumber = instance.numbers[index]
        atom.Position = instance.positions[index]
        atcoll.add(label, atom)
        atcoll.add_relation("unit_cell", "hasSpatialDirectPart", label)

    return atcoll


# Load metadata collection from step 1
metacoll = dlite.Collection(
    "json://usercase_metadata.json?mode=r#usercase_ontology"
)

# Load dlite-representation of atoms structure from step 3
coll = dlite.Collection("json://usercase_appdata.json?mode=r#usercase_appdata")
inst = coll.get("atoms")

# Do the mapping
new = map_app2common(inst, metacoll)


# Append the new atoms collection to the storage
new.save("json://usercase_data.json?mode=w")
