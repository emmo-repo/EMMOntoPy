"""Test the `ontokit docs` sub-command."""

from argparse import Namespace
import tempfile
from pathlib import Path

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
        captured["docs_dir"] = args.docs_dir
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


def test_docs_subcommand_refreshes_generated_inputs(tmp_path, monkeypatch):
    """Generated build inputs should be refreshed on each docs run."""
    from ontopy.ontokit import docs as docs_module

    root = tmp_path
    build_dir = root / "build"
    docs_dir = root / "docs"
    public_dir = root / "public"

    build_dir.mkdir()
    docs_dir.mkdir()
    (root / ".ontokit_conf.yml").write_text(
        "\n".join(
            [
                "ONTOLOGY_NAME: core",
                "ONTOLOGY_PREFIX: ssbd",
                "ONTOLOGY_IRI: https://w3id.org/ssbd",
                "GITHUB_REPOSITORY: ssbd-ontology/core",
                "BUILD_DIR: build",
            ]
        )
        + "\n",
        encoding="utf8",
    )
    (docs_dir / "index.md").write_text(
        "# Updated landing page\n\nJSON-LD Playground\n",
        encoding="utf8",
    )
    stale_build_docs = build_dir / "docs"
    stale_build_docs.mkdir()
    (stale_build_docs / "index.md").write_text(
        "# Stale landing page\n\nContext link\n",
        encoding="utf8",
    )
    (build_dir / "index.rst").write_text("stale index\n", encoding="utf8")
    (build_dir / "conf.py").write_text("stale conf\n", encoding="utf8")
    public_dir.mkdir()
    (public_dir / "old.html").write_text("old public\n", encoding="utf8")

    class DummyOntology:
        def load(self):
            return self

    class DummyOD:
        def __init__(self, *_args, **_kwargs):
            self.index_calls = []
            self.conf_calls = []
            self.refdoc_calls = []

        def add_reference(self, *_args, **_kwargs):
            return None

        def write_reference_docs(self, outdir, overwrite=False):
            self.refdoc_calls.append((Path(outdir), overwrite))

        def write_index_template(
            self, indexfile, docfile=None, overwrite=False, docs_dir=None
        ):
            self.index_calls.append(
                (Path(indexfile), Path(docfile), overwrite, Path(docs_dir))
            )
            Path(indexfile).write_text("fresh index\n", encoding="utf8")

        def write_conf_template(
            self,
            conffile,
            docfile=None,
            overwrite=False,
            github_repository=None,
        ):
            self.conf_calls.append(
                (
                    Path(conffile),
                    Path(docfile),
                    overwrite,
                    github_repository,
                )
            )
            Path(conffile).write_text("fresh conf\n", encoding="utf8")

        def copy_css_file(self):
            return None

        def copy_js_file(self):
            return None

    captured = {}

    def fake_get_ontology(_path):
        return DummyOntology()

    def fake_od(*args, **kwargs):
        captured["od"] = DummyOD(*args, **kwargs)
        return captured["od"]

    def fake_sphinx_main(_args):
        return 0

    monkeypatch.setattr(docs_module, "get_ontology", fake_get_ontology)
    monkeypatch.setattr(docs_module, "OntologyDocumentation", fake_od)
    monkeypatch.setattr(docs_module, "sphinx_main", fake_sphinx_main)

    docs_module.docs_subcommand(
        Namespace(
            root=str(root),
            imported=True,
            recursive=False,
            iri_regex="https://w3id.org/ssbd",
            outfile=None,
            ontology_file=None,
            docs_dir=None,
            debug=False,
        )
    )

    od = captured["od"]
    assert od.refdoc_calls == [(build_dir, True)]
    assert od.index_calls == [
        (build_dir / "index.rst", build_dir / "core.rst", True, docs_dir)
    ]
    assert od.conf_calls == [
        (
            build_dir / "conf.py",
            build_dir / "core.rst",
            True,
            "ssbd-ontology/core",
        )
    ]
    assert (build_dir / "index.rst").read_text(
        encoding="utf8"
    ) == "fresh index\n"
    assert (build_dir / "conf.py").read_text(encoding="utf8") == "fresh conf\n"
    assert (build_dir / "docs" / "index.md").read_text(encoding="utf8") == (
        (docs_dir / "index.md").read_text(encoding="utf8")
    )
    assert not public_dir.exists()
