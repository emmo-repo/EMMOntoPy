"""Module for the ontokit setup sub-command."""

# pylint: disable=fixme

import shutil
import subprocess  # nosec
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
    parser.add_argument(
        "--github-pages-branch",
        default="gh-pages",
        metavar="NAME",
        help="Name of the GitHub Pages branch [gh-pages]",
    )
    parser.add_argument(
        "--remote",
        default="origin",
        metavar="NAME",
        help="Remote git repository [origin]",
    )
    parser.add_argument(
        "--no-init",
        action="store_true",
        help="Do not try to initialise GitHub Pages branch.",
    )


def setup_subcommand(args):
    """Implements the setup sub-command."""

    thisdir = Path(__file__).resolve().parent
    srcdir = thisdir / "setup"

    root = Path(args.root).resolve()
    github_dir = root / ".github"
    workflows_dir = github_dir / "workflows"
    scripts_dir = github_dir / "scripts"
    workflows_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

    # TODO: infer ONTOLOGY_PREFIX and ONTOLOGY_IRI
    ontology_name = args.ontology_name if args.ontology_name else root.name
    ontology_prefix = args.ontology_prefix
    ontology_iri = args.ontology_iri

    def ignore(src, names):
        """Return file names to ignore when copying."""
        # pylint: disable=unused-argument
        return [name for name in names if name.endswith("~")]

    shutil.copy(srcdir / "emmocheck_conf.yml", root / ".github")
    shutil.copytree(
        srcdir / "scripts",
        root / ".github" / "scripts",
        ignore=ignore,
        dirs_exist_ok=True,
    )

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

    # Initialise github pages branch
    if not args.no_init:
        args = [
            scripts_dir / "init_ghpages.sh",
            f"--ghpages={args.github_pages_branch}",
            f"--ontology_name={ontology_name}",
            f"--ontology_prefix={ontology_prefix}",
            f"--ontology_iri={ontology_iri}",
            f"--remote={args.remote}",
        ]
        subprocess.call(args, shell=True)  # nosec
