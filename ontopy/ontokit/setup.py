"""Module for the ontokit setup sub-command."""

# pylint: disable=fixme

import shutil
from glob import glob
from pathlib import Path
from string import Template


def setup_arguments(subparsers):
    """Define arguments for the setup sub-command."""
    parser = subparsers.add_parser(
        "setup",
        help=(
            "Set up a repository with various github workflows, including "
            "publishing of squashed and inferred ontologies, generation of "
            "documentation, releases, etc..."
        ),
    )
    parser.set_defaults(subcommand=setup_subcommand)
    parser.add_argument(
        "root",
        metavar="PATH",
        help="Root folder of repository to setup.",
    )
    parser.add_argument(
        "--ontology-name",
        "-n",
        metavar="NAME",
        help=(
            "Name of the ontology.  By default it is inferred from the base "
            "name of the `root` folder."
        ),
    )
    parser.add_argument(
        "--ontology-prefix",
        "-p",
        metavar="PREFIX",
        help=(
            "Prefix for the ontology.  By default it is inferred from the "
            "turtle file `{ONTOLOGY_NAME}.ttl`."
        ),
    )
    parser.add_argument(
        "--ontology-iri",
        "-i",
        metavar="IRI",
        help=(
            "IRI for the ontology.  By default it is inferred from the "
            "turtle file `{ONTOLOGY_NAME}.ttl`."
        ),
    )


def setup_subcommand(args):
    """Implements the setup sub-command."""

    thisdir = Path(__file__).resolve().parent
    srcdir = thisdir / "setup"

    root = Path(args.root)
    workflows_dir = root / ".github" / "workflows"
    workflows_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

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
