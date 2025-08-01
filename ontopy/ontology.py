# -*- coding: utf-8 -*-
"""A module adding additional functionality to owlready2.

If desirable some of these additions may be moved back into owlready2.
"""
# pylint: disable=too-many-lines,fixme,arguments-differ,protected-access
from typing import TYPE_CHECKING, Optional, Union
import os
import fnmatch
import itertools
import inspect
import warnings
import uuid
import tempfile
import types
import re
from pathlib import Path
from collections import defaultdict
from collections.abc import Iterable
from urllib.request import HTTPError, URLError

import rdflib
from rdflib.util import guess_format

import owlready2
from owlready2 import locstr
from owlready2.entity import ThingClass
from owlready2.prop import ObjectPropertyClass, DataPropertyClass
from owlready2 import AnnotationPropertyClass
from owlready2.base import rdf_type

from ontopy.factpluspluswrapper.sync_factpp import sync_reasoner_factpp
from ontopy.utils import (  # pylint: disable=cyclic-import
    english,
    asstring,
    read_catalog,
    write_catalog,
    infer_version,
    convert_imported,
    directory_layout,
    FMAP,
    IncompatibleVersion,
    isinteractive,
    NoSuchLabelError,
    OWLREADY2_FORMATS,
    ReadCatalogError,
    _validate_installed_version,
    LabelDefinitionError,
    AmbiguousLabelError,
    EntityClassDefinitionError,
    EMMOntoPyException,
)

if TYPE_CHECKING:
    from typing import Iterator, List, Sequence, Generator


# Default annotations to look up
DEFAULT_LABEL_ANNOTATIONS = [
    "http://www.w3.org/2004/02/skos/core#prefLabel",
    "http://www.w3.org/2000/01/rdf-schema#label",
    "http://www.w3.org/2004/02/skos/core#altLabel",
]


def get_ontology(*args, **kwargs):
    """Returns a new Ontology from `base_iri`.

    This is a convenient function for calling World.get_ontology()."""
    return World().get_ontology(*args, **kwargs)


class World(owlready2.World):
    """A subclass of owlready2.World."""

    def __init__(self, *args, **kwargs):
        # Caches stored in the world
        self._cached_catalogs = {}  # maps url to (mtime, iris, dirs)
        self._iri_mappings = {}  # all iri mappings loaded so far
        super().__init__(*args, **kwargs)

    def get_ontology(
        self,
        base_iri: str = "emmo-inferred",
        OntologyClass: "owlready2.Ontology" = None,
        label_annotations: "Sequence" = None,
    ) -> "Ontology":
        # pylint: disable=too-many-branches
        """Returns a new Ontology from `base_iri`.

        Arguments:
            base_iri: The base IRI of the ontology. May be one of:
                - valid URL (possible excluding final .owl or .ttl)
                - file name (possible excluding final .owl or .ttl)
                - "emmo": load latest version of asserted EMMO
                - "emmo-inferred": load latest version of inferred EMMO
                  (default)
                - "emmo-development": load latest inferred development
                  version of EMMO. Until first stable release
                  emmo-inferred and emmo-development will be the same.
            OntologyClass: If given and `base_iri` doesn't correspond
                to an existing ontology, a new ontology is created of
                this Ontology subclass.  Defaults to `ontopy.Ontology`.
            label_annotations: Sequence of label IRIs used for accessing
                entities in the ontology given that they are in the ontology.
                Label IRIs not in the ontology will need to be added to
                ontologies in order to be accessible.
                Defaults to DEFAULT_LABEL_ANNOTATIONS if set to None.
        """
        base_iri = base_iri.as_uri() if isinstance(base_iri, Path) else base_iri

        if base_iri == "emmo":
            base_iri = "https://w3id.org/emmo/"
        elif base_iri == "emmo-inferred":
            base_iri = "https://w3id.org/emmo/inferred"
        elif base_iri == "emmo-development":
            base_iri = (
                "https://raw.githubusercontent.com/emmo-repo/EMMO/"
                "refs/heads/dev/emmo.ttl"
            )

        if base_iri in self.ontologies:
            onto = self.ontologies[base_iri]
        elif base_iri + "#" in self.ontologies:
            onto = self.ontologies[base_iri + "#"]
        elif base_iri + "/" in self.ontologies:
            onto = self.ontologies[base_iri + "/"]
        else:
            if os.path.exists(base_iri):
                iri = os.path.abspath(base_iri)
            elif os.path.exists(base_iri + ".ttl"):
                iri = os.path.abspath(base_iri + ".ttl")
            elif os.path.exists(base_iri + ".owl"):
                iri = os.path.abspath(base_iri + ".owl")
            else:
                iri = base_iri

            if iri[-1] not in "/#":
                iri += "#"

            if OntologyClass is None:
                OntologyClass = Ontology

            onto = OntologyClass(self, iri)

        if label_annotations:
            onto.label_annotations = list(label_annotations)

        return onto

    def get_unabbreviated_triples(
        self, subject=None, predicate=None, obj=None, blank=None
    ):
        # pylint: disable=invalid-name
        """Returns all triples unabbreviated.
        Imported ontologies not included.

        If any of the `subject`, `predicate` or `obj` arguments are given,
        only matching triples will be returned.

        If `blank` is given, it will be used to represent blank nodes.
        """
        return _get_unabbreviated_triples(
            self, subject=subject, predicate=predicate, obj=obj, blank=blank
        )


