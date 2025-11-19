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
    outfile4 = outdir / "test_ontoconvert4.ttl"
    ontoconvert.main(
        [
            "--copy-annotation=prefLabel-->"
            "http://www.w3.org/2004/02/skos/core#hiddenLabel",
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

    # Test 5 - custom namespace prefix
    infile5 = ontodir / "testonto.ttl"
    outfile5 = outdir / "test_ontoconvert5.ttl"
    ontoconvert.main(
        [
            "--namespace=dct:http://purl.org/dc/terms/",
            "--namespace=bib:http://purl.org/ontology/bibo/",
            str(infile5),
            str(outfile5),
        ]
    )
    input5 = infile5.read_text()
    output5 = outfile5.read_text()
    assert "@prefix dcterms: <http://purl.org/dc/terms/> ." in input5
    assert "@prefix dct: <http://purl.org/dc/terms/> ." in output5
    assert "@prefix bibo: <http://purl.org/ontology/bibo/> ." in input5
    assert "@prefix bib: <http://purl.org/ontology/bibo/> ." in output5

    # Test 6 - recursive convert
    infile6 = ontodir / "ani.ttl"
    outfile6 = "ani.ttl"
    ontoconvert.main(
        [
            "--recursive",
            "--overwrite",
            "--namespace=animal:https://w3id.org/emmo/domain/animal#",
            f"--output-dir={outdir}/test_ontoconvert6",
            "--output-format=turtle",
            "--catalog-file=catalog-v001.xml",
            str(infile6),
            str(outfile6),
        ]
    )
    assert (outdir / "test_ontoconvert6" / "catalog-v001.xml").exists()
    assert (outdir / "test_ontoconvert6" / "ani.ttl").exists()
    assert (outdir / "test_ontoconvert6" / "animal.ttl").exists()
    assert (outdir / "test_ontoconvert6" / "mammal.ttl").exists()
    assert (
        outdir / "test_ontoconvert6" / "animal" / "catalog-v001.xml"
    ).exists()
    assert (
        outdir / "test_ontoconvert6" / "animal" / "vertebrates.ttl"
    ).exists()
    assert (outdir / "test_ontoconvert6" / "animal" / "birds.ttl").exists()
    ani = (outdir / "test_ontoconvert6" / "ani.ttl").read_text()
    assert "owl:imports" in ani
    birds = (outdir / "test_ontoconvert6" / "animal" / "birds.ttl").read_text()
    assert "owl:imports" in birds

    # Test 7 - combine --recursive and --squash
    infile7 = ontodir / "ani.ttl"
    outfile7 = "ani.ttl"
    ontoconvert.main(
        [
            "--recursive",
            "--overwrite",
            "--namespace=animal:https://w3id.org/emmo/domain/animal#",
            f"--output-dir={outdir}/test_ontoconvert7",
            "--output-format=turtle",
            "--squash",
            str(infile7),
            str(outfile7),
        ]
    )
    assert (outdir / "test_ontoconvert7" / "ani.ttl").exists()
    assert (outdir / "test_ontoconvert7" / "animal.ttl").exists()
    assert (outdir / "test_ontoconvert7" / "mammal.ttl").exists()
    assert (
        outdir / "test_ontoconvert7" / "animal" / "vertebrates.ttl"
    ).exists()
    assert (outdir / "test_ontoconvert7" / "animal" / "birds.ttl").exists()
    ani = (outdir / "test_ontoconvert7" / "ani.ttl").read_text()
    assert "owl:imports" not in ani
    birds = (outdir / "test_ontoconvert7" / "animal" / "birds.ttl").read_text()
    assert "owl:imports" not in birds
