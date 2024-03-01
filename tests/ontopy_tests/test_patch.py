"""Tests Owlready2 patches implemented in ontopy/patch.py

"""

import re

import pytest

from ontopy import get_ontology
from owlready2 import owl, Inverse

from utilities import setassert


def test_get_by_label_onto(emmo: "Ontology") -> None:
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
    setassert(
        emmo.Atom.get_annotations(all=True).keys(),
        {
            "qualifiedCardinality",
            "minQualifiedCardinality",
            "prefLabel",
            "abstract",
            "hiddenLabel",
            "etymology",
            "altLabel",
            "example",
            "elucidation",
            "OWLDLRestrictedAxiom",
            "wikipediaReference",
            "conceptualisation",
            "logo",
            "comment",
            "dbpediaReference",
            "definition",
            "VIMTerm",
            "creator",
            "iupacReference",
            "contact",
            "omReference",
            "ISO9000Reference",
            "ISO80000Reference",
            "qudtReference",
            "contributor",
            "license",
            "ISO14040Reference",
            "figure",
            "title",
            "publisher",
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
    assert (
        emmo.wikipediaReference
    )  # Check that wikipediaReference is in ontology
    assert (
        emmo.Atom.wikipediaReference == []
    )  # Check that wikipediaReference can be acceses as attribute


def test_get_indirect_is_a() -> None:
    import re
    from ontopy import get_ontology

    emmo = get_ontology("emmo-development").load()
    assert any(
        re.match("^emmo.*\.hasDimensionString.value(.*)$", str(e))
        for e in emmo.MicroPascal.get_indirect_is_a()
    )
    assert all(
        re.match("^emmo.*\.Item$", str(e)) is None
        for e in emmo.MicroPascal.get_indirect_is_a()
    )
    assert any(
        re.match("^emmo.*\.Item$", str(e))
        for e in emmo.MicroPascal.get_indirect_is_a(skip_classes=False)
    )


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
