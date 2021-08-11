from emmo import World
from emmo.utils import write_catalog
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
emmopath = ('https://raw.githubusercontent.com/emmo-repo/emmo-repo.github.io/'
            'master/versions/1.0.0-beta/emmo-inferred-chemistry2.ttl')
emmo = world.get_ontology(emmopath).load()
emmo.sync_python_names()

emmo.base_iri = emmo.base_iri.rstrip('/#')
catalog_mappings = {emmo.base_iri: emmopath}

# Create new ontology

onto = world.get_ontology('http://emmo.info/emmo/domain/periodic-table#')
onto.base_iri = 'http://emmo.info/emmo#'
onto.imported_ontologies.append(emmo)
onto.sync_python_names()

# Make classes required that are not already in EMMO
with onto:

    class EMMOAgreedQuantativePropertyAssignment(
            onto.AgreedQuantitativePropertyAssignment):
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

        assignment = EMMOAgreedQuantativePropertyAssignment(
            lname + 'AtomicAtomicNumberAssignment')
        assignment.hasParticipant = [EMMOCommittee, at, number]
        print(
            at.hasConventionalQuantity[0].hasQuantityValue[0].hasNumericalData,
            at.is_a[0].hasChemicalSymbol,
            at.name,
            at.hasConventionalQuantity[1].hasQuantityValue[0].hasNumericalData)

# Save new ontology as owl
onto.sync_attributes(name_policy='uuid', name_prefix='EMMO_')
version_iri = "http://emmo.info/emmo/1.0.0-beta/domain/periodic-table"
onto.set_version(version_iri=version_iri)
onto.dir_label = False
thisdir = os.path.abspath(os.path.dirname(__file__))
catalog_mappings[version_iri] = 'periodic-table.ttl'

onto.metadata.abstract.append(en(
    'The periodic table domain ontology provide a simple reference '
    'implementation of all atoms in the periodic table with a few '
    'selected conventional properties.  It is ment as both an example '
    'for other domain ontologies as well as a useful assert by itself. '
    'Periodic table is released under the Creative Commons Attribution 4.0 '
    'International license (CC BY 4.0).'))

onto.metadata.title.append(en('Periodic table'))
onto.metadata.creator.append(en('Jesper Friis'))
onto.metadata.contributor.append(en('SINTEF'))
onto.metadata.creator.append(en('Emanuele Ghedini'))
onto.metadata.contributor.append(en('University of Bologna'))
onto.metadata.publisher.append(en('EMMC ASBL'))
onto.metadata.license.append(en(
    'https://creativecommons.org/licenses/by/4.0/legalcode'))
version = '1.0.0-beta'
onto.metadata.versionInfo.append(en(version))
onto.metadata.comment.append(en(
    'The EMMO requires FacT++ reasoner plugin in order to visualize all'
    'inferences and class hierarchy (ctrl+R hotkey in Protege).'))
onto.metadata.comment.append(en(
    'This ontology is generated with data from the ASE Python package.'))
onto.metadata.comment.append(en(
    'Contacts:\n'
    'Gerhard Goldbeck\n'
    'Goldbeck Consulting Ltd (UK)\n'
    'email: gerhard@goldbeck-consulting.com\n'
    '\n'
    'Emanuele Ghedini\n'
    'University of Bologna (IT)\n'
    'email: emanuele.ghedini@unibo.it'
    ))
onto.save(os.path.join(thisdir, 'periodic-table.ttl'), overwrite=True)
write_catalog(catalog_mappings)
