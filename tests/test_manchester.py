from ontopy import get_ontology
from ontopy.manchester import evaluate
from owlready2 import And, Or, Not, Inverse, locstr

from pathlib import Path


thisdir = Path(__file__).resolve().parent
ontopath = thisdir / "testonto" / "emmo" / "emmo-squashed.ttl"

emmo = get_ontology(ontopath).load()


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
    check(
        "(Atom and Molecule) or Proton",
        (emmo.Atom & emmo.Molecule) | emmo.Proton,
    )
    check(
        "inverse(hasPart) value universe",
        Inverse(emmo.hasPart).value(emmo.universe),
    )
    # literal data restriction
    check('hasSymbolValue value "hello"', emmo.hasSymbolValue.value("hello"))
    check("hasSymbolValue value 42", emmo.hasSymbolValue.value(42))
    check("hasSymbolValue value 3.14", emmo.hasSymbolValue.value(3.14))
    check(
        'hasSymbolValue value "abc"^^xsd:string',
        emmo.hasSymbolValue.value("abc"),
    )
    check(
        'hasSymbolValue value "hello"@en',
        emmo.hasSymbolValue.value(locstr("hello", "en")),
    )
    # Note that prefixes are now automatically set to name of file
    check(
        "emmo-squashed:hasPart some emmo-squashed:Atom",
        emmo.hasPart.some(emmo.Atom),
    )


if __name__ == "__main__":
    test_manchester()
