from ontopy import get_ontology
from ontopy.manchester import evaluate
from owlready2 import And, Or, Not, Inverse


emmo = get_ontology().load()


def check(s, expected):
    r = evaluate(emmo, s)
    print(s, "-->", r)
    assert repr(r) == repr(expected)


def test_manchester():
    check("Item", emmo.Item)
    check("not Item", Not(emmo.Item))
    check("not not Item", emmo.Item)
    check("not (not Item)", Not(Not(emmo.Item)))
    check("hasPart some Atom", emmo.hasPart.some(emmo.Atom))
    check("Atom and not Molecule", emmo.Atom & Not(emmo.Molecule))
    check("Atom and (not Molecule)", emmo.Atom & Not(emmo.Molecule))
    check("not Atom and Molecule", Not(emmo.Atom) & emmo.Molecule)
    check("(not Atom) and Molecule", Not(emmo.Atom) & emmo.Molecule)
    check("inverse hasPart some Atom", Inverse(emmo.hasPart).some(emmo.Atom))
    check("inverse(hasPart) some Atom", Inverse(emmo.hasPart).some(emmo.Atom))
    check("not hasPart some Atom", Not(emmo.hasPart.some(emmo.Atom)))
    check("not (hasPart some Atom)", Not(emmo.hasPart.some(emmo.Atom)))
    check("hasPart some (not Atom)", emmo.hasPart.some(Not(emmo.Atom)))
    check("hasPart some not Atom", emmo.hasPart.some(Not(emmo.Atom)))
    check("not hasPart some not Atom", Not(emmo.hasPart.some(Not(emmo.Atom))))
    check(
        "hasPart only (inverse hasPart some not Atom)",
        emmo.hasPart.only(Inverse(emmo.hasPart).some(Not(emmo.Atom))),
    )
    check(
        "hasPart only inverse hasPart some not Atom",
        emmo.hasPart.only(Inverse(emmo.hasPart).some(Not(emmo.Atom))),
    )
    check(
        "Atom and Molecule and Proton",
        emmo.Atom & (emmo.Molecule & emmo.Proton),
    )
    check(
        "Atom and (Molecule and Proton)",
        emmo.Atom & (emmo.Molecule & emmo.Proton),
    )
    check(
        "(Atom and Molecule) or Proton",
        (emmo.Atom & emmo.Molecule) | emmo.Proton,
    )
