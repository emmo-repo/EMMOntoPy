"""Test the `emmocheck` tool."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import ModuleType
    from typing import Callable


# if True:
def test_run() -> None:
    """Check that running `emmocheck` works."""
    from ontopy.testutils import ontodir, get_tool_module

    test_file = ontodir / "models.ttl"
    emmocheck = get_tool_module("emmocheck")

    # The main() method will raise an exception on error, so it is
    # sufficient to just call it here

    status = emmocheck.main(["--skip=test_description", str(test_file)])
    assert status == 0

    # This will fail because the ontology does not contain
    # the emmo.properties elucidation, description
    # or conceptualisation.
    status = emmocheck.main([str(test_file)])
    assert status == 1


def test_number_of_rdfslabels_opt_in(tmp_path) -> None:
    """Check that `test_number_of_rdfslabels` only runs when enabled."""
    from ontopy.testutils import get_tool_module

    emmocheck = get_tool_module("emmocheck")

    ontofile = tmp_path / "rdfslabels.ttl"
    ontofile.write_text(
        """@prefix : <http://example.org/test#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<http://example.org/test> a owl:Ontology .

:BadClass a owl:Class ;
  rdfs:label "Bad class"@en ;
  rdfs:label "Another label"@en .
""",
        encoding="utf-8",
    )

    configfile = tmp_path / "emmocheck.yml"
    configfile.write_text("skip:\n  - test_*\n", encoding="utf-8")

    status = emmocheck.main(
        [
            "--configfile",
            str(configfile),
            str(ontofile),
        ]
    )
    assert status == 0

    status = emmocheck.main(
        [
            "--configfile",
            str(configfile),
            "--enable=test_number_of_rdfslabels",
            str(ontofile),
        ]
    )
    assert status == 1
