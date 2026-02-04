"""Module for the ontokit docs sub-command."""

# pylint: disable=fixme

import shutil
from pathlib import Path

import yaml

from sphinx.cmd.build import main as sphinx_main

from ontopy.ontodoc_rst import OntologyDocumentation
from ontopy.ontology import get_ontology


def docs_arguments(subparsers):
    """Define arguments for the docs sub-command."""
    parser = subparsers.add_parser(
        "docs",
        help=("Create the html documentation for the ontology."),
    )
    parser.set_defaults(subcommand=docs_subcommand)

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


def docs_subcommand(args):  # pylint: disable=too-many-locals
    """Implements the docs sub-command."""

    root = Path(args.root).resolve()
    workflows_dir = root / ".github" / "workflows"
    # check that workflows dir exists, raise error saying that it is missing
    # and ask to run setup first
    if not workflows_dir.exists():
        raise FileNotFoundError(
            f"The workflows directory {workflows_dir} does not exist. "
            "Please run ontokit setup first."
        )

    # Find the file cd_ghpages.yml in the workflows directory
    cd_ghpages_file = workflows_dir / "cd_ghpages.yml"
    if not cd_ghpages_file.exists():
        raise FileNotFoundError(
            f"The file {cd_ghpages_file} does not exist. "
            "Please run ontokit setup first."
        )
    # Parse the file cd_ghpages.yml to find the ontology name, prefix, and IRI
    with open(cd_ghpages_file, "r") as f:
        config = yaml.safe_load(f)

    env = config.get("env", {})

    ontology_name = env.get("ONTOLOGY_NAME")
    # ontology_prefix = env.get("ONTOLOGY_PREFIX")
    # ontology_iri = env.get("ONTOLOGY_IRI")

    # Path to ontology file
    # assumes the ontology for docc: build/ontology_name-inferred.ttl
    ontofile = root / "build" / f"{ontology_name}.ttl"  # INFERRED?
    onto = get_ontology(ontofile).load()
    od = OntologyDocumentation(
        onto,
        recursive=args.imported,
        iri_regex=args.iri_regex,
    )

    if not args.outfile:
        docfile = root / "build" / f"{ontology_name}.rst"
    else:
        docfile = root / Path(args.outfile)
    indexfile = docfile.with_name("index.rst")
    conffile = docfile.with_name("conf.py")
    od.write_refdoc(docfile=docfile)
    print(indexfile, type(indexfile))

    # if not indexfile.exists():
    print(f"Generating index template: {indexfile}")
    od.write_index_template(
        indexfile=indexfile, docfile=docfile, overwrite=True
    )
    # if not conffile.exists():
    print(f"Generating configuration template: {conffile}")
    od.write_conf_template(conffile=conffile, docfile=docfile, overwrite=True)
    (Path("build") / "_static").mkdir(parents=True, exist_ok=True)

    od.copy_css_file()  # Use default CSS file

    public_dir = "public"

    def build_docs(src="build", out=public_dir):
        # Equivalent to: sphinx-build -b html build/ public/
        print("g=")
        args = ["-b", "html", src, out]
        print("h=")
        # status = build_main([
        # "-b", "html",
        # "docs",
        # str(build_dir / "html"),
        # ])
        code = sphinx_main(args)
        print("i=")
        if code != 0:
            print("j=")
            raise RuntimeError(f"sphinx-build failed with exit code {code}")
        print("k=")

    # Remove build/ if it exists
    path_public_dir = root / public_dir
    if path_public_dir.exists() and path_public_dir.is_dir():
        shutil.rmtree(path_public_dir)
    print("f)")
    build_docs("build", public_dir)
