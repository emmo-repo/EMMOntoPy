"""Some generic utility functions."""

# pylint: disable=protected-access,invalid-name,redefined-outer-name
# pylint: disable=import-outside-toplevel
import os
import sys
import re
import datetime
import inspect
import tempfile
import textwrap
from pathlib import Path
from sqlite3 import IntegrityError
from typing import TYPE_CHECKING
import urllib.request
import urllib.parse
import warnings
import defusedxml.ElementTree as ET
from packaging.version import parse as parse_version, Version

from rdflib import Graph, URIRef
from rdflib.util import guess_format
from rdflib.plugin import PluginException

import owlready2
from owlready2.namespace import rdf_type, owl_imports, owl_ontology

from ontopy.exceptions import (
    NoSuchLabelError,
    ReadCatalogError,
    UnknownVersion,
    IncompatibleVersion,
)

if TYPE_CHECKING:
    from typing import Optional, Union


# Preferred language
PREFERRED_LANGUAGE = "en"

# Format mappings: file extension -> rdflib format name
FMAP = {
    "": "turtle",
    "ttl": "turtle",
    "n3": "ntriples",
    "nt": "ntriples",
    "owl": "xml",
    "rdfxml": "xml",
}

# Format extension supported by owlready2
OWLREADY2_FORMATS = "rdfxml", "owl", "xml", "ntriples"


def english(string):
    """Returns `string` as an English location string."""
    return owlready2.locstr(string, lang="en")


def isinteractive():
    """Returns true if we are running from an interactive interpreater,
    false otherwise."""
    return bool(
        hasattr(__builtins__, "__IPYTHON__")
        or sys.flags.interactive
        or hasattr(sys, "ps1")
    )


def get_preferred_language(langstrings: list, lang=None) -> str:
    """Given a list of localised strings, return the one in language
    `lang`. If `lang` is not given, use
    `ontopy.utils.PREFERRED_LANGUAGE`.  If no one match is found,
    return the first one with no language tag or fallback to the first
    string.

    The preferred language is stored as a module variable. You can
    change it with:

    >>> import ontopy.utils
    >>> ontopy.utils.PREFERRED_LANGUAGE = "en"

    """
    if lang is None:
        lang = PREFERRED_LANGUAGE
    for langstr in langstrings:
        if hasattr(langstr, "lang") and langstr.lang == lang:
            return str(langstr)
    for langstr in langstrings:
        if not hasattr(langstr, "lang"):
            return langstr
    return str(langstrings[0])


def get_label(entity):
    """Returns the label of an entity."""
    # pylint: disable=too-many-return-statements
    if hasattr(entity, "namespace"):
        onto = entity.namespace.ontology
        if onto.label_annotations:
            for la in onto.label_annotations:
                try:
                    label = entity[la]
                    if label:
                        return get_preferred_language(label)
                except (NoSuchLabelError, AttributeError, TypeError):
                    continue
    if hasattr(entity, "prefLabel") and entity.prefLabel:
        return get_preferred_language(entity.prefLabel)
    if hasattr(entity, "label") and entity.label:
        return get_preferred_language(entity.label)
    if hasattr(entity, "__name__"):
        return entity.__name__
    if hasattr(entity, "name"):
        return str(entity.name)
    if isinstance(entity, str):
        return entity
    return repr(entity)


def getiriname(iri):
    """Return name part of an IRI.

    The name part is what follows after the last slash or hash.
    """
    res = urllib.parse.urlparse(iri)
    return res.fragment if res.fragment else res.path.rsplit("/", 1)[-1]


