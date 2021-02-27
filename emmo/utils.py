"""Some generic utility functions.
"""
import os
import re
import datetime
import xml.etree.ElementTree as ET

from rdflib import Graph, URIRef

import owlready2


def asstring(expr, link='{name}', n=0, exclude_object=False):
    """Returns a string representation of `expr`, which may be an entity,
    restriction, or logical expression of these.  `link` is a format
    string for formatting references to entities or relations.  It may
    contain the keywords "name", "url" and "lowerurl".
    `n` is the recursion depth and only intended for internal use.
    If `exclude_object` is true, the object will be excluded in restrictions.
    """
    def fmt(e):
        """Returns the formatted label of `e`."""
        name = None
        for attr in ('prefLabel', 'label'):
            if hasattr(e, attr) and getattr(e, attr):
                name = getattr(e, attr)
                if not isinstance(name, str) and hasattr(name, '__getitem__'):
                    name = name[0]
                break
        if not name:
            name = str(e).replace('.', ':')
        url = name if re.match(r'^[a-z]+://', name) else '#' + name
        return link.format(name=name, url=url, lowerurl=url.lower())

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
        return 'inverse(%s)' % fmt(expr.property)
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


def convert_imported(input, output, input_format=None, output_format='xml',
                     url_from_catalog=False, catalog_file='catalog-v001.xml'):
    """Convert imported ontologies.

    Store the output in a directory structure matching the source
    files.  This require catalog file(s) to be present.

    Args:
        input: input ontology file name
        output: output ontology file path.  The directory part of `output`
            will be the root of the generated directory structure
        input_format: input format.  The default is to infer from `input`
        output_format: output format.  The default is to infer from `output`
        url_from_catalog: bool.  Whether to read urls form catalog file.
        catalog_file: name of catalog file, that maps ontology IRIs to
            local file names
    """
    inroot = os.path.dirname(os.path.abspath(input))
    outroot = os.path.dirname(os.path.abspath(output))
    outext = os.path.splitext(output)[1]

    if url_from_catalog:
        d, dirs = read_catalog(inroot, catalog_file=catalog_file,
                               recursive=True, return_paths=True)

        # Create output dirs and copy catalog files
        for indir in dirs:
            outdir = os.path.normpath(
                os.path.join(outroot, os.path.relpath(indir, inroot)))
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            with open(os.path.join(indir, catalog_file), mode='rt') as f:
                s = f.read()
            for path in d.values():
                newpath = os.path.splitext(path)[0] + outext
                s = s.replace(
                    os.path.basename(path), os.path.basename(newpath)
                )
            with open(os.path.join(outdir, catalog_file), mode='wt') as f:
                f.write(s)
    else:
        d = {}

    outpaths = set()

    def recur(graph, outext):
        for imported in graph.objects(predicate=URIRef(
                'http://www.w3.org/2002/07/owl#imports')):
            inpath = d.get(str(imported), str(imported))
            if inpath.startswith(('http://', 'https://')):
                outpath = os.path.join(outroot, inpath.split('/')[-1])
            else:
                outpath = os.path.join(outroot, os.path.relpath(
                        inpath, inroot))
            outpath = os.path.splitext(os.path.normpath(
                outpath))[0] + outext
            if outpath not in outpaths:
                outpaths.add(outpath)
                g = Graph()
                g.parse(inpath, format=input_format)
                g.serialize(destination=outpath, format=output_format)
                recur(g, outext)

    # Write output files
    g = Graph()
    g.parse(input, format=input_format)
    g.serialize(destination=output, format=output_format)
    recur(g, outext)


def squash_imported(input, output, input_format=None, output_format='xml',
                    catalog_file='catalog-v001.xml'):
    """Convert imported ontologies and squash them into a single file.

    If a catalog file exists in the same directory as the input file it will
    be used to load possible imported ontologies.

    The the squash rdflib graph is returned.
    """
    inroot = os.path.dirname(os.path.abspath(input))
    if catalog_file and os.path.exists(os.path.join(inroot, catalog_file)):
        d = read_catalog(inroot, catalog_file=catalog_file, recursive=True)
    else:
        d = {}

    imported = set()

    def recur(g):
        for s, p, o in g.triples(
                (None, URIRef('http://www.w3.org/2002/07/owl#imports'), None)):
            g.remove((s, p, o))
            iri = d.get(str(o), str(o))
            if iri not in imported:
                imported.add(iri)
                g2 = Graph()
                g2.parse(iri, format=input_format)
                recur(g2)
                for t in g2.triples((None, None, None)):
                    graph.add(t)

    graph = Graph()
    graph.parse(input, format=input_format)
    recur(graph)
    if output:
        graph.serialize(destination=output, format=output_format)
    return graph


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


def ontology_annotation(onto, imported=True):
    """Annotate all entities with the `ontology_name` and `ontology_iri`.

    If imported is true, imported ontologies will also be annotated.

    The ontology name and IRI are important contextual information
    that is lost when ontologies are inferred and/or squashed.  This
    function retain this information as annotations.
    """
    pass
