"""Module for the ontokit docs sub-command."""

# pylint: disable=fixme

import shutil
from pathlib import Path

from sphinx.cmd.build import main as sphinx_main

from ontopy.ontodoc_rst import OntologyDocumentation
from ontopy.ontology import get_ontology
from ontopy.ontokit.config import (
    get_config_path,
    load_config,
    missing_required_variables,
)


def docs_arguments(subparsers):
    """Define arguments for the docs sub-command."""
    parser = subparsers.add_parser(
        "docs",
        help=("Create the html documentation for the ontology."),
    )
    parser.set_defaults(subcommand=docs_subcommand)

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show Python traceback on error.",
    )

    parser.add_argument(
        "root",
        metavar="PATH",
        help="Root folder of repository to create html documentation for."
        "Should be the same as used in the setup command.",
    )

    parser.add_argument(
        "--imported",
        "-i",
        action="store_false",
        help=("Whether to include imported ontologies. Default is False."),
    )

    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help=(
            "Whether to recursively import all imported ontologies. "
            "Implies `imported=True`."
        ),
    )

    parser.add_argument(
        "--iri-regex",
        "-x",
        help=(
            "A regular expression that the IRI of documented entities "
            "should match."
        ),
    )

    parser.add_argument(
        "--outfile",
        "-o",
        metavar="FILE",
        help="Output file for the generated documentation (reStructuredText)."
        "Default is 'docs/index.rst'.",
    )

    parser.add_argument(
        "--ontology-file",
        "-f",
        metavar="FILE",
        help=(
            "Path to the ontology file to document in the auto-generated "
            "reference index, relative to the root directory. Default is "
            "'build/ontology_name.ttl', where 'ontology_name' is "
            "the value of ONTOLOGY_NAME in the configuration file."
        ),
    )


def docs_subcommand(args):  # pylint: disable=too-many-locals
    """Implements the docs sub-command."""
    root = Path(args.root).resolve()
    config_path = get_config_path(root)
    if not config_path.exists():
        raise FileNotFoundError(
            f"The ontokit configuration file {config_path} does not exist. "
            "Please run ontokit setup first."
        )

    config = load_config(config_path)
    missing = missing_required_variables(config)
    if missing:
        required = ", ".join(missing)
        raise ValueError(
            "Missing required variables in "
            f"{config_path}: {required}. "
            "Please update the file and rerun `ontokit docs`."
        )

    ontology_name = config.get("ONTOLOGY_NAME")
    github_repository = config.get("GITHUB_REPOSITORY")
    build_dir = config.get("BUILD_DIR", "build")

    # Path to ontology file
    if args.ontology_file:
        ontofile = root / args.ontology_file
    else:
        ontofile = (
            root / build_dir / f"{ontology_name}.ttl"
        )  # INFERRED as default?
    onto = get_ontology(ontofile).load()
    od = OntologyDocumentation(
        onto,
        recursive=args.imported,
        iri_regex=args.iri_regex,
    )

    if not args.outfile:
        docfile = root / build_dir / f"{ontology_name}.rst"
    else:
        docfile = root / Path(args.outfile)
    indexfile = docfile.with_name("index.rst")
    conffile = docfile.with_name("conf.py")
    od.write_refdoc(docfile=docfile)
    # if not indexfile.exists():
    od.write_index_template(
        indexfile=indexfile, docfile=docfile, overwrite=True
    )
    # if not conffile.exists():
    od.write_conf_template(
        conffile=conffile,
        docfile=docfile,
        overwrite=True,
        github_repository=github_repository,
    )
    (Path(build_dir) / "_static").mkdir(parents=True, exist_ok=True)

    od.copy_css_file()  # Use default CSS file
    od.copy_js_file()  # Use default collapsible-TOC JS file

    public_dir = "public"

    def build_docs(src, out):
        # Equivalent to: sphinx-build -b html build/ public/
        args = ["-b", "html", src, out]
        code = sphinx_main(args)
        if code != 0:
            raise RuntimeError(f"sphinx-build failed with exit code {code}")

    # Remove public dir if it exists
    path_public_dir = root / public_dir
    if path_public_dir.exists() and path_public_dir.is_dir():
        shutil.rmtree(path_public_dir)
    build_docs(build_dir, public_dir)
