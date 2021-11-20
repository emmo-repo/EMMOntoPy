from ontopy import get_ontology
from ontopy.manchester import evaluate
from owlready2 import And, Or, Not, Inverse


def test(s, expected, no_traceback=True):
    if no_traceback:
        try:
            r = evaluate(emmo, s)
        except pp.ParseException as e:
            print('**', s, f'-- ParseError: {e}')
        except Exception as e:
            print('**', s, f'-- EvalError: {e}')
    else:
        r = evaluate(emmo, s)

    if repr(r) == repr(expected):
        print(s, f'--> {r}')
    else:
        print('**', s, f'-- Failed: {r} != {expected}')


emmo = get_ontology().load()

test('Item', emmo.Item)
test('not Item', Not(emmo.Item))
test('not not Item', emmo.Item)
test('hasPart some Atom', emmo.hasPart.some(emmo.Atom))
test('Atom and not Molecule', emmo.Atom & Not(emmo.Molecule))
test('Atom and (not Molecule)', emmo.Atom & Not(emmo.Molecule))
test('not Atom and Molecule', Not(emmo.Atom) & emmo.Molecule)
test('(not Atom) and Molecule', Not(emmo.Atom) & emmo.Molecule)
test('inverse hasPart some Atom', Inverse(emmo.hasPart).some(emmo.Atom))
test('inverse(hasPart) some Atom', Inverse(emmo.hasPart).some(emmo.Atom))
test('not hasPart some Atom', Not(emmo.hasPart.some(emmo.Atom)))
test('not (hasPart some Atom)', Not(emmo.hasPart.some(emmo.Atom)))
test('hasPart some (not Atom)', emmo.hasPart.some(Not(emmo.Atom)))
test('hasPart some not Atom', emmo.hasPart.some(Not(emmo.Atom)))
test('not hasPart some not Atom', Not(emmo.hasPart.some(Not(emmo.Atom))))
test('hasPart only (inverse hasPart some not Atom)',
     emmo.hasPart.only(Inverse(emmo.hasPart).some(Not(emmo.Atom))))
test('hasPart only inverse hasPart some not Atom',
     emmo.hasPart.only(Inverse(emmo.hasPart).some(Not(emmo.Atom))))