def asstring(
    expr,
    link="{label}",
    recursion_depth=0,
    exclude_object=False,
    ontology=None,
) -> str:
    """Returns a string representation of `expr`.

    Arguments:
        expr: The entity, restriction or logical expression to represent.
        link: A template for links.  May contain the following variables:
            - {iri}: The full IRI of the concept.
            - {name}: Name-part of IRI.
            - {ref}: "#{name}" if the base iri of hte ontology has the same
              root as {iri}, otherwise "{iri}".
            - {label}: The label of the concept.
            - {lowerlabel}: The label of the concept in lower case and with
              spaces replaced with hyphens.
        recursion_depth: Recursion depth. Only intended for internal use.
        exclude_object: If true, the object will be excluded in restrictions.
        ontology: Ontology object.

    Returns:
        String representation of `expr`.
    """
    # pylint: disable=too-many-return-statements,too-many-branches,too-many-statements
    if ontology is None:
        ontology = expr.ontology

    def fmt(entity):
        """Returns the formatted label of an entity."""
        if isinstance(entity, str):
            if ontology and ontology.world[entity]:
                iri = ontology.world[entity].iri
            elif (
                ontology
                and re.match("^[a-zA-Z0-9_+-]+$", entity)
                and entity in ontology
            ):
                iri = ontology[entity].iri
            else:
                # This may not be a valid IRI, but the best we can do
                iri = entity
            label = entity
        else:
            iri = entity.iri
            label = get_label(entity)
        name = getiriname(iri)
        start = iri.split("#", 1)[0] if "#" in iri else iri.rsplit("/", 1)[0]
        ref = f"#{name}" if ontology.base_iri.startswith(start) else iri
        return link.format(
            entity=entity,
            name=name,
            ref=ref,
            iri=iri,
            label=label,
            lowerlabel=label.lower().replace(" ", "-"),
        )

    if isinstance(expr, str):
        # return link.format(name=expr)
        return fmt(expr)
    if isinstance(expr, owlready2.Restriction):
        rlabel = owlready2.class_construct._restriction_type_2_label[expr.type]

        if isinstance(
            expr.property,
            (owlready2.ObjectPropertyClass, owlready2.DataPropertyClass),
        ):
            res = fmt(expr.property)
        elif isinstance(expr.property, owlready2.Inverse):
            string = asstring(
                expr.property.property,
                link,
                recursion_depth + 1,
                ontology=ontology,
            )
            res = f"Inverse({string})"
        else:
            print(
                f"*** WARNING: unknown restriction property: {expr.property!r}"
            )
            res = fmt(expr.property)

        if not rlabel:
            pass
        elif expr.type in (owlready2.MIN, owlready2.MAX, owlready2.EXACTLY):
            res += f" {rlabel} {expr.cardinality}"
        elif expr.type in (
            owlready2.SOME,
            owlready2.ONLY,
            owlready2.VALUE,
            owlready2.HAS_SELF,
        ):
            res += f" {rlabel}"
        else:
            print("*** WARNING: unknown relation", expr, rlabel)
            res += f" {rlabel}"

        if not exclude_object:
            string = asstring(
                expr.value, link, recursion_depth + 1, ontology=ontology
            )
            res += (
                f" {string!r}" if isinstance(expr.value, str) else f" {string}"
            )
        return res

    Datatype = get_datatype_class()
    if isinstance(expr, Datatype):
        return str(expr).rsplit(".", 1)[-1]

    if isinstance(expr, owlready2.Or):
        res = " or ".join(
            [
                asstring(c, link, recursion_depth + 1, ontology=ontology)
                for c in expr.Classes
            ]
        )
        return res if recursion_depth == 0 else f"({res})"
    if isinstance(expr, owlready2.And):
        res = " and ".join(
            [
                asstring(c, link, recursion_depth + 1, ontology=ontology)
                for c in expr.Classes
            ]
        )
        return res if recursion_depth == 0 else f"({res})"
    if isinstance(expr, owlready2.Not):
        string = asstring(
            expr.Class, link, recursion_depth + 1, ontology=ontology
        )
        return f"not {string}"
    if isinstance(expr, owlready2.ThingClass):
        return fmt(expr)
    if isinstance(expr, owlready2.PropertyClass):
        return fmt(expr)
    if isinstance(expr, owlready2.Thing):  # instance (individual)
        return fmt(expr)
    if isinstance(expr, owlready2.class_construct.Inverse):
        return f"inverse({fmt(expr.property)})"
    if isinstance(expr, owlready2.disjoint.AllDisjoint):
        return fmt(expr)

    if isinstance(expr, (bool, int, float)):
        return repr(expr)
    # Check for subclasses
    if inspect.isclass(expr):
        if issubclass(expr, (bool, int, float, str)):
            return fmt(expr.__class__.__name__)
        if issubclass(expr, datetime.date):
            return "date"
        if issubclass(expr, datetime.time):
            return "datetime"
        if issubclass(expr, datetime.datetime):
            return "datetime"

    raise RuntimeError(f"Unknown expression: {expr!r} (type: {type(expr)!r})")


