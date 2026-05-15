"""Test ontodoc"""


# if True:
def test_ontodoc():
    """Test ontodoc."""
    from ontopy import get_ontology
    from ontopy.ontodoc_rst import (
        OntologyDocumentation,
        ReferenceDocumentation,
    )
    from ontopy.testutils import ontodir
    import owlready2

    # onto = get_ontology("https://w3id.org/emmo/1.0.0-rc1").load()
    onto = get_ontology(ontodir / "mammal.ttl").load()
    # onto.sync_reasoner(include_imported=True)

    od = OntologyDocumentation(
        onto, recursive=True, iri_regex="https://w3id.org/emmo"
    )
    ref = ReferenceDocumentation(
        onto,
        recursive=True,
        iri_regex="https://w3id.org/emmo",
        title="Mammal Reference",
    )

    od.add_reference(
        onto,
        recursive=True,
        iri_regex="https://w3id.org/emmo",
        title="Second Mammal Reference",
        docfile="mammal-second.rst",
        subsections="classes",
    )

    assert "Mammal Reference" in ref.get_refdoc()
    combined = od.get_combined_refdoc()
    assert "Reference Index" in combined
    assert "Second Mammal Reference" in combined
    assert od.get_refdoc(reference_index=1) == od.get_refdoc(
        reference_index=1,
        subsections="classes",
    )
    print(od.get_refdoc())


def test_ontodoc_slash_namespace_internal_links():
    """Internal links should stay distinct for same labels across ontologies."""
    import owlready2

    from ontopy import get_ontology
    from ontopy.ontodoc_rst import ReferenceDocumentation

    onto = get_ontology("http://example.com/onto/")
    onto2 = get_ontology("http://example.com/anotheronto/")
    onto.imported_ontologies.append(onto2)

    with onto2:

        class Animal(owlready2.Thing):
            pass

    with onto:

        class Animal(owlready2.Thing):
            pass

        class Dog(Animal, onto2.Animal):
            pass

    doc = ReferenceDocumentation(onto, imported=False).get_refdoc(
        subsections="classes"
    )
    print(doc)

    assert '<div id="Animal"></div>' in doc
    assert "href='#http://example.com/onto/Animal'" not in doc
    assert "href='#http://example.com/anotheronto/Animal'" not in doc
    assert (
        "<a href='#Animal' onclick=\"if(!document.getElementById('Animal'))"
        "{window.location.href='http://example.com/onto/Animal'; "
        'return false;}">Animal</a>'
    ) in doc
    assert ("<a href='http://example.com/anotheronto/Animal'>Animal</a>") in doc
    assert (
        "<a href='#Animal' onclick=\"if(!document.getElementById('Animal'))"
        "{window.location.href='http://example.com/anotheronto/Animal'; "
        'return false;}">Animal</a>'
    ) not in doc


def test_animal_html_reference_doc():
    """Generate HTML reference documentation for all animal ontologies.

    This writes RST reference documentation to tests/output/ and then builds
    a Sphinx HTML site under tests/output/_build/html/. Local runs can open
    the generated index in a browser, while CI verifies that the same
    documentation build completes successfully.

    To see the written output of the test, which describes where the
    generated files are located, run pytest as
    pytest -rP tests/test_ontodoc_rst.py::test_animal_html_reference_doc

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
