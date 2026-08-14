"""Module for the ontokit setup sub-command."""

# pylint: disable=fixme

import re
import shutil
import subprocess  # nosec
from glob import glob
from pathlib import Path

from ontopy.ontokit.config import (
    create_config,
    get_config_path,
    load_config,
    missing_required_variables,
    print_config,
    update_config,
)


def _infer_repository(root, remote, provider):
    """Infer repository path from git remote URL.

    Returns `owner/repo` for GitHub remotes and `group[/subgroup]/repo`
    for GitLab remotes.
    """
    # pylint: disable=too-many-return-statements
    cmd = ["git", "-C", str(root), "remote", "get-url", remote]
    proc = subprocess.run(  # nosec
        cmd,
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None

    remote_url = proc.stdout.strip()
    patterns = (
        r"^git@[^:]+:(?P<path>.+?)(?:\.git)?$",
        r"^https://[^/]+/(?P<path>.+?)(?:\.git)?/?$",
        r"^ssh://git@[^/]+/(?P<path>.+?)(?:\.git)?/?$",
    )
    path = None
    for pattern in patterns:
        match = re.match(pattern, remote_url)
        if match:
            path = match.group("path").strip("/")
            break

    if not path:
        return None

    segments = [segment for segment in path.split("/") if segment]
    if provider == "github":
        if len(segments) != 2:
            return None
        return "/".join(segments)

    if provider == "gitlab":
        if len(segments) < 2:
            return None
        return "/".join(segments)

    return None


def _infer_git_base_url(root, remote):
    """Infer Git server host from git remote URL."""
    cmd = ["git", "-C", str(root), "remote", "get-url", remote]
    proc = subprocess.run(  # nosec
        cmd,
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None

    remote_url = proc.stdout.strip()
    patterns = (
        r"^git@(?P<host>[^:]+):.+$",
        r"^https?://(?P<host>[^/]+)/.+$",
        r"^ssh://git@(?P<host>[^/]+)/.+$",
    )
    for pattern in patterns:
        match = re.match(pattern, remote_url)
        if match:
            return match.group("host")
    return None


def setup_arguments(subparsers):
    """Define arguments for the setup sub-command."""
    parser = subparsers.add_parser(
        "setup",
        help=(
            "Set up a repository with CI/CD workflows (GitHub by default), "
            "including "
            "publishing of squashed and inferred ontologies, generation of "
            "documentation, releases, etc..."
        ),
    )
    parser.set_defaults(subcommand=setup_subcommand)
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show Python traceback on error.",
    )
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
        "--ci-provider",
        choices=("github", "gitlab"),
        default="github",
        help="CI provider to scaffold workflows for [github]. "
        "Note: ontokit setup is primarily designed for GitHub "
        "and some features may not work as expected with GitLab. "
        "Users are free to further develop the generated CI "
        "configuration to suit their needs.",
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
        "--github-repository",
        "-g",
        metavar="OWNER/REPO",
        help=(
            "Repository in the form OWNER/REPO or GROUP/SUBGROUP/REPO. "
            "If omitted, inferred from --remote."
        ),
    )
    parser.add_argument(
        "--git-base-url",
        metavar="HOST",
        help=(
            "Git server base host (for example github.com, gitlab.com, "
            "git.company.com). If omitted, inferred from --remote."
        ),
    )
    parser.add_argument(
        "--no-init",
        action="store_true",
        help="Do not try to initialise GitHub Pages branch.",
    )


def setup_subcommand(
    args,
):  # pylint: disable=too-many-locals,too-many-statements
    """Implements the setup sub-command."""

    thisdir = Path(__file__).resolve().parent
    srcdir = thisdir / "setuptemplates"
    ci_provider = args.ci_provider

    root = Path(args.root).resolve()
    github_dir = root / ".github"
    gitlab_dir = root / ".gitlab"

    if ci_provider == "github":
        workflows_dir = github_dir / "workflows"
        scripts_dir = github_dir / "scripts"
        workflows_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
        ci_root_dir = github_dir
    else:
        scripts_dir = gitlab_dir / "scripts"
        gitlab_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
        ci_root_dir = gitlab_dir

    # TODO: infer ONTOLOGY_PREFIX and ONTOLOGY_IRI
    ontology_name = args.ontology_name if args.ontology_name else root.name
    ontology_prefix = args.ontology_prefix
    ontology_iri = args.ontology_iri
    git_repository = args.github_repository or _infer_repository(
        root, args.remote, ci_provider
    )
    git_base_url = args.git_base_url or _infer_git_base_url(root, args.remote)
    if not git_base_url:
        git_base_url = "github.com" if ci_provider == "github" else "gitlab.com"

    config_path = get_config_path(root)
    defaults = {
        "ONTOLOGY_NAME": ontology_name,
        "ONTOLOGY_PREFIX": ontology_prefix,
        "ONTOLOGY_IRI": ontology_iri,
        "GIT_REPOSITORY": git_repository,
        "GIT_BASE_URL": git_base_url,
        "BUILD_DIR": "build",
        "REFERENCE_SUBSECTIONS": "all",
        "REFERENCE_IMPORTED": "false",
        "REFERENCE_RECURSIVE": "true",
        "REFERENCE_IRI_REGEX": f"{ontology_iri}#",
    }
    if config_path.exists():
        config = load_config(config_path)
        config, added = update_config(config_path, config, defaults)
        if added:
            print(
                f"Updated ontokit configuration at {config_path} "
                f"(added: {', '.join(added)}):"
            )
        else:
            print(f"Loaded existing ontokit configuration from {config_path}:")
    else:
        config = create_config(config_path, defaults)
        print(f"Created ontokit configuration at {config_path}:")
    print_config(config)

    missing = missing_required_variables(config)
    if missing:
        required = ", ".join(missing)
        raise ValueError(
            "Missing required variables in "
            f"{config_path}: {required}. "
            "Please update the file and rerun `ontokit setup`."
        )

    ontology_name = config["ONTOLOGY_NAME"]
    ontology_prefix = config["ONTOLOGY_PREFIX"]
    ontology_iri = config["ONTOLOGY_IRI"]
    git_repository = config["GIT_REPOSITORY"]

    def ignore(src, names):
        """Return file names to ignore when copying."""
        # pylint: disable=unused-argument
        ignored = [name for name in names if name.endswith("~")]
        if ci_provider == "gitlab" and Path(src) == srcdir / "scripts":
            ignored.append("init_ghpages.sh")
        return ignored

    shutil.copy(srcdir / "emmocheck_conf.yml", ci_root_dir)
    shutil.copytree(
        srcdir / "scripts",
        scripts_dir,
        ignore=ignore,
        dirs_exist_ok=True,
    )

    if ci_provider == "github":
        for fname in glob(str(srcdir / "workflows" / "*.yml")):
            outfile = workflows_dir / Path(fname).name
            shutil.copy(fname, outfile)
    else:
        shutil.copy(srcdir / "gitlab-ci.yml", root / ".gitlab-ci.yml")

    # Initialise github pages branch
    if ci_provider == "github" and not args.no_init:
        args = [
            scripts_dir / "init_ghpages.sh",
            f"--ghpages={args.github_pages_branch}",
            f"--ontology_name={ontology_name}",
            f"--ontology_prefix={ontology_prefix}",
            f"--ontology_iri={ontology_iri}",
            f"--remote={args.remote}",
        ]
        subprocess.call(args, shell=True)  # nosec
