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
import os

from emmo import get_ontology


# Load EMMO
emmo = get_ontology()
emmo.load()
#emmo.sync_reasoner()

# Create a new ontology with out extensions that imports EMMO
onto = get_ontology('onto.owl')
onto.imported_ontologies.append(emmo)
onto.base_iri = 'http://www.emmc.info/emmc-csa/demo#'

# Add new classes and object/data properties needed by the use case
with onto:

    #
    # Relations
    # =========
    class hasUnit(emmo.hasPart):
        """Associates a unit to a property."""
        pass

    class isUnitFor(emmo.hasPart):
        """Associates a property to a unit."""
        inverse_property = hasUnit

    class hasType(emmo.hasConvention):
        """Associates a type (string, number...) to a property."""
        pass

    class isTypeOf(emmo.hasConvention):
        """Associates a property to a type (string, number...)."""
        inverse_property = hasType

    #
    # Types
    # =====
    #class Integer(emmo.Number):
    #    pass
    #
    #class Real(emmo.Number):
    #    pass
    #
    #class String(emmo.number):
    #    pass

    #
    # Units
    # =====
    class SIUnit(emmo.MeasurementUnit):
        """Base class for all SI units."""
        pass

    class Meter(SIUnit):
        label = ['m']

    class SquareMeter(SIUnit):
        label = ['m²']

    class Pascal(SIUnit):
        label = ['Pa']

    #
    # Properties
    # ==========
    class Position(emmo.PhysicalQuantity):
        """Spatial position of an physical entity."""
        is_a = [hasUnit.exactly(1, Meter),
                hasType.exactly(3, emmo.Real)]

    class Area(emmo.PhysicalQuantity):
        """Area of a surface."""
        is_a = [hasUnit.exactly(1, SquareMeter),
                hasType.exactly(1, emmo.Real)]

    class Pressure(emmo.PhysicalQuantity):
        """The force applied perpendicular to the surface of an object per
        unit area."""
        is_a = [hasUnit.exactly(1, Pascal),
                hasType.exactly(1, emmo.Real)]

    class StiffnessTensor(Pressure):
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
        is_a = [hasUnit.exactly(1, Pascal),
                hasType.exactly(36, emmo.Real)]

    class AtomicNumber(emmo.PhysicalQuantity):
        """Number of protons in the nucleus of an atom."""
        is_a = [hasType.exactly(1, emmo.Integer)]

    class LatticeVector(emmo.PhysicalQuantity):
        """A vector that participitates defining the unit cell."""
        is_a = [hasUnit.exactly(1, Meter),
                hasType.exactly(3, emmo.Real)]

    class Spacegroup(emmo.DescriptiveProperty):
        """A spacegroup is the symmetry group off all symmetry operations
        that apply to a crystal structure.

        It is identifies by its Hermann-Mauguin symbol or space group
        number (and setting) in the International tables of
        Crystallography."""
        is_a = [hasType.exactly(1, emmo.String)]
        pass

    class Plasticity(emmo.PhysicalQuantity):
        """Describes Yield stress and material hardening."""
        is_a = [hasUnit.exactly(1, Pascal),
                hasType.min(2, emmo.Real)]

    class TractionSeparation(Pressure):
        """The force required to separate two materials a certain distance per
        interface area.  Hence, traction_separation is a curve, that
        numerically can be represented as a series of (force,
        separation_distance) pairs."""
        is_a = [hasUnit.exactly(1, Pascal),
                hasType.min(4, emmo.Real)]

    class LoadCurve(Pressure):
        """A measure for the displacement of a material as function of the
        appliced force."""
        is_a = [hasUnit.exactly(1, Pascal),
                hasType.min(4, emmo.Real)]

    #
    # Subdimensional
    # ==============
    class Interface(emmo.Plane):
        """A 2D surface associated with a boundary.

        Commonly referred to as "interface".
        """
        is_a = [emmo.hasProperty.exactly(1, Area),
                emmo.hasProperty.exactly(1, TractionSeparation)]

    #
    # Material classes
    # ================

    # Crystallography-related classes
    # -------------------------------
    class CrystalUnitCell(emmo.Mesoscopic):
        """A volume defined by the 3 unit cell vectors.  It contains the atoms
        constituting the unit cell of a crystal."""
        is_a = [emmo.hasSpatialDirectPart.some(emmo.BondedAtom),
                emmo.hasSpatialPart.some(Interface),
                emmo.hasProperty.exactly(3, LatticeVector),
                emmo.hasProperty.exactly(1, StiffnessTensor)]

    class Crystal(emmo.Solid):
        """A periodic crystal structure."""
        is_a = [emmo.hasSpatialDirectPart.only(CrystalUnitCell),
                emmo.hasProperty.exactly(1, Spacegroup)]

    # Add some properties to our atoms
    emmo.BondedAtom.is_a.append(emmo.hasProperty.exactly(1, AtomicNumber))
    emmo.BondedAtom.is_a.append(emmo.hasProperty.exactly(1, Position))

    # Continuum
    # ---------
    class Boundary(emmo.Continuum):
        """A boundary is a 4D region of spacetime shared by two material
        entities."""
        equivalient_to = [emmo.hasSpatialDirectPart.exactly(2, emmo.Continuum)]
        is_a = [emmo.hasSpatialPart.exactly(1, Interface)]

    class Phase(emmo.Continuum):
        """A phase is a continuum in which properties are homogeneous and can
        have different state of matter."""
        is_a = [emmo.hasProperty.exactly(1, StiffnessTensor),
                emmo.hasProperty.exactly(1, Plasticity)]

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
            emmo.hasProperty.exactly(1, LoadCurve)]

    #
    # Models
    # ======


# Sync attributes to make sure that all classes get a `label` and to
# include the docstrings in the comments
onto.sync_attributes()


# Run the reasoner
#onto.sync_reasoner()


# Save our new EMMO-based ontology.
#
# It seems that owlready2 by default is appending to the existing
# ontology.  To get a clean version, we simply delete the owl file if
# it already exists.
owlfile = 'usercase_ontology.owl'
if os.path.exists(owlfile):
    os.remove(owlfile)
onto.save(owlfile)
