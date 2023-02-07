# -*- coding: utf-8 -*-
"""A module adding additional functionality to owlready2.

If desirable some of these additions may be moved back into owlready2.
"""
# pylint: disable=too-many-lines,fixme,arguments-differ,protected-access
from typing import TYPE_CHECKING, Optional, Union, Sequence
import os
import itertools
import inspect
import warnings
import uuid
import tempfile
import types
from pathlib import Path
from collections import defaultdict
from collections.abc import Iterable
from urllib.request import HTTPError, URLError

import rdflib
from rdflib.util import guess_format

import owlready2
from owlready2 import locstr
from owlready2.entity import ThingClass

from ontopy.factpluspluswrapper.sync_factpp import sync_reasoner_factpp
from ontopy.utils import (
    asstring,
    read_catalog,
    write_catalog,
    infer_version,
    convert_imported,
    FMAP,
    IncompatibleVersion,
    isinteractive,
    NoSuchLabelError,
    OWLREADY2_FORMATS,
    ReadCatalogError,
    _validate_installed_version,
    LabelDefinitionError,
    ThingClassDefinitionError,
    EMMOntoPyException,
)

if TYPE_CHECKING:
    from typing import List


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

    def get_ontology(self, base_iri="emmo-inferred"):
        """Returns a new Ontology from `base_iri`.

        The `base_iri` argument may be one of:
          - valid URL (possible excluding final .owl or .ttl)
          - file name (possible excluding final .owl or .ttl)
          - "emmo": load latest version of asserted EMMO
          - "emmo-inferred": load latest version of inferred EMMO
            (default)
          - "emmo-development": load latest inferred development version
            of EMMO. Until first stable release emmo-inferred and
            emmo-development will be the same.
        """
        base_iri = base_iri.as_uri() if isinstance(base_iri, Path) else base_iri

        if base_iri == "emmo":
            base_iri = (
                "http://emmo-repo.github.io/versions/1.0.0-beta4/emmo.ttl"
            )
        elif base_iri == "emmo-inferred":
            base_iri = (
                "https://emmo-repo.github.io/versions/1.0.0-beta4/"
                "emmo-inferred.ttl"
            )
        elif base_iri == "emmo-development":
            base_iri = (
                "https://emmo-repo.github.io/versions/1.0.0-beta4/"
                "emmo-inferred.ttl"
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
            onto = Ontology(self, iri)

        return onto

    def get_unabbreviated_triples(
        self, subject=None, predicate=None, obj=None, blank=None
    ):
        # pylint: disable=invalid-name
        """Returns all triples unabbreviated.

        If any of the `subject`, `predicate` or `obj` arguments are given,
        only matching triples will be returned.

        If `blank` is given, it will be used to represent blank nodes.
        """
        return _get_unabbreviated_triples(
            self, subject=subject, predicate=predicate, obj=obj, blank=blank
        )


class Ontology(owlready2.Ontology):  # pylint: disable=too-many-public-methods
    """A generic class extending owlready2.Ontology."""

    def __init__(self, *args, **kwargs):
        # Properties controlling what annotations that are considered by
        # get_by_label()
        super().__init__(*args, **kwargs)
        self._label_annotations = None
        self.prefix = None

    # Properties controlling what annotations that are considered by
    # get_by_label()
    label_annotations = property(
        fget=lambda self: self._label_annotations,
        doc="List of label annotation searched for by get_by_label().",
    )

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

    def __dir__(self):
        set_dir = set(super().__dir__())
        lst = list(self.get_entities(imported=self._dir_imported))
        if self._dir_preflabel:
            set_dir.update(
                _.prefLabel.first() for _ in lst if hasattr(_, "prefLabel")
            )
        if self._dir_label:
            set_dir.update(_.label.first() for _ in lst if hasattr(_, "label"))
        if self._dir_name:
            set_dir.update(_.name for _ in lst if hasattr(_, "name"))

        set_dir.difference_update({None})  # get rid of possible None
        return sorted(set_dir)

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

    def get_by_label(
        self, label: str, label_annotations: str = None, prefix: str = None
    ):
        """Returns entity with label annotation `label`.

        Args:
           label: label so serach for.
               May be written as 'label' or 'prefix:label'.
               get_by_label('prefix:label') ==
               get_by_label('label', prefix='prefix').
           label_annotations: a sequence of label annotation names to look up.
               Defaults to the `label_annotations` property.
           prefix: if provided, it should be the last component of
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
        # pylint: disable=too-many-arguments,too-many-branches
        if not isinstance(label, str):
            raise TypeError(
                f"Invalid label definition, must be a string: {label!r}"
            )
        if " " in label:
            raise ValueError(
                f"Invalid label definition, {label!r} contains spaces."
            )
        if self._label_annotations is None:
            for iri in DEFAULT_LABEL_ANNOTATIONS:
                try:
                    self.add_label_annotation(iri)
                except ValueError:
                    pass

        splitlabel = label.split(":")
        if len(splitlabel) > 2:
            raise ValueError(
                f"Invalid label definition, {label!r}"
                " contains more than one ':' ."
                "The string before ':' indicates the prefix. "
                "The string after ':' indicates the label."
            )
        if len(splitlabel) == 2:
            label = splitlabel[1]
            if prefix and prefix != splitlabel[0]:
                warnings.warn(
                    f"Prefix given both as argument ({prefix}) "
                    f"and in label ({splitlabel[0]}). "
                    "Prefix given in label takes presendence "
                )
            prefix = splitlabel[0]

        if prefix:
            entitylist = self.get_by_label_all(
                label,
                label_annotations=label_annotations,
                prefix=prefix,
            )
            if len(entitylist) > 0:
                return entitylist[0]

            raise NoSuchLabelError(
                f"No label annotations matches {label!r}  with prefix "
                f"{prefix!r}"
            )
            # if label in self._namespaces:
            #    return self._namespaces[label]

        if label_annotations is None:
            annotations = (a.name for a in self.label_annotations)
        else:
            annotations = (
                a.name if hasattr(a, "storid") else a for a in label_annotations
            )
        for key in annotations:
            entity = self.search_one(**{key: label})
            if entity:
                return entity

        if self._special_labels and label in self._special_labels:
            return self._special_labels[label]

        entity = self.world[self.base_iri + label]
        if entity:
            return entity

        raise NoSuchLabelError(f"No label annotations matches {label!r}")

    def get_by_label_all(self, label, label_annotations=None, prefix=None):
        """Like get_by_label(), but returns a list with all matching labels.

        Returns an empty list if no matches could be found.
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
            annotations = (_.name for _ in self.label_annotations)
        else:
            annotations = (
                _.name if hasattr(_, "storid") else _ for _ in label_annotations
            )
        entity = self.world.search(**{next(annotations): label})
        for key in annotations:
            entity.extend(self.world.search(**{key: label}))

        if self._special_labels and label in self._special_labels:
            entity.append(self._special_labels[label])

        entity_accessed_directly = self.world[self.base_iri + label]
        if entity_accessed_directly and entity_accessed_directly not in entity:
            entity.append(entity_accessed_directly)

        if prefix:
            return [_ for _ in entity if _.namespace.ontology.prefix == prefix]
        return entity

    def add_label_annotation(self, iri):
        """Adds label annotation used by get_by_label().

        May be provided either as an IRI or as its owlready2 representation.
        """
        if self._label_annotations is None:
            self._label_annotations = []
        label_annotation = iri if hasattr(iri, "storid") else self.world[iri]
        if label_annotation is None:
            warnings.warn(f"adding new IRI to ontology: {iri}")
            name = iri.rsplit("/")[-1].rsplit("#")[-1]
            bases = (owlready2.AnnotationProperty,)
            with self:
                label_annotation = types.new_class(name, bases)
        if label_annotation not in self._label_annotations:
            self._label_annotations.append(label_annotation)

    def remove_label_annotation(self, iri):
        """Removes label annotation used by get_by_label().

        May be provided either as an IRI or as its owlready2 representation.
        """
        label_annotation = iri if hasattr(iri, "storid") else self.world[iri]
        if not label_annotation:
            raise ValueError(f"IRI not in ontology: {iri}")
        self._label_annotations.remove(label_annotation)

    def set_common_prefix(
        self,
        iri_base: str = "http://emmo.info/emmo",
        prefix: str = "emmo",
    ) -> None:
        """Set a common prefix for all imported ontologies
        with the same first part of the base_iri.

        Args:
            iri_base: The start of the base_iri to look for. Defaults to
                the emmo base_iri http://emmo.info/emmo
            prefix: the desired prefix. Defaults to emmo.
        """
        if self.base_iri.startswith(iri_base):
            self.prefix = prefix
        for onto in self.imported_ontologies:
            onto.set_common_prefix(iri_base=iri_base, prefix=prefix)

    def load(  # pylint: disable=too-many-arguments,arguments-renamed
        self,
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

        Parameters
        ----------
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
            for iri in DEFAULT_LABEL_ANNOTATIONS:
                self.add_label_annotation(iri)
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
        mkdir=False,
        overwrite=False,
        recursive=False,
        squash=False,
        write_catalog_file=False,
        append_catalog=False,
        catalog_file="catalog-v001.xml",
    ):
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
        squash: bool
            If true, rdflib will be used to save the current ontology
            together with all its sub-ontologies into `filename`.
            It make no sense to combine this with `recursive`.
        write_catalog_file: bool
            Whether to also write a catalog file to disk.
        append_catalog: bool
            Whether to append to an existing catalog file.
        catalog_file: str | Path
            Name of catalog file.  If not an absolute path, it is prepended
            to `dir`.
        """
        # pylint: disable=redefined-builtin,too-many-arguments
        # pylint: disable=too-many-statements,too-many-branches
        # pylint: disable=too-many-locals,arguments-renamed
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
                filename = f"{self.name}.{fmt}"
            else:
                raise TypeError("`filename` and `format` cannot both be None.")
        filename = os.path.join(dir, filename)
        dir = Path(filename).resolve().parent

        if mkdir:
            outdir = Path(filename).parent.resolve()
            if not outdir.exists():
                outdir.mkdir(parents=True)

        if not format:
            format = guess_format(filename, fmap=FMAP)
        fmt = revmap.get(format, format)

        if overwrite and filename and os.path.exists(filename):
            os.remove(filename)

        EMMO = rdflib.Namespace(  # pylint:disable=invalid-name
            "http://emmo.info/emmo#"
        )

        if recursive:
            if squash:
                raise ValueError(
                    "`recursive` and `squash` should not both be true"
                )
            base = self.base_iri.rstrip("#/")
            for onto in self.imported_ontologies:
                obase = onto.base_iri.rstrip("#/")
                newdir = Path(dir) / os.path.relpath(obase, base)
                onto.save(
                    filename=None,
                    format=format,
                    dir=newdir.resolve(),
                    mkdir=mkdir,
                    overwrite=overwrite,
                    recursive=recursive,
                    squash=squash,
                    write_catalog_file=write_catalog_file,
                    append_catalog=append_catalog,
                    catalog_file=catalog_file,
                )

        if squash:
            from rdflib import (  # pylint:disable=import-outside-toplevel
                URIRef,
                RDF,
                OWL,
            )

            graph = self.world.as_rdflib_graph()
            graph.namespace_manager.bind("emmo", EMMO)

            # Remove anonymous namespace and imports
            graph.remove((URIRef("http://anonymous"), RDF.type, OWL.Ontology))
            imports = list(graph.triples((None, OWL.imports, None)))
            for triple in imports:
                graph.remove(triple)

            graph.serialize(destination=filename, format=format)
        elif format in OWLREADY2_FORMATS:
            super().save(file=filename, format=fmt)
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
                super().save(tmpfile, format="rdfxml")
                graph = rdflib.Graph()
                graph.parse(tmpfile, format="xml")
                graph.serialize(destination=filename, format=format)
            finally:
                os.remove(tmpfile)

        if write_catalog_file:
            mappings = {}
            base = self.base_iri.rstrip("#/")

            def append(onto):
                obase = onto.base_iri.rstrip("#/")
                newdir = Path(dir) / os.path.relpath(obase, base)
                newpath = newdir.resolve() / f"{onto.name}.{fmt}"
                relpath = os.path.relpath(newpath, dir)
                mappings[onto.get_version(as_iri=True)] = str(relpath)
                for imported in onto.imported_ontologies:
                    append(imported)

            if recursive:
                append(self)
            write_catalog(
                mappings,
                output=catalog_file,
                directory=dir,
                append=append_catalog,
            )

    def get_imported_ontologies(self, recursive=False):
        """Return a list with imported ontologies.

        If `recursive` is `True`, ontologies imported by imported ontologies
        are also returned.
        """

        def rec_imported(onto):
            for ontology in onto.imported_ontologies:
                if ontology not in imported:
                    imported.add(ontology)
                    rec_imported(ontology)

        if recursive:
            imported = set()
            rec_imported(self)
            return list(imported)

        return self.imported_ontologies

    def get_entities(  # pylint: disable=too-many-arguments
        self,
        imported=True,
        classes=True,
        individuals=True,
        object_properties=True,
        data_properties=True,
        annotation_properties=True,
    ):
        """Return a generator over (optionally) all classes, individuals,
        object_properties, data_properties and annotation_properties.

        If `imported` is `True`, entities in imported ontologies will also
        be included.
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
        for entity in itertools.chain(*generator):
            yield entity

    def classes(self, imported=False):
        """Returns an generator over all classes.

        If `imported` is `True`, will imported classes are also returned.
        """
        if imported:
            return self.world.classes()
        return super().classes()

    def individuals(self, imported=False):
        """Returns an generator over all individuals.

        If `imported` is `True`, will imported individuals are also returned.
        """
        if imported:
            return self.world.individuals()
        return super().individuals()

    def object_properties(self, imported=False):
        """Returns an generator over all object properties.

        If `imported` is true, will imported object properties are also
        returned.
        """
        if imported:
            return self.world.object_properties()
        return super().object_properties()

    def data_properties(self, imported=False):
        """Returns an generator over all data properties.

        If `imported` is true, will imported data properties are also
        returned.
        """
        if imported:
            return self.world.data_properties()
        return super().data_properties()

    def annotation_properties(self, imported=False):
        """Returns a generator iterating over all annotation properties
        defined in the current ontology.

        If `imported` is true, annotation properties in imported ontologies
        will also be included.
        """
        if imported:
            return self.world.annotation_properties()
        return super().annotation_properties()

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
        self, reasoner="FaCT++", include_imported=False, **kwargs
    ):
        """Update current ontology by running the given reasoner.

        Supported values for `reasoner` are 'Pellet', 'HermiT' and 'FaCT++'.

        If `include_imported` is true, the reasoner will also reason
        over imported ontologies.  Note that this may be **very** slow
        with Pellet and HermiT.

        Keyword arguments are passed to the underlying owlready2 function.
        """
        if reasoner == "FaCT++":
            sync = sync_reasoner_factpp
        elif reasoner == "Pellet":
            sync = owlready2.sync_reasoner_pellet
        elif reasoner == "HermiT":
            sync = owlready2.sync_reasoner_hermit
        else:
            raise ValueError(
                f"unknown reasoner {reasoner!r}. Supported reasoners "
                'are "Pellet", "HermiT" and "FaCT++".'
            )

        # For some reason we must visit all entities once before running
        # the reasoner...
        list(self.get_entities())

        with self:
            if include_imported:
                sync(self.world, **kwargs)
            else:
                sync(self, **kwargs)

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
        )
        return self.object_properties()

    def get_annotations(self, entity):
        """Returns a dict with annotations for `entity`.  Entity may be given
        either as a ThingClass object or as a label."""
        warnings.warn(
            "Ontology.get_annotations(entity) is deprecated. Use "
            "entity.get_annotations() instead.",
            DeprecationWarning,
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
        leafs=(),
        include_leafs=True,
        strict_leafs=False,
        exclude=None,
        sort=False,
    ):
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
                        branch.update(_branch(cls, leafs))
            else:
                branch = (
                    {
                        root,
                    }
                    if include_leafs
                    else set()
                )
            return branch

        if isinstance(root, str):
            root = self.get_by_label(root)

        leafs = set(
            self.get_by_label(leaf) if isinstance(leaf, str) else leaf
            for leaf in leafs
        )
        leafs.discard(root)

        if exclude:
            exclude = set(
                self.get_by_label(e) if isinstance(e, str) else e
                for e in exclude
            )
            leafs.update(exclude)

        branch = _branch(root, leafs)

        # Exclude all descendants of any leaf
        if strict_leafs:
            descendants = root.descendants()
            for leaf in leafs:
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
        """Returns true if the entity is a defined class."""
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
        return version_info.strip('"').strip("'")

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

    def get_ancestors(self, classes, include="all", strict=True):
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

        def addancestors(entity, counter, subject):
            if counter > 0:
                for parent in entity.get_parents(strict=True):
                    subject.add(parent)
                    addancestors(parent, counter - 1, subject)

        if isinstance(include, str) and include.isdigit():
            include = int(include)

        if include == "all":
            ancestors.update(*(_.ancestors() for _ in classes))
        elif include == "closest":
            closest = self.closest_common_ancestor(*classes)
            for cls in classes:
                ancestors.update(
                    _ for _ in cls.ancestors() if closest in _.ancestors()
                )
        elif isinstance(include, int):
            for entity in classes:
                addancestors(entity, int(include), ancestors)
        elif include not in (None, "None", "none", ""):
            raise ValueError('include must be "all", "closest" or None')

        if strict:
            return ancestors.difference(classes)
        return ancestors

    def get_descendants(
        self,
        classes: "Union[List, ThingClass]",
        common: bool = False,
        generations: int = None,
    ) -> set:
        """Return descendants/subclasses of all classes in `classes`.
        Args:
            classes: to be provided as list.
            common: whether to only return descendants common to all classes.
            generations: Include this number of generations, default is all.
        Returns:
            A set of descendants for given number of generations.
            If 'common'=True, the common descendants are returned
            within the specified number of generations.
            'generations' defaults to all.
        """

        if not isinstance(classes, Sequence):
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

    def new_entity(
        self, name: str, parent: Union[ThingClass, Iterable]
    ) -> ThingClass:
        """Create and return new entity

        Makes a new entity in the ontology with given parent(s).
        Return the new entity.

        Throws exception if name consists of more than one word.
        """
        if len(name.split(" ")) > 1:
            raise LabelDefinitionError(
                f"Error in label name definition '{name}': "
                f"Label consists of more than one word."
            )
        parents = tuple(parent) if isinstance(parent, Iterable) else (parent,)
        for thing in parents:
            if not isinstance(thing, owlready2.ThingClass):
                raise ThingClassDefinitionError(
                    f"Error in parent definition: "
                    f"'{thing}' is not an owlready2.ThingClass."
                )

        with self:
            entity = types.new_class(name, parents)
        return entity


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
            for sub_item in flatten(item):
                yield sub_item
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
    self, subject=None, predicate=None, obj=None, blank=None
):
    """Help function returning all matching triples unabbreviated.

    If `blank` is given, it will be used to represent blank nodes.
    """
    # pylint: disable=invalid-name
    abb = (
        None if subject is None else self._abbreviate(subject),
        None if predicate is None else self._abbreviate(predicate),
        None if obj is None else self._abbreviate(obj),
    )
    for s, p, o in self._get_obj_triples_spo_spo(*abb):
        yield (
            _unabbreviate(self, s, blank=blank),
            _unabbreviate(self, p, blank=blank),
            _unabbreviate(self, o, blank=blank),
        )
    for s, p, o, d in self._get_data_triples_spod_spod(*abb, d=""):
        yield (
            _unabbreviate(self, s, blank=blank),
            _unabbreviate(self, p, blank=blank),
            f'"{o}"{d}'
            if isinstance(d, str)
            else f'"{o}"^^{_unabbreviate(self, d)}'
            if d
            else o,
        )