def camelsplit(string):
    """Splits CamelCase string before upper case letters (except
    if there is a sequence of upper case letters)."""
    if len(string) < 2:
        return string
    result = []
    prev_lower = False
    prev_isspace = True
    char = string[0]
    for next_char in string[1:]:
        if (not prev_isspace and char.isupper() and next_char.islower()) or (
            prev_lower and char.isupper()
        ):
            result.append(" ")
        result.append(char)
        prev_lower = char.islower()
        prev_isspace = char.isspace()
        char = next_char
    result.append(char)
    return "".join(result)


def read_catalog(  # pylint: disable=too-many-locals,too-many-statements,too-many-arguments
    uri,
    *,
    catalog_file="catalog-v001.xml",
    baseuri=None,
    recursive=False,
    relative_to=None,
    return_paths=False,
    visited_iris=None,
    visited_paths=None,
):
    """Reads a Protègè catalog file and returns as a dict.

    The returned dict maps the ontology IRI (name) to its actual
    location (URI).  The location can be either an absolute file path
    or a HTTP, HTTPS or FTP web location.

    `uri` is a string locating the catalog file. It may be a http or
    https web location or a file path.

    The `catalog_file` argument spesifies the catalog file name and is
    used if `path` is used when `recursive` is true or when `path` is a
    directory.

    If `baseuri` is not None, it will be used as the base URI for the
    mapped locations.  Otherwise it defaults to `uri` with its final
    component omitted.

    If `recursive` is true, catalog files in sub-folders are also read.

    if `relative_to` is given, the paths in the returned dict will be
    relative to this path.

    If `return_paths` is true, a set of directory paths to source
    files is returned in addition to the default dict.

    The `visited_uris` and `visited_paths` arguments are only intended for
    internal use to avoid infinite recursions.

    A ReadCatalogError is raised if the catalog file cannot be found.
    """
    # pylint: disable=too-many-branches

    # Protocols supported by urllib.request
    web_protocols = "http://", "https://", "ftp://"
    uri = str(uri)  # in case uri is a pathlib.Path object
    iris = visited_iris if visited_iris else {}
    dirs = visited_paths if visited_paths else set()
    if uri in iris:
        return (iris, dirs) if return_paths else iris

    if uri.startswith(web_protocols):
        # Call read_catalog() recursively to ensure that the temporary
        # file is properly cleaned up
        with tempfile.TemporaryDirectory() as tmpdir:
            destfile = os.path.join(tmpdir, catalog_file)
            uris = {  # maps uri to base
                uri: (baseuri if baseuri else os.path.dirname(uri)),
                f'{uri.rstrip("/")}/{catalog_file}': (
                    baseuri if baseuri else uri.rstrip("/")
                ),
                f"{os.path.dirname(uri)}/{catalog_file}": (
                    os.path.dirname(uri)
                ),
            }
            for url, base in uris.items():
                try:
                    # The URL can only contain the schemes from `web_protocols`.
                    _, msg = urllib.request.urlretrieve(url, destfile)  # nosec
                except urllib.request.URLError:
                    continue
                else:
                    if "Content-Length" not in msg:
                        continue

                    return read_catalog(
                        destfile,
                        catalog_file=catalog_file,
                        baseuri=baseuri if baseuri else base,
                        recursive=recursive,
                        return_paths=return_paths,
                        visited_iris=iris,
                        visited_paths=dirs,
                    )
            raise ReadCatalogError(
                "Cannot download catalog from URLs: " + ", ".join(uris)
            )
    elif uri.startswith("file://"):
        path = uri[7:]
    else:
        path = uri

    if os.path.isdir(path):
        dirname = os.path.abspath(path)
        filepath = os.path.join(dirname, catalog_file)
    else:
        catalog_file = os.path.basename(path)
        filepath = os.path.abspath(path)
        dirname = os.path.dirname(filepath)

    def gettag(entity):
        return entity.tag.rsplit("}", 1)[-1]

    def load_catalog(filepath):
        if not os.path.exists(filepath):
            raise ReadCatalogError("No such catalog file: " + filepath)
        dirname = os.path.normpath(os.path.dirname(filepath))
        dirs.add(baseuri if baseuri else dirname)
        xml = ET.parse(filepath)
        root = xml.getroot()
        if gettag(root) != "catalog":
            raise ReadCatalogError(
                f"expected root tag of catalog file {filepath!r} to be "
                '"catalog"'
            )
        for child in root:
            if gettag(child) == "uri":
                load_uri(child, dirname)
            elif gettag(child) == "group":
                for uri in child:
                    load_uri(uri, dirname)

    def load_uri(uri, dirname):
        if gettag(uri) != "uri":
            raise ValueError(f"{gettag(uri)!r} should be 'uri'.")
        uri_as_str = uri.attrib["uri"]
        if uri_as_str.startswith(web_protocols):
            url = uri_as_str
        else:
            uri_as_str = os.path.normpath(uri_as_str)
            if baseuri and baseuri.startswith(web_protocols):
                url = f"{baseuri}/{uri_as_str}"
            else:
                url = os.path.join(baseuri if baseuri else dirname, uri_as_str)

        iris.setdefault(uri.attrib["name"], url)
        if recursive:
            directory = os.path.dirname(url)
            if directory not in dirs:
                catalog = os.path.join(directory, catalog_file)
                if catalog.startswith(web_protocols):
                    iris_, dirs_ = read_catalog(
                        catalog,
                        catalog_file=catalog_file,
                        baseuri=None,
                        recursive=recursive,
                        return_paths=True,
                        visited_iris=iris,
                        visited_paths=dirs,
                    )
                    iris.update(iris_)
                    dirs.update(dirs_)
                else:
                    load_catalog(catalog)

    load_catalog(filepath)

    if relative_to:
        for iri, path in iris.items():
            iris[iri] = os.path.relpath(path, relative_to)

    if return_paths:
        return iris, dirs
    return iris


