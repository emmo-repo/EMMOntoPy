"""Tests Owlready2 patches implemented in ontopy/patch.py

Implemented as a script, such that it easy to understand and use for debugging.
"""
from ontopy import get_ontology

from owlready2 import owl, Inverse


emmo = get_ontology().load()


# Test some ThingClass extensions implemented in patch.py
assert emmo.Atom.get_preferred_label() == "Atom"

assert emmo.Atom.get_parents() == {
    emmo.CausalSystem,
    emmo.CompositeParticle,
    emmo.MolecularEntity,
}

assert set(emmo.Atom.get_annotations().keys()) == {
    "prefLabel",
    "altLabel",
    "elucidation",
}


# Test item access/assignment/deletion for ThingClass
assert emmo.Atom["altLabel"] == ["ChemicalElement"]

emmo.Atom["altLabel"] = "Element"
assert emmo.Atom["altLabel"] == ["ChemicalElement", "Element"]

del emmo.Atom["altLabel"]
assert emmo.Atom["altLabel"] == []

emmo.Atom["altLabel"] = "ChemicalElement"
assert emmo.Atom["altLabel"] == ["ChemicalElement"]


# TODO: Fix disjoint_with().
# It seems not to take into account disjoint unions.
# assert set(emmo.Collection.disjoint_with()) == {emmo.Item}

assert set(str(s) for s in emmo.CausalChain.get_indirect_is_a()) == set(
    str(s)
    for s in {
        Inverse(emmo.hasPart).value(emmo.universe),
        emmo.CausalObject,
        emmo.Particle,
        emmo.hasPart.some(emmo.Quantum),
        emmo.hasTemporalPart.only(emmo.CausalChain | emmo.Quantum),
        emmo.hasTemporalPart.some(emmo.CausalChain | emmo.Quantum),
    }
)
assert set(
    str(s) for s in emmo.CausalChain.get_indirect_is_a(skip_classes=False)
) == set(
    str(s)
    for s in {
        Inverse(emmo.hasPart).value(emmo.universe),
        emmo.CausalObject,
        emmo.EMMO,
        emmo.Item,
        emmo.Particle,
        emmo.hasPart.some(emmo.Quantum),
        emmo.hasTemporalPart.only(emmo.CausalChain | emmo.Quantum),
        emmo.hasTemporalPart.some(emmo.CausalChain | emmo.Quantum),
        owl.Thing,
    }
)

assert emmo.Atom.is_defined == False
assert emmo.Holistic.is_defined == True
