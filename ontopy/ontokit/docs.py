"""Module for the ontokit docs sub-command."""

# pylint: disable=fixme

import shutil
from glob import glob
from pathlib import Path
from string import Template


def docs_arguments(subparsers):
    """Define arguments for the docs sub-command."""
    parser = subparsers.add_parser(
        "docs",
        help=("Create the html documentation for the ontology."),
    )
    parser.set_defaults(subcommand=docs_subcommand)


def docs_subcommand(args):
    """Implements the docs sub-command."""

    thisdir = Path(__file__).resolve().parent
    srcdir = thisdir / "setup"

    root = Path(args.root)
    workflows_dir = root / ".github" / "workflows"
    # check that workflows dir exists, raise error saying that it is missing
    # and ask to run setup first
    if not workflows_dir.exists():
        raise FileNotFoundError(
            f"The workflows directory {workflows_dir} does not exist. "
            "Please run ontokit setup first."
        )

    # TODO: infer ONTOLOGY_PREFIX and ONTOLOGY_IRI
    ontology_name = args.ontology_name if args.ontology_name else root.name
    ontology_prefix = args.ontology_prefix
    ontology_iri = args.ontology_iri

    shutil.copy(srcdir / "emmocheck_conf.yml", root / ".github")

    for fname in glob(str(srcdir / "workflows" / "*.yml")):
        template = Template(Path(fname).read_text())
        substituted = template.safe_substitute(
            {
                "ONTOLOGY_NAME": ontology_name,
                "ONTOLOGY_PREFIX": ontology_prefix,
                "ONTOLOGY_IRI": ontology_iri,
            }
        )
        outfile = workflows_dir / Path(fname).name
        outfile.write_text(substituted)
