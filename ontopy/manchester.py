"""Evaluate Manchester syntax

This module compiles restrictions and logical constructs in Manchester
syntax into Owlready2 classes. The main function in this module is
`manchester.evaluate()`, see its docstring for usage example.

Pyparsing is used under the hood for parsing.
"""
# pylint: disable=unused-import,wrong-import-order
import pyparsing as pp
import ontopy  # noqa F401 -- ontopy must be imported before owlready2
import owlready2


GRAMMAR = None  # Global cache


def manchester_expression():
    """Returns pyparsing grammer for a Manchester expression.

    This function is mostly for internal use.

    See also: https://www.w3.org/TR/owl2-manchester-syntax/
    """
    # pylint: disable=global-statement,invalid-name,expression-not-assigned
    global GRAMMAR
    if GRAMMAR:
        return GRAMMAR

    # Subset of the Manchester grammar for expressions
    # It is based on https://www.w3.org/TR/owl2-manchester-syntax/
    # but allows logical constructs within restrictions (like Protege)
    ident = pp.Word(pp.alphas + "_", pp.alphanums + "_", asKeyword=True)
    uint = pp.Word(pp.nums)
    logOp = pp.oneOf(["and", "or"], asKeyword=True)
    expr = pp.Forward()
    restriction = pp.Forward()
    primary = pp.Keyword("not")[...] + (
        restriction | ident("cls") | pp.nestedExpr("(", ")", expr)
    )
    objPropExpr = (
        pp.Literal("inverse")
        + pp.Suppress("(")
        + ident("objProp")
        + pp.Suppress(")")
        | pp.Literal("inverse") + ident("objProp")
        | ident("objProp")
    )
    restriction << (
        objPropExpr + pp.Keyword("some") + expr
        | objPropExpr + pp.Keyword("only") + expr
        | objPropExpr + pp.Keyword("Self")
        | objPropExpr + pp.Keyword("value") + ident("individual")
        | objPropExpr + pp.Keyword("min") + uint + expr
        | objPropExpr + pp.Keyword("max") + uint + expr
        | objPropExpr + pp.Keyword("exactly") + uint + expr
    )
    expr << primary + (logOp("op") + expr)[...]

    GRAMMAR = expr
    return expr


class ManchesterError(Exception):
    """Raised on invalid Manchester notation."""


def evaluate(ontology: owlready2.Ontology, expr: str):
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
    # pylint: disable=invalid-name,no-else-return,too-many-return-statements
    # pylint: disable=too-many-branches
    def _eval(r):
        """Recursively evaluate expression produced by pyparsing into an
        Owlready2 construct."""

        def fneg(x):
            """Negates the argument if `neg` is true."""
            return owlready2.Not(x) if neg else x

        if isinstance(r, str):  # r is atomic, returns its owlready2 repr
            return ontology[r]

        neg = False  # whether the expression starts with "not"
        while r[0] == "not":
            r.pop(0)  # strip off the "not" and proceed
            neg = not neg

        if len(r) == 1:  # r is either a atomic or a parenthesised
            # subexpression that should be further evaluated
            if isinstance(r[0], str):
                return fneg(ontology[r[0]])
            else:
                return fneg(_eval(r[0]))
        elif r.op:  # r contains a logical operator: and/or
            ops = {"and": owlready2.And, "or": owlready2.Or}
            if r.op not in ops:
                raise ManchesterError(f"unexpected logical operator: {r.op}")
            op = ops[r.op]
            if len(r) == 3:
                return op([fneg(_eval(r[0])), _eval(r[2])])
            else:
                arg1 = fneg(_eval(r[0]))
                r.pop(0)
                r.pop(0)
                return op([arg1, _eval(r)])
        elif r.objProp:  # r is a restriction
            if r[0] == "inverse":
                r.pop(0)
                prop = owlready2.Inverse(ontology[r[0]])
            else:
                prop = ontology[r[0]]
            rtype = r[1]
            if rtype == "Self":
                return fneg(prop.has_self())
            r.pop(0)
            r.pop(0)
            f = getattr(prop, rtype)
            if rtype in ("some", "only"):
                return fneg(f(_eval(r)))
            elif rtype in ("min", "max", "exactly"):
                cardinality = r.pop()
                return fneg(f(cardinality, _eval(r)))
            else:
                raise ManchesterError(f"invalid restriction type: {rtype}")
        else:
            raise ManchesterError(f"invalid expression: {r}")

    grammar = manchester_expression()
    return _eval(grammar.parseString(expr))
