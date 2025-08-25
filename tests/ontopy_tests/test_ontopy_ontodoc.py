from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from ontopy.ontology import Ontology


def test_ontodoc(emmo: "Ontology", repo_dir: "Path", tmpdir: "Path") -> None:
    import pytest

    pytest.importorskip("graphviz")
    from ontopy.ontodoc import OntoDoc, DocPP

    iris = set(_.namespace.base_iri for _ in emmo.classes())
    iris.update(set(_.namespace.base_iri for _ in emmo.object_properties()))

    inputfile = repo_dir / "tests" / "doc.md"
    assert inputfile.exists()

    ontodoc = OntoDoc(emmo)

    template = inputfile.read_text()
    docpp = DocPP(
        template,
        ontodoc,
        basedir=inputfile.parent,
        figdir=tmpdir / "genfigs",
    )
    docpp.process()
    (tmpdir / "doc-output.md").write_text(docpp.get_buffer())
