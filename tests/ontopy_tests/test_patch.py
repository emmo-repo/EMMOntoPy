"""Tests Owlready2 patches implemented in ontopy/patch.py

Implemented as a script, such that it easy to understand and use for debugging.
"""
import pytest

from ontopy import get_ontology

from owlready2 import owl, Inverse

from utilities import setassert

emmo = get_ontology().load()


# Test some ThingClass extensions implemented in patch.py
assert str(emmo.Atom.get_preferred_label()) == "Atom"

assert emmo.Atom.get_parents() == {emmo.MolecularEntity}

setassert(
    emmo.Atom.get_annotations().keys(),
    {
        "prefLabel",
        "altLabel",
        "elucidation",
        "comment",
    },
)


# Test item access/assignment/deletion for classes
setassert(emmo.Atom["altLabel"], {"ChemicalElement"})

with pytest.raises(KeyError):
    emmo.Atom["hasPart"]

emmo.Atom["altLabel"] = "Element"
setassert(emmo.Atom["altLabel"], {"ChemicalElement", "Element"})

del emmo.Atom["altLabel"]
assert emmo.Atom["altLabel"] == []

emmo.Atom.altLabel = "ChemicalElement"
assert emmo.Atom["altLabel"] == ["ChemicalElement"]


assert emmo.Atom.is_defined == False
assert emmo.Holistic.is_defined == True

# TODO: Fix disjoint_with().
# It seems not to take into account disjoint unions.
# assert set(emmo.Collection.disjoint_with()) == {emmo.Item}


# Comment out these tests for now because Owlready2 automatically converts
# `Inverse(emmo.hasPart)` to `emmo.isPartOf`.
#
# Also, check whether ancestors() does any inferences from disjoint unions, etc.
# If it does, it might be better to reley on ancestors() instead of implementing
# get_indirect_is_a() as a separate method
# assert emmo.CausalChain.get_indirect_is_a() == {
#    Inverse(emmo.hasPart).value(emmo.universe),
#    emmo.CausalParticle,
#    emmo.CausalStructure,
#    emmo.hasPart.some(emmo.Quantum),
#    emmo.hasTemporalPart.only(emmo.CausalPath | emmo.Quantum),
#    emmo.hasTemporalPart.some(emmo.CausalPath | emmo.Quantum),
# }
# assert emmo.CausalChain.get_indirect_is_a(skip_classes=False) == {
#    Inverse(emmo.hasPart).value(emmo.universe),
#    emmo.CausalObject,
#    emmo.EMMO,
#    emmo.Item,
#    emmo.Particle,
#    emmo.hasPart.some(emmo.Quantum),
#    emmo.hasTemporalPart.only(emmo.CausalChain | emmo.Quantum),
#    emmo.hasTemporalPart.some(emmo.CausalChain | emmo.Quantum),
#    owl.Thing,
# }