class Ontology(owlready2.Ontology):  # pylint: disable=too-many-public-methods
    """A generic class extending owlready2.Ontology.

    Additional attributes:
        iri: IRI of this ontology.  Currently only used for serialisation
            with rdflib. Defaults to None, meaning `base_iri` will be used
            instead.
        label_annotations: List of label annotations, i.e. annotations
            that are recognised by the get_by_label() method. Defaults
            to `[skos:prefLabel, rdf:label, skos:altLabel]`.
        prefix: Prefix for this ontology. Defaults to None.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iri = None
        self.label_annotations = DEFAULT_LABEL_ANNOTATIONS[:]
        self.prefix = None

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
        fset=lambda self, v: setattr(self, "_dir_preflabel", bool(v)),
        doc="Whether to include entity prefLabel in dir() listing.",
    )
    dir_label = property(
        fget=lambda self: self._dir_label,
        fset=lambda self, v: setattr(self, "_dir_label", bool(v)),
        doc="Whether to include entity label in dir() listing.",
    )
    dir_name = property(
        fget=lambda self: self._dir_name,
        fset=lambda self, v: setattr(self, "_dir_name", bool(v)),
        doc="Whether to include entity name in dir() listing.",
    )
    dir_imported = property(
        fget=lambda self: self._dir_imported,
        fset=lambda self, v: setattr(self, "_dir_imported", bool(v)),
        doc="Whether to include imported ontologies in dir() listing.",
    )

    # Other settings
    _colon_in_label = False
    colon_in_label = property(
        fget=lambda self: self._colon_in_label,
        fset=lambda self, v: setattr(self, "_colon_in_label", bool(v)),
        doc="Whether to accept colon in name-part of IRI.  "
        "If true, the name cannot be prefixed.",
    )

    def __dir__(self):
        dirset = set(super().__dir__())
        lst = list(self.get_entities(imported=self._dir_imported))
        if self._dir_preflabel:
            dirset.update(
                str(dir.prefLabel.first())
                for dir in lst
                if hasattr(dir, "prefLabel")
            )
        if self._dir_label:
            dirset.update(
                str(dir.label.first()) for dir in lst if hasattr(dir, "label")
            )
        if self._dir_name:
            dirset.update(dir.name for dir in lst if hasattr(dir, "name"))
        dirset.difference_update({None})  # get rid of possible None
        return sorted(dirset)

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
        return True

    def __objclass__(self):
        # Play nice with inspect...
        pass

    def __hash__(self):
        """Returns a hash based on base_iri.
        This is done to keep Ontology hashable when defining __eq__.
        """
        return hash(self.base_iri)

    def __eq__(self, other):
        """Checks if this ontology is equal to `other`.

        This function compares the result of
        ``set(self.get_unabbreviated_triples(label='_:b'))``,
        i.e. blank nodes are not distinguished, but relations to blank
        nodes are included.
        """
        return set(self.get_unabbreviated_triples(blank="_:b")) == set(
            other.get_unabbreviated_triples(blank="_:b")
        )

    def get_unabbreviated_triples(
        self, subject=None, predicate=None, obj=None, blank=None
    ):
        """Returns all matching triples unabbreviated.

        If `blank` is given, it will be used to represent blank nodes.
        """
        # pylint: disable=invalid-name
        return _get_unabbreviated_triples(
            self, subject=subject, predicate=predicate, obj=obj, blank=blank
        )

    def set_default_label_annotations(self):
        """Sets the default label annotations."""
        warnings.warn(
            "Ontology.set_default_label_annotations() is deprecated. "
            "Default label annotations are set by Ontology.__init__(). ",
            DeprecationWarning,
            stacklevel=2,
        )
        self.label_annotations = DEFAULT_LABEL_ANNOTATIONS[:]

    def get_by_label(
        self,
        label: str,
        *,
        label_annotations: str = None,
        prefix: str = None,
        imported: bool = True,
        colon_in_label: bool = None,
    ):
        """Returns entity with label annotation `label`.

        Arguments:
           label: label so search for.
               May be written as 'label' or 'prefix:label'.
               get_by_label('prefix:label') ==
               get_by_label('label', prefix='prefix').
           label_annotations: a sequence of label annotation names to look up.
               Defaults to the `label_annotations` property.
           prefix: if provided, it should be the last component of
               the base iri of an ontology (with trailing slash (/) or hash
               (#) stripped off).  The search for a matching label will be
               limited to this namespace.
           imported: Whether to also look for `label` in imported ontologies.
           colon_in_label: Whether to accept colon (:) in a label or name-part
               of IRI.  Defaults to the `colon_in_label` property of `self`.
               Setting this true cannot be combined with `prefix`.

        If several entities have the same label, only the one which is
        found first is returned.Use get_by_label_all() to get all matches.

        Note, if different prefixes are provided in the label and via
        the `prefix` argument a warning will be issued and the
        `prefix` argument will take precedence.

        A NoSuchLabelError is raised if `label` cannot be found.
        """
        # pylint: disable=too-many-arguments,too-many-branches,invalid-name
        if not isinstance(label, str):
            raise TypeError(
                f"Invalid label definition, must be a string: '{label}'"
            )

        if label_annotations is None:
            label_annotations = self.label_annotations

        if colon_in_label is None:
            colon_in_label = self._colon_in_label
        if colon_in_label:
            if prefix:
                raise ValueError(
                    "`prefix` cannot be combined with `colon_in_label`"
                )
        else:
            splitlabel = label.split(":", 1)
            if len(splitlabel) == 2 and not splitlabel[1].startswith("//"):
                label = splitlabel[1]
                if prefix and prefix != splitlabel[0]:
                    warnings.warn(
                        f"Prefix given both as argument ({prefix}) "
                        f"and in label ({splitlabel[0]}). "
                        "Prefix given in argument takes precedence. "
                    )
                if not prefix:
                    prefix = splitlabel[0]

        if prefix:
            entityset = self.get_by_label_all(
                label,
                label_annotations=label_annotations,
                prefix=prefix,
            )
            if len(entityset) == 1:
                return entityset.pop()
            if len(entityset) > 1:
                raise AmbiguousLabelError(
                    f"Several entities have the same label '{label}' "
                    f"with prefix '{prefix}'."
                )
            raise NoSuchLabelError(
                f"No label annotations matches for '{label}' "
                f"with prefix '{prefix}'."
            )

        # Label is a full IRI
        entity = self.world[label]
        if entity:
            return entity

        get_triples = (
            self.world._get_data_triples_spod_spod
            if imported
            else self._get_data_triples_spod_spod
        )

        for storid in self._to_storids(label_annotations):
            for s, _, _, _ in get_triples(None, storid, label, None):
                return self.world[self._unabbreviate(s)]

        # Special labels
        if self._special_labels and label in self._special_labels:
            return self._special_labels[label]

        # Check if label is a name under base_iri
        entity = self.world[self.base_iri + label]
        if entity:
            return entity

        # Check label is the name of an entity
        for entity in self.get_entities(imported=imported):
            if label == entity.name:
                return entity

        raise NoSuchLabelError(f"No label annotations matches '{label}'")

    def get_by_label_all(
        self,
        label,
        label_annotations=None,
        prefix=None,
        exact_match=False,
    ) -> "Set[Optional[owlready2.entity.EntityClass]]":
        """Returns set of entities with label annotation `label`.

        Arguments:
           label: label so search for.
               May be written as 'label' or 'prefix:label'.  Wildcard matching
               using glob pattern is also supported if `exact_match` is set to
               false.
           label_annotations: a sequence of label annotation names to look up.
               Defaults to the `label_annotations` property.
           prefix: if provided, it should be the last component of
               the base iri of an ontology (with trailing slash (/) or hash
               (#) stripped off).  The search for a matching label will be
               limited to this namespace.
           exact_match: Do not treat "*" and brackets as special characters
               when matching.  May be useful if your ontology has labels
               containing such labels.

        Returns:
            Set of all matching entities or an empty set if no matches
            could be found.
        """
        if not isinstance(label, str):
            raise TypeError(
                f"Invalid label definition, " f"must be a string: {label!r}"
            )
        if " " in label:
            raise ValueError(
                f"Invalid label definition, {label!r} contains spaces."
            )

        if label_annotations is None:
            label_annotations = self.label_annotations

        entities = set()

        # Check label annotations
        if exact_match:
            for storid in self._to_storids(label_annotations):
                entities.update(
                    self.world._get_by_storid(s)
                    for s, _, _ in self.world._get_data_triples_spod_spod(
                        None, storid, str(label), None
                    )
                )
        else:
            for storid in self._to_storids(label_annotations):
                label_entity = self._unabbreviate(storid)
                key = (
                    label_entity.name
                    if hasattr(label_entity, "name")
                    else label_entity
                )
                entities.update(self.world.search(**{key: label}))

        if self._special_labels and label in self._special_labels:
            entities.update(self._special_labels[label])

        # Check name-part of IRI
        if exact_match:
            entities.update(
                ent for ent in self.get_entities() if ent.name == str(label)
            )
        else:
            matches = fnmatch.filter(
                (ent.name for ent in self.get_entities()), label
            )
            entities.update(
                ent for ent in self.get_entities() if ent.name in matches
            )

        if prefix:
            return set(
                ent
                for ent in entities
                if ent.namespace.ontology.prefix == prefix
            )
        return entities

    def _to_storids(self, sequence, create_if_missing=False):
        """Return a list of storid's corresponding to the elements in the
        sequence `sequence`.

        The elements may be either be full IRIs (strings) or Owlready2
        entities with an associated storid.

        If `create_if_missing` is true, new Owlready2 entities will be
        created for IRIs that not already are associated with an
        entity.  Otherwise such IRIs will be skipped in the returned
        list.
        """
        if not sequence:
            return []
        storids = []
        for element in sequence:
            if hasattr(element, "storid"):
                storids.append(element.storid)
            else:
                storid = self.world._abbreviate(element, create_if_missing)
                if storid:
                    storids.append(storid)
        return storids

    def add_label_annotation(self, iri):
        """Adds label annotation used by get_by_label()."""
        warnings.warn(
            "Ontology.add_label_annotations() is deprecated. "
            "Direct modify the `label_annotations` attribute instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        if hasattr(iri, "iri"):
            iri = iri.iri
        if iri not in self.label_annotations:
            self.label_annotations.append(iri)

    def remove_label_annotation(self, iri):
        """Removes label annotation used by get_by_label()."""
        warnings.warn(
            "Ontology.remove_label_annotations() is deprecated. "
            "Direct modify the `label_annotations` attribute instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        if hasattr(iri, "iri"):
            iri = iri.iri
        try:
            self.label_annotations.remove(iri)
        except ValueError:
            pass

    def set_common_prefix(
        self,
        iri_base: str = "https://w3id.org/emmo/inferred",
        prefix: str = "emmo",
        visited: "Optional[Set]" = None,
    ) -> None:
        """Set a common prefix for all imported ontologies
        with the same first part of the base_iri.

        Note that this function might give unintended results.
        I.e. if `https://w3id.org/emmo` is given as iri_base
        all imported domain ontologies adhering to the
        emmo standard for base_iri will be given the same
        prefix as well as emmo itself.

        The default is to set the prefix to emmo only for emmo-inferred.

        Args:
            iri_base: The start of the base_iri to look for. Defaults to
                the emmo base_iri https://w3id.org/emmo/inferred
            prefix: the desired prefix. Defaults to emmo.
            visited: Ontologies to skip. Only intended for internal use.
        """
        if visited is None:
            visited = set()
        if self.base_iri.startswith(iri_base):
            self.prefix = prefix

        # If importing emmo-inferred set prefix to emmo
        if (
            iri_base == "https://w3id.org/emmo/inferred"
            and self.prefix == "inferred"
            and prefix == "emmo"
            and self.base_iri == "https://w3id.org/emmo#"
        ):
            self.prefix = prefix
        for onto in self.imported_ontologies:
            if not onto in visited:
                visited.add(onto)
                onto.set_common_prefix(
                    iri_base=iri_base, prefix=prefix, visited=visited
                )

    def load(  # pylint: disable=too-many-arguments,arguments-renamed
        self,
        *,
        only_local=False,
        filename=None,
        format=None,  # pylint: disable=redefined-builtin
        reload=None,
        reload_if_newer=False,
        url_from_catalog=None,
        catalog_file="catalog-v001.xml",
        emmo_based=True,
        prefix=None,
        prefix_emmo=None,
        **kwargs,
    ):
        """Load the ontology.

        Arguments
        ---------
        only_local: bool
            Whether to only read local files.  This requires that you
            have appended the path to the ontology to owlready2.onto_path.
        filename: str
            Path to file to load the ontology from.  Defaults to `base_iri`
            provided to get_ontology().
        format: str
            Format of `filename`.  Default is inferred from `filename`
            extension.
        reload: bool
            Whether to reload the ontology if it is already loaded.
        reload_if_newer: bool
            Whether to reload the ontology if the source has changed since
            last time it was loaded.
        url_from_catalog: bool | None
            Whether to use catalog file to resolve the location of `base_iri`.
            If None, the catalog file is used if it exists in the same
            directory as `filename`.
        catalog_file: str
            Name of Protègè catalog file in the same folder as the
            ontology.  This option is used together with `only_local` and
            defaults to "catalog-v001.xml".
        emmo_based: bool
            Whether this is an EMMO-based ontology or not, default `True`.
        prefix: defaults to self.get_namespace.name if
        prefix_emmo: bool, default None. If emmo_based is True it
            defaults to True and sets the prefix of all imported ontologies
            with base_iri starting with 'http://emmo.info/emmo' to emmo
        kwargs:
            Additional keyword arguments are passed on to
            owlready2.Ontology.load().
        """
        # TODO: make sure that `only_local` argument is respected...

        if self.loaded:
            return self
        self._load(
            only_local=only_local,
            filename=filename,
            format=format,
            reload=reload,
            reload_if_newer=reload_if_newer,
            url_from_catalog=url_from_catalog,
            catalog_file=catalog_file,
            **kwargs,
        )

        # Enable optimised search by get_by_label()
        if self._special_labels is None and emmo_based:
            top = self.world["http://www.w3.org/2002/07/owl#topObjectProperty"]
            self._special_labels = {
                "Thing": owlready2.Thing,
                "Nothing": owlready2.Nothing,
                "topObjectProperty": top,
                "owl:Thing": owlready2.Thing,
                "owl:Nothing": owlready2.Nothing,
                "owl:topObjectProperty": top,
            }
        # set prefix if another prefix is desired
        # if we do this, shouldn't we make the name of all
        # entities of the given ontology to the same?
        if prefix:
            self.prefix = prefix
        else:
            self.prefix = self.name

        if emmo_based and prefix_emmo is None:
            prefix_emmo = True
        if prefix_emmo:
            self.set_common_prefix()

        return self

    def _load(  # pylint: disable=too-many-arguments,too-many-locals,too-many-branches,too-many-statements
        self,
        *,
        only_local=False,
        filename=None,
        format=None,  # pylint: disable=redefined-builtin
        reload=None,
        reload_if_newer=False,
        url_from_catalog=None,
        catalog_file="catalog-v001.xml",
        **kwargs,
    ):
        """Help function for load()."""
        web_protocol = "http://", "https://", "ftp://"
        url = str(filename) if filename else self.base_iri.rstrip("/#")
        if url.startswith(web_protocol):
            baseurl = os.path.dirname(url)
            catalogurl = baseurl + "/" + catalog_file
        else:
            if url.startswith("file://"):
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
            not_reload = not reload and (
                not reload_if_newer
                or getmtime(catalogurl)
                > self.world._cached_catalogs[catalogurl][0]
            )
            # get iris from catalog already in cached catalogs
            if catalogurl in self.world._cached_catalogs and not_reload:
                _, iris, dirs = self.world._cached_catalogs[catalogurl]
            # do not update cached_catalogs if url already in _iri_mappings
            # and reload not forced
            elif url in self.world._iri_mappings and not_reload:
                pass
            # update iris from current catalogurl
            else:
                try:
                    iris, dirs = read_catalog(
                        uri=catalogurl,
                        recursive=False,
                        return_paths=True,
                        catalog_file=catalog_file,
                    )
                except ReadCatalogError:
                    if url_from_catalog is not None:
                        raise
                    self.world._cached_catalogs[catalogurl] = (0.0, {}, set())
                else:
                    self.world._cached_catalogs[catalogurl] = (
                        getmtime(catalogurl),
                        iris,
                        dirs,
                    )
            self.world._iri_mappings.update(iris)
        resolved_url = self.world._iri_mappings.get(url, url)
        # Append paths from catalog file to onto_path
        for path in sorted(dirs, reverse=True):
            if path not in owlready2.onto_path:
                owlready2.onto_path.append(path)

        # Use catalog file to update IRIs of imported ontologies
        # in internal store and try to load again...
        if self.world._iri_mappings:
            for abbrev_iri in self.world._get_obj_triples_sp_o(
                self.storid, owlready2.owl_imports
            ):
                iri = self._unabbreviate(abbrev_iri)
                if iri in self.world._iri_mappings:
                    self._del_obj_triple_spo(
                        self.storid, owlready2.owl_imports, abbrev_iri
                    )
                    self._add_obj_triple_spo(
                        self.storid,
                        owlready2.owl_imports,
                        self._abbreviate(self.world._iri_mappings[iri]),
                    )

        # Load ontology
        try:
            self.loaded = False
            fmt = format if format else guess_format(resolved_url, fmap=FMAP)
            if fmt and fmt not in OWLREADY2_FORMATS:
                # Convert filename to rdfxml before passing it to owlready2
                graph = rdflib.Graph()
                try:
                    graph.parse(resolved_url, format=fmt)
                except URLError as err:
                    raise EMMOntoPyException(
                        "URL error", err, resolved_url
                    ) from err

                with tempfile.NamedTemporaryFile() as handle:
                    graph.serialize(destination=handle, format="xml")
                    handle.seek(0)
                    return super().load(
                        only_local=True,
                        fileobj=handle,
                        reload=reload,
                        reload_if_newer=reload_if_newer,
                        format="rdfxml",
                        **kwargs,
                    )
            elif resolved_url.startswith(web_protocol):
                return super().load(
                    only_local=only_local,
                    reload=reload,
                    reload_if_newer=reload_if_newer,
                    **kwargs,
                )

            else:
                with open(resolved_url, "rb") as handle:
                    return super().load(
                        only_local=only_local,
                        fileobj=handle,
                        reload=reload,
                        reload_if_newer=reload_if_newer,
                        **kwargs,
                    )
        except owlready2.OwlReadyOntologyParsingError:
            # Owlready2 is not able to parse the ontology - most
            # likely because imported ontologies must be resolved
            # using the catalog file.

            # Reraise if we don't want to read from the catalog file
            if not url_from_catalog and url_from_catalog is not None:
                raise

            warnings.warn(
                "Recovering from Owlready2 parsing error... might be deprecated"
            )

            # Copy the ontology into a local folder and try again
            with tempfile.TemporaryDirectory() as handle:
                output = os.path.join(handle, os.path.basename(resolved_url))
                convert_imported(
                    input_ontology=resolved_url,
                    output_ontology=output,
                    input_format=fmt,
                    output_format="xml",
                    url_from_catalog=url_from_catalog,
                    catalog_file=catalog_file,
                )

                self.loaded = False
                with open(output, "rb") as handle:
                    try:
                        return super().load(
                            only_local=True,
                            fileobj=handle,
                            reload=reload,
                            reload_if_newer=reload_if_newer,
                            format="rdfxml",
                            **kwargs,
                        )
                    except HTTPError as exc:  # Add url to HTTPError message
                        raise HTTPError(
                            url=exc.url,
                            code=exc.code,
                            msg=f"{exc.url}: {exc.msg}",
                            hdrs=exc.hdrs,
                            fp=exc.fp,
                        ).with_traceback(exc.__traceback__)

        except HTTPError as exc:  # Add url to HTTPError message
            raise HTTPError(
                url=exc.url,
                code=exc.code,
                msg=f"{exc.url}: {exc.msg}",
                hdrs=exc.hdrs,
                fp=exc.fp,
            ).with_traceback(exc.__traceback__)

    def save(
        self,
        filename=None,
        format=None,
        dir=".",
        *,
        mkdir=False,
        overwrite=False,
        recursive=False,
        squash=False,
        namespaces=None,
        write_catalog_file=False,
        append_catalog=False,
        catalog_file="catalog-v001.xml",
        **kwargs,
    ) -> Path:
        """Writes the ontology to file.

        Parameters
        ----------
        filename: None | str | Path
            Name of file to write to.  If None, it defaults to the name
            of the ontology with `format` as file extension.
        format: str
            Output format. The default is to infer it from `filename`.
        dir: str | Path
            If `filename` is a relative path, it is a relative path to `dir`.
        mkdir: bool
            Whether to create output directory if it does not exists.
        owerwrite: bool
            If true and `filename` exists, remove the existing file before
            saving.  The default is to append to an existing ontology.
        recursive: bool
            Whether to save imported ontologies recursively.  This is
            commonly combined with `filename=None`, `dir` and `mkdir`.
            Note that depending on the structure of the ontology and
            all imports the ontology might end up in a subdirectory.
            If filename is given, the ontology is saved to the given
            directory.
            The path to the final location is returned.
        squash: bool
            If true, rdflib will be used to save the current ontology
            together with all its sub-ontologies into `filename`.
            When combining with `recursive`, a folder structure of partly
            overlapping single-file ontologies will be created.
        namespaces: dict
            Dict mapping prefixes to additional namespaces. Only used when
            saving to turtle.
        write_catalog_file: bool
            Whether to also write a catalog file to disk.
        append_catalog: bool
            Whether to append to an existing catalog file.
        catalog_file: str | Path
            Name of catalog file.  If not an absolute path, it is prepended
            to `dir`.

        Returns
        --------
            The path to the saved ontology.
        """
        # pylint: disable=redefined-builtin,too-many-arguments
        # pylint: disable=too-many-statements,too-many-branches
        # pylint: disable=too-many-locals,arguments-renamed,invalid-name

        # Extend rdflib defaults with namespaces suggested by FOOPS
        if namespaces is None:
            namespaces = {}
        default_namespaces = {
            "": self.base_iri,
            "locn": "http://www.w3.org/ns/locn#",
            "swrl": "http://www.w3.org/2003/11/swrl#",
            "bibo": "http://purl.org/ontology/bibo/",
        }
        for prefix, ns in default_namespaces.items():
            if ns not in namespaces.values():
                namespaces[prefix] = ns

        if not _validate_installed_version(
            package="rdflib", min_version="6.0.0"
        ) and format == FMAP.get("ttl", ""):
            from rdflib import (  # pylint: disable=import-outside-toplevel
                __version__ as __rdflib_version__,
            )

            warnings.warn(
                IncompatibleVersion(
                    "To correctly convert to Turtle format, rdflib must be "
                    "version 6.0.0 or greater, however, the detected rdflib "
                    "version used by your Python interpreter is "
                    f"{__rdflib_version__!r}. For more information see the "
                    "'Known issues' section of the README."
                )
            )

        revmap = {value: key for key, value in FMAP.items()}
        if filename is None:
            if format:
                fmt = revmap.get(format, format)
                file = f"{self.name}.{fmt}"
            else:
                raise TypeError("`filename` and `format` cannot both be None.")
        else:
            file = filename
        filepath = os.path.join(
            dir, file if isinstance(file, (str, Path)) else file.name
        )
        returnpath = filepath

        dir = Path(filepath).resolve().parent

        if mkdir:
            outdir = Path(filepath).parent.resolve()
            if not outdir.exists():
                outdir.mkdir(parents=True)

        if not format:
            format = guess_format(file, fmap=FMAP)
        fmt = revmap.get(format, format)

        if overwrite and os.path.exists(filepath):
            os.remove(filepath)

        if recursive:
            layout = directory_layout(self)
            if filename:
                layout[self] = file.rstrip(f".{fmt}")
            # Update path to where the ontology is saved
            # Note that filename should include format when given
            returnpath = Path(dir) / f"{layout[self]}.{fmt}"
            for onto, path in layout.items():
                fname = Path(dir) / f"{path}.{fmt}"
                onto.save(
                    filename=fname,
                    format=format,
                    dir=dir,
                    mkdir=mkdir,
                    overwrite=overwrite,
                    recursive=False,
                    squash=squash,
                    namespaces=namespaces,
                    write_catalog_file=False,
                    **kwargs,
                )

            if write_catalog_file:
                catalog_files = set()
                irimap = {}
                for onto, path in layout.items():
                    irimap[onto.get_version(as_iri=True)] = (
                        f"{dir}/{path}.{fmt}"
                    )
                    catalog_files.add(Path(path).parent / catalog_file)

                for catfile in catalog_files:
                    write_catalog(
                        irimap.copy(),
                        output=catfile,
                        directory=dir,
                        append=append_catalog,
                    )
        elif squash:
            URIRef, RDF, OWL = rdflib.URIRef, rdflib.RDF, rdflib.OWL

            # Make a copy of the owlready2 graph object to not mess with
            # owlready2 internals
            graph = rdflib.Graph()
            for triple in self.world.as_rdflib_graph():
                graph.add(triple)

            # Add additional namespaces to the graph
            for prefix, ns in namespaces.items():
                graph.namespace_manager.bind(
                    prefix, rdflib.Namespace(ns), override=True
                )

            # Remove all ontology-declarations in the graph that are
            # not the current ontology.
            for s, _, _ in graph.triples(  # pylint: disable=not-an-iterable
                (None, RDF.type, OWL.Ontology)
            ):
                if str(s).rstrip("/#") != self.base_iri.rstrip("/#"):
                    for (
                        _,
                        p,
                        o,
                    ) in graph.triples(  # pylint: disable=not-an-iterable
                        (s, None, None)
                    ):
                        graph.remove((s, p, o))
                graph.remove((s, OWL.imports, None))

            # Insert correct IRI of the ontology
            if self.iri:
                base_iri = URIRef(self.base_iri)
                for s, p, o in graph.triples(  # pylint: disable=not-an-iterable
                    (base_iri, None, None)
                ):
                    graph.remove((s, p, o))
                    graph.add((URIRef(self.iri), p, o))

            graph.serialize(destination=filepath, format=format)
        elif format in OWLREADY2_FORMATS:
            super().save(file=filepath, format=fmt, **kwargs)
        else:
            # The try-finally clause is needed for cleanup and because
            # we have to provide delete=False to NamedTemporaryFile
            # since Windows does not allow to reopen an already open
            # file.
            try:
                with tempfile.NamedTemporaryFile(
                    suffix=".owl", delete=False
                ) as handle:
                    tmpfile = handle.name
                super().save(tmpfile, format="ntriples", **kwargs)
                graph = rdflib.Graph()
                graph.parse(tmpfile, format="ntriples")

                # Add additional namespaces to the output graph
                for prefix, ns in namespaces.items():
                    graph.namespace_manager.bind(
                        prefix, rdflib.Namespace(ns), override=True
                    )

                if self.iri:
                    base_iri = rdflib.URIRef(self.base_iri)
                    for (
                        s,
                        p,
                        o,
                    ) in graph.triples(  # pylint: disable=not-an-iterable
                        (base_iri, None, None)
                    ):
                        graph.remove((s, p, o))
                        graph.add((rdflib.URIRef(self.iri), p, o))
                graph.serialize(destination=filepath, format=format)
            finally:
                os.remove(tmpfile)

        if write_catalog_file and not recursive:
            write_catalog(
                {self.get_version(as_iri=True): filepath},
                output=catalog_file,
                directory=dir,
                append=append_catalog,
            )
        return Path(returnpath)

    def copy(self):
        """Return a copy of the ontology."""
        with tempfile.TemporaryDirectory() as dirname:
            filename = self.save(
                dir=dirname,
                format="turtle",
                recursive=True,
                write_catalog_file=True,
                mkdir=True,
            )
            ontology = get_ontology(filename).load()
            ontology.name = self.name
        return ontology

    def get_imported_ontologies(self, recursive=False):
        """Return a list with imported ontologies.

        If `recursive` is `True`, ontologies imported by imported ontologies
        are also returned.
        """

        def rec_imported(onto, imported):
            for ontology in onto.imported_ontologies:
                # pylint: disable=possibly-used-before-assignment
                if ontology not in imported:
                    imported.add(ontology)
                    rec_imported(ontology, imported)

        if recursive:
            imported = set()
            rec_imported(self, imported)
            return list(imported)

        return self.imported_ontologies

    def get_entities(  # pylint: disable=too-many-arguments
        self,
        *,
        imported: bool = True,
        classes: bool = True,
        individuals: bool = True,
        object_properties: bool = True,
        data_properties: bool = True,
        annotation_properties: bool = True,
        properties: bool = True,
    ) -> "Generator[Union[str, object], None, None]":
        """
        This method returns a generator over entities in the ontology,
        including the following categories:
        - Classes (`owl:Class` or `rdfs:Class`)
        - Individuals
        - Object properties (`owl:ObjectProperty`)
        - Data properties (`owl:DataProperty`)
        - Annotation properties (`owl:AnnotationProperty`)
        - Properties (`rdfs:Property`)

        Notes:
        - If `properties` is `True`, `rdfs:Property` entities will be returned
        as IRIs (strings) rather than Python objects.
        - When `imported` is `True`, entities from imported ontologies will
        also be included.

        Arguments:
            imported (bool): Whether to include entities from imported
        ontologies. Defaults to `True`.
            classes (bool): Whether to include classes. Defaults to `True`.
            individuals (bool): Whether to include individuals.
        Defaults to `True`.
            object_properties (bool): Whether to include object properties.
        Defaults to `True`.
            data_properties (bool): Whether to include data properties.
        Defaults to `True`.
            annotation_properties (bool): Whether to include annotation
        properties. Defaults to `True`.
            properties (bool): Whether to include `rdfs:Property` entities.
        Defaults to `True`.

        Yields:
            Entities matching the specified filters.

        """

        generator = []
        if classes:
            generator.append(self.classes(imported))
        if individuals:
            generator.append(self.individuals(imported))
        if object_properties:
            generator.append(self.object_properties(imported))
        if data_properties:
            generator.append(self.data_properties(imported))
        if annotation_properties:
            generator.append(self.annotation_properties(imported))
        if properties:
            generator.append(self.properties(imported))
        yield from itertools.chain(*generator)

    def classes(self, imported=False):
        """Returns an generator over all classes.

        Arguments:
            imported: if `True`, entities in imported ontologies
                are also returned.
        """
        return self._entities("classes", imported=imported)

    def _entities(
        self, entity_type, imported=False
    ):  # pylint: disable=too-many-branches
        """Returns an generator over all entities of the desired type.
        This is a helper function for `classes()`, `individuals()`,
        `object_properties()`, `data_properties()`,
        `annotation_properties()` and `properties`.

        Arguments:
            entity_type: The type of entity desired given as a string.
                Can be any of `classes`, `individuals`,
                `object_properties`, `data_properties`,
                `annotation_properties` or `properties`.
            imported: if `True`, entities in imported ontologies
                are also returned.
        """

        generator = []
        if imported:
            ontologies = self.get_imported_ontologies(recursive=True)
            ontologies.append(self)
            for onto in ontologies:
                if entity_type == "classes":
                    for cls in list(onto.classes()):
                        generator.append(cls)
                elif entity_type == "individuals":
                    for ind in list(onto.individuals()):
                        generator.append(ind)
                elif entity_type == "object_properties":
                    for prop in list(onto.object_properties()):
                        generator.append(prop)
                elif entity_type == "data_properties":
                    for prop in list(onto.data_properties()):
                        generator.append(prop)
                elif entity_type == "annotation_properties":
                    for prop in list(onto.annotation_properties()):
                        generator.append(prop)
                elif entity_type == "properties":
                    generator.append(list(onto.properties()))
        else:
            if entity_type == "classes":
                generator = list(super().classes())
                # Add new triples of type rdfs:Class
                rdf_schema_class = self._abbreviate(
                    "http://www.w3.org/2000/01/rdf-schema#Class"
                )
                for s in self._get_obj_triples_po_s(rdf_type, rdf_schema_class):
                    if not s < 0:
                        generator.append(self.world._get_by_storid(s))
            elif entity_type == "individuals":
                generator = super().individuals()
            elif entity_type == "object_properties":
                generator = super().object_properties()
            elif entity_type == "data_properties":
                generator = super().data_properties()
            elif entity_type == "annotation_properties":
                generator = super().annotation_properties()
            elif entity_type == "properties":
                generator = self.properties()

        yield from generator

    def individuals(self, imported=False):
        """Returns an generator over all individuals.

        Arguments:
            imported: if `True`, entities in imported ontologies
                are also returned.
        """
        return self._entities("individuals", imported=imported)

    def object_properties(self, imported=False):
        """Returns an generator over all object_properties.

        Arguments:
            imported: if `True`, entities in imported ontologies
                are also returned.
        """
        return self._entities("object_properties", imported=imported)

    def data_properties(self, imported=False):
        """Returns an generator over all data_properties.

        Arguments:
            imported: if `True`, entities in imported ontologies
                are also returned.
        """
        return self._entities("data_properties", imported=imported)

    def annotation_properties(self, imported=False):
        """Returns an generator over all annotation_properties.

        Arguments:
            imported: if `True`, entities in imported ontologies
                are also returned.

        """
        return self._entities("annotation_properties", imported=imported)

    def properties(self, imported=False):
        """Returns an generator over all properties.
        It searches for owl:object_properties, owl:data_properties,
        owl:annotation_properties and rdf:Properties

        Arguments:
            imported: if `True`, entities in imported ontologies
                are also returned.
        """
        generator = []
        for prop in list(
            self._entities("object_properties", imported=imported)
        ):
            generator.append(prop)

        for prop in list(
            self._entities("annotation_properties", imported=imported)
        ):
            generator.append(prop)

        for prop in list(self._entities("data_properties", imported=imported)):
            generator.append(prop)

        rdf_property = self._abbreviate(
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
        )
        for s in self._get_obj_triples_po_s(rdf_type, rdf_property):
            if not s < 0:
                generator.append(self._unabbreviate(s))
                # generator.append(self[self._unabbreviate(s)])
                # generator.append(self.world._get_by_storid(s))
        yield from generator

    def get_root_classes(self, imported=False):
        """Returns a list or root classes."""
        return [
            cls
            for cls in self.classes(imported=imported)
            if not cls.ancestors().difference(set([cls, owlready2.Thing]))
        ]

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

    def sync_python_names(self, annotations=("prefLabel", "label", "altLabel")):
        """Update the `python_name` attribute of all properties.

        The python_name attribute will be set to the first non-empty
        annotation in the sequence of annotations in `annotations` for
        the property.
        """

        def update(gen):
            for prop in gen:
                for annotation in annotations:
                    if hasattr(prop, annotation) and getattr(prop, annotation):
                        prop.python_name = getattr(prop, annotation).first()
                        break

        update(
            self.get_entities(
                classes=False,
                individuals=False,
                object_properties=False,
                data_properties=False,
            )
        )
        update(
            self.get_entities(
                classes=False, individuals=False, annotation_properties=False
            )
        )

    def rename_entities(
        self,
        annotations=("prefLabel", "label", "altLabel"),
    ):
        """Set `name` of all entities to the first non-empty annotation in
        `annotations`.

        Warning, this method changes all IRIs in the ontology.  However,
        it may be useful to make the ontology more readable and to work
        with it together with a triple store.
        """
        for entity in self.get_entities():
            for annotation in annotations:
                if hasattr(entity, annotation):
                    name = getattr(entity, annotation).first()
                    if name:
                        entity.name = name
                        break

    def sync_reasoner(
        self, reasoner="HermiT", include_imported=False, **kwargs
    ):
        """Update current ontology by running the given reasoner.

        Supported values for `reasoner` are 'HermiT' (default), Pellet
        and 'FaCT++'.

        If `include_imported` is true, the reasoner will also reason
        over imported ontologies.  Note that this may be **very** slow.

        Keyword arguments are passed to the underlying owlready2 function.
        """
        # pylint: disable=too-many-branches,too-many-locals
        # pylint: disable=unexpected-keyword-arg,invalid-name
        removed_gspo = []  # obj: (ontology, s, p, o)
        removed_gspod = []  # data: (ontology, s, p, o, d)

        if reasoner == "FaCT++":
            sync = sync_reasoner_factpp
            remove_custom_datatypes = True
        elif reasoner == "Pellet":
            sync = owlready2.sync_reasoner_pellet
            remove_custom_datatypes = False
        elif reasoner == "HermiT":
            sync = owlready2.sync_reasoner_hermit
            remove_custom_datatypes = True
        else:
            raise ValueError(
                f"Unknown reasoner '{reasoner}'. Supported reasoners "
                "are 'Pellet', 'HermiT' and 'FaCT++'."
            )

        if include_imported:
            ontologies = [self] + self.get_imported_ontologies(recursive=True)
        else:
            ontologies = [self]

        if remove_custom_datatypes:
            datatype = self._abbreviate(
                "http://www.w3.org/2000/01/rdf-schema#Datatype"
            )
            for onto in ontologies:
                # Collect all defined rdfs:Datatype instances
                for s, p, o in onto._get_obj_triples_spo_spo(o=datatype):
                    for s2, p2, o2 in onto._get_obj_triples_spo_spo(s=s):
                        removed_gspo.append((onto, s2, p2, o2))

                # Datatype instances that are known to crash the reasoner
                datatypes = (
                    "http://www.w3.org/2002/07/owl#rational",
                    "http://www.w3.org/1999/02/22-rdf-syntax-ns#HTML",
                    "http://www.w3.org/1999/02/22-rdf-syntax-ns#JSON",
                    "http://www.w3.org/2001/XMLSchema#NCName",
                    "http://www.w3.org/2001/XMLSchema#NMTOKEN",
                    "http://www.w3.org/2001/XMLSchema#Name",
                    "http://www.w3.org/2001/XMLSchema#base64Binary",
                    "http://www.w3.org/2001/XMLSchema#dateTimeStamp",
                    "http://www.w3.org/2001/XMLSchema#hexBinary",
                    "http://www.w3.org/2001/XMLSchema#language",
                    "http://www.w3.org/2001/XMLSchema#nonPositiveInteger",
                    "http://www.w3.org/2001/XMLSchema#normalizedString",
                    "http://www.w3.org/2001/XMLSchema#token",
                    "http://www.w3.org/2001/XMLSchema#unsignedByte",
                    "http://www.w3.org/2001/XMLSchema#unsignedInt",
                    "http://www.w3.org/2001/XMLSchema#unsignedLong",
                    "http://www.w3.org/2001/XMLSchema#unsignedShort",
                )
                for dtype in datatypes:
                    d = onto._abbreviate(dtype)
                    for s, p, o in onto._get_obj_triples_spo_spo(o=d):
                        for s2, p2, o2 in onto._get_obj_triples_spo_spo(s=s):
                            removed_gspo.append((onto, s2, p2, o2))

        # Remove triples selected for removal
        try:
            for g, s, p, o in removed_gspo:
                g._del_obj_triple_spo(s, p, o)
            for g, s, p, o, d in removed_gspod:
                g._del_data_triple_spod(s, p, o, d)

            # Run reasoner
            with self:
                if include_imported:
                    sync(self.world, **kwargs)
                else:
                    sync(self, **kwargs)

        # Restore removed triples
        finally:
            for g, s, p, o in removed_gspo:
                g._add_obj_triple_spo(s, p, o)
            for g, s, p, o, d in removed_gspod:
                g.world._del_data_triple_spod(s, p, o, d)

    def sync_attributes(  # pylint: disable=too-many-branches
        self,
        name_policy=None,
        name_prefix="",
        class_docstring="comment",
        sync_imported=False,
    ):
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
                        If the name is already valid accoridng to this standard
                        it will not be regenerated.
          "sequential"  `name_prefix` followed a sequantial number.
        EMMO conventions imply ``name_policy=='uuid'``.

        If `sync_imported` is true, all imported ontologies are also
        updated.

        The `class_docstring` argument specifies the annotation that
        class docstrings are mapped to.  Defaults to "comment".
        """
        for cls in itertools.chain(
            self.classes(),
            self.object_properties(),
            self.data_properties(),
            self.annotation_properties(),
        ):
            if not hasattr(cls, "prefLabel"):
                # no prefLabel - create new annotation property..
                with self:
                    # pylint: disable=invalid-name,missing-class-docstring
                    # pylint: disable=unused-variable
                    class prefLabel(owlready2.label):
                        pass

                cls.prefLabel = [locstr(cls.__name__, lang="en")]
            elif not cls.prefLabel:
                cls.prefLabel.append(locstr(cls.__name__, lang="en"))
            if class_docstring and hasattr(cls, "__doc__") and cls.__doc__:
                getattr(cls, class_docstring).append(
                    locstr(inspect.cleandoc(cls.__doc__), lang="en")
                )

        for ind in self.individuals():
            if not hasattr(ind, "prefLabel"):
                # no prefLabel - create new annotation property..
                with self:
                    # pylint: disable=invalid-name,missing-class-docstring
                    # pylint: disable=function-redefined
                    class prefLabel(owlready2.label):
                        iri = "http://www.w3.org/2004/02/skos/core#prefLabel"

                ind.prefLabel = [locstr(ind.name, lang="en")]
            elif not ind.prefLabel:
                ind.prefLabel.append(locstr(ind.name, lang="en"))

        chain = itertools.chain(
            self.classes(),
            self.individuals(),
            self.object_properties(),
            self.data_properties(),
            self.annotation_properties(),
        )
        if name_policy == "uuid":
            for obj in chain:
                try:
                    # Passing the following means that the name is valid
                    # and need not be regenerated.
                    if not obj.name.startswith(name_prefix):
                        raise ValueError
                    uuid.UUID(obj.name.lstrip(name_prefix), version=5)
                except ValueError:
                    obj.name = name_prefix + str(
                        uuid.uuid5(uuid.NAMESPACE_DNS, obj.name)
                    )
        elif name_policy == "sequential":
            for obj in chain:
                counter = 0
                while f"{self.base_iri}{name_prefix}{counter}" in self:
                    counter += 1
                obj.name = f"{name_prefix}{counter}"
        elif name_policy is not None:
            raise TypeError(f"invalid name_policy: {name_policy!r}")

        if sync_imported:
            for onto in self.imported_ontologies:
                onto.sync_attributes()

    def get_relations(self):
        """Returns a generator for all relations."""
        warnings.warn(
            "Ontology.get_relations() is deprecated. Use "
            "onto.object_properties() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.object_properties()

    def get_annotations(self, entity):
        """Returns a dict with annotations for `entity`.  Entity may be given
        either as a ThingClass object or as a label."""
        warnings.warn(
            "Ontology.get_annotations(entity) is deprecated. Use "
            "entity.get_annotations() instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        if isinstance(entity, str):
            entity = self.get_by_label(entity)
        res = {"comment": getattr(entity, "comment", "")}
        for annotation in self.annotation_properties():
            res[annotation.label.first()] = [
                obj.strip('"')
                for _, _, obj in self.get_triples(
                    entity.storid, annotation.storid, None
                )
            ]
        return res

    def get_branch(  # pylint: disable=too-many-arguments
        self,
        root,
        leaves=(),
        include_leaves=True,
        *,
        strict_leaves=False,
        exclude=None,
        sort=False,
    ):
        """Returns a set with all direct and indirect subclasses of `root`.
        Any subclass found in the sequence `leaves` will be included in
        the returned list, but its subclasses will not.  The elements
        of `leaves` may be ThingClass objects or labels.

        Subclasses of any subclass found in the sequence `leaves` will
        be excluded from the returned list, where the elements of `leaves`
        may be ThingClass objects or labels.

        If `include_leaves` is true, the leaves are included in the returned
        list, otherwise they are not.

        If `strict_leaves` is true, any descendant of a leaf will be excluded
        in the returned set.

        If given, `exclude` may be a sequence of classes, including
        their subclasses, to exclude from the output.

        If `sort` is True, a list sorted according to depth and label
        will be returned instead of a set.
        """

        def _branch(root, leaves):
            if root not in leaves:
                branch = {
                    root,
                }
                for cls in root.subclasses():
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
                    if root in cls.get_parents(strict=True):
                        branch.update(_branch(cls, leaves))
            else:
                branch = (
                    {
                        root,
                    }
                    if include_leaves
                    else set()
                )
            return branch

        if isinstance(root, str):
            root = self.get_by_label(root)

        leaves = set(
            self.get_by_label(leaf) if isinstance(leaf, str) else leaf
            for leaf in leaves
        )
        leaves.discard(root)

        if exclude:
            exclude = set(
                self.get_by_label(e) if isinstance(e, str) else e
                for e in exclude
            )
            leaves.update(exclude)

        branch = _branch(root, leaves)

        # Exclude all descendants of any leaf
        if strict_leaves:
            descendants = root.descendants()
            for leaf in leaves:
                if leaf in descendants:
                    branch.difference_update(
                        leaf.descendants(include_self=False)
                    )

        if exclude:
            branch.difference_update(exclude)

        # Sort according to depth, then by label
        if sort:
            branch = sorted(
                sorted(branch, key=asstring),
                key=lambda x: len(x.mro()),
            )

        return branch

    def is_individual(self, entity):
        """Returns true if entity is an individual."""
        if isinstance(entity, str):
            entity = self.get_by_label(entity)
        return isinstance(entity, owlready2.Thing)

    # FIXME - deprecate this method as soon the ThingClass property
    #         `defined_class` works correct in Owlready2
    def is_defined(self, entity):
        """Returns true if the entity is a defined class.

        Deprecated, use the `is_defined` property of the classes
        (ThingClass subclasses) instead.
        """
        warnings.warn(
            "This method is deprecated.  Use the `is_defined` property of "
            "the classes instad.",
            DeprecationWarning,
            stacklevel=2,
        )
        if isinstance(entity, str):
            entity = self.get_by_label(entity)
        return hasattr(entity, "equivalent_to") and bool(entity.equivalent_to)

    def get_version(self, as_iri=False) -> str:
        """Returns the version number of the ontology as inferred from the
        owl:versionIRI tag or, if owl:versionIRI is not found, from
        owl:versionINFO.

        If `as_iri` is True, the full versionIRI is returned.
        """
        version_iri_storid = self.world._abbreviate(
            "http://www.w3.org/2002/07/owl#versionIRI"
        )
        tokens = self.get_triples(s=self.storid, p=version_iri_storid)
        if (not tokens) and (as_iri is True):
            raise TypeError(
                "No owl:versionIRI "
                f"in Ontology {self.base_iri!r}. "
                "Search for owl:versionInfo with as_iri=False"
            )
        if tokens:
            _, _, obj = tokens[0]
            version_iri = self.world._unabbreviate(obj)
            if as_iri:
                return version_iri
            return infer_version(self.base_iri, version_iri)

        version_info_storid = self.world._abbreviate(
            "http://www.w3.org/2002/07/owl#versionInfo"
        )
        tokens = self.get_triples(s=self.storid, p=version_info_storid)
        if not tokens:
            raise TypeError(
                "No versionIRI or versionInfo " f"in Ontology {self.base_iri!r}"
            )
        _, _, version_info = tokens[0]
        return version_info.split("^^")[0].strip('"')

    def set_version(self, version=None, version_iri=None):
        """Assign version to ontology by asigning owl:versionIRI.

        If `version` but not `version_iri` is provided, the version
        IRI will be the combination of `base_iri` and `version`.
        """
        _version_iri = "http://www.w3.org/2002/07/owl#versionIRI"
        version_iri_storid = self.world._abbreviate(_version_iri)
        if self._has_obj_triple_spo(  # pylint: disable=unexpected-keyword-arg
            # For some reason _has_obj_triples_spo exists in both
            # owlready2.namespace.Namespace (with arguments subject/predicate)
            # and in owlready2.triplelite._GraphManager (with arguments s/p)
            # owlready2.Ontology inherits from Namespace directly
            # and pylint checks that.
            # It actually accesses the one in triplelite.
            # subject=self.storid, predicate=version_iri_storid
            s=self.storid,
            p=version_iri_storid,
        ):
            self._del_obj_triple_spo(s=self.storid, p=version_iri_storid)

        if not version_iri:
            if not version:
                raise TypeError(
                    "Either `version` or `version_iri` must be provided"
                )
            head, tail = self.base_iri.rstrip("#/").rsplit("/", 1)
            version_iri = "/".join([head, version, tail])

        self._add_obj_triple_spo(
            s=self.storid,
            p=self.world._abbreviate(_version_iri),
            o=self.world._abbreviate(version_iri),
        )

    def get_graph(self, **kwargs):
        """Returns a new graph object.  See  emmo.graph.OntoGraph.

        Note that this method requires the Python graphviz package.
        """
        # pylint: disable=import-outside-toplevel,cyclic-import
        from ontopy.graph import OntoGraph

        return OntoGraph(self, **kwargs)

    @staticmethod
    def common_ancestors(cls1, cls2):
        """Return a list of common ancestors for `cls1` and `cls2`."""
        return set(cls1.ancestors()).intersection(cls2.ancestors())

    def number_of_generations(self, descendant, ancestor):
        """Return shortest distance from ancestor to descendant"""
        if ancestor not in descendant.ancestors():
            raise ValueError("Descendant is not a descendant of ancestor")
        return self._number_of_generations(descendant, ancestor, 0)

    def _number_of_generations(self, descendant, ancestor, counter):
        """Recursive help function to number_of_generations(), return
        distance between a ancestor-descendant pair (counter+1)."""
        if descendant.name == ancestor.name:
            return counter
        try:
            return min(
                self._number_of_generations(parent, ancestor, counter + 1)
                for parent in descendant.get_parents()
                if ancestor in parent.ancestors()
            )
        except ValueError:
            return counter

    def closest_common_ancestors(self, cls1, cls2):
        """Returns a list with closest_common_ancestor for cls1 and cls2"""
        distances = {}
        for ancestor in self.common_ancestors(cls1, cls2):
            distances[ancestor] = self.number_of_generations(
                cls1, ancestor
            ) + self.number_of_generations(cls2, ancestor)
        return [
            ancestor
            for ancestor, distance in distances.items()
            if distance == min(distances.values())
        ]

    @staticmethod
    def closest_common_ancestor(*classes):
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
        raise EMMOntoPyException(
            "A closest common ancestor should always exist !"
        )

    def get_ancestors(
        self,
        classes: "Union[List, ThingClass]",
        closest: bool = False,
        generations: int = None,
        strict: bool = True,
    ) -> set:
        """Return ancestors of all classes in `classes`.
        Args:
            classes: class(es) for which ancestors should be returned.
            generations: Include this number of generations, default is all.
            closest: If True, return all ancestors up to and including the
                closest common ancestor. Return all if False.
            strict: If True returns only real ancestors, i.e. `classes` are
                are not included in the returned set.
        Returns:
            Set of ancestors to `classes`.
        """
        if not isinstance(classes, Iterable):
            classes = [classes]

        ancestors = set()
        if not classes:
            return ancestors

        def addancestors(entity, counter, subject):
            if counter > 0:
                for parent in entity.get_parents(strict=True):
                    subject.add(parent)
                    addancestors(parent, counter - 1, subject)

        if closest:
            if generations is not None:
                raise ValueError(
                    "Only one of `generations` or `closest` may be specified."
                )

            closest_ancestor = self.closest_common_ancestor(*classes)
            for cls in classes:
                ancestors.update(
                    anc
                    for anc in cls.ancestors()
                    if closest_ancestor in anc.ancestors()
                )
        elif isinstance(generations, int):
            for entity in classes:
                addancestors(entity, generations, ancestors)
        else:
            ancestors.update(*(cls.ancestors() for cls in classes))

        if strict:
            return ancestors.difference(classes)
        return ancestors

    def get_descendants(
        self,
        classes: "Union[List, ThingClass]",
        generations: int = None,
        common: bool = False,
    ) -> set:
        """Return descendants/subclasses of all classes in `classes`.
        Args:
            classes: class(es) for which descendants are desired.
            common: whether to only return descendants common to all classes.
            generations: Include this number of generations, default is all.
        Returns:
            A set of descendants for given number of generations.
            If 'common'=True, the common descendants are returned
            within the specified number of generations.
            'generations' defaults to all.
        """

        if not isinstance(classes, Iterable):
            classes = [classes]

        descendants = {name: [] for name in classes}

        def _children_recursively(num, newentity, parent, descendants):
            """Helper function to get all children up to generation."""
            for child in self.get_children_of(newentity):
                descendants[parent].append(child)
                if num < generations:
                    _children_recursively(num + 1, child, parent, descendants)

        if generations == 0:
            return set()

        if not generations:
            for entity in classes:
                descendants[entity] = entity.descendants()
                # only include proper descendants
                descendants[entity].remove(entity)
        else:
            for entity in classes:
                _children_recursively(1, entity, entity, descendants)

        results = descendants.values()
        if common is True:
            return set.intersection(*map(set, results))
        return set(flatten(results))

    def get_wu_palmer_measure(self, cls1, cls2):
        """Return Wu-Palmer measure for semantic similarity.

        Returns Wu-Palmer measure for semantic similarity between
        two concepts.
        Wu, Palmer; ACL 94: Proceedings of the 32nd annual meeting on
        Association for Computational Linguistics, June 1994.
        """
        cca = self.closest_common_ancestor(cls1, cls2)
        ccadepth = self.number_of_generations(cca, self.Thing)
        generations1 = self.number_of_generations(cls1, cca)
        generations2 = self.number_of_generations(cls2, cca)
        return 2 * ccadepth / (generations1 + generations2 + 2 * ccadepth)

    def new_entity(  # pylint: disable=too-many-arguments,too-many-branches,too-many-positional-arguments
        self,
        name: str,
        parent: Union[
            ThingClass,
            ObjectPropertyClass,
            DataPropertyClass,
            AnnotationPropertyClass,
            Iterable,
        ],
        entitytype: Optional[
            Union[
                str,
                ThingClass,
                ObjectPropertyClass,
                DataPropertyClass,
                AnnotationPropertyClass,
            ]
        ] = "class",
        preflabel: Optional[str] = None,
        iri: Optional[str] = None,
    ) -> Union[
        ThingClass,
        ObjectPropertyClass,
        DataPropertyClass,
        AnnotationPropertyClass,
    ]:
        """Create and return new entity

        Args:
            name: name of the entity
            parent: parent(s) of the entity
            entitytype: type of the entity,
                default is 'class' (str) 'ThingClass' (owlready2 Python class).
                Other options
                are 'data_property', 'object_property',
                'annotation_property' (strings) or the
                Python classes ObjectPropertyClass,
                DataPropertyClass and AnnotationProperty classes.
            preflabel: if given, add this as a skos:prefLabel annotation
                to the new entity.  If None (default), `name` will
                be added as prefLabel if skos:prefLabel is in the ontology
                and listed in `self.label_annotations`.  Set `preflabel` to
                False, to avoid assigning a prefLabel.
            iri: IRI of the entity.  If None, a new IRI will be generated
                based on the ontology base IRI and the entity name.

        Returns:
            the new entity.

        Throws exception if name consists of more than one word, if type is not
        one of the allowed types, or if parent is not of the correct type.
        By default, the parent is Thing.

        """
        # pylint: disable=invalid-name
        if " " in name:
            raise LabelDefinitionError(
                f"Error in label name definition '{name}': "
                f"Label consists of more than one word."
            )
        parents = tuple(parent) if isinstance(parent, Iterable) else (parent,)
        if entitytype == "class":
            parenttype = owlready2.ThingClass
        elif entitytype == "data_property":
            parenttype = owlready2.DataPropertyClass
        elif entitytype == "object_property":
            parenttype = owlready2.ObjectPropertyClass
        elif entitytype == "annotation_property":
            parenttype = owlready2.AnnotationPropertyClass
        elif entitytype in [
            ThingClass,
            ObjectPropertyClass,
            DataPropertyClass,
            AnnotationPropertyClass,
        ]:
            parenttype = entitytype
        else:
            raise EntityClassDefinitionError(
                f"Error in entity type definition: "
                f"'{entitytype}' is not a valid entity type."
            )
        for thing in parents:
            if not isinstance(thing, parenttype):
                raise EntityClassDefinitionError(
                    f"Error in parent definition: "
                    f"'{thing}' is not an {parenttype}."
                )

        with self:
            entity = types.new_class(name, parents)
            if iri:
                entity.iri = iri
            preflabel_iri = "http://www.w3.org/2004/02/skos/core#prefLabel"
            if preflabel:
                if not self.world[preflabel_iri]:
                    pref_label = self.new_annotation_property(
                        "prefLabel",
                        parent=[owlready2.AnnotationProperty],
                    )
                    pref_label.iri = preflabel_iri
                entity.prefLabel = english(preflabel)
            elif (
                preflabel is None
                and preflabel_iri in self.label_annotations
                and self.world[preflabel_iri]
            ):
                entity.prefLabel = english(name)

        return entity

    # Method that creates new ThingClass using new_entity
    def new_class(
        self,
        name: str,
        parent: Union[ThingClass, Iterable],
        iri: Optional[str] = None,
    ) -> ThingClass:
        """Create and return new class.

        Args:
            name: name of the class
            parent: parent(s) of the class
            iri: IRI of the new class.  If None, a new IRI will be generated
                based on the ontology base IRI and the entity name.


        Returns:
            the new class.
        """
        return self.new_entity(name, parent, "class", iri=iri)

    # Method that creates new ObjectPropertyClass using new_entity
    def new_object_property(
        self,
        name: str,
        parent: Union[ObjectPropertyClass, Iterable],
        iri: Optional[str] = None,
    ) -> ObjectPropertyClass:
        """Create and return new object property.

        Args:
            name: name of the object property
            parent: parent(s) of the object property
            iri: IRI of the new object property.  If None, a new IRI will be
                based on the ontology base IRI and the entity name.
        Returns:
            the new object property.
        """
        return self.new_entity(name, parent, "object_property", iri=iri)

    # Method that creates new DataPropertyClass using new_entity
    def new_data_property(
        self,
        name: str,
        parent: Union[DataPropertyClass, Iterable],
        iri: Optional[str] = None,
    ) -> DataPropertyClass:
        """Create and return new data property.

        Args:
            name: name of the data property
            parent: parent(s) of the data property
            iri: IRI of the new data property.  If None, a new IRI will be
                based on the ontology base IRI and the entity name.

        Returns:
            the new data property.
        """
        return self.new_entity(name, parent, "data_property", iri=iri)

    # Method that creates new AnnotationPropertyClass using new_entity
    def new_annotation_property(
        self,
        name: str,
        parent: Union[AnnotationPropertyClass, Iterable],
        iri: Optional[str] = None,
    ) -> AnnotationPropertyClass:
        """Create and return new annotation property.

        Args:
            name: name of the annotation property
            parent: parent(s) of the annotation property
            iri: IRI of the new annotation property.  If None, a new IRI will
                be based on the ontology base IRI and the entity name.
        Returns:
            the new annotation property.
        """
        return self.new_entity(name, parent, "annotation_property", iri=iri)

    def difference(self, other: owlready2.Ontology) -> set:
        """Return a set of triples that are in this, but not in the
        `other` ontology."""
        # pylint: disable=invalid-name
        s1 = set(self.get_unabbreviated_triples(blank="_:b"))
        s2 = set(other.get_unabbreviated_triples(blank="_:b"))
        return s1.difference(s2)

    def find(
        self, text: str, domain="world", case_sensitive=False, regex=False
    ) -> "Iterator":
        """A simple alternative to the  Owlready2 `search()` method.

        This method searches through all literal strings in the given domain.

        Args:
            text: Free text string to search for.
            domain: Domain to search. Should be one of:
                - "ontology": Current ontology.
                - "imported": Current and all imported ontologies.
                - "world": The world.
            case_sensitive: Whether the search is case sensitive.
            regex: Whether to use regular expression search.

        Returns:
            Iterator over `(subject, predicate, literal_string)` triples,
            converted to EMMOntoPy objects.

        """
        # pylint: disable=too-many-locals,too-many-branches

        if domain == "ontology":
            ontologies = [self]
        elif domain == "imported":
            ontologies = [self] + self.get_imported_ontologies(recursive=True)
        elif domain == "world":
            ontologies = [self.world]
        else:
            raise ValueError(
                "`domain` must be 'ontology', 'imported' or 'world'. "
                f"Got: {domain}"
            )

        # Define our match function
        if regex:
            flags = 0 if case_sensitive else re.IGNORECASE
            pattern = re.compile(f"{text}", flags=flags)

            def matchfun(string):
                """Match function using regex."""
                return re.match(pattern, string)

        else:
            if not case_sensitive:
                text = text.lower()

            def matchfun(string):
                """Match function without regex."""
                if case_sensitive:
                    return text in string
                return text in string.lower()

        ontology_storid = self.world._abbreviate(
            "http://www.w3.org/2002/07/owl#Ontology"
        )
        for onto in ontologies:
            for s, p, o, _ in onto._get_data_triples_spod_spod(
                None, None, None, None
            ):
                predicate = self.world.get(self.world._unabbreviate(p))
                if isinstance(o, str) and matchfun(o):
                    assert isinstance(
                        s, int
                    ), "subject should be a storid"  # nosec
                    if s >= 0:
                        subject = self.world.get(self.world._unabbreviate(s))
                        if s == ontology_storid:
                            yield self.world.get_ontology(
                                subject.iri
                            ), predicate, o
                        yield subject, predicate, o
                    else:
                        yield BlankNode(self.world, s), predicate, o


class BlankNode:
    """Represents a blank node.

    A blank node is a node that is not a literal and has no IRI.
    Resources represented by blank nodes are also called anonumous resources.
    Only the subject or object in an RDF triple can be a blank node.
    """

    def __init__(self, onto: Union[World, Ontology], storid: int):
        """Initiate a blank node.

        Args:
            onto: Ontology or World instance.
            storid: The storage id of the blank node.
        """
        if storid >= 0:
            raise ValueError(
                f"A BlankNode is supposed to have a negative storid: {storid}"
            )
        self.onto = onto
        self.storid = storid

    def __repr__(self):
        return repr(f"_:b{-self.storid}")

    def __hash__(self):
        return hash((self.onto, self.storid))

    def __eq__(self, other):
        """For now blank nodes always compare true against each other."""
        return isinstance(other, BlankNode)


def flatten(items):
    """Yield items from any nested iterable."""
    for item in items:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten(item)
        else:
            yield item


def _unabbreviate(
    onto: Union[World, Ontology],
    storid: Union[int, str],
    blank: Optional[str] = None,
):
    """Help function returning unabbreviation of `storid`.

    The `storid` argument is normally be an integer corresponding to
    a store id.  If it is not an integer, it is assumed to already
    be unabbreviated and returned as is.

    If `blank` is given, it will be used to represent blank nodes
    (corresponding to a negative store id).
    """
    if isinstance(storid, int):
        # negative storid corresponds to blank nodes
        if storid >= 0:
            return onto._unabbreviate(storid)
        return BlankNode(onto, storid) if blank is None else blank
    return storid


def _get_unabbreviated_triples(
    onto, subject=None, predicate=None, obj=None, blank=None
):
    """Help function returning all matching triples unabbreviated.
    Does not include imported ontologies.

    If `blank` is given, it will be used to represent blank nodes.
    """
    # pylint: disable=invalid-name
    abb = (
        None if subject is None else onto._abbreviate(subject),
        None if predicate is None else onto._abbreviate(predicate),
        None if obj is None else onto._abbreviate(obj),
    )
    for s, p, o in onto._get_obj_triples_spo_spo(*abb):
        yield (
            _unabbreviate(onto, s, blank=blank),
            _unabbreviate(onto, p, blank=blank),
            _unabbreviate(onto, o, blank=blank),
        )
    for s, p, o, d in onto._get_data_triples_spod_spod(*abb, d=None):
        yield (
            _unabbreviate(onto, s, blank=blank),
            _unabbreviate(onto, p, blank=blank),
            (
                f'"{o}"{d}'
                if isinstance(d, str)
                else f'"{o}"^^{_unabbreviate(onto, d)}' if d else o
            ),
        )
