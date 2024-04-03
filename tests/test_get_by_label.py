import pytest


def test_get_by_label_onto(repo_dir) -> None:
    """Test that label annotations are added correctly if they are not added before
    using get_by_label
    """
    from ontopy import get_ontology
    from ontopy.ontology import NoSuchLabelError, DEFAULT_LABEL_ANNOTATIONS
    import owlready2

    # create ontology with one class and check that it is found
    testonto = get_ontology("http://domain_ontology/new_ontology")
    testonto.new_entity("Class", owlready2.Thing)

    assert testonto.label_annotations == DEFAULT_LABEL_ANNOTATIONS
    assert testonto.get_by_label("Class") == testonto.Class
    assert testonto.get_by_label_all("*") == {testonto.Class}

    testonto.new_annotation_property(
        "SpecialAnnotation", owlready2.AnnotationProperty
    )
    testonto.Class.SpecialAnnotation.append("This is a comment")

    testonto.new_entity("Klasse", testonto.Class)

    with pytest.raises(AttributeError):
        assert testonto.Klasse.prefLabel == ["Klasse"]

    assert testonto.get_by_label_all("*") == {
        testonto.Class,
        testonto.SpecialAnnotation,
        testonto.Klasse,
    }

    # Add prefLabel to ontology
    preflabel = testonto.new_annotation_property(
        "prefLabel",
        parent=[owlready2.AnnotationProperty],
    )
    preflabel.iri = "http://www.w3.org/2004/02/skos/core#prefLabel"

    # After prefLabel was added to the ontology, prefLabels can be accessed
    with pytest.raises(AssertionError):
        assert testonto.prefLabel.prefLabel == ["prefLabel"]
    testonto.prefLabel.prefLabel = "prefLabel"
    assert testonto.prefLabel.prefLabel == ["prefLabel"]

    with pytest.raises(AssertionError):
        assert testonto.Klasse.prefLabel == ["Klasse"]

    testonto.new_entity("UnderKlasse", testonto.Klasse)
    assert testonto.UnderKlasse.prefLabel.en == ["UnderKlasse"]

    assert testonto.get_by_label_all("*") == {
        testonto.prefLabel,
        testonto.Class,
        testonto.SpecialAnnotation,
        testonto.Klasse,
        testonto.UnderKlasse,
    }
    assert testonto.get_by_label_all("Class*") == {
        testonto.Class,
    }

    # Check that imported ontologies are searched
    imported_onto = testonto.world.get_ontology(
        repo_dir / "tests" / "testonto" / "testonto.ttl"
    ).load()
    testonto.imported_ontologies.append(imported_onto)
    assert imported_onto.get_by_label("TestClass")
    assert imported_onto.get_by_label("models:TestClass")

    assert testonto.get_by_label("TestClass")

    # Check exact_match=True in get_by_label_all()
    assert testonto.get_by_label_all("*", exact_match=True) == set()
    assert testonto.get_by_label_all("Clas*", exact_match=True) == set()
    assert testonto.get_by_label_all("Class", exact_match=True) == {
        testonto.Class,
    }

    # Test with label annotations given directly when creating the ontology
    testonto2 = get_ontology(
        "http://domain_ontology/new_ontology",
        label_annotations=[
            "http://www.w3.org/2004/02/skos/core#prefLabel",
            "http://www.w3.org/2004/02/skos/core#altLabel",
        ],
    )

    testonto2.new_annotation_property(
        "prefLabel",
        parent=[owlready2.AnnotationProperty],
    )
    testonto2.new_entity("Class", owlready2.Thing, preflabel="Klasse")

    assert testonto2.get_by_label("Klasse") == testonto2.Class


def test_get_by_label_emmo(emmo: "Ontology") -> None:
    # Loading emmo-inferred where everything is sqashed into one ontology
    from emmopy import get_emmo
    from ontopy import get_ontology
    from ontopy.ontology import NoSuchLabelError
    from ontopy.testutils import ontodir

    emmo = get_emmo()
    assert emmo[emmo.Atom.name] == emmo.Atom
    assert emmo[emmo.Atom.iri] == emmo.Atom

    # Load an ontology with imported sub-ontologies
    # XXX: doesn't work at the moment
    # onto = get_ontology("https://w3id.org/emmo/domain/battery").load()
    # assert onto.Electrolyte.prefLabel.en.first() == "Electrolyte"
    onto = get_ontology(ontodir / "testonto.ttl").load()
    assert onto.TestClass.prefLabel.en.first() == "TestClass"

    # Check colon_in_name argument
    emmo.Atom.altLabel.append("Element:X")
    with pytest.raises(NoSuchLabelError):
        emmo.get_by_label("Element:X")

    assert emmo.get_by_label("Element:X", colon_in_label=True) == emmo.Atom
