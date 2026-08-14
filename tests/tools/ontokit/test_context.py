"""Tests for the `ontokit context` sub-command."""

import json

from ontopy.testutils import get_tool_module, ontodir


def test_animal_context_with_and_without_imported(tmp_path):
    """Generate JSON-LD context from ani.ttl with and without imports."""
    ontokit = get_tool_module("ontokit")
    no_imports_output = tmp_path / "context-no-imports.json"
    with_imports_output = tmp_path / "context-with-imports.json"

    ontokit.main(["context", str(ontodir / "ani.ttl"), str(no_imports_output)])
    ontokit.main(
        [
            "context",
            str(ontodir / "ani.ttl"),
            str(with_imports_output),
            "--include-imported",
        ]
    )

    assert no_imports_output.exists()
    assert with_imports_output.exists()

    context_no_imports = json.loads(
        no_imports_output.read_text(encoding="utf8")
    )
    context_with_imports = json.loads(
        with_imports_output.read_text(encoding="utf8")
    )

    # ani.ttl only contains ontology metadata, so entities come from imports.
    assert "Animal" not in context_no_imports["@context"]

    assert "Animal" in context_with_imports["@context"]
    assert "Mammal" in context_with_imports["@context"]
    assert "Bird" in context_with_imports["@context"]
    assert context_with_imports["@context"]["Animal"] == {
        "@id": "https://w3id.org/emmo/domain/animal#Animal",
        "@type": "http://www.w3.org/2002/07/owl#Class",
    }
    assert context_with_imports["@context"]["latinName"] == {
        "@id": "https://w3id.org/emmo/domain/animal#scientificName",
        "@type": "http://www.w3.org/1999/02/22-rdf-syntax-ns#plainLiteral",
    }
    assert context_with_imports["@context"]["hasLegs"] == {
        "@id": "https://w3id.org/emmo/domain/animal#hasLegs",
        "@type": "http://www.w3.org/2001/XMLSchema#int",
    }
    assert context_with_imports["@context"]["chases"] == {
        "@id": "https://w3id.org/emmo/domain/animal#chases",
        "@type": "@id",
    }


def test_animal_context_include_namespace_filter(tmp_path):
    """Only terms in selected namespace should be present in context."""
    ontokit = get_tool_module("ontokit")
    filtered_output = tmp_path / "context-animal-namespace.json"

    ontokit.main(
        [
            "context",
            str(ontodir / "ani.ttl"),
            str(filtered_output),
            "--include-imported",
            "--include-namespace",
            "https://w3id.org/emmo/domain/animal#",
        ]
    )

    context_filtered = json.loads(filtered_output.read_text(encoding="utf8"))
    ctx = context_filtered["@context"]

    # Kept because it belongs to the selected namespace.
    assert "Animal" in ctx
    assert "Bird" in ctx
    assert "chases" in ctx
    assert "hasLegs" in ctx

    # Excluded because these come from imported mammal namespace.
    assert "Mammal" not in ctx
    assert "Mouse" not in ctx
