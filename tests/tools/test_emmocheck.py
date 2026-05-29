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


def test_number_of_rdfslabels(tmp_path) -> None:
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


def test_preflabel_checks(tmp_path) -> None:
    """Check prefLabel checks run by default and label checks are opt-in."""
    from ontopy.testutils import get_tool_module

    emmocheck = get_tool_module("emmocheck")

    ok_ontofile = tmp_path / "preflabel_ok.ttl"
    ok_ontofile.write_text(
        """@prefix : <http://example.org/test#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<http://example.org/test> a owl:Ontology .

:prefLabel a owl:AnnotationProperty .

:MyClass a owl:Class ;
  rdfs:label "not CamelCase"@en ;
    :prefLabel "MyClass"@en .

:hasPart a owl:ObjectProperty ;
  rdfs:label "NotLowerCamel"@en ;
    :prefLabel "hasPart"@en .
""",
        encoding="utf-8",
    )

    bad_ontofile = tmp_path / "preflabel_bad.ttl"
    bad_ontofile.write_text(
        """@prefix : <http://example.org/test#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<http://example.org/test> a owl:Ontology .

:prefLabel a owl:AnnotationProperty .

:MyClass a owl:Class ;
  rdfs:label "MyClass"@en ;
    :prefLabel "notCamelCase"@en .

:hasPart a owl:ObjectProperty ;
  rdfs:label "hasPart"@en ;
    :prefLabel "NotLowerCamel"@en .
""",
        encoding="utf-8",
    )

    label_ok_ontofile = tmp_path / "label_ok.ttl"
    label_ok_ontofile.write_text(
        """@prefix : <http://example.org/test#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<http://example.org/test> a owl:Ontology .

:prefLabel a owl:AnnotationProperty .

:MyClass a owl:Class ;
    rdfs:label "not CamelCase"@en ;
        :prefLabel "MyClass"@en .

:hasPart a owl:ObjectProperty ;
  rdfs:label "hasPart"@en ;
    :prefLabel "hasPart"@en .

:isGoodAnnotation a owl:AnnotationProperty ;
    rdfs:label "isGoodAnnotation"@en ;
        :prefLabel "isGoodAnnotation"@en .

""",
        encoding="utf-8",
    )

    non_object_bad_ontofile = tmp_path / "property_preflabel_non_object.ttl"
    non_object_bad_ontofile.write_text(
        """@prefix : <http://example.org/test#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<http://example.org/test> a owl:Ontology .

:prefLabel a owl:AnnotationProperty .

:hasBadDatatype a owl:DatatypeProperty ;
    :prefLabel "NotLowerCamel"@en .

:hasGoodObject a owl:ObjectProperty ;
    :prefLabel "hasGoodObject"@en .
""",
        encoding="utf-8",
    )

    configfile = tmp_path / "emmocheck.yml"
    configfile.write_text("skip:\n  - test_*\n", encoding="utf-8")

    status = emmocheck.main(
        [
            "--configfile",
            str(configfile),
            str(ok_ontofile),
        ]
    )
    assert status == 0

    status = emmocheck.main(
        [
            "--configfile",
            str(configfile),
            str(label_ok_ontofile),
        ]
    )
    assert status == 0

    status = emmocheck.main(
        [
            "--configfile",
            str(configfile),
            "--enable=test_class_label",
            "--enable=test_object_property_label",
            str(bad_ontofile),
        ]
    )
    assert status == 1

    status = emmocheck.main(
        [
            "--configfile",
            str(configfile),
            "--enable=test_class_label",
            "--enable=test_object_property_label",
            str(label_ok_ontofile),
        ]
    )
    assert status == 1

    status = emmocheck.main(
        [
            "--configfile",
            str(configfile),
            "--enable=test_property_preflabel",
            str(non_object_bad_ontofile),
        ]
    )
    assert status == 1


def test_preflabel_uniqueness_within_namespace(tmp_path) -> None:
    """Check that prefLabel uniqueness can be validated per namespace."""
    from ontopy.testutils import get_tool_module

    emmocheck = get_tool_module("emmocheck")

    ok_ontofile = tmp_path / "preflabel_unique_ok.ttl"
    ok_ontofile.write_text(
        """@prefix : <http://example.org/test#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

<http://example.org/test> a owl:Ontology .

:prefLabel a owl:AnnotationProperty .

:ClassOne a owl:Class ;
  :prefLabel "ClassOne"@en .

:ClassTwo a owl:Class ;
  :prefLabel "ClassTwo"@en .
""",
        encoding="utf-8",
    )

    bad_ontofile = tmp_path / "preflabel_unique_bad.ttl"
    bad_ontofile.write_text(
        """@prefix : <http://example.org/test#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

<http://example.org/test> a owl:Ontology .

:prefLabel a owl:AnnotationProperty .

:ClassOne a owl:Class ;
  :prefLabel "Duplicated"@en .

:ClassTwo a owl:Class ;
  :prefLabel "Duplicated"@en .
""",
        encoding="utf-8",
    )

    configfile = tmp_path / "emmocheck.yml"
    configfile.write_text("skip:\n  - test_*\n", encoding="utf-8")

    status = emmocheck.main(
        [
            "--configfile",
            str(configfile),
            "--enable=test_unique_labels",
            str(ok_ontofile),
        ]
    )
    assert status == 0

    status = emmocheck.main(
        [
            "--configfile",
            str(configfile),
            "--enable=test_unique_labels",
            str(bad_ontofile),
        ]
    )
    assert status == 1


