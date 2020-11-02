"""Some generic utility functions.
"""
import os
import re
import datetime
import xml.etree.ElementTree as ET

import owlready2


def asstring(expr, link='{name}', n=0, exclude_object=False):
    """Returns a string representation of `expr`, which may be an entity,
    restriction, or logical expression of these.  `link` is a format
    string for formatting references to entities or relations.  It may
    contain the keywords "name" and "url".
    `n` is the recursion depth and only intended for internal use.
    If `exclude_object` is true, the object will be excluded in restrictions.
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

        if isinstance(expr.property, (
                owlready2.ObjectPropertyClass,
                owlready2.DataPropertyClass)):
            s = fmt(expr.property)
        elif isinstance(expr.property, owlready2.Inverse):
            s = 'Inverse(%s)' % asstring(expr.property.property, link, n + 1)
        else:
            print('*** WARNING: unknown restriction property: %r' %
                  expr.property)
            s = fmt(expr.property)

        if not rlabel:
            pass
        elif expr.type in (owlready2.MIN, owlready2.MAX, owlready2.EXACTLY):
            s += ' %s %d' % (rlabel, expr.cardinality)
        elif expr.type in (owlready2.SOME, owlready2.ONLY,
                           owlready2.VALUE, owlready2.HAS_SELF):
            s += ' %s' % rlabel
        else:
            print('*** WARNING: unknown relation', expr, rlabel)
            s += ' %s' % rlabel

        if not exclude_object:
            if isinstance(expr.value, str):
                s += ' "%s"' % asstring(expr.value, link, n + 1)
            else:
                s += ' %s' % asstring(expr.value, link, n + 1)
        return s

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
    elif isinstance(expr, owlready2.class_construct.Inverse):
        return fmt(expr)
    elif isinstance(expr, owlready2.disjoint.AllDisjoint):
        return fmt(expr)
    elif isinstance(expr, (bool, int, float)):
        return repr(expr)
    # Check for subclasses
    elif issubclass(expr, (bool, int, float, str)):
        return fmt(expr.__class__.__name__)
    elif issubclass(expr, datetime.date):
        return 'date'
    elif issubclass(expr, datetime.time):
        return 'datetime'
    elif issubclass(expr, datetime.datetime):
        return 'datetime'
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


def read_catalog(path, catalog_file='catalog-v001.xml', recursive=False,
                 return_paths=False):
    """Reads a Protègè catalog file and returns a dict mapping IRIs to
    absolute paths.

    The `catalog_file` argument spesifies the catalog file name and is
    used if `path` is used when `recursive` is true or when `path` is a
    directory.

    If `recursive` is true, catalog files in sub-folders are also read.

    If `return_paths` is true, a set of directory paths to source
    files is returned in addition to the default dict.
    """
    iris = {}
    dirs = set()
    if os.path.isdir(path):
        dirname = os.path.abspath(path)
        filepath = os.path.join(dirname, catalog_file)
    else:
        catalog_file = os.path.basename(path)
        filepath = os.path.abspath(path)
        dirname = os.path.dirname(filepath)

    def gettag(e):
        return e.tag.rsplit('}', 1)[-1]

    def load_catalog(filepath):
        dirname = os.path.normpath(os.path.dirname(filepath))
        dirs.add(dirname)
        xml = ET.parse(filepath)
        root = xml.getroot()
        if gettag(root) != 'catalog':
            raise ValueError('expected root tag of catalog file %r to be '
                             '"catalog"', filepath)
        for child in root:
            if gettag(child) == 'uri':
                load_uri(child, dirname)
            elif gettag(child) == 'group':
                for uri in child:
                    load_uri(uri, dirname)

    def load_uri(uri, dirname):
        assert gettag(uri) == 'uri'
        s = uri.attrib['uri']
        if s.startswith('http://') or s.startswith('https://'):
            iris.setdefault(uri.attrib['name'], s)
        else:
            filepath = os.path.join(dirname, uri.attrib['uri'])
            iris.setdefault(uri.attrib['name'], filepath)
            dir = os.path.normpath(os.path.dirname(filepath))
            if recursive and dir not in dirs:
                catalog = os.path.join(dir, catalog_file)
                load_catalog(catalog)

    load_catalog(filepath)
    if return_paths:
        return iris, dirs
    else:
        return iris


def infer_version(iri, version_iri):
    """Infer version from IRI and versionIRI."""
    if str(version_iri[:len(iri)]) == str(iri):
        version = version_iri[len(iri):].lstrip('/')
    else:
        j = 0
        v = []
        for i in range(len(iri)):
            while i + j < len(version_iri) and iri[i] != version_iri[i + j]:
                v.append(version_iri[i + j])
                j += 1
        version = ''.join(v).lstrip('/').rstrip('/#')

    if '/' in version:
        raise ValueError('version IRI %r is not consistent with base IRI '
                         '%r' % (version_iri, iri))
    return version
