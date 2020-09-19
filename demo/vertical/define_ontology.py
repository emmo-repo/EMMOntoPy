#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""An example script that uses EMMO to describe a vertical use case on
welding aluminium to steel and how the thin layer of intermetallic
that are formed at the interface is influencing the overall
properties.  Based on TEM observations using scanning precision
electron diffraction (SPED) the following (simplified) sequence of
intermetallic phases could be established:

    Al | alpha-AlFeSi | Fe4Al13 | Fe2Al5 | Fe

which is consistent with phase stability when the Fe-concentration is
increasing when going from left to right.

In this case study three scales are considered:

  - Macroscopic scale: predicts the overall mechanical behaviour of
    the welded structure during deformation.

  - Microscopic scale: a local crystal plasticity model of a small
    part of the interface.  The constitutive equations were based on
    the results from DFT.  The results from this model was used to
    calibrate decohesion elements for the macroscopic scale.

  - Electronic scale: elastic properties of the individual phases as
    well work of decohesion within and at the interfaces between the
    phases were calculated with DFT [1].  The calculation of work of
    decohesion was performed as a series of rigid steps, providing
    stress-strain relations in both tensile and shear.

References
----------
[1] Khalid et al. Proc. Manufact. 15 (2018) 1407

"""
from emmo import World


# Load EMMO
world = World(filename='demo.sqlite3')
# emmo = world.get_ontology('http://emmo.info/emmo/1.0.0-alpha2')
emmo = world.get_ontology('emmo-inferred')
emmo.load()
# emmo.sync_reasoner()

# Create a new ontology with out extensions that imports EMMO
onto = world.get_ontology('http://www.emmc.info/emmc-csa/demo#')
onto.imported_ontologies.append(emmo)


# Add new classes and object/data properties needed by the use case
with onto:

    #
    # Relations
    # =========
    class hasType(emmo.hasConvention):
        """Associates a type (string, number...) to a property."""
        pass

    class isTypeOf(emmo.hasConvention):
        """Associates a property to a type (string, number...)."""
        inverse_property = hasType

    #
    # Units
    # =====

    # TODO: remove
    class SquareLengthDimension(emmo.PhysicalDimension):
        is_a = [emmo.hasSymbolData.value('T0 L2 M0 I0 Θ0 N0 J0')]

    # TODO: remove
    class SquareMetre(emmo.SICoherentDerivedUnit):
        emmo.altLabel = ['m²']
        is_a = [emmo.hasPhysicalDimension.only(SquareLengthDimension)]

    #
    # Properties
    # ==========

    # TODO: update instead of redefine Position
    class Position(emmo.Length):
        """Spatial position of an physical entity."""
        is_a = [emmo.hasReferenceUnit.only(emmo.hasPhysicalDimension.only(
                 emmo.LengthDimension)),
                hasType.exactly(3, emmo.Real)]

    # TODO: remove
    class Area(emmo.ISQDerivedQuantity):
        """Extent of a surface."""
        is_a = [
            emmo.hasReferenceUnit.only(emmo.hasPhysicalDimension.only(
                SquareLengthDimension)),
            hasType.exactly(1, emmo.Real),
        ]

    emmo.Pressure.is_a.append(hasType.exactly(1, emmo.Real))

    # TODO: update when we have dimensionality
    class StiffnessTensor(emmo.Pressure):
        r"""The stiffness tensor $c_{ijkl}$ is a property of a continuous
        elastic material that relates stresses to strains (Hooks's
        law) according to

            $\sigma_{ij} = c_{ijkl} \epsilon_{kl}$

        Due to symmetry and using the Voight notation, the stiffness
        tensor can be represented as a symmetric 6x6 matrix

            / c_1111  c_1122  c_1133  c_1123  c_1131  c_1112 \
            | c_2211  c_2222  c_2233  c_2223  c_2231  c_2212 |
            | c_3311  c_3322  c_3333  c_3323  c_3331  c_3312 |
            | c_2311  c_2322  c_2333  c_2323  c_2331  c_2312 |
            | c_3111  c_3122  c_3133  c_3123  c_3131  c_3112 |
            \ c_1211  c_1222  c_1233  c_1223  c_1231  c_1212 /

        """
        is_a = [hasType.exactly(36, emmo.Real)]

    # class Spacegroup(emmo.DescriptiveProperty):
    #     """A spacegroup is the symmetry group off all symmetry operations
    #     that apply to a crystal structure.
    #
    #     It is identifies by its Hermann-Mauguin symbol or space group
    #     number (and setting) in the International tables of
    #     Crystallography."""
    #     is_a = [hasType.exactly(1, emmo.String)]
    #     pass

    # class Plasticity(emmo.PhysicalQuantity):
    #     """Describes Yield stress and material hardening."""
    #     is_a = [hasUnit.exactly(1, Pascal),
    #             hasType.min(2, emmo.Real)]

    ''' Will be included when dimensionality is inplace in EMMO'''

    # class TractionSeparation(Pressure):
    #     """The force required to separate two materials a certain distance
    #     per interface area.  Hence, traction_separation is a curve, that
    #     numerically can be represented as a series of (force,
    #     separation_distance) pairs."""
    #     is_a = [hasUnit.exactly(1, Pascal),
    #             hasType.min(4, emmo.Real)]

    # class LoadCurve(Pressure):
    #     """A measure for the displacement of a material as function of the
    #     appliced force."""
    #     is_a = [hasUnit.exactly(1, Pascal),
    #             hasType.min(4, emmo.Real)]

    # Crystallography-related classes
    # TODO: import crystallography ontology instead
    # -------------------------------
    class LatticeVector(emmo.Length):
        """A vector that participitates defining the unit cell."""
        is_a = [hasType.exactly(3, emmo.Real)]

    # FIXME - CrystalUnitCell is not a matter, but a model or a symbolic
    #         Just use crystalography
    class CrystalUnitCell(emmo.Material):
        """A volume defined by the 3 unit cell vectors.  It contains the atoms
        constituting the unit cell of a crystal."""
        is_a = [emmo.hasSpatialDirectPart.some(emmo.BondedAtom),
                emmo.hasProperty.exactly(3, LatticeVector),
                emmo.hasProperty.exactly(1, StiffnessTensor)]

    class InterfaceModel(CrystalUnitCell):
        is_a = [emmo.hasProperty.some(Area)]

    class Crystal(emmo.Solid):
        """A periodic crystal structure."""
        is_a = [emmo.hasSpatialDirectPart.only(CrystalUnitCell)]

    # Add some properties to our atoms
    emmo.Atom.is_a.append(emmo.hasProperty.exactly(1, Position))

    # Continuum
    # ---------
    class Boundary(emmo.Continuum):
        """A boundary is a 4D region of spacetime shared by two material
        entities."""
        equivalent_to = [emmo.hasSpatialDirectPart.exactly(2, emmo.Continuum)]
        is_a = [emmo.hasProperty.exactly(1, Area)]

    class Phase(emmo.Continuum):
        """A phase is a continuum in which properties are homogeneous and can
        have different state of matter."""
        is_a = [emmo.hasProperty.exactly(1, StiffnessTensor)]

    class RVE(emmo.Continuum):
        """Representative volume element.  The minimum volume that is
        representative for the system in question."""
        is_a = [emmo.hasSpatialDirectPart.only(Phase | Boundary)]

    class WeldedComponent(emmo.Component):
        """A welded component consisting of two materials welded together
        using a third welding material.  Hence it has spatial direct
        parts 3 materials and two boundaries."""
        is_a = [
            emmo.hasSpatialDirectPart.exactly(3, emmo.Material),
            emmo.hasSpatialDirectPart.exactly(2, Boundary),
            # emmo.hasProperty.exactly(1, LoadCurve),
        ]


# Sync attributes to make sure that all classes get a `label` and to
# include the docstrings in the comments
onto.sync_attributes(name_policy='uuid', name_prefix='DEMO_')


# Run the reasoner
# onto.sync_reasoner()

# set version of ontology
onto.set_version("0.9")

# Save our new EMMO-based ontology to demo.owl
onto.save('demo.owl', overwrite=True)

# ...and to the sqlite3 database.
world.save()