def write_catalog(
    irimap: dict,
    output: "Union[str, Path]" = "catalog-v001.xml",
    directory: "Union[str, Path]" = ".",
    relative_paths: bool = True,
    append: bool = False,
):  # pylint: disable=redefined-builtin
    """Write catalog file do disk.

    Arguments:
        irimap: dict mapping ontology IRIs (name) to actual locations
            (URIs).  It has the same format as the dict returned by
            read_catalog().
        output: name of catalog file.
        directory: directory path to the catalog file.  Only used if `output`
            is a relative path.
        relative_paths: whether to write file paths inside the catalog as
            relative paths (instead of  absolute paths).
        append: whether to append to a possible existing catalog file.
            If false, an existing file will be overwritten.
    """
    filename = Path(directory) / output

    if relative_paths:
        irimap = irimap.copy()  # don't modify provided irimap
        for iri, path in irimap.items():
            if os.path.isabs(path):
                irimap[iri] = os.path.relpath(path, filename.parent)

    if filename.exists() and append:
        iris = read_catalog(filename)
        iris.update(irimap)
        irimap = iris

    res = [
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
        '<catalog prefer="public" '
        'xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">',
        '    <group id="Folder Repository, directory=, recursive=true, '
        'Auto-Update=false, version=2" prefer="public" xml:base="">',
    ]
    for iri, path in irimap.items():
        res.append(f'        <uri name="{iri}" uri="{path}"/>')
    res.append("    </group>")
    res.append("</catalog>")
    with open(filename, "wt") as handle:
        handle.write("\n".join(res) + "\n")


def _validate_installed_version(
    package: str, min_version: "Union[str, Version]"
) -> bool:
    """Validate an installed package.

    Examine whether a minimum version is installed in the used Python
    interpreter for a specific package.

    Parameters:
        package: The package to be investigated as a string, e.g., `"rdflib"`.
        min_version: The minimum version expected to be installed.

    Raises:
        UnknownVersion: If the supplied package does not have a `__version__`
            attribute.

    Returns:
        Whether or not the installed version is equal to or greater than the
        `min_version`.

    """
    # pylint: disable=import-outside-toplevel
    import importlib

    if isinstance(min_version, str):
        min_version = parse_version(min_version)
    elif isinstance(min_version, Version):
        # We have the format we want
        pass
    else:
        raise TypeError(
            "min_version should be either a str or packaging.Version. "
            "The latter classes being from the packaging.version module."
        )

    installed_package = importlib.import_module(package)
    installed_package_version = getattr(installed_package, "__version__", None)
    if not installed_package_version:
        raise UnknownVersion(
            f"Cannot retrieve version information from package {package!r}."
        )

    return parse_version(installed_package_version) >= min_version


