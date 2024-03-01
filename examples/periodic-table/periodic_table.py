"""Periodic table example."""

# pylint: disable=import-error,too-few-public-methods,invalid-name
import os
import types

import ase

from ontopy import World
from ontopy.utils import write_catalog

import owlready2  # pylint: disable=wrong-import-order


# define function that returns a string in English in owlready2
def english(string):
    """Returns `s` as an English location string."""
    return owlready2.locstr(string, lang="en")


# Load emmo
world = World()  # to make it extensible for when an ontology gets very large
EMMO_PATH = (
    "https://raw.githubusercontent.com/emmo-repo/emmo-repo.github.io/"
    "master/versions/1.0.0-beta/emmo-inferred-chemistry2.ttl"
)
emmo = world.get_ontology(EMMO_PATH).load()
emmo.sync_python_names()

emmo.base_iri = emmo.base_iri.rstrip("/#")
catalog_mappings = {emmo.base_iri: EMMO_PATH}

# Create new ontology

onto = world.get_ontology("http://emmo.info/emmo/domain/periodic-table#")
onto.base_iri = "http://emmo.info/emmo#"
onto.imported_ontologies.append(emmo)
onto.sync_python_names()

# Make classes required that are not already in EMMO
with onto:

    class EMMOAgreedQuantativePropertyAssignment(
        onto.AgreedQuantitativePropertyAssignment
    ):
        """The class of conventional assignments performed by the EMMO
        Comittee."""

    class EMMOAtomicNumber(onto.AtomicNumber):
        """Atomic number declared by the EMMO committee as a conventional
        quantitative property."""

    class EMMOAtomicMass(onto.AtomicMass):
        """Atomic mass declared by the EMMO committee as a conventional
        quantitative property.
        Values taken from IUPAC2016.
        """

    class hasChemicalSymbol(onto.hasSymbolData):
        """Conventional chemical symbol of an atomic element."""

        range = [str]


with onto:
    # Define the interpreter (viewpoint)
    EMMOCommittee = onto.Interpreter("EMMOCommittee")

    for Z, (symbol, name, atomic_mass) in enumerate(
        zip(
            ase.data.chemical_symbols,
            ase.data.atomic_names,
            ase.data.atomic_masses_iupac2016,
        )
    ):
        if not name:
            continue  # skip Z=0
        lname = name.lower()

        # Make a new class of this atom type
        AtomClass = types.new_class(name + "Atom", (onto.Atom,))
        AtomClass.elucidation.append(english(f"Atom subclass for {lname}."))
        AtomClass.is_a.append(hasChemicalSymbol.value(symbol))

        # Set atomic number
        atomic_number = onto.Integer(
            lname + "AtomicNumberValue", hasNumericalData=int(Z)
        )
        number = EMMOAtomicNumber(
            lname + "AtomicNumber",
            hasReferenceUnit=[onto.UnitOne],
            hasQuantityValue=[atomic_number],
        )

        # Set mass
        mval = onto.Real(
            lname + "AtomicMassValue", hasNumericalData=float(atomic_mass)
        )
        mass = EMMOAtomicMass(lname + "AtomicMass")
        mass.hasReferenceUnit = [onto.Dalton]
        mass.hasQuantityValue = [mval]

        # make individual of this atom type and assign conventional quantities
        atom = AtomClass(lname, hasConventionalQuantity=[number, mass])

        assignment = EMMOAgreedQuantativePropertyAssignment(
            lname + "AtomicAtomicNumberAssignment"
        )
        assignment.hasParticipant = [EMMOCommittee, atom, number]
        print(
            atom.hasConventionalQuantity[0]
            .hasQuantityValue[0]
            .hasNumericalData,
            atom.is_a[0].hasChemicalSymbol,
            atom.name,
            atom.hasConventionalQuantity[1]
            .hasQuantityValue[0]
            .hasNumericalData,
        )

# Save new ontology as owl
onto.sync_attributes(name_policy="uuid", name_prefix="EMMO_")
VERSION_IRI = "http://emmo.info/emmo/1.0.0-beta/domain/periodic-table"
onto.set_version(version_iri=VERSION_IRI)
onto.dir_label = False
thisdir = os.path.abspath(os.path.dirname(__file__))
catalog_mappings[VERSION_IRI] = "periodic-table.ttl"

onto.metadata.abstract.append(
    english(
        "The periodic table domain ontology provide a simple reference "
        "implementation of all atoms in the periodic table with a few "
        "selected conventional properties.  It is ment as both an example "
        "for other domain ontologies as well as a useful assert by itself. "
        "Periodic table is released under the Creative Commons Attribution 4.0"
        " International license (CC BY 4.0)."
    )
)

onto.metadata.title.append(english("Periodic table"))
onto.metadata.creator.append(english("Jesper Friis"))
onto.metadata.contributor.append(english("SINTEF"))
onto.metadata.creator.append(english("Emanuele Ghedini"))
onto.metadata.contributor.append(english("University of Bologna"))
onto.metadata.publisher.append(english("EMMC ASBL"))
onto.metadata.license.append(
    english("https://creativecommons.org/licenses/by/4.0/legalcode")
)
VERSION = "1.0.0-beta"
onto.metadata.versionInfo.append(english(VERSION))
onto.metadata.comment.append(
    english(
        "The EMMO requires FacT++ reasoner plugin in order to visualize all"
        "inferences and class hierarchy (ctrl+R hotkey in Protege)."
    )
)
onto.metadata.comment.append(
    english("This ontology is generated with data from the ASE Python package.")
)
onto.metadata.comment.append(
    english(
        "Contacts:\n"
        "Gerhard Goldbeck\n"
        "Goldbeck Consulting Ltd (UK)\n"
        "email: gerhard@goldbeck-consulting.com\n"
        "\n"
        "Emanuele Ghedini\n"
        "University of Bologna (IT)\n"
        "email: emanuele.ghedini@unibo.it"
    )
)
onto.save(os.path.join(thisdir, "periodic-table.ttl"), overwrite=True)
write_catalog(catalog_mappings)
