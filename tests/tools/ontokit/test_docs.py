"""Test the `ontokit docs` sub-command."""

import tempfile

import pytest


def test_run() -> None:
    """Check that running `ontokit docs` with arguments works."""
    from ontopy.ontokit import docs as docs_module
    from ontopy.testutils import get_tool_module

    captured = {}

    def fake_docs_subcommand(args):
        captured["root"] = args.root
        captured["recursive"] = args.recursive
        captured["iri_regex"] = args.iri_regex
        captured["outfile"] = args.outfile
        captured["ontology_file"] = args.ontology_file
        return 0

    monkeypatch = pytest.MonkeyPatch()
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            monkeypatch.setattr(
                docs_module,
                "docs_subcommand",
                fake_docs_subcommand,
            )

            ontokit = get_tool_module("ontokit")
            status = ontokit.main(
                [
                    "docs",
                    str(tmpdir),
                    "--recursive",
                    "--iri-regex",
                    "https://example.org/demo/.*",
                    "--outfile",
                    "docs/custom.rst",
                    "--ontology-file",
                    "build/custom.ttl",
                ]
            )

            assert status == 0
            assert captured["root"] == str(tmpdir)
            assert captured["recursive"] is True
            assert captured["iri_regex"] == "https://example.org/demo/.*"
            assert captured["outfile"] == "docs/custom.rst"
            assert captured["ontology_file"] == "build/custom.ttl"
    finally:
        monkeypatch.undo()
