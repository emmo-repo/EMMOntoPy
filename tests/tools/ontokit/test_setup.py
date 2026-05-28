"""Tests for the `ontokit setup` sub-command."""

from argparse import Namespace
from types import SimpleNamespace

from ontopy.ontokit import setup as ontokit_setup


def test_run_setup_passes_ci_provider(tmp_path, monkeypatch):
    """Check that CLI parsing forwards --ci-provider to setup handler."""
    from ontopy.testutils import get_tool_module

    captured = {}

    def fake_setup_subcommand(args):
        captured["root"] = args.root
        captured["ci_provider"] = args.ci_provider
        return 0

    monkeypatch.setattr(
        ontokit_setup, "setup_subcommand", fake_setup_subcommand
    )

    ontokit = get_tool_module("ontokit")
    status = ontokit.main(["setup", str(tmp_path), "--ci-provider", "gitlab"])

    assert status == 0
    assert captured["root"] == str(tmp_path)
    assert captured["ci_provider"] == "gitlab"


def test_setup_subcommand_writes_gitlab_files(tmp_path):
    """GitLab provider should scaffold .gitlab-ci.yml and .gitlab support files."""
    args = Namespace(
        root=str(tmp_path),
        ci_provider="gitlab",
        ontology_name="demo",
        ontology_prefix="demo",
        ontology_iri="https://example.org/demo",
        github_pages_branch="gh-pages",
        remote="origin",
        github_repository="mygroup/myrepo",
        git_base_url=None,
        no_init=True,
        debug=False,
    )

    ontokit_setup.setup_subcommand(args)

    assert (tmp_path / ".gitlab-ci.yml").exists()
    assert (tmp_path / ".gitlab" / "emmocheck_conf.yml").exists()
    assert not (tmp_path / ".gitlab" / "scripts" / "init_ghpages.sh").exists()
    assert not (tmp_path / ".github" / "workflows").exists()


def test_setup_subcommand_does_not_init_ghpages_for_gitlab(
    tmp_path, monkeypatch
):
    """GitLab provider should not execute GitHub Pages init logic."""
    args = Namespace(
        root=str(tmp_path),
        ci_provider="gitlab",
        ontology_name="demo",
        ontology_prefix="demo",
        ontology_iri="https://example.org/demo",
        github_pages_branch="gh-pages",
        remote="origin",
        github_repository="mygroup/myrepo",
        git_base_url=None,
        no_init=False,
        debug=False,
    )

    called = {}

    def fake_call(*_args, **_kwargs):
        called["value"] = True
        return 0

    monkeypatch.setattr(ontokit_setup.subprocess, "call", fake_call)
    ontokit_setup.setup_subcommand(args)

    assert not called


def test_infer_repository_github(monkeypatch, tmp_path):
    """GitHub owner/repo should be inferred from SSH and HTTPS remotes."""

    def fake_run(*_args, **_kwargs):
        return SimpleNamespace(
            returncode=0,
            stdout="git@github.com:myorg/myrepo.git\n",
        )

    monkeypatch.setattr(ontokit_setup.subprocess, "run", fake_run)
    inferred = ontokit_setup._infer_repository(tmp_path, "origin", "github")
    assert inferred == "myorg/myrepo"


def test_infer_repository_gitlab_subgroup(monkeypatch, tmp_path):
    """GitLab subgroup paths should be preserved in inferred repository."""

    def fake_run(*_args, **_kwargs):
        return SimpleNamespace(
            returncode=0,
            stdout="git@gitlab.example.org:group/subgroup/myrepo.git\n",
        )

    monkeypatch.setattr(ontokit_setup.subprocess, "run", fake_run)
    inferred = ontokit_setup._infer_repository(tmp_path, "origin", "gitlab")
    assert inferred == "group/subgroup/myrepo"


def test_infer_git_base_url_from_company_remote(monkeypatch, tmp_path):
    """Base host should be inferred from enterprise/self-hosted remotes."""

    def fake_run(*_args, **_kwargs):
        return SimpleNamespace(
            returncode=0,
            stdout="git@git.company.example:group/subgroup/myrepo.git\n",
        )

    monkeypatch.setattr(ontokit_setup.subprocess, "run", fake_run)
    inferred = ontokit_setup._infer_git_base_url(tmp_path, "origin")
    assert inferred == "git.company.example"
