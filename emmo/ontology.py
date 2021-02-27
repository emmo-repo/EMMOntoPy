# -*- coding: utf-8 -*-
"""A module adding additional functionality to owlready2. The main additions
includes:
  - Visualisation of taxonomy and ontology as graphs (using pydot, see
    ontograph.py).

The class extension is defined within.

If desirable some of this may be moved back into owlready2.
"""
import sys
import os
import itertools
import inspect
import warnings
import uuid
import tempfile
from collections import defaultdict

import rdflib
from rdflib.util import guess_format

import owlready2
from owlready2 import locstr

from .utils import asstring, read_catalog, infer_version, convert_imported
from .factpluspluswrapper.sync_factpp import sync_reasoner_factpp
from .ontograph import OntoGraph  # FIXME: depricate...


class NoSuchLabelError(LookupError, AttributeError):
    """Error raised when a label cannot be found."""
    pass


# owl categories
categories = (
    'annotation_properties',
    'data_properties',
    'object_properties',
    'classes',
    'individuals',
)


def get_ontology(*args, **kwargs):
    """Returns a new Ontology from `base_iri`.

    This is a convenient function for calling World.get_ontology()."""
    return World().get_ontology(*args, **kwargs)


def isinteractive():
    """Returns true if we are running from an interactive interpreater,
    false otherwise."""
    return bool(hasattr(__builtins__, '__IPYTHON__') or
                sys.flags.interactive or
                hasattr(sys, 'ps1'))


class World(owlready2.World):
    """A subclass of owlready2.World."""

    def get_ontology(self, base_iri='emmo-inferred'):
        """Returns a new Ontology from `base_iri`.

        The `base_iri` argument may be one of:
          - valid URL (possible excluding final .owl or .ttl)
          - file name (possible excluding final .owl or .ttl)
          - "emmo": load latest stable version of asserted EMMO
          - "emmo-inferred": load latest stable version of inferred EMMO
            (default)
          - "emmo-development": load latest inferred development version
            of EMMO
        """
        if base_iri == 'emmo':
            base_iri = 'http://emmo.info/emmo'
        elif base_iri == 'emmo-inferred':
            base_iri = (
                'https://emmo-repo.github.io/latest-stable/emmo-inferred.ttl')
        elif base_iri == 'emmo-development':
            base_iri = (
                'https://emmo-repo.github.io/development/emmo-inferred.ttl')

        if base_iri in self.ontologies:
            onto = self.ontologies[base_iri]
        elif base_iri + '#' in self.ontologies:
            onto = self.ontologies[base_iri + '#']
        elif base_iri + '/' in self.ontologies:
            onto = self.ontologies[base_iri + '/']
        else:
            if os.path.exists(base_iri):
                iri = os.path.abspath(base_iri)
            elif os.path.exists(base_iri + '.ttl'):
                iri = os.path.abspath(base_iri + '.ttl')
            elif os.path.exists(base_iri + '.owl'):
                iri = os.path.abspath(base_iri + '.owl')
            else:
                iri = base_iri

            if iri[-1] not in '/#':
                iri += '#'
            onto = Ontology(self, iri)

        return onto