def convert_imported(  # pylint: disable=too-many-arguments,too-many-locals
    input_ontology: "Union[Path, str]",
    output_ontology: "Union[Path, str]",
    *,
    input_format: "Optional[str]" = None,
    output_format: str = "xml",
    url_from_catalog: "Optional[bool]" = None,
    catalog_file: str = "catalog-v001.xml",
):
    """Convert imported ontologies.

    Store the output in a directory structure matching the source
    files.  This require catalog file(s) to be present.

    Warning:
        To convert to Turtle (`.ttl`) format, you must have installed
        `rdflib>=6.0.0`. See [Known issues](../../../#known-issues) for
        more information.

    Arguments:
        input_ontology: input ontology file name
        output_ontology: output ontology file path. The directory part of
            `output` will be the root of the generated directory structure
        input_format: input format. The default is to infer from
            `input_ontology`
        output_format: output format. The default is to infer from
            `output_ontology`
        url_from_catalog: Whether to read urls form catalog file.
            If False, the catalog file will be used if it exists.
        catalog_file: name of catalog file, that maps ontology IRIs to
            local file names
    """
    inroot = os.path.dirname(os.path.abspath(input_ontology))
    outroot = os.path.dirname(os.path.abspath(output_ontology))
    outext = os.path.splitext(output_ontology)[1]

    if url_from_catalog is None:
        url_from_catalog = os.path.exists(os.path.join(inroot, catalog_file))

    if url_from_catalog:
        iris, dirs = read_catalog(
            inroot, catalog_file=catalog_file, recursive=True, return_paths=True
        )

        # Create output dirs and copy catalog files
        for indir in dirs:
            outdir = os.path.normpath(
                os.path.join(outroot, os.path.relpath(indir, inroot))
            )
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            with open(
                os.path.join(indir, catalog_file), mode="rt", encoding="utf8"
            ) as handle:
                content = handle.read()
            for path in iris.values():
                newpath = os.path.splitext(path)[0] + outext
                content = content.replace(
                    os.path.basename(path), os.path.basename(newpath)
                )
            with open(
                os.path.join(outdir, catalog_file), mode="wt", encoding="utf8"
            ) as handle:
                handle.write(content)
    else:
        iris = {}

    outpaths = set()

    def recur(graph, outext):
        for imported in graph.objects(
            predicate=URIRef("http://www.w3.org/2002/07/owl#imports")
        ):
            inpath = iris.get(str(imported), str(imported))
            if inpath.startswith(("http://", "https://", "ftp://")):
                outpath = os.path.join(outroot, inpath.split("/")[-1])
            else:
                outpath = os.path.join(outroot, os.path.relpath(inpath, inroot))
            outpath = os.path.splitext(os.path.normpath(outpath))[0] + outext
            if outpath not in outpaths:
                outpaths.add(outpath)
                fmt = (
                    input_format
                    if input_format
                    else guess_format(inpath, fmap=FMAP)
                )
                new_graph = Graph()
                new_graph.parse(iris.get(inpath, inpath), format=fmt)
                new_graph.serialize(destination=outpath, format=output_format)
                recur(new_graph, outext)

    # Write output files
    fmt = (
        input_format
        if input_format
        else guess_format(input_ontology, fmap=FMAP)
    )

    if not _validate_installed_version(
        package="rdflib", min_version="6.0.0"
    ) and (output_format == FMAP.get("ttl", "") or outext == "ttl"):
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

    graph = Graph()
    try:
        graph.parse(input_ontology, format=fmt)
    except PluginException as exc:  # Add input_ontology to exception msg
        raise PluginException(
            f'Cannot load "{input_ontology}": {exc.msg}'
        ).with_traceback(exc.__traceback__)
    graph.serialize(destination=output_ontology, format=output_format)
    recur(graph, outext)


