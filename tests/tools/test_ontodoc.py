"""Test the `ontodoc` tool."""

from typing import TYPE_CHECKING
import pytest


def test_run() -> None:
    """Check that running `ontodoc` works."""

    pytest.importorskip("graphviz")
    from ontopy.testutils import ontodir, outdir, get_tool_module

    ontodoc = get_tool_module("ontodoc")

    test_file = ontodir / "models.ttl"
    ontodoc = get_tool_module("ontodoc")

    ontodoc.main([str(test_file), str(outdir / "test.md")])
    ontodoc.main(
        [str(test_file), "--format=simple-html", str(outdir / "test.html")]
    )


def test_run_w_individual() -> None:
    """Check that running `ontodoc` works when there is an individual."""
    pytest.importorskip("graphviz")
    from ontopy.testutils import ontodir, outdir, get_tool_module

    test_file = ontodir / "testonto_w_individual.ttl"
    ontodoc = get_tool_module("ontodoc")

    ontodoc.main([str(test_file), str(outdir / "test.md")])
    ontodoc.main(
        [str(test_file), "--format=simple-html", str(outdir / "test.html")]
    )


@pytest.mark.filterwarnings(
    "ignore:Ignoring instance"
)  # currently pytest is set to accept warnings, but this might change in the future
def test_run_w_punning() -> None:
    """Check that running `ontodoc` works even if there is a punned individual.
    This will throw and extra warning as the punned individual will be ignored.
    """
    pytest.importorskip("graphviz")
    from ontopy.testutils import ontodir, outdir, get_tool_module

    test_file = ontodir / "testonto_w_punning.ttl"
    ontodoc = get_tool_module("ontodoc")

    ontodoc.main([str(test_file), str(outdir / "test.md")])
    ontodoc.main(
        [str(test_file), "--format=simple-html", str(outdir / "test.html")]
    )


def test_ontodoc_rst() -> None:
    """Test reStructuredText output with ontodoc."""
    from ontopy.testutils import ontodir, outdir, get_tool_module

    ontodoc = get_tool_module("ontodoc")
    ontodoc.main(
        [
            "--imported",
            "--reasoner=HermiT",
            "--iri-regex=^https://w3id.org/emmo/domain",
            str(ontodir / "mammal.ttl"),
            str(outdir / "mammal.rst"),
        ]
    )
    rstfile = outdir / "mammal.rst"
    assert rstfile.exists()
    content = rstfile.read_text()
    assert "latinName" in content
