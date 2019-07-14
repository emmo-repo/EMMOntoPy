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
from emmo import get_ontology
from owlready2 import sync_reasoner_pellet

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
    class has_unit(emmo.has_part):
        """Associates a unit to a property."""
        pass

    class is_unit_for(emmo.is_part_of):
        """Associates a property to a unit."""
        inverse_property = has_unit

    class has_type(emmo.has_convention):
        """Associates a type (string, number...) to a property."""
        pass

    class is_type_of(emmo.is_convention_for):
        """Associates a property to a type (string, number...)."""
        inverse_property = has_type

    #
    # Types
    # =====
    class integer(emmo.number):
        pass

    class real(emmo.number):
        pass

    class string(emmo.number): #['well-formed']): #FIXME Ontology "emmo-all-inferred" has no such label: well-formed
        pass

    #
    # Units
    # =====
    class SI_unit(emmo.measurement_unit):
        """Base class for all SI units."""
        pass

    class meter(SI_unit):
        label = ['m']

    class square_meter(SI_unit):
        label = ['m²']

    class pascal(SI_unit):
        label = ['Pa']


    #
    # Properties
    # ==========
    class position(emmo.physical_quantity):
        """Spatial position of an physical entity."""
        is_a = [has_unit.exactly(1, meter),
                has_type.exactly(3, real)]

    class area(emmo.physical_quantity):
        """Area of a surface."""
        is_a = [has_unit.exactly(1, square_meter),
                has_type.exactly(1, real)]

    class pressure(emmo.physical_quantity):
        """The force applied perpendicular to the surface of an object per
        unit area."""
        is_a = [has_unit.exactly(1, pascal),
                has_type.exactly(1, real)]

    class stiffness_tensor(pressure):
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
        is_a = [has_unit.exactly(1, pascal),
                has_type.exactly(36, real)]

    class atomic_number(emmo.physical_quantity):
        """Number of protons in the nucleus of an atom."""
        is_a = [has_type.exactly(1, integer)]

    class lattice_vector(emmo.physical_quantity):
        """A vector that participitates defining the unit cell."""
        is_a = [has_unit.exactly(1, meter),
                has_type.exactly(3, real)]

    class spacegroup(emmo.descriptive_property):
        """A spacegroup is the symmetry group off all symmetry operations
        that apply to a crystal structure.

        It is identifies by its Hermann-Mauguin symbol or space group
        number (and setting) in the International tables of
        Crystallography."""
        is_a = [has_type.exactly(1, string)]
        pass

    class plasticity(emmo.physical_quantity):
        """Describes Yield stress and material hardening."""
        is_a = [has_unit.exactly(1, pascal),
                has_type.min(2, real)]

    class traction_separation(pressure):
        """The force required to separate two materials a certain distance per
        interface area.  Hence, traction_separation is a curve, that
        numerically can be represented as a series of (force,
        separation_distance) pairs."""
        is_a = [has_unit.exactly(1, pascal),
                has_type.min(4, real)]

    class load_curve(pressure):
        """A measure for the displacement of a material as function of the
        appliced force."""
        is_a = [has_unit.exactly(1, pascal),
                has_type.min(4, real)]

    #
    # Subdimensional
    # ==============
    class interface(emmo.surface):
        """A 2D surface associated with a boundary.

        Commonly referred to as "interface".
        """
        is_a = [emmo.has_property.exactly(1, area),
                emmo.has_property.exactly(1, traction_separation)]



    #
    # Material classes
    # ================

    # Crystallography-related classes
    # -------------------------------
    class crystal_unit_cell(emmo.mesoscopic):
        """A volume defined by the 3 unit cell vectors.  It contains the atoms
        constituting the unit cell of a crystal."""
        is_a = [emmo.has_spatial_direct_part.some(emmo['e-bonded_atom']),
                emmo.has_space_slice.some(interface),
                emmo.has_property.exactly(3, lattice_vector),
                emmo.has_property.exactly(1, stiffness_tensor)]

    class crystal(emmo.solid):
        """A periodic crystal structure."""
        is_a = [emmo.has_spatial_direct_part.only(crystal_unit_cell),
                emmo.has_property.exactly(1, spacegroup)]

    # Add some properties to our atoms
    emmo['e-bonded_atom'].is_a.append(emmo.has_property.exactly(1, atomic_number))
    emmo['e-bonded_atom'].is_a.append(emmo.has_property.exactly(1, position))

    # Continuum
    # ---------
    class boundary(emmo.state):
        """A boundary is a 4D region of spacetime shared by two material
        entities."""
        equivalient_to = [emmo.has_spatial_direct_part.exactly(2, emmo.state)]
        is_a = [emmo.has_space_slice.exactly(1, interface)]

    class phase(emmo.continuum):
        """A phase is a continuum in which properties are homogeneous and can
        have different state of matter."""
        is_a = [emmo.has_property.exactly(1, stiffness_tensor),
                emmo.has_property.exactly(1, plasticity)]

    class rve(emmo.continuum):
        """Representative volume element.  The minimum volume that is
        representative for the system in question."""
        is_a = [emmo.has_spatial_direct_part.only(phase | boundary)]

    class welded_component(emmo.component):
        """A welded component consisting of two materials welded together
        using a third welding material.  Hence it has spatial direct
        parts 3 materials and two boundaries."""
        is_a = [
            emmo.has_spatial_direct_part.exactly(3, emmo.material),
            emmo.has_spatial_direct_part.exactly(2, boundary),
            emmo.has_property.exactly(1, load_curve)]


    #
    # Models
    # ======




# Sync attributes to make sure that all classes get a `label` and to
# include the docstrings in the comments
onto.sync_attributes()


# Sync the reasoner - we use Pellet here becuse HermiT is very slow
sync_reasoner_pellet([onto])


# Save our new EMMO-based ontology.
#
# It seems that owlready2 by default is appending to the existing
# ontology.  To get a clean version, we simply delete the owl file if
# it already exists.
owlfile = 'usercase_ontology.owl'
import os
if os.path.exists(owlfile):
    os.remove(owlfile)
onto.save(owlfile)
