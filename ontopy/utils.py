"""Some generic utility functions.
"""
# pylint: disable=protected-access
import os
import sys
import re
import datetime
import tempfile
from pathlib import Path
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


if TYPE_CHECKING:
    from typing import Optional, Union


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


class EMMOntoPyException(Exception):
    """A BaseException class for EMMOntoPy"""


class EMMOntoPyWarning(Warning):
    """A BaseWarning class for EMMOntoPy"""


class IncompatibleVersion(EMMOntoPyWarning):
    """An installed dependency version may be incompatible with a functionality
    of this package - or rather an outcome of a functionality.
    This is not critical, hence this is only a warning."""


class UnknownVersion(EMMOntoPyException):
    """Cannot retrieve version from a package."""


class IndividualWarning(EMMOntoPyWarning):
    """A warning related to an individual, e.g. punning."""


class NoSuchLabelError(LookupError, AttributeError, EMMOntoPyException):
    """Error raised when a label cannot be found."""


class LabelDefinitionError(EMMOntoPyException):
    """Error in label definition."""


class ThingClassDefinitionError(EMMOntoPyException):
    """Error in ThingClass definition."""


def isinteractive():
    """Returns true if we are running from an interactive interpreater,
    false otherwise."""
    return bool(
        hasattr(__builtins__, "__IPYTHON__")
        or sys.flags.interactive
        or hasattr(sys, "ps1")
    )


def get_label(entity):
    """Returns the label of an entity."""
    if hasattr(entity, "prefLabel") and entity.prefLabel:
        return entity.prefLabel.first()
    if hasattr(entity, "label") and entity.label:
        return entity.label.first()
    if hasattr(entity, "__name__"):
        return entity.__name__
    if hasattr(entity, "name"):
        return str(entity.name)
    if isinstance(entity, str):
        return entity
    return repr(entity)


def asstring(  # pylint: disable=too-many-return-statements,too-many-branches
    expr, link="{name}", recursion_depth=0, exclude_object=False
):
    """Returns a string representation of `expr`, which may be an entity,
    restriction, or logical expression of these.  `link` is a format
    string for formatting references to entities or relations.  It may
    contain the keywords "name", "url" and "lowerurl".
    `recursion_depth` is the recursion depth and only intended for internal
    use. If `exclude_object` is true, the object will be excluded in
    restrictions.
    """

    def fmt(entity):
        """Returns the formatted label of an entity."""
        name = None
        for attr in ("prefLabel", "label", "__name__", "name"):
            if hasattr(entity, attr) and getattr(entity, attr):
                name = getattr(entity, attr)
                if not isinstance(name, str) and hasattr(name, "__getitem__"):
                    name = name[0]
                break
        if not name:
            name = str(entity).replace(".", ":")
        url = name if re.match(r"^[a-z]+://", name) else "#" + name
        return link.format(name=name, url=url, lowerurl=url.lower())

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
            res = f"Inverse({asstring(expr.property.property, link, recursion_depth + 1)})"  # pylint: disable=line-too-long
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
            if isinstance(expr.value, str):
                res += f" {asstring(expr.value, link, recursion_depth + 1)!r}"
            else:
                res += f" {asstring(expr.value, link, recursion_depth + 1)}"
        return res
    if isinstance(expr, owlready2.Or):
        res = " or ".join(
            [asstring(c, link, recursion_depth + 1) for c in expr.Classes]
        )
        return res if recursion_depth == 0 else f"({res})"
    if isinstance(expr, owlready2.And):
        res = " and ".join(
            [asstring(c, link, recursion_depth + 1) for c in expr.Classes]
        )
        return res if recursion_depth == 0 else f"({res})"
    if isinstance(expr, owlready2.Not):
        return f"not {asstring(expr.Class, link, recursion_depth + 1)}"
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


class ReadCatalogError(IOError):
    """Error reading catalog file."""


def read_catalog(  # pylint: disable=too-many-locals,too-many-statements,too-many-arguments
    uri,
    catalog_file="catalog-v001.xml",
    baseuri=None,
    recursive=False,
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

    If `return_paths` is true, a set of directory paths to source
    files is returned in addition to the default dict.

    The `visited_uris` and `visited_paths` arguments are only intended for
    internal use to avoid infinite recursions.

    A ReadCatalogError is raised if the catalog file cannot be found.
    """
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
    if return_paths:
        return iris, dirs
    return iris


def write_catalog(
    mappings: dict,
    output: "Union[str, Path]" = "catalog-v001.xml",
    directory: "Union[str, Path]" = ".",
    relative_paths: bool = True,
    append: bool = False,
):  # pylint: disable=redefined-builtin
    """Write catalog file do disk.

    Args:
        mappings: dict mapping ontology IRIs (name) to actual locations
            (URIs).  It has the same format as the dict returned by
            read_catalog().
        output: name of catalog file.
        directory: directory path to the catalog file.  Only used if `output`
            is a relative path.
        relative_paths: whether to write absolute or relative paths to
            for file paths inside the catalog file.
        append: whether to append to a possible existing catalog file.
            If false, an existing file will be overwritten.
    """
    web_protocol = "http://", "https://", "ftp://"
    if relative_paths:
        for key, item in mappings.items():
            if not item.startswith(web_protocol):
                mappings[key] = os.path.relpath(item, Path(directory).resolve())
    filename = (Path(directory) / output).resolve()
    if filename.exists() and append:
        iris = read_catalog(filename)
        iris.update(mappings)
        mappings = iris

    res = [
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
        '<catalog prefer="public" '
        'xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">',
        '    <group id="Folder Repository, directory=, recursive=true, '
        'Auto-Update=false, version=2" prefer="public" xml:base="">',
    ]
    for key, value in dict(mappings).items():
        res.append(f'        <uri name="{key}" uri="{value}"/>')
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

    Args:
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
    for entity in onto.get_entities():
        if hasattr(entity, annotation) and getattr(entity, annotation):
            onto._add_data_triple_spod(
                entity.storid, exactMatch, entity.iri, ""
            )
            entity.name = getattr(entity, annotation).first()


def normalise_url(url):
    """Returns `url` in a normalised form."""
    splitted = urllib.parse.urlsplit(url)
    components = list(splitted)
    components[2] = os.path.normpath(splitted.path)
    return urllib.parse.urlunsplit(components)
