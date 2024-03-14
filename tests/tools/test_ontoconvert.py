"""Test the `ontoconvert` tool."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
    from types import ModuleType
    from typing import Callable


# if True:
def test_run() -> None:
    """Check that running `ontoconvert` works."""
    import re
    from ontopy.testutils import ontodir, outdir, get_tool_module

    ontoconvert = get_tool_module("ontoconvert")

    # Test 1
    ontoconvert.main(
        [str(ontodir / "models.ttl"), str(outdir / "test_ontoconvert1.ttl")]
    )
    output1 = (outdir / "test_ontoconvert1.ttl").read_text()
    assert re.search("@prefix : <http://emmo.info/models#>", output1)
    assert re.search("<http://emmo.info/models> .* owl:Ontology", output1)
    assert re.search("testclass .* owl:Class", output1)

    # Test 2 - squash
    ontoconvert.main(
        [
            "-asw",
            "--iri=https://w3id.org/ex/testonto",
            "--base-iri=https://w3id.org/ex/testonto#",
            str(ontodir / "testonto.ttl"),
            str(outdir / "test_ontoconvert2.ttl"),
        ]
    )
    output2 = (outdir / "test_ontoconvert2.ttl").read_text()
    assert re.search("@prefix : <https://w3id.org/ex/testonto#>", output2)
    assert re.search("<https://w3id.org/ex/testonto> .* owl:Ontology", output2)
    assert re.search("testclass .* owl:Class", output2)

    # Test 3 - copy-annotation
    ontoconvert.main(
        [
            "-p",
            "--iri=https://w3id.org/ex/testonto",
            "--base-iri=https://w3id.org/ex/testonto#",
            str(ontodir / "testonto.ttl"),
            str(outdir / "test_ontoconvert3.ttl"),
        ]
    )
    input3 = (ontodir / "testonto.ttl").read_text()
    output3 = (outdir / "test_ontoconvert3.ttl").read_text()
    assert not re.search('rdfs:label "hasAnnotationProperty"@en', input3)
    assert re.search('rdfs:label "hasAnnotationProperty"@en', output3)

    # Test 4 - copy-annotation with source as annotation label
    ontoconvert.main(
        [
            "-c prefLabel-->http://www.w3.org/2004/02/skos/core#hiddenLabel",
            "--iri=https://w3id.org/ex/testonto",
            "--base-iri=https://w3id.org/ex/testonto#",
            str(ontodir / "testonto.ttl"),
            str(outdir / "test_ontoconvert4.ttl"),
        ]
    )
    input4 = (ontodir / "testonto.ttl").read_text()
    output4 = (outdir / "test_ontoconvert4.ttl").read_text()
    assert not re.search('skos:hiddenLabel "hasAnnotationProperty"@en', input4)
    assert re.search('skos:hiddenLabel "hasAnnotationProperty"@en', output4)
