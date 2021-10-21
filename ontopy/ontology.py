# -*- coding: utf-8 -*-
"""A module adding additional functionality to owlready2. The main additions
includes:
  - Visualisation of taxonomy and ontology as graphs (using pydot, see
    ontograph.py).

The class extension is defined within.

If desirable some of this may be moved back into owlready2.
"""
import os
import itertools
import inspect
import warnings
import uuid
import tempfile
import types
from collections import defaultdict

import rdflib
from rdflib.util import guess_format

import owlready2
from owlready2 import locstr

from ontopy.factpluspluswrapper.sync_factpp import sync_reasoner_factpp

from ontopy.utils import (
    asstring, read_catalog, infer_version, convert_imported
)
from ontopy.utils import (
    FMAP,
    IncompatibleVersion,
    isinteractive,
    OWLREADY2_FORMATS,
    ReadCatalogError,
    _validate_installed_version,
)
from ontopy.ontograph import OntoGraph  # FIXME: deprecate...


# Default annotations to look up
DEFAULT_LABEL_ANNOTATIONS = [
    'http://www.w3.org/2004/02/skos/core#prefLabel',
    'http://www.w3.org/2000/01/rdf-schema#label',
    'http://www.w3.org/2004/02/skos/core#altLabel',
]


class NoSuchLabelError(LookupError, AttributeError):
    """Error raised when a label cannot be found."""
    pass


def get_ontology(*args, **kwargs):
    """Returns a new Ontology from `base_iri`.

    This is a convenient function for calling World.get_ontology()."""
    return World().get_ontology(*args, **kwargs)


