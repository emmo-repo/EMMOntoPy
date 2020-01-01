"""Some generic utility functions.
"""
import re

import owlready2


def asstring(expr, link='{name}', n=0):
    """Returns a string representation of `expr`, which may be an entity,
    restriction, or logical expression of these.  `link` is a format
    string for formatting references to entities or relations.  It may
    contain the keywords "name" and "url".
    `n` is the recursion depth and only intended for internal use.
    """
    def fmt(e):
        """Returns the formatted label of `e`."""
        name = str(e.label.first() if hasattr(e, 'label') and e.label else e)
        if re.match(r'^[a-z]+://', name):
            return link.format(name=name, url=name, lowerurl=name.lower())
        if hasattr(e, 'label') and e.label:
            name = e.label.first()
            url = name if re.match(r'^[a-z]+://', name) else '#' + name
            return link.format(name=name, url=url, lowerurl=url.lower())
        elif re.match(r'^[a-z]+://', str(e)):
            return link.format(name=e, url=e, lowerurl=e.lower())
        else:
            return str(e).replace('owl.', 'owl:')

    if isinstance(expr, str):
        # return link.format(name=expr)
        return fmt(expr)
    elif isinstance(expr, owlready2.Restriction):
        rlabel = owlready2.class_construct._restriction_type_2_label[expr.type]
        if not rlabel:
            s = '%s %s'
        elif expr.type in (owlready2.MIN, owlready2.MAX, owlready2.EXACTLY):
            s = '(%%s %s %d %%s)' % (rlabel, expr.cardinality)
        elif expr.type in (owlready2.SOME, owlready2.ONLY,
                           owlready2.VALUE, owlready2.HAS_SELF):
            s = '(%%s %s %%s)' % rlabel
        else:
            print('*** WARNING: unknown relation', expr, rlabel)
            s = '(%%s %s %%s)' % rlabel
        return s % (fmt(expr.property), asstring(expr.value, link, n + 1))
    elif isinstance(expr, owlready2.Or):
        s = '%s' if n == 0 else '(%s)'
        return s % ' or '.join([asstring(c, link, n + 1)
                                for c in expr.Classes])
    elif isinstance(expr, owlready2.And):
        s = '%s' if n == 0 else '(%s)'
        return s % ' and '.join([asstring(c, link, n + 1)
                                 for c in expr.Classes])
    elif isinstance(expr, owlready2.Not):
        return 'not %s' % asstring(expr.Class, link, n + 1)
    elif isinstance(expr, owlready2.ThingClass):
        return fmt(expr)
    elif isinstance(expr, owlready2.PropertyClass):
        return fmt(expr)
    elif isinstance(expr, owlready2.Thing):  # instance (individual)
        return fmt(expr)
    elif isinstance(expr, bool):
        return repr(expr)
    elif isinstance(expr, owlready2.class_construct.Inverse):
        return fmt(expr)
    elif isinstance(expr, owlready2.disjoint.AllDisjoint):
        return fmt(expr)
    else:
        raise RuntimeError('Unknown expression: %r (type: %r)' % (
            expr, type(expr)))


def camelsplit(s):
    """Splits CamelCase string `s` before upper case letters (except
    if there is a sequence of upper case letters)."""
    if len(s) < 2:
        return s
    result = []
    prev_lower = False
    prev_isspace = True
    c = s[0]
    for next in s[1:]:
        if ((not prev_isspace and c.isupper() and next.islower()) or
                prev_lower and c.isupper()):
            result.append(' ')
        result.append(c)
        prev_lower = c.islower()
        prev_isspace = c.isspace()
        c = next
    result.append(next)
    return ''.join(result)
