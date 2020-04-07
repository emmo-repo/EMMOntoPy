#!/usr/bin/env python3
import sys
import os
import itertools

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology  # noqa: E402, F401

import owlready2  # noqa: E402, F401


emmo = get_ontology()
emmo.load()
# emmo.sync_reasoner()


onto = get_ontology('onto.owl')
onto.imported_ontologies.append(emmo)
onto.base_iri = 'http://emmo.info/examples/test#'

with onto:

    class Hydrogen(emmo.Atom):
        pass

    class Oxygen(emmo.Atom):
        pass

    class H2O(emmo.Molecule):
        """Water molecule."""
        emmo.hasSpatialDirectPart.exactly(2, Hydrogen)
        emmo.hasSpatialDirectPart.exactly(1, Oxygen)

    # Create some
    H1 = Hydrogen()
    H2 = Hydrogen()
    O = Oxygen()  # noqa: E741
    w = H2O()
    w.hasSpatialDirectPart = [H1, H2,  O]


onto.sync_attributes(name_policy='sequential', name_prefix='myonto_')
assert 'myonto_0' in onto
assert 'myonto_6' in onto

onto.sync_attributes(name_policy='uuid', name_prefix='onto_')
assert w.name.startswith('onto_')
assert len(w.name) == 5 + 36


# Remove all traces of onto such that they do not mess up other tests
# when running pytest
for e in itertools.chain(onto.classes(), onto.individuals()):
    owlready2.destroy_entity(e)
