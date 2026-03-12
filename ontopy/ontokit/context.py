"""Ontokit module for generating JSON-LD context from an ontology."""

# pylint: disable=too-many-locals

import datetime
import json
from itertools import chain

from ontopy import get_ontology
from ontopy.utils import get_label

import owlready2  # pylint: disable=wrong-import-order


def context_arguments(subparsers):
    """Define arguments for the context sub-command."""
    parser = subparsers.add_parser(
        "context", help="Generate a context file from ontology."
    )
    parser.set_defaults(subcommand=context_subcommand)
    parser.add_argument(
        "input",
        metavar="ONTOLOGY",
        help="Input ontology. Either a file path or an URL.",
    )
    parser.add_argument(
        "output",
        metavar="CONTEXT",
        nargs="?",
        help=(
            "Name of output context file. "
            "If omitted, is the context written to stdout."
        ),
    )
    parser.add_argument(
        "--include-imported",
        "-i",
        action="store_true",
        help=(
            "Whether to include properties and classes from imported "
            "ontologies."
        ),
    )
    parser.add_argument(
        "--indent", type=int, default=2, help="Indentation in JSON-LD output."
    )
    parser.add_argument(
        "--namespace",
        "-n",
        metavar="PREFIX:NAMESPACE",
        action="append",
        default=[],
        help=(
            "Additional prefix:namespace pair that will be added to the "
            "output context.  May be added multiple times."
        ),
    )


def context_subcommand(args):
    """Implements the context sub-command."""
    # pylint: disable=invalid-name
    RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    OWL = "http://www.w3.org/2002/07/owl#"
    XSD = "http://www.w3.org/2001/XMLSchema#"

    # Data properties known by owlready2
    dataprop = {
        int: XSD + "int",
        float: XSD + "double",
        bool: XSD + "boolean",
        str: XSD + "int",
        owlready2.normstr: XSD + "normalizedString",
        owlready2.locstr: RDF + "langString",
        datetime.date: XSD + "date",
        datetime.time: XSD + "time",
        datetime.datetime: XSD + "dateTime",
    }

    onto = get_ontology(args.input).load()
    prefixes = {}
    items = {}

    # Get default prefixes from arguments
    for arg in args.namespace:
        prefix, ns = arg.split(":", 1)
        prefixes[prefix] = ns

    # Object properties
    d = {}
    for prop in onto.object_properties(args.include_imported):
        label = get_label(prop)
        if label:
            d[label] = {"@id": prop.iri, "@type": "@id"}
            prefixes.setdefault(prop.namespace.name, prop.namespace.base_iri)
    items.update({k: d[k] for k in sorted(d)})

    # Annotations and data properties
    d = {}
    for prop in chain(
        onto.annotation_properties(args.include_imported),
        onto.data_properties(args.include_imported),
    ):
        label = get_label(prop)
        tp = (
            RDF + "plainLiteral"
            if not prop.range or prop.range[0] not in dataprop
            else dataprop[prop.range[0]]
        )
        if label:
            d[label] = {"@id": prop.iri, "@type": tp}
            prefixes[prop.namespace.name] = prop.namespace.base_iri
    items.update({k: d[k] for k in sorted(d)})

    # Classes
    d = {}
    for cls in onto.classes(args.include_imported):
        label = get_label(cls)
        if label:
            d[label] = {"@id": cls.iri, "@type": OWL + "Class"}
            prefixes[cls.namespace.name] = cls.namespace.base_iri
    items.update({k: d[k] for k in sorted(d)})

    ctx = {"@version": 1.1}
    ctx.update({k: prefixes[k] for k in sorted(prefixes)})
    ctx.update(items)
    context = {"@context": ctx}

    if args.output:
        with open(args.output, "wt", encoding="utf-8") as f:
            json.dump(context, f, indent=args.indent)
    else:
        print(json.dumps(context, indent=args.indent))
