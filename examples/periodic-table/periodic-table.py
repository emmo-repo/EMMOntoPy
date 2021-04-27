from emmo import World
import ase
import types
import owlready2
import rdflib
from rdflib.namespace import OWL, DCTERMS, RDFS
from rdflib import URIRef, Literal
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
onto.save(os.path.join(thisdir,'periodic-table.owl'), overwrite=True)

# Do final manipulation with rdflib
BASE = rdflib.Namespace('http://emmo.info/emmo/domain/periodic-table')

g = rdflib.Graph()
g.bind('skos', rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#'))
g.bind('', rdflib.term.URIRef('http://emmo.info/emmo#'))
g.parse('periodic-table.owl', format='xml')

# Add version to imported ontologies
version = '1.0.0-beta'
for s, p, o in g.triples((None, OWL.imports, None)):
    o2 = URIRef(o.replace('http://emmo.info/emmo/',
                          'http://emmo.info/emmo/%s/' % version))
    g.remove((s, p, o))
    g.add((s, p, o2))

# Add ontology annotations
g.add((URIRef(BASE), OWL.versionInfo, Literal(version)))
g.add((URIRef(BASE), DCTERMS.title, Literal('Periodic table', lang='en')))
g.add((URIRef(BASE), DCTERMS.creator, Literal('Jesper Friis')))
g.add((URIRef(BASE), DCTERMS.contributor, Literal('SINTEF')))
g.add((URIRef(BASE), DCTERMS.creator, Literal('Emanuele Ghedini')))
g.add((URIRef(BASE), DCTERMS.contributor, Literal('University of Bologne')))
g.add((URIRef(BASE), DCTERMS.publisher, Literal('EMMC ASBL')))
g.add((URIRef(BASE), DCTERMS.license,
       Literal('https://creativecommons.org/licenses/by/4.0/legalcode')))

g.add((URIRef(BASE), DCTERMS.abstract,
       Literal('''\
The periodic table domain ontology provide a simple reference \
implementation of all atoms in the periodic table with a few \
selected conventional properties.  It is ment as both an example \
for other domain ontologies as well as a useful assert by itself.
Periodic table is released under the Creative Commons Attribution 4.0 \
International license (CC BY 4.0).
''', lang='en')))

g.add((URIRef(BASE), RDFS.comment,
       Literal('''\
The EMMO requires FacT++ reasoner plugin in order to visualize all \
inferences and class hierarchy (ctrl+R hotkey in Protege).
''', lang='en')))

g.add((URIRef(BASE), RDFS.comment,
       Literal('''\
This ontology is generated with data from the ASE Python package.
''', lang='en')))

g.add((URIRef(BASE), RDFS.comment,
       Literal('''\
Contacts:
Gerhard Goldbeck
Goldbeck Consulting Ltd (UK)
email: gerhard@goldbeck-consulting.com
Emanuele Ghedini
University of Bologna (IT)
email: emanuele.ghedini@unibo.it
''', lang='en')))


# Store in turtle format
g.serialize(destination='periodic-table.ttl', format='turtle', base=BASE)
