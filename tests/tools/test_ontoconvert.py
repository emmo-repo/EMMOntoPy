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

    # Test 3 - copy-emmo-annotations
    infile3 = ontodir / "domainonto.ttl"
    outfile3 = outdir / "test_ontoconvert3.ttl"
    ontoconvert.main(
        [
            "--copy-emmo-annotations",
            "--iri=https://w3id.org/ex/testonto",
            "--base-iri=https://w3id.org/ex/testonto#",
            str(infile3),
            str(outfile3),
        ]
    )
    input3 = infile3.read_text()
    output3 = outfile3.read_text()
    assert 'rdfs:label "hasAnnotationProperty"@en' not in input3
    assert 'rdfs:label "hasAnnotationProperty"@en' in output3
    assert 'rdfs:comment "A test class."@en' not in input3
    assert 'rdfs:comment "A test class."@en' in output3

    # Test 4 - copy-annotation with source as annotation label
    infile4 = ontodir / "testonto.ttl"
    outfile4 = outdir / "test_ontoconvert3.ttl"
    ontoconvert.main(
        [
            "-c prefLabel-->http://www.w3.org/2004/02/skos/core#hiddenLabel",
            "--iri=https://w3id.org/ex/testonto",
            "--base-iri=https://w3id.org/ex/testonto#",
            str(infile4),
            str(outfile4),
        ]
    )
    input4 = infile4.read_text()
    output4 = outfile4.read_text()
    assert not re.search('skos:hiddenLabel "hasAnnotationProperty"@en', input4)
    assert re.search('skos:hiddenLabel "hasAnnotationProperty"@en', output4)
