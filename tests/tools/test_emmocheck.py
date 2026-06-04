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


def test_unique_labels(tmp_path) -> None:
    """Check unique-label behavior using ontology fixtures from testonto."""
    from pathlib import Path

    from emmopy import emmocheck as emmocheck_module
    from ontopy.testutils import get_tool_module, ontodir

    emmocheck = get_tool_module("emmocheck")

    def run_emmocheck(args):
        emmocheck_module.TestEMMOConventions.config = {}
        return emmocheck.main(args)

    def run_case(
        ontofile,
        expected_status,
        labels=None,
        skipmodules=None,
    ):
        configfile = tmp_path / f"{Path(ontofile).stem}_emmocheck.yml"
        lines = ["skip:", "  - test_*"]
        test_unique_labels_config = {}
        if labels:
            test_unique_labels_config["labels"] = list(labels)
        if skipmodules:
            test_unique_labels_config["skipmodules"] = list(skipmodules)
        if test_unique_labels_config:
            lines.append("test_unique_labels:")
            for key, values in test_unique_labels_config.items():
                lines.append(f"  {key}:")
                for v in values:
                    lines.append(f"    - {v}")
        configfile.write_text("\n".join(lines) + "\n", encoding="utf-8")

        args = [
            "--configfile",
            str(configfile),
            "--enable=test_unique_labels",
            str(ontodir / ontofile),
        ]
        status = run_emmocheck(args)
        assert status == expected_status

    run_case("animal.ttl", 1)
    # minischema does not have prefLabels, but labels
    run_case("minischema.ttl", 1)
    run_case("minischema.ttl", 0, labels=("label",))
    run_case("minischema.ttl", 1, labels=("label", "prefLabel"))
    run_case(
        "minischema.ttl",
        0,
        labels=("label",),
        skipmodules=("schema.org",),
    )
