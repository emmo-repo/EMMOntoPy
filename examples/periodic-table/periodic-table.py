from emmo import World
import ase
import types
import owlready2
import os


# define function that returns a string in English in owlready2
def en(s):
    """Returns `s` as an English location string."""
    return owlready2.locstr(s, lang='en')


# Load emmo
world = World()  # to make it extensible for when an ontology gets very large
emmo = world.get_ontology(
        'https://raw.githubusercontent.com/emmo-repo/EMMO/periodic-table/'
        'middle/middle.ttl').load()
emmo.sync_python_names()

# Create new ontology
onto = world.get_ontology('http://emmo.info/emmo/domain/periodic-table#')
onto.base_iri = 'http://emmo.info/emmo#'
onto.imported_ontologies.append(emmo)
onto.sync_python_names()

# Make classes required that are not already in EMMO
with onto:

    class EMMOConventionalQuantityAssignment(
            onto.ConventionalQuantitativePropertyAssignment):
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
    EMMOCommittee = onto.Interpreter('EMMOCommittee')

    for Z, (s, name, m) in enumerate(zip(
            ase.data.chemical_symbols,
            ase.data.atomic_names,
            ase.data.atomic_masses_iupac2016)):
        if not name:
            continue  # skip Z=0
        lname = name.lower()

        # Make a new class of this atom type
        AtomClass = types.new_class(name + 'Atom', (onto.Atom, ))
        AtomClass.elucidation.append(en('Atom subclass for %s.' % lname))
        AtomClass.is_a.append(hasChemicalSymbol.value(s))

        # Set atomic number
        z = onto.Integer(lname + 'AtomicNumberValue',
                         hasNumericalData=int(Z))
        number = EMMOAtomicNumber(lname + 'AtomicNumber',
                                  hasReferenceUnit=[onto.UnitOne],
                                  hasQuantityValue=[z])

        # Set mass
        mval = onto.Real(lname + 'AtomicMassValue',
                         hasNumericalData=float(m))
        mass = EMMOAtomicMass(lname + 'AtomicMass')
        mass.hasReferenceUnit = [onto.Dalton]
        mass.hasQuantityValue = [mval]

        # make individual of this atom type and assign conventional quantities
        at = AtomClass(lname,
                       hasConventionalQuantity=[number, mass])

        assignment = EMMOConventionalQuantityAssignment(
            lname + 'AtomicAtomicNumberAssignment')
        assignment.hasParticipant = [EMMOCommittee, at, number]
        print(
            at.hasConventionalQuantity[0].hasQuantityValue[0].hasNumericalData,
            at.is_a[0].hasChemicalSymbol[0],
            at.name,
            at.hasConventionalQuantity[1].hasQuantityValue[0].hasNumericalData)

# Save new ontology as owl
onto.sync_attributes(name_policy='uuid', name_prefix='EMMO_')
onto.set_version(
    version_iri="http://emmo.info/emmo/1.0.0-beta/domain/periodic-table")
onto.dir_label = False
thisdir = os.path.abspath(os.path.dirname(__file__))

onto.metadata.abstract.append(en(
    'The periodic table domain ontology provide a simple reference '
    'implementation of all atoms in the periodic table with a few '
    'selected conventional properties.  It is ment as both an example '
    'for other domain ontologies as well as a useful assert by itself. '
    'Periodic table is released under the Creative Commons Attribution 4.0 '
    'International license (CC BY 4.0).'))


onto.save(os.path.join(thisdir, 'periodic-table.ttl'), overwrite=True)