def infer_version(iri, version_iri):
    """Infer version from IRI and versionIRI."""
    if str(version_iri[: len(iri)]) == str(iri):
        version = version_iri[len(iri) :].lstrip("/")
    else:
        j = 0
        version_parts = []
        for i, char in enumerate(iri):
            while i + j < len(version_iri) and char != version_iri[i + j]:
                version_parts.append(version_iri[i + j])
                j += 1
        version = "".join(version_parts).lstrip("/").rstrip("/#")

    if "/" in version:
        raise ValueError(
            f"version IRI {version_iri!r} is not consistent with base IRI "
            f"{iri!r}"
        )
    return version


def annotate_source(onto, imported=True):
    """Annotate all entities with the base IRI of the ontology using
    `rdfs:isDefinedBy` annotations.

    If `imported` is true, all entities in imported sub-ontologies will
    also be annotated.

    This is contextual information that is otherwise lost when the ontology
    is squashed and/or inferred.
    """
    source = onto._abbreviate(
        "http://www.w3.org/2000/01/rdf-schema#isDefinedBy"
    )
    for entity in onto.get_entities(imported=imported):
        triple = (
            entity.storid,
            source,
            onto._abbreviate(entity.namespace.ontology.base_iri),
        )
        if not onto._has_obj_triple_spo(*triple):
            onto._add_obj_triple_spo(*triple)


def rename_iris(onto, annotation="prefLabel"):
    """For IRIs with the given annotation, change the name of the entity
    to the value of the annotation.  Also add an `skos:exactMatch`
    annotation referring to the old IRI.
    """
    exactMatch = onto._abbreviate(  # pylint:disable=invalid-name
        "http://www.w3.org/2004/02/skos/core#exactMatch"
    )
    anyURI = onto._abbreviate(  # pylint:disable=invalid-name
        "http://www.w3.org/2001/XMLSchema#anyURI"
    )
    for entity in onto.get_entities():
        if hasattr(entity, annotation) and getattr(entity, annotation):
            onto._add_data_triple_spod(
                entity.storid, exactMatch, entity.iri, anyURI
            )
            entityname = str(entity.name)
            name = getattr(entity, annotation).first()
            if str(name) != entityname:
                try:
                    entity.name = name
                except IntegrityError as exc:
                    raise ValueError(
                        f"cannot set name of {entityname} to '{name}')"
                    ) from exc


def rename_ontology(onto, regex, repl):
    """Rename all ontologies matching `regex`."""
    versionIRI = "http://www.w3.org/2002/07/owl#versionIRI"
    ontologies = [onto] + onto.get_imported_ontoloties(recursive=True)
    for ontology in ontologies:
        if re.match(regex, ontology.base_iri):
            newname = re.sub(regex, repl, ontology.base_iri)
            ontology.base_iri = newname

            if versionIRI in ontology.metadata and re.match(
                regex, ontology.metadata.versionIRI
            ):
                newiri = re.sub(regex, repl, ontology.metadata.versionIRI)
                ontology.metadata.versionIRI = newiri


def normalise_url(url):
    """Returns `url` in a normalised form."""
    splitted = urllib.parse.urlsplit(url)
    components = list(splitted)
    components[2] = os.path.normpath(splitted.path)
    return urllib.parse.urlunsplit(components)


def get_format(outfile: str, default: str, fmt: str = None):
    """Infer format from outfile and format."""
    if fmt is None:
        fmt = os.path.splitext(outfile)[1]
    if not fmt:
        fmt = default
    return fmt.lstrip(".")