class World(owlready2.World):
    """A subclass of owlready2.World."""
    def __init__(self, *args, **kwargs):
        # Caches stored in the world
        self._cached_catalogs = {}  # maps url to (mtime, iris, dirs)
        self._iri_mappings = {}     # all iri mappings loaded so far
        super().__init__(*args, **kwargs)

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
            base_iri = (
                'https://raw.githubusercontent.com/emmo-repo/'
                'EMMO/master/emmo.ttl')
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
    # Properties controlling what annotations that are considered by
    # get_by_label()
    _label_annotations = []
    label_annotations = property(
        fget=lambda self: self._label_annotations,
        doc='List of label annotation searched for by get_by_label().')

    # Name of special unlabeled entities, like Thing, Nothing, etc...
    _special_labels = None

    # Some properties for customising dir() listing - useful in
    # interactive sessions...
    _dir_preflabel = isinteractive()
    _dir_label = isinteractive()
    _dir_name = False
    _dir_imported = isinteractive()
    dir_preflabel = property(
        fget=lambda self: self._dir_preflabel,
        fset=lambda self, v: setattr(self, '_dir_preflabel', bool(v)),
        doc='Whether to include entity prefLabel in dir() listing.')
    dir_label = property(
        fget=lambda self: self._dir_label,
        fset=lambda self, v: setattr(self, '_dir_label', bool(v)),
        doc='Whether to include entity label in dir() listing.')
    dir_name = property(
        fget=lambda self: self._dir_name,
        fset=lambda self, v: setattr(self, '_dir_name', bool(v)),
        doc='Whether to include entity name in dir() listing.')
    dir_imported = property(
        fget=lambda self: self._dir_imported,
        fset=lambda self, v: setattr(self, '_dir_imported', bool(v)),
        doc='Whether to include imported ontologies in dir() '
        'listing.')

    def __dir__(self):
        s = set(super().__dir__())
        lst = list(self.get_entities(imported=self._dir_imported))
        if self._dir_preflabel:
            s.update(e.prefLabel.first() for e in lst
                     if hasattr(e, 'prefLabel'))
        if self._dir_label:
            s.update(e.label.first() for e in lst if hasattr(e, 'label'))
        if self._dir_name:
            s.update(e.name for e in lst if hasattr(e, 'name'))

        s.difference_update({None})  # get rid of possible None
        return sorted(s)

    def __getitem__(self, name):
        item = super().__getitem__(name)
        if not item:
            item = self.get_by_label(name)
        return item

    def __getattr__(self, name):
        attr = super().__getattr__(name)
        if not attr:
            attr = self.get_by_label(name)
        return attr

    def __contains__(self, other):
        if self.world[other]:
            return True
        try:
            self.get_by_label(other)
        except NoSuchLabelError:
            return False
        else:
            return True

    def __objclass__(self):
        # Play nice with inspect...
        pass

    def get_by_label(self, label, label_annotations=None, namespace=None):
        """Returns entity with label annotation `label`.

        `label_annotations` is a sequence of label annotation names to look up.
        Defaults to the `label_annotations` property.

        If `namespace` is provided, it should be the last component of
        the base iri of an ontology (with trailing slash (/) or hash
        (#) stripped off).  The search for a matching label will be
        limited to this namespace.

        If several entities have the same label, only the one which is
        found first is returned.Use get_by_label_all() to get all matches.

        A NoSuchLabelError is raised if `label` cannot be found.

        Note
        ----
        The current implementation also supports "*" as a wildcard
        matching any number of characters. This may change in the future.
        """
        if 'namespaces' in self.__dict__:
            if namespace:
                if namespace in self.namespaces:
                    for e in self.get_by_label_all(
                            label, label_annotations=label_annotations):
                        if e.namespace == self.namespaces[namespace]:
                            return e
                raise NoSuchLabelError('No label annotations matches "%s" in '
                                       'namespace "%s"' % (label, namespace))
            elif label in self.namespaces:
                return self.namespaces[label]

        if label_annotations is None:
            annotations = (la.name for la in self.label_annotations)
        else:
            annotations = (s.name if hasattr(s, 'storid') else s
                           for s in label_annotations)
        for key in annotations:
            e = self.search_one(**{key: label})
            if e:
                return e

        if self._special_labels and label in self._special_labels:
            return self._special_labels[label]

        e = self.world[self.base_iri + label]
        if e:
            return e

        raise NoSuchLabelError('No label annotations matches %s' % label)

    def get_by_label_all(self, label, label_annotations=None, namespace=None):
        """Like get_by_label(), but returns a list with all matching labels.

        Returns an empty list if no matches could be found.
        """
        if label_annotations is None:
            annotations = (la.name for la in self.label_annotations)
        else:
            annotations = (s.name if hasattr(s, 'storid') else s
                           for s in label_annotations)
        e = self.world.search(**{annotations.__next__(): label})
        for key in annotations:
            e.extend(self.world.search(**{key: label}))
        if self._special_labels and label in self._special_labels:
            e.append(self._special_labels[label])
        if namespace:
            return [ns for ns in e if ns.namespace.name == namespace]
        return e

    def add_label_annotation(self, iri):
        """Adds label annotation used by get_by_label().

        May be provided either as an IRI or as its owlready2 representation.
        """
        la = iri if hasattr(iri, 'storid') else self.world[iri]
        if not la:
            raise ValueError('IRI not in ontology: %s' % iri)
        if la not in self._label_annotations:
            self._label_annotations.append(la)

    def remove_label_annotation(self, iri):
        """Removes label annotation used by get_by_label().

        May be provided either as an IRI or as its owlready2 representation.
        """
        la = iri if hasattr(iri, 'storid') else self.world[iri]
        if not la:
            raise ValueError('IRI not in ontology: %s' % iri)
        self._label_annotations.remove(la)

    def load(self, only_local=False, filename=None, format=None,
             reload=None, reload_if_newer=False, url_from_catalog=None,
             catalog_file='catalog-v001.xml', tmpdir=None,
             EMMObased=True, **kwargs):
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
        url_from_catalog : bool | None
            Whether to use catalog file to resolve the location of `base_iri`.
            If None, the catalog file is used if it exists in the same
            directory as `filename`.
        catalog_file : str
            Name of Protègè catalog file in the same folder as the
            ontology.  This option is used together with `only_local` and
            defaults to "catalog-v001.xml".
        tmpdir : str
            Path to temporary directory.
        EMMObased : bool
            Whether this is an EMMO-based ontology or not, default `True`.
        kwargs
            Additional keyword arguments are passed on to
            owlready2.Ontology.load().
        """
        # TODO: make sure that `only_local` argument is respected...

        if self.loaded:
            return self
        self._load(only_local=only_local, filename=filename, format=format,
                   reload=reload, reload_if_newer=reload_if_newer,
                   url_from_catalog=url_from_catalog,
                   catalog_file=catalog_file,
                   tmpdir=tmpdir, **kwargs)

        # Enable optimised search by get_by_label()
        if self._special_labels is None and EMMObased:
            for iri in DEFAULT_LABEL_ANNOTATIONS:
                self.add_label_annotation(iri)
            t = self.world['http://www.w3.org/2002/07/owl#topObjectProperty']
            self._special_labels = {
                'Thing': owlready2.Thing,
                'Nothing': owlready2.Nothing,
                'topObjectProperty': t,
                'owl:Thing': owlready2.Thing,
                'owl:Nothing': owlready2.Nothing,
                'owl:topObjectProperty': t,
            }

        return self

    def _load(self, only_local=False, filename=None, format=None,
              reload=None, reload_if_newer=False, url_from_catalog=None,
              catalog_file='catalog-v001.xml', tmpdir=None,
              EMMObased=True,
              **kwargs):
        """Help function for _load()."""
        web_protocol = 'http://', 'https://', 'ftp://'

        url = filename if filename else self.base_iri.rstrip('/#')
        if url.startswith(web_protocol):
            baseurl = os.path.dirname(url)
            catalogurl = baseurl + '/' + catalog_file
        else:
            if url.startswith('file://'):
                url = url[7:]
            url = os.path.normpath(os.path.abspath(url))
            baseurl = os.path.dirname(url)
            catalogurl = os.path.join(baseurl, catalog_file)

        def getmtime(path):
            if os.path.exists(path):
                return os.path.getmtime(path)
            return 0.0

        # Resolve url from catalog file
        iris = {}
        dirs = set()
        if url_from_catalog or url_from_catalog is None:
            not_reload = (not reload and
                          (not reload_if_newer or
                           getmtime(catalogurl) > self.world._cached_catalogs[
                               catalogurl][0]))
            # get iris from catalog already in cached catalogs
            if (catalogurl in self.world._cached_catalogs and not_reload):
                mtime, iris, dirs = self.world._cached_catalogs[catalogurl]
            # do not update cached_catalogs if url already in _iri_mappings
            # and reload not forced
            elif (url in self.world._iri_mappings and not_reload):
                pass
            # update iris from current catalogurl
            else:
                try:
                    iris, dirs = read_catalog(
                        uri=catalogurl,
                        recursive=False,
                        return_paths=True,
                        catalog_file=catalog_file)
                except ReadCatalogError:
                    if url_from_catalog is not None:
                        raise
                    self.world._cached_catalogs[catalogurl] = (
                        0.0, {}, set())
                else:
                    self.world._cached_catalogs[catalogurl] = (
                        getmtime(catalogurl), iris, dirs)
            self.world._iri_mappings.update(iris)
        resolved_url = self.world._iri_mappings.get(url, url)

        # Append paths from catalog file to onto_path
        for d in sorted(dirs, reverse=True):
            if d not in owlready2.onto_path:
                owlready2.onto_path.append(d)

        # Use catalog file to update IRIs of imported ontologies
        # in internal store and try to load again...
        if self.world._iri_mappings:
            for abbrev_iri in self.world._get_obj_triples_sp_o(
                    self.storid, owlready2.owl_imports):
                iri = self._unabbreviate(abbrev_iri)
                if iri in self.world._iri_mappings:
                    self._del_obj_triple_spo(
                        self.storid,
                        owlready2.owl_imports,
                        abbrev_iri)
                    self._add_obj_triple_spo(
                        self.storid,
                        owlready2.owl_imports,
                        self._abbreviate(self.world._iri_mappings[iri]))

        # Load ontology
        try:
            self.loaded = False
            fmt = format if format else guess_format(resolved_url, fmap=FMAP)
            if fmt and fmt not in OWLREADY2_FORMATS:
                # Convert filename to rdfxml before passing it to owlready2
                g = rdflib.Graph()
                g.parse(resolved_url, format=fmt)
                with tempfile.NamedTemporaryFile() as f:
                    g.serialize(destination=f, format='xml')
                    f.seek(0)
                    return super().load(only_local=True,
                                        fileobj=f,
                                        reload=reload,
                                        reload_if_newer=reload_if_newer,
                                        format='rdfxml',
                                        **kwargs)
            elif resolved_url.startswith(web_protocol):
                return super().load(only_local=only_local,
                                    reload=reload,
                                    reload_if_newer=reload_if_newer,
                                    **kwargs)

            else:
                with open(resolved_url, 'rb') as f:
                    return super().load(only_local=only_local,
                                        fileobj=f,
                                        reload=reload,
                                        reload_if_newer=reload_if_newer,
                                        **kwargs)
        except owlready2.OwlReadyOntologyParsingError:
            # Owlready2 is not able to parse the ontology - most
            # likely because imported ontologies must be resolved
            # using the catalog file.

            # Reraise if we don't want to read from the catalog file
            if not url_from_catalog and url_from_catalog is not None:
                raise

            warnings.warn('Recovering from Owlready2 parsing error... '
                          'might be deprecated')

            # Copy the ontology into a local folder and try again
            with tempfile.TemporaryDirectory() as tmpdir:
                output = os.path.join(tmpdir, os.path.basename(resolved_url))
                convert_imported(input=resolved_url,
                                 output=output,
                                 input_format=fmt,
                                 output_format='xml',
                                 url_from_catalog=url_from_catalog,
                                 catalog_file=catalog_file)

                self.loaded = False
                with open(output, 'rb') as f:
                    return super().load(only_local=True,
                                        fileobj=f,
                                        reload=reload,
                                        reload_if_newer=reload_if_newer,
                                        format='rdfxml',
                                        **kwargs)

    def save(self, filename=None, format=None, overwrite=False, **kwargs):
        """Writes the ontology to file.

        If `overwrite` is true and filename exists, it will be removed
        before saving.  The default is to append an existing ontology.
        """
        if overwrite and filename and os.path.exists(filename):
            os.remove(filename)

        if not format:
            format = guess_format(filename, fmap=FMAP)

        if (
            not _validate_installed_version(
                package="rdflib", min_version="6.0.0"
            )
            and format == FMAP.get("ttl", "")
        ):
            from rdflib import __version__ as __rdflib_version__

            warnings.warn(
                IncompatibleVersion(
                    "To correctly convert to Turtle format, rdflib must be "
                    "version 6.0.0 or greater, however, the detected rdflib "
                    "version used by your Python interpreter is "
                    f"{__rdflib_version__!r}. For more information see the "
                    "'Known issues' section of the README."
                )
            )

        if format in OWLREADY2_FORMATS:
            revmap = {v: k for k, v in FMAP.items()}
            super().save(file=filename, format=revmap[format], **kwargs)
        else:
            with tempfile.NamedTemporaryFile(suffix='.owl') as f:
                super().save(file=f.name, format='rdfxml', **kwargs)
                g = rdflib.Graph()
                g.parse(f.name, format='xml')
                g.serialize(destination=filename, format=format)

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
        g = []
        if classes:
            g.append(self.classes(imported))
        if individuals:
            g.append(self.individuals(imported))
        if object_properties:
            g.append(self.object_properties(imported))
        if data_properties:
            g.append(self.data_properties(imported))
        if annotation_properties:
            g.append(self.annotation_properties(imported))
        for e in itertools.chain(*g):
            yield e

    def classes(self, imported=False):
        """Returns an generator over all classes.

        If `imported` is true, will imported classes are also returned.
        """
        if imported:
            return self.world.classes()
        else:
            return super().classes()

    def individuals(self, imported=False):
        """Returns an generator over all individuals.

        If `imported` is true, will imported individuals are also returned.
        """
        if imported:
            return self.world.individuals()
        else:
            return super().individuals()

    def object_properties(self, imported=False):
        """Returns an generator over all object properties.

        If `imported` is true, will imported object properties are also
        returned.
        """
        if imported:
            return self.world.object_properties()
        else:
            return super().object_properties()

    def data_properties(self, imported=False):
        """Returns an generator over all data properties.

        If `imported` is true, will imported data properties are also
        returned.
        """
        if imported:
            return self.world.data_properties()
        else:
            return super().data_properties()

    def annotation_properties(self, imported=False):
        """Returns a generator iterating over all annotation properties
        defined in the current ontology.

        If `imported` is true, annotation properties in imported ontologies
        will also be included.
        """
        if imported:
            return self.world.annotation_properties()
        else:
            return super().annotation_properties()

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
                while f'{self.base_iri}{name_prefix}{n}' in self:
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
        warnings.warn('Ontology.get_annotations(entity) is deprecated.  '
                      'Use entity.get_annotations() instead.',
                      DeprecationWarning)

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
            head, tail = self.base_iri.rstrip('#/').rsplit('/', 1)
            version_iri = '/'.join([head, version, tail])

        self._add_obj_triple_spo(
            s=self.storid,
            p=self.world._abbreviate(versionIRI),
            o=self.world._abbreviate(version_iri),
        )

    def get_graph(self, **kwargs):
        """Returns a new graph object.  See  emmo.graph.OntoGraph.

        Note that this method requires the Python graphviz package.
        """
        from ontopy.graph import OntoGraph
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

    def get_ancestors(self, classes, include='all', strict=True):
        """Return ancestors of all classes in `classes`.
        classes to be provided as list

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

    def get_wu_palmer_measure(self, cls1, cls2):
        """ Return Wu-Palmer measure for semantic similarity.

        Returns Wu-Palmer measure for semantic similarity between
        two concepts.
        Wu, Palmer; ACL 94: Proceedings of the 32nd annual meeting on
        Association for Computational Linguistics, June 1994.
        """
        cca = self.closest_common_ancestor(cls1, cls2)
        ccadepth = self.number_of_generations(cca, self.Thing)
        n1 = self.number_of_generations(cls1, cca)
        n2 = self.number_of_generations(cls2, cca)
        return 2 * ccadepth / (n1 + n2 + 2 * ccadepth)

    def new_entity(self, name, parent):
        """Create and return new entity

        Makes a new entity in the ontology with given parent.
        Return the new entity
        """
        with self:
            e = types.new_class(name, (parent, ))
        return e
