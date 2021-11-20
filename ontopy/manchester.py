"""Evaluate Manchester syntax."""
import pyparsing as pp
import ontopy  # noqa F401 -- ontopy must be imported before owlready2
import owlready2


GRAMMAR = None  # Global cache


def manchester_expression():
    """Returns pyparsing grammer for a Manchester expression.

    See also: https://www.w3.org/TR/owl2-manchester-syntax/
    """
    global GRAMMAR
    if GRAMMAR:
        return GRAMMAR

    ident = pp.Word(pp.alphas + '_', pp.alphanums + '_', asKeyword=True)
    uint = pp.Word(pp.nums)
    logOp = pp.oneOf(['and', 'or'], asKeyword=True)
    expr = pp.Forward()
    restriction = pp.Forward()
    primary = pp.Keyword('not')[...] + (
        restriction | ident('cls') | pp.nestedExpr('(', ')', expr))
    objPropExpr = (
        pp.Literal('inverse') + pp.Suppress('(') + ident('objProp') +
        pp.Suppress(')') |
        pp.Literal('inverse') + ident('objProp') |
        ident('objProp'))
    restriction << (
        objPropExpr + pp.Keyword('some') + expr |
        objPropExpr + pp.Keyword('only') + expr |
        objPropExpr + pp.Keyword('Self') |
        objPropExpr + pp.Keyword('value') + ident('individual') |
        objPropExpr + pp.Keyword('min') + uint + expr |
        objPropExpr + pp.Keyword('max') + uint + expr |
        objPropExpr + pp.Keyword('exactly') + uint + expr)
    expr << primary + (logOp('op') + expr)[...]
    GRAMMAR = expr
    return expr


class ManchesterError(Exception):
    """Raised on invalid Manchester notation."""


def evaluate(ontology : owlready2.Ontology, expr : str):
    """Evaluate expression in Manchester syntax.

    Args:
        ontology: The ontology within which the expression will be evaluated.
        expr: Manchester expression to be evaluated.

    Returns:
        An Owlready2 construct that corresponds to the expression.

    Example:
    >>> from ontopy.manchester import evaluate
    >>> from ontopy import get_ontology
    >>> emmo = get_ontology.load()

    >>> restriction = evaluate(emmo, 'hasPart some Atom')
    >>> cls = evaluate(emmo, 'Atom')
    >>> expr = evaluate(emmo, 'Atom or Molecule')

    """
    def _eval(r):
        """Evaluate parsed expression."""
        def fneg(x):
            return owlready2.Not(x) if neg else x

        if isinstance(r, str):
            return ontology[r]

        neg = False
        while r[0] == 'not':
            r.pop(0)
            neg = not neg

        if len(r) == 1:
            if isinstance(r[0], str):
                return fneg(ontology[r[0]])
            else:
                return fneg(_eval(r[0]))
        elif r.op:
            ops = {'and': owlready2.And, 'or': owlready2.Or}
            if r.op not in ops:
                raise ManchesterError(f'unexpected logical operator: {r.op}')
            op = ops[r.op]
            if len(r) == 3:
                return op([fneg(_eval(r[0])), _eval(r[2])])
            else:
                arg1 = fneg(_eval(r[0]))
                r.pop(0)
                r.pop(0)
                return op([arg1, _eval(r)])
        elif r.objProp:
            if r[0] == 'inverse':
                r.pop(0)
                prop = owlready2.Inverse(ontology[r[0]])
            else:
                prop = ontology[r[0]]
            rtype = r[1]
            if rtype == 'Self':
                return fneg(prop.has_self())
            r.pop(0)
            r.pop(0)
            f = getattr(prop, rtype)
            if rtype in ('some', 'only'):
                return fneg(f(_eval(r)))
            elif rtype in ('min', 'max', 'exactly'):
                cardinality = r.pop()
                return fneg(f(cardinality, _eval(r)))
            else:
                raise ManchesterError(f'invalid restriction type: {rtype}')
        else:
            raise ManchesterError(f'invalid expression: {r}')

    grammar = manchester_expression()
    return _eval(grammar.parseString(expr))