def directory_layout(onto):
    """Analyse IRIs of imported ontologies and suggested a directory
    layout for saving recursively.

    Arguments:
        onto: Ontology to analyse.

    Returns:
        layout: A dict mapping ontology objects to relative path names
            derived from the ontology IRIs. No file name extension are
            added.

    Example:
        Assume that our ontology `onto` has IRI `ex:onto`. If it directly
        or indirectly imports ontologies with IRIs `ex:A/ontoA`, `ex:B/ontoB`
        and `ex:A/C/ontoC`, this function will return the following dict:

            {
                onto: "onto",
                ontoA: "A/ontoA",
                ontoB: "B/ontoB",
                ontoC: "A/C/ontoC",
            }

        where `ontoA`, `ontoB` and `ontoC` are imported Ontology objects.
    """
    all_imported = [
        imported.base_iri for imported in onto.indirectly_imported_ontologies()
    ]
    # get protocol and domain of all imported ontologies
    namespace_roots = set()
    for iri in all_imported:
        protocol, domain, *_ = urllib.parse.urlsplit(iri)
        namespace_roots.add("://".join([protocol, domain]))

    def recur(o):
        baseiri = o.base_iri.rstrip("/#")

        # Some heuristics here to reproduce the EMMO layout.
        # It might not apply to all ontologies, so maybe it should be
        # made optional?  Alternatively, change EMMO ontology IRIs to
        # match the directory layout.
        emmolayout = (
            any(
                oo.base_iri.startswith(baseiri + "/")
                for oo in o.imported_ontologies
            )
            or o.base_iri == "http://emmo.info/emmo/mereocausality#"
        )

        layout[o] = (
            baseiri + "/" + os.path.basename(baseiri) if emmolayout else baseiri
        )
        for imported in o.imported_ontologies:
            if imported not in layout:
                recur(imported)

    layout = {}
    recur(onto)
    # Strip off initial common prefix from all paths
    if len(namespace_roots) == 1:
        prefix = os.path.commonprefix(list(layout.values()))
        for o, path in layout.items():
            layout[o] = path[len(prefix) :].lstrip("/")
    else:
        for o, path in layout.items():
            for namespace_root in namespace_roots:
                if path.startswith(namespace_root):
                    layout[o] = (
                        urllib.parse.urlsplit(namespace_root)[1]
                        + path[len(namespace_root) :]
                    )

    return layout


def copy_annotation(onto, src, dst):
    """In all classes and properties in `onto`, copy annotation `src` to `dst`.

    Arguments:
        onto: Ontology to work on.
        src: Name of source annotation.
        dst: Name or IRI of destination annotation.  Use IRI if the
            destination annotation is not already in the ontology.
    """
    if onto.world[src]:
        src = onto.world[src]
    elif src in onto:
        src = onto[src]
    else:

        warnings.warn(f"skipping copy for missing source annotation: {src}")
        return

    if onto.world[dst]:
        dst = onto.world[dst]
    elif dst in onto:
        dst = onto[dst]
    else:
        if "://" not in dst:
            raise ValueError(
                "new destination annotation property must be provided as "
                "a full IRI"
            )
        name = min(dst.rsplit("#")[-1], dst.rsplit("/")[-1], key=len)
        iri = dst
        dst = onto.new_annotation_property(name, owlready2.AnnotationProperty)
        dst.iri = iri

    for e in onto.get_entities():
        new = getattr(e, src.name).first()
        if new and new not in getattr(e, dst.name):
            getattr(e, dst.name).append(new)


def get_datatype_class():
    """Return a class representing rdfs:Datatype."""
    # This is a hack, but I find no other way to access rdfs:Datatype
    # with Owlready2...

    # These cannot be imported at module initialisation time...
    from ontopy import get_ontology
    from ontopy import utils  # pylint: disable=import-self

    # Check is Datatype is cached in module __dict__
    if hasattr(utils, "_Datatype"):
        return utils._Datatype

    # Use try-finally clause instead of delete=True to avoid problems
    # with file-locking on Windows
    filename = None
    try:
        with tempfile.NamedTemporaryFile(
            suffix=".ttl", mode="wt", delete=False
        ) as f:
            filename = f.name
            f.write(
                textwrap.dedent(
                    """
                    @prefix : <http://example.com/onto#> .
                    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
                    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
                    @prefix owl: <http://www.w3.org/2002/07/owl#> .

                    <http://example.com/onto> rdf:type owl:Ontology .

                    :new_datatype rdf:type rdfs:Datatype .
                    """
                )
            )

        onto = get_ontology(filename).load()
        Datatype = onto.new_datatype.__class__
        utils._Datatype = Datatype  # cache Datatype in module __dict__
        return Datatype

    finally:
        if filename:
            os.unlink(filename)