def test_unique_labels_can_be_configured(tmp_path) -> None:
    """Check that label properties to validate can be configured."""
    from ontopy.testutils import get_tool_module

    emmocheck = get_tool_module("emmocheck")

    ontofile = tmp_path / "label_unique_bad.ttl"
    ontofile.write_text(
        """@prefix : <http://example.org/test#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<http://example.org/test> a owl:Ontology .

:prefLabel a owl:AnnotationProperty .

:ClassOne a owl:Class ;
  rdfs:label "Duplicated"@en ;
  :prefLabel "ClassOne"@en .

:ClassTwo a owl:Class ;
  rdfs:label "Duplicated"@en ;
  :prefLabel "ClassTwo"@en .
""",
        encoding="utf-8",
    )

    configfile = tmp_path / "emmocheck.yml"
    configfile.write_text(
        "skip:\n"
        "  - test_*\n"
        "test_unique_labels:\n"
        "  labels:\n"
        "    - label\n",
        encoding="utf-8",
    )

    status = emmocheck.main(
        [
            "--configfile",
            str(configfile),
            "--enable=test_unique_labels",
            str(ontofile),
        ]
    )
    assert status == 1


def test_unique_labels_checks_imported_by_default(tmp_path) -> None:
    """Imported ontologies should be checked by default."""
    from ontopy.testutils import get_tool_module

    emmocheck = get_tool_module("emmocheck")

    imported_ontofile = tmp_path / "imported.ttl"
    imported_uri = imported_ontofile.resolve().as_uri()
    imported_ontofile.write_text(
        f"""@prefix : <{imported_uri}#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<{imported_uri}> a owl:Ontology .

:ImportedOne a owl:Class ;
    rdfs:label "Duplicated"@en .

:ImportedTwo a owl:Class ;
    rdfs:label "Duplicated"@en .
""",
        encoding="utf-8",
    )

    main_ontofile = tmp_path / "main.ttl"
    main_uri = main_ontofile.resolve().as_uri()
    main_ontofile.write_text(
        f"""@prefix : <{main_uri}#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<{main_uri}> a owl:Ontology ;
    owl:imports <{imported_uri}> .

:MainClass a owl:Class ;
    rdfs:label "MainClass"@en .
""",
        encoding="utf-8",
    )

    configfile = tmp_path / "emmocheck.yml"
    configfile.write_text(
        "skip:\n"
        "  - test_*\n"
        "test_unique_labels:\n"
        "  labels:\n"
        "    - label\n",
        encoding="utf-8",
    )

    status = emmocheck.main(
        [
            "--configfile",
            str(configfile),
            "--enable=test_unique_labels",
            str(main_ontofile),
        ]
    )
    assert status == 1


def test_unique_labels_allows_same_iri_in_imported_files(tmp_path) -> None:
    """The same entity IRI declared in multiple files should not count as duplicate."""
    from ontopy.testutils import get_tool_module

    emmocheck = get_tool_module("emmocheck")

    imported_ontofile = tmp_path / "imported_same_iri.ttl"
    imported_uri = imported_ontofile.resolve().as_uri()
    imported_ontofile.write_text(
        f"""@prefix : <{imported_uri}#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<{imported_uri}> a owl:Ontology .

:Shared a owl:Class ;
    rdfs:label "Shared"@en .
""",
        encoding="utf-8",
    )

    main_ontofile = tmp_path / "main_same_iri.ttl"
    main_uri = main_ontofile.resolve().as_uri()
    main_ontofile.write_text(
        f"""@prefix : <{main_uri}#> .
@prefix imp: <{imported_uri}#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<{main_uri}> a owl:Ontology ;
    owl:imports <{imported_uri}> .

imp:Shared a owl:Class ;
    rdfs:label "Shared"@en .
""",
        encoding="utf-8",
    )

    configfile = tmp_path / "emmocheck.yml"
    configfile.write_text(
        "skip:\n"
        "  - test_*\n"
        "test_unique_labels:\n"
        "  labels:\n"
        "    - label\n",
        encoding="utf-8",
    )

    status = emmocheck.main(
        [
            "--configfile",
            str(configfile),
            "--enable=test_unique_labels",
            str(main_ontofile),
        ]
    )
    assert status == 0