class Ontology(owlready2.Ontology, OntoGraph):
    """A generic class extending owlready2.Ontology.
    """

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __getattr__(self, name):
        attr = super().__getattr__(name)
        if not attr:
            attr = self.get_by_label(name)
        return attr

    # Some properties for customising dir() listing.
    # Very useful in interactive sessions.
    dir_preflabel = property(
        fget=lambda self: getattr(self, '_dir_preflabel', isinteractive()),
        fset=lambda self, v: setattr(self, '_dir_preflabel', bool(v)),
        doc='Whether to include entity prefLabel in dir() listing.')
    dir_label = property(
        fget=lambda self: getattr(self, '_dir_label', isinteractive()),
        fset=lambda self, v: setattr(self, '_dir_label', bool(v)),
        doc='Whether to include entity label in dir() listing.')
    dir_name = property(
        fget=lambda self: getattr(self, '_dir_name', False),
        fset=lambda self, v: setattr(self, '_dir_name', bool(v)),
        doc='Whether to entity name in dir() listing.')
    dir_imported = property(
        fget=lambda self: getattr(self, '_dir_imported', isinteractive()),
        fset=lambda self, v: setattr(self, '_dir_imported', bool(v)),
        doc='Whether to include imported ontologies in dir() '
        'listing.')

    def __dir__(self):
        s = set(super().__dir__())
        if self.dir_preflabel:
            s.update(e.prefLabel.first() for e in
                     self.get_entities(imported=self.dir_imported)
                     if hasattr(e, 'prefLabel'))
        if self.dir_label:
            s.update(e.label.first() for e in
                     self.get_entities(imported=self.dir_imported)
                     if hasattr(e, 'label'))
        if self.dir_name:
            s.update(e.name for e in
                     self.get_entities(imported=self.dir_imported)
                     if hasattr(e, 'name'))
        s.difference_update({None})  # get rid of possible None
        return sorted(s)

    def __contains__(self, other):
        try:
            self[other]
            return True
        except NoSuchLabelError:
            return False

    def __objclass__(self):
        # Play nice with inspect...
        pass

    def load(self, only_local=False, filename=None, format=None,
             reload=None, reload_if_newer=False, url_from_catalog=False,
             catalog_file='catalog-v001.xml', tmpdir=None,
             **kwargs):
        """Load the ontology.

        Parameters
        ----------
        only_local : bool
            Whether to only read local files.  This requires that you
            have appended the path to the ontology to owlready2.onto_path.
        filename : str
            Path to file to load the ontology from.  Defaults to `base_iri`
            provided to get_ontology().
        format : str
            Format of `filename`.  Default is inferred from `filename`
            extension.
        reload : bool
            Whether to reload the ontology if it is already loaded.
        reload_if_newer : bool
            Whether to reload the ontology if the source has changed since
            last time it was loaded.
        url_from_catalog : bool
            Use catalog file if `base_iri` cannot be resolved.
        catalog_file : str
            Name of Protègè catalog file in the same folder as the
            ontology.  This option is used together with `only_local` and
            defaults to "catalog-v001.xml".
        tmpdir : str
            Path to temporary directory.
        kwargs
            Additional keyword arguments are passed on to
            owlready2.Ontology.load().
        """
        fmap = {
            'n3': 'ntriples',
            'ttl': 'turtle',
        }

        # If filename is not given, infer it from base_iri (if possible)
        if not filename:
            web_protocols = ('http://', 'https://', )
            fmt = format if format else guess_format(
                self.base_iri.rstrip('/#'), fmap=fmap)
            if not self.base_iri.startswith(web_protocols):
                filename = self.base_iri.rstrip('#/')
                if filename.startswith('file://'):
                    filename = filename[7:]
            elif fmt and fmt not in ('xml', 'ntriples'):
                g = rdflib.Graph()
                g.parse(self.base_iri, format=fmt)
                with tempfile.NamedTemporaryFile() as f:
                    # If reading from an URL of an unsupported format,
                    # serialize to a temporary file in rdfxml format and
                    # load() in the superclass
                    g.serialize(destination=f, format='xml')
                    f.seek(0)
                    self.loaded = False
                    return super().load(only_local=True,
                                        fileobj=f,
                                        reload=reload,
                                        reload_if_newer=reload_if_newer,
                                        format='rdfxml',
                                        **kwargs)

        # Convert filename to owl if it is in a format not supported
        # by owlready2
        if filename:
            if not format:
                format = guess_format(filename, fmap=fmap)
            if format not in ('xml', 'ntriples'):
                with tempfile.TemporaryDirectory() as tmpdir:
                    if not os.path.exists(tmpdir):
                        os.makedirs(tmpdir)
                    output = os.path.join(tmpdir, os.path.splitext(
                        os.path.basename(filename))[0] + '.owl')
                    convert_imported(filename, output,
                                     input_format=format, output_format='xml',
                                     url_from_catalog=url_from_catalog,
                                     catalog_file=catalog_file)
                    return self.load(only_local=True,
                                     filename=output,
                                     format='xml',
                                     reload=reload,
                                     reload_if_newer=reload_if_newer,
                                     url_from_catalog=url_from_catalog,
                                     catalog_file=catalog_file,
                                     **kwargs)

        # Append paths from catalog file to onto_path
        dirpath = os.path.normpath(
            os.path.dirname(filename or self.base_iri.rstrip('/#')))
        if only_local and os.path.exists(os.path.join(dirpath, catalog_file)):
            iris, dirs = read_catalog(
                dirpath, recursive=True, return_paths=True,
                catalog_file=catalog_file)
            for d in sorted(dirs, reverse=True):
                if d not in owlready2.onto_path:
                    owlready2.onto_path.append(d)

        fileobj = open(filename, 'rb') if filename else None

        try:
            super().load(only_local=only_local, fileobj=fileobj, reload=reload,
                         reload_if_newer=reload_if_newer, **kwargs)
        except owlready2.OwlReadyOntologyParsingError:
            if url_from_catalog:
                print('no url from catalog')
                # Use catalog file to update IRIs of imported ontologies
                # in internal store and try to load again...
                iris = read_catalog(dirpath, catalog_file=catalog_file)
                for abbrev_iri in self.world._get_obj_triples_sp_o(
                        self.storid, owlready2.owl_imports):
                    iri = self._unabbreviate(abbrev_iri)
                    if iri in iris:
                        self._del_obj_triple_spo(self.storid,
                                                 owlready2.owl_imports,
                                                 abbrev_iri)
                        self._add_obj_triple_spo(self.storid,
                                                 owlready2.owl_imports,
                                                 self._abbreviate(iris[iri]))
                self.loaded = False
                super().load(only_local=only_local, fileobj=fileobj,
                             reload=reload, reload_if_newer=reload_if_newer,
                             **kwargs)
            else:
                raise
        finally:
            if fileobj:
                fileobj.close()

        return self

    def save(self, filename=None, format='rdfxml', overwrite=False, **kwargs):
        """Writes the ontology to file.

        If `overwrite` is true and filename exists, it will be removed
        before saving.  The default is to append an existing ontology.
        """
        if overwrite and filename and os.path.exists(filename):
            os.remove(filename)
        super().save(file=filename, format=format, **kwargs)

    def get_imported_ontologies(self, recursive=False):
        """Return a list with imported ontologies.

        If `recursive` is true, ontologies imported by imported ontologies
        are also returned.
        """
        def rec_imported(onto):
            for o in onto.imported_ontologies:
                if o not in imported:
                    imported.add(o)
                    rec_imported(o)

        if recursive:
            imported = set()
            rec_imported(self)
            return list(imported)
        else:
            return self.imported_ontologies

    def get_entities(self, imported=True, classes=True, individuals=True,
                     object_properties=True, data_properties=True,
                     annotation_properties=True):
        """Return a generator over (optionally) all classes, individuals,
        object_properties, data_properties and annotation_properties.

        If `imported` is true, entities in imported ontologies will also
        be included.
        """
        categories = set([
            'classes' if classes else None,
            'individuals' if individuals else None,
            'object_properties' if object_properties else None,
            'data_properties' if data_properties else None,
            'annotation_properties' if annotation_properties else None,
        ]).difference([None])
        for e in itertools.chain.from_iterable(
                getattr(owlready2.Ontology, c)(self) for c in categories):
            yield e
        if imported:
            for onto in self.get_imported_ontologies(recursive=True):
                for e in itertools.chain.from_iterable(
                        getattr(owlready2.Ontology, c)(onto)
                        for c in categories):
                    yield e

    def classes(self, imported=False):
        """Returns an generator over all classes.

        If `imported` is true, will imported classes are also returned.
        """
        return self.get_entities(
            imported=imported, classes=True, individuals=False,
            object_properties=False, data_properties=False,
            annotation_properties=False)

    def individuals(self, imported=False):
        """Returns an generator over all individuals.

        If `imported` is true, will imported individuals are also returned.
        """
        return self.get_entities(
            imported=imported, classes=False, individuals=True,
            object_properties=False, data_properties=False,
            annotation_properties=False)

    def object_properties(self, imported=False):
        """Returns an generator over all object properties.

        If `imported` is true, will imported object properties are also
        returned.
        """
        return self.get_entities(
            imported=imported, classes=False, individuals=False,
            object_properties=True, data_properties=False,
            annotation_properties=False)

    def data_properties(self, imported=False):
        """Returns an generator over all data properties.

        If `imported` is true, will imported data properties are also
        returned.
        """
        return self.get_entities(
            imported=imported, classes=False, individuals=False,
            object_properties=False, data_properties=True,
            annotation_properties=False)

    def annotation_properties(self, imported=False):
        """Returns a generator iterating over all annotation properties
        defined in the current ontology.

        If `imported` is true, annotation properties in imported ontologies
        will also be included.
        """
        return self.get_entities(
            imported=imported, classes=False, individuals=False,
            object_properties=False, data_properties=False,
            annotation_properties=True)

    def get_root_classes(self, imported=False):
        """Returns a list or root classes."""
        return [cls for cls in self.classes(imported=imported)
                if not cls.ancestors().difference(set([cls, owlready2.Thing]))]

    def get_root_object_properties(self, imported=False):
        """Returns a list of root object properties."""
        props = set(self.object_properties(imported=imported))
        return [p for p in props if not props.intersection(p.is_a)]

    def get_root_data_properties(self, imported=False):
        """Returns a list of root object properties."""
        props = set(self.data_properties(imported=imported))
        return [p for p in props if not props.intersection(p.is_a)]

    def get_roots(self, imported=False):
        """Returns all class, object_property and data_property roots."""
        roots = self.get_root_classes(imported=imported)
        roots.extend(self.get_root_object_properties(imported=imported))
        roots.extend(self.get_root_data_properties(imported=imported))
        return roots

    def get_by_label(self, label):
        """Returns entity by label.

        If several entities have the same label, only the one which is
        found first is returned.  A KeyError is raised if `label`
        cannot be found.
        """
        return self._get_by_label(label)

    def _get_by_label(self, label, visited=None):
        """Recursive help function for get_by_label()."""
        # Strip off colon in labels
        if ':' in label:
            label = label.split(':')[-1]

        # Include self among already visited ontologies
        if visited is None:
            visited = set()
        visited.add(self)

        # Handle labels of the form 'namespace.label' recursively
        if '.' in label:
            head, sep, tail = label.partition('.')
            ns = self.get_namespace(head)
            return ns.ontology._get_by_label(tail, visited=visited)

        # Check for name in all categories in self
        for category in categories:
            method = getattr(self, category)
            for entity in method():
                if hasattr(entity, 'prefLabel') and label in entity.prefLabel:
                    return entity
                elif hasattr(entity, 'label') and label in entity.label:
                    return entity
                elif hasattr(entity, 'altLabel') and label in entity.altLabel:
                    return entity
        # Check for special names
        d = {
                'Nothing': owlready2.Nothing,
        }
        if label in d:
            return d[label]
        # Check whether `label` matches a Python class name of any category
        lst = [cls for cls in itertools.chain.from_iterable(
            getattr(self, category)() for category in categories)
             if hasattr(cls, '__name__') and cls.__name__ == label]
        if len(lst) == 1:
            return lst[0]
        elif len(lst) > 1:
            raise NoSuchLabelError('There is more than one Python class with '
                                   'name %r' % label)
        elif label is owlready2.Thing or label == 'Thing':
            return owlready2.Thing

        # Check imported ontologies
        for onto in self.imported_ontologies:
            if onto not in visited:
                visited.add(onto)
                onto.__class__ = self.__class__  # change type of onto (magic)
                try:
                    return onto._get_by_label(label, visited=visited)
                except NoSuchLabelError:
                    pass

        # Fallback to check whether we have a class in the current or any
        # of the imported ontologies whos name matches `label`
        for onto in [self] + self.imported_ontologies:
            lst = [cls for cls in onto.classes() if cls.__name__ == label]
            if len(lst) == 1:
                return lst[0]
            elif len(lst) > 1:
                raise NoSuchLabelError('There is more than one class with '
                                       'name %r' % label)
        # Label cannot be found
        raise NoSuchLabelError('Ontology "%s" has no such label: %s' % (
            self.name, label))

    def get_by_label_all(self, label):
        """Like get_by_label(), but returns a list of all entities with
        matching labels.
        """
        return [entity for entity in
                itertools.chain.from_iterable(
                    getattr(self, c)() for c in categories)
                if ((hasattr(entity, 'prefLabel') and
                     label in entity.prefLabel) or
                    (hasattr(entity, 'label') and
                     label in entity.label) or
                    (hasattr(entity, 'altLabel') and
                     label in entity.altLabel))]

    def sync_python_names(self,
                          annotations=('prefLabel', 'label', 'altLabel')):
        """Update the `python_name` attribute of all properties.

        The python_name attribute will be set to the first non-empty
        annotation in the sequence of annotations in `annotations` for
        the property.
        """
        def update(gen):
            for prop in gen:
                for a in annotations:
                    if hasattr(prop, a) and getattr(prop, a):
                        prop.python_name = getattr(prop, a).first()
                        break

        update(self.get_entities(
            classes=False, individuals=False,
            object_properties=False, data_properties=False))
        update(self.get_entities(
            classes=False, individuals=False, annotation_properties=False))

    def rename_entities(
        self,
        annotations=('prefLabel', 'label', 'altLabel'),
    ):
        """Set `name` of all entities to the first non-empty annotation in
        `annotations`.

        Warning, this method changes all IRIs in the ontology.  However,
        it may be useful to make the ontology more readable and to work
        with it together with a triple store.
        """
        for e in self.get_entities():
            for a in annotations:
                if hasattr(e, a):
                    name = getattr(e, a).first()
                    if name:
                        e.name = name
                        break

    def sync_reasoner(self, reasoner='FaCT++', include_imported=False,
                      **kwargs):
        """Update current ontology by running the given reasoner.

        Supported values for `reasoner` are 'Pellet', 'HermiT' and 'FaCT++'.

        If `include_imported` is true, the reasoner will also reason
        over imported ontologies.  Note that this may be **very** slow
        with Pellet and HermiT.

        Keyword arguments are passed to the underlying owlready2 function.
        """
        if reasoner == 'Pellet':
            sync = owlready2.sync_reasoner_pellet
        elif reasoner == 'HermiT':
            sync = owlready2.sync_reasoner_hermit
        elif reasoner == 'FaCT++':
            sync = sync_reasoner_factpp
        else:
            raise ValueError('unknown reasoner %r.  Supported reasoners'
                             'are "Pellet", "HermiT" and "FaCT++".', reasoner)

        if include_imported:
            with self:
                sync(**kwargs)
        else:
            sync([self], **kwargs)

    def sync_attributes(self, name_policy=None, name_prefix='',
                        class_docstring='comment', sync_imported=False):
        """This method is intended to be called after you have added new
        classes (typically via Python) to make sure that attributes like
        `label` and `comments` are defined.

        If a class, object property, data property or annotation
        property in the current ontology has no label, the name of
        the corresponding Python class will be assigned as label.

        If a class, object property, data property or annotation
        property has no comment, it will be assigned the docstring of
        the corresponding Python class.

        `name_policy` specify wether and how the names in the ontology
        should be updated.  Valid values are:
          None          not changed
          "uuid"        `name_prefix` followed by a global unique id (UUID).
          "sequential"  `name_prefix` followed a sequantial number.
        EMMO conventions imply ``name_policy=='uuid'``.

        If `sync_imported` is true, all imported ontologies are also
        updated.

        The `class_docstring` argument specifies the annotation that
        class docstrings are mapped to.  Defaults to "comment".
        """
        for cls in itertools.chain(
                self.classes(), self.object_properties(),
                self.data_properties(), self.annotation_properties()):
            if not hasattr(cls, 'prefLabel'):
                # no prefLabel - create new annotation property..
                with self:
                    class prefLabel(owlready2.label):
                        pass
                cls.prefLabel = [locstr(cls.__name__, lang='en')]
            elif not cls.prefLabel:
                cls.prefLabel.append(locstr(cls.__name__, lang='en'))
            if class_docstring and hasattr(cls, '__doc__') and cls.__doc__:
                getattr(cls, class_docstring).append(
                    locstr(inspect.cleandoc(cls.__doc__), lang='en'))

        for ind in self.individuals():
            if not hasattr(ind, 'prefLabel'):
                # no prefLabel - create new annotation property..
                with self:
                    class prefLabel(owlready2.label):  # noqa: F811
                        pass
                ind.prefLabel = [locstr(ind.name, lang='en')]
            elif not ind.prefLabel:
                ind.prefLabel.append(locstr(ind.name, lang='en'))

        chain = itertools.chain(
            self.classes(), self.individuals(), self.object_properties(),
            self.data_properties(), self.annotation_properties())
        if name_policy == 'uuid':
            for obj in chain:
                obj.name = name_prefix + str(uuid.uuid5(uuid.NAMESPACE_DNS,
                                                        obj.name))
        elif name_policy == 'sequential':
            for obj in chain:
                n = 0
                while name_prefix + str(n) in self:
                    n += 1
                obj.name = name_prefix + str(n)
        elif name_policy is not None:
            raise TypeError('invalid name_policy: %r' % (name_policy, ))

        if sync_imported:
            for onto in self.imported_ontologies:
                onto.sync_attributes()

    def get_relations(self):
        """Returns a generator for all relations."""
        warnings.warn('Ontology.get_relations() is deprecated.  '
                      'Use onto.object_properties() instead.',
                      DeprecationWarning)
        return self.object_properties()

    def get_annotations(self, entity):
        """Returns a dict with annotations for `entity`.  Entity may be given
        either as a ThingClass object or as a label."""
        warnings.warn('Ontology.get_annotations(cls) is deprecated.  '
                      'Use cls.get_annotations() instead.', DeprecationWarning)

        if isinstance(entity, str):
            entity = self.get_by_label(entity)
        d = {'comment': getattr(entity, 'comment', '')}
        for a in self.annotation_properties():
            d[a.label.first()] = [
                o.strip('"') for s, p, o in
                self.get_triples(entity.storid, a.storid, None)]
        return d

    def get_branch(self, root, leafs=(), include_leafs=True,
                   strict_leafs=False, exclude=None, sort=False):
        """Returns a set with all direct and indirect subclasses of `root`.
        Any subclass found in the sequence `leafs` will be included in
        the returned list, but its subclasses will not.  The elements
        of `leafs` may be ThingClass objects or labels.

        Subclasses of any subclass found in the sequence `leafs` will
        be excluded from the returned list, where the elements of `leafs`
        may be ThingClass objects or labels.

        If `include_leafs` is true, the leafs are included in the returned
        list, otherwise they are not.

        If `strict_leafs` is true, any descendant of a leaf will be excluded
        in the returned set.

        If given, `exclude` may be a sequence of classes, including
        their subclasses, to exclude from the output.

        If `sort` is True, a list sorted according to depth and label
        will be returned instead of a set.
        """
        def _branch(root, leafs):
            if root not in leafs:
                branch = {root, }
                for c in root.subclasses():
                    # Defining a branch is actually quite tricky.  Consider
                    # the case:
                    #
                    #      L isA R
                    #      A isA L
                    #      A isA R
                    #
                    # where R is the root, L is a leaf and A is a direct
                    # child of both.  Logically, since A is a child of the
                    # leaf we want to skip A.  But a strait forward imple-
                    # mentation will see that A is a child of the root and
                    # include it.  Requireing that the R should be a strict
                    # parent of A solves this.
                    if root in c.get_parents(strict=True):
                        branch.update(_branch(c, leafs))
            else:
                branch = {root, } if include_leafs else set()
            return branch

        if isinstance(root, str):
            root = self.get_by_label(root)

        leafs = set(self.get_by_label(leaf) if isinstance(leaf, str)
                    else leaf for leaf in leafs)
        leafs.discard(root)

        if exclude:
            exclude = set(self.get_by_label(e) if isinstance(e, str)
                          else e for e in exclude)
            leafs.update(exclude)

        branch = _branch(root, leafs)

        # Exclude all descendants of any leaf
        if strict_leafs:
            descendants = root.descendants()
            for leaf in leafs:
                if leaf in descendants:
                    branch.difference_update(leaf.descendants(
                        include_self=False))

        if exclude:
            branch.difference_update(exclude)

        # Sort according to depth, then by label
        if sort:
            branch = sorted(sorted(branch, key=lambda x: asstring(x)),
                            key=lambda x: len(x.mro()))

        return branch

    def is_individual(self, entity):
        """Returns true if entity is an individual."""
        if isinstance(entity, str):
            entity = self.get_by_label(entity)
        return isinstance(entity, owlready2.Thing)

    # FIXME - deprecate this method as soon the ThingClass property
    #         `defined_class` works correct in Owlready2
    def is_defined(self, entity):
        """Returns true if the entity is a defined class."""
        if isinstance(entity, str):
            entity = self.get_by_label(entity)
        return hasattr(entity, 'equivalent_to') and bool(entity.equivalent_to)

    def get_version(self, as_iri=False):
        """Returns the version number of the ontology as inferred from the
        owl:versionIRI tag.

        If `as_iri` is True, the full versionIRI is returned.
        """
        versionIRI_storid = self.world._abbreviate(
            'http://www.w3.org/2002/07/owl#versionIRI')
        tokens = self.get_triples(s=self.storid, p=versionIRI_storid)
        if not tokens:
            raise TypeError('No versionIRI in Ontology %r' % self.base_iri)
        s, p, o = tokens[0]
        versionIRI = self.world._unabbreviate(o)
        if as_iri:
            return versionIRI
        else:
            return infer_version(self.base_iri, versionIRI)

    def set_version(self, version=None, version_iri=None):
        """Assign version to ontology by asigning owl:versionIRI.

        If `version` but not `version_iri` is provided, the version
        IRI will be the combination of `base_iri` and `version`.
        """
        versionIRI = 'http://www.w3.org/2002/07/owl#versionIRI'
        versionIRI_storid = self.world._abbreviate(versionIRI)
        if self._has_obj_triple_spo(s=self.storid, p=versionIRI_storid):
            self._del_obj_triple_spo(s=self.storid, p=versionIRI_storid)

        if not version_iri:
            if not version:
                raise TypeError(
                    'Either `version` or `version_iri` must be provided')
            version_iri = self.base_iri.rstrip('#/') + '/' + version

        self._add_obj_triple_spo(
            s=self.storid,
            p=self.world._abbreviate(versionIRI),
            o=self.world._abbreviate(version_iri),
        )

    def get_graph(self, **kwargs):
        """Returns a new graph object.  See  emmo.graph.OntoGraph.

        Note that this method requires the Python graphviz package.
        """
        from .graph import OntoGraph
        return OntoGraph(self, **kwargs)

    def common_ancestors(self, cls1, cls2):
        """Return a list of common ancestors for `cls1` and `cls2`."""
        return set(cls1.ancestors()).intersection(cls2.ancestors())

    def number_of_generations(self, descendant, ancestor):
        """ Return shortest distance from ancestor to descendant"""
        if ancestor not in descendant.ancestors():
            raise ValueError('Descendant is not a descendant of ancestor')
        return self._number_of_generations(descendant, ancestor, 0)

    def _number_of_generations(self, descendant, ancestor, n):
        """Recursive help function to number_of_generations(), return
        distance between a ancestor-descendant pair (n+1)."""
        if descendant.name == ancestor.name:
            return n
        return min(self._number_of_generations(parent, ancestor, n + 1)
                   for parent in descendant.get_parents()
                   if ancestor in parent.ancestors())

    def closest_common_ancestors(self, cls1, cls2):
        """Returns a list with closest_common_ancestor for cls1 and cls2"""
        distances = {}
        for ancestor in self.common_ancestors(cls1, cls2):
            distances[ancestor] = (self.number_of_generations(cls1, ancestor) +
                                   self.number_of_generations(cls2, ancestor))
        return [ancestor for ancestor, distance in distances.items()
                if distance == min(distances.values())]

    def closest_common_ancestor(self, *classes):
        """Returns closest_common_ancestor for the given classes."""
        mros = [cls.mro() for cls in classes]
        track = defaultdict(int)
        while mros:
            for mro in mros:
                cur = mro.pop(0)
                track[cur] += 1
                if track[cur] == len(classes):
                    return cur
                if len(mro) == 0:
                    mros.remove(mro)
        assert(0)  # should never be reached...

    def get_ancestors(self, classes, include=None, strict=True):
        """Return ancestors of all classes in `classes`.

        The values of `include` may be:
          - None: ignore this argument
          - "all": Include all ancestors.
          - "closest": Include all ancestors up to the closest common
            ancestor of all classes.
          - int: Include this number of ancestor levels.  Here `include`
            may be an integer or a string that can be converted to int.
        """
        ancestors = set()
        if not classes:
            return ancestors

        def addancestors(e, n, s):
            if n > 0:
                for p in e.get_parents(strict=True):
                    s.add(p)
                    addancestors(p, n - 1, s)

        if isinstance(include, str) and include.isdigit():
            include = int(include)

        if include == 'all':
            ancestors.update(*(c.ancestors() for c in classes))
        elif include == 'closest':
            closest = self.closest_common_ancestor(*classes)
            for c in classes:
                ancestors.update(a for a in c.ancestors()
                                 if closest in a.ancestors())
        elif isinstance(include, int):
            for e in classes:
                addancestors(e, int(include), ancestors)
        elif include not in (None, 'None', 'none', ''):
            raise ValueError('include must be "all", "closest" or None')

        if strict:
            return ancestors.difference(classes)
        else:
            return ancestors
