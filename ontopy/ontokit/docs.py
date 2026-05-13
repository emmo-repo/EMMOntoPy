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

    parser.add_argument(
        "--docs-dir",
        metavar="DIR",
        help=(
            "Documentation directory to include in the generated "
            "documentation. "
            "Typically the README.md which is included as the landing page "
            "of the documentation links to the docs dir and its contents. "
            "If not provided, the README.md will be included in the "
            "documentation, but the docs dir will not be included."
        ),
    )


# pylint: disable=too-many-locals,too-many-statements,too-many-branches
def docs_subcommand(args):
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
    reference_indices = config.get("REFERENCE_INDICES", [])
    primary_subsections = config.get("REFERENCE_SUBSECTIONS", "all")

    docs_dir = root / args.docs_dir if args.docs_dir else None
    if docs_dir is None:
        default_docs_dir = root / "docs"
        if default_docs_dir.is_dir():
            docs_dir = default_docs_dir

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
        imported=args.imported,
        recursive=args.recursive,
        iri_regex=args.iri_regex,
        subsections=primary_subsections,
    )

    # Optional additional reference indices provided by .ontokit_conf.yml
    if reference_indices and not isinstance(reference_indices, list):
        raise ValueError(
            "REFERENCE_INDICES in .ontokit_conf.yml must be a list."
        )

    for ref in reference_indices:
        if not isinstance(ref, dict):
            raise ValueError("Each REFERENCE_INDICES entry must be a mapping.")
        ref_ontology_file = ref.get("ontology_file")
        if not ref_ontology_file:
            raise ValueError(
                "Each REFERENCE_INDICES entry must define 'ontology_file'."
            )
        ref_onto = get_ontology(root / ref_ontology_file).load()
        od.add_reference(
            ref_onto,
            imported=ref.get("imported", args.imported),
            recursive=ref.get("recursive", False),
            iri_regex=ref.get("iri_regex", args.iri_regex),
            title=ref.get("title", "Reference Index"),
            docfile=ref.get("docfile"),
            subsections=ref.get("subsections", "all"),
        )

    if not args.outfile:
        docfile = root / build_dir / f"{ontology_name}.rst"
    else:
        docfile = root / Path(args.outfile)
    indexfile = docfile.with_name("index.rst")
    conffile = docfile.with_name("conf.py")
    # Write all configured reference indices.
    od.write_reference_docs(outdir=docfile.parent, overwrite=True)
    od.write_index_template(
        indexfile=indexfile,
        docfile=docfile,
        overwrite=True,
        docs_dir=docs_dir,
    )
    od.write_conf_template(
        conffile=conffile,
        docfile=docfile,
        overwrite=True,
        github_repository=github_repository,
    )
    (root / build_dir / "_static").mkdir(parents=True, exist_ok=True)

    od.copy_css_file()  # Use default CSS file
    od.copy_js_file()  # Use default collapsible-TOC JS file

    if docs_dir:
        # Copy repository docs into the build dir so Sphinx consumes the
        # latest landing pages and markdown content on every run.
        dst_docs_dir = root / build_dir / docs_dir.name
        if dst_docs_dir.exists():
            shutil.rmtree(dst_docs_dir)
        shutil.copytree(docs_dir, dst_docs_dir)

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
