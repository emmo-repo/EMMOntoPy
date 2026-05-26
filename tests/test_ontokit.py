"""Test ontokit"""


def test_animal_html_reference_doc():
    """Generate HTML reference documentation for all animal ontologies.

    This writes RST reference documentation to tests/output/ and then builds
    a Sphinx HTML site under tests/output/_build/html/. Local runs can open
    the generated index in a browser, while CI verifies that the same
    documentation build completes successfully.

    To see the written output of the test, which describes where the
    generated files are located, run pytest as
    pytest -rP tests/test_ontokit.py::test_animal_html_reference_doc

    """
    import shutil
    from pathlib import Path

    from sphinx.cmd.build import main as sphinx_main

    from ontopy import get_ontology
    from ontopy.ontodoc_rst import OntologyDocumentation, SETUPTEMPLATES_DIR
    from ontopy.testutils import ontodir

    output_dir = Path(__file__).parent / "output"

    # ani.ttl is the entry-point ontology that imports all animal sub-ontologies
    onto = get_ontology(ontodir / "ani.ttl").load()

    od = OntologyDocumentation(
        onto,
        recursive=True,
        iri_regex="https://w3id.org/emmo",
        title="Animal Ontology Reference",
    )

    # Write RST reference files and Sphinx configuration
    od.write_reference_docs(outdir=output_dir, overwrite=True)
    od.write_index_template(
        indexfile=output_dir / "index.rst",
        overwrite=True,
    )
    od.write_conf_template(
        conffile=output_dir / "conf.py",
        overwrite=True,
    )

    static_dir = output_dir / "_static"
    static_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(
        SETUPTEMPLATES_DIR / "css" / "custom.css",
        static_dir / "custom.css",
    )
    shutil.copyfile(
        SETUPTEMPLATES_DIR / "js" / "toc-collapsible.js",
        static_dir / "toc-collapsible.js",
    )

    # Verify all animal sub-ontologies are represented in the RST output
    ani_rst = output_dir / "ani.rst"
    assert ani_rst.exists(), f"Expected RST file not found: {ani_rst}"
    rst_content = ani_rst.read_text(encoding="utf8")

    # animal.ttl entities
    assert "Animal" in rst_content, "Missing 'Animal' from animal.ttl"
    assert (
        "FourLeggedAnimal" in rst_content
    ), "Missing 'FourLeggedAnimal' from animal.ttl"

    # mammal.ttl entities
    assert "Mammal" in rst_content, "Missing 'Mammal' from mammal.ttl"
    assert "Cat" in rst_content, "Missing 'Cat' from mammal.ttl"

    # animal/vertebrates.ttl entities
    assert (
        "Vertebrate" in rst_content
    ), "Missing 'Vertebrate' from vertebrates.ttl"
    assert (
        "VertebralColumn" in rst_content
    ), "Missing 'VertebralColumn' from vertebrates.ttl"

    # animal/birds.ttl entities
    assert "Bird" in rst_content, "Missing 'Bird' from birds.ttl"
    assert "Raven" in rst_content, "Missing 'Raven' from birds.ttl"

    # Build HTML with Sphinx
    build_dir = output_dir / "_build" / "html"
    build_dir.mkdir(parents=True, exist_ok=True)
    exit_code = sphinx_main(["-b", "html", str(output_dir), str(build_dir)])
    assert exit_code == 0, f"sphinx-build failed with exit code {exit_code}"

    index_html = build_dir / "index.html"
    assert index_html.exists(), f"Expected HTML output not found: {index_html}"
    print(
        f"\nAnimal ontology HTML docs available at: file://{index_html.resolve()}"
    )
