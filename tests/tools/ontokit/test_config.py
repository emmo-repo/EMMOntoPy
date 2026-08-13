"""Tests for ontopy.ontokit.config."""

import io

import yaml

from ontopy.ontokit.config import (
    CONFIG_FILENAME,
    REQUIRED_CONFIG_KEYS,
    create_config,
    get_config_path,
    load_config,
    missing_required_variables,
    print_config,
    update_config,
)

SAMPLE_DEFAULTS = {
    "ONTOLOGY_NAME": "MyOntology",
    "ONTOLOGY_PREFIX": "myonto",
    "ONTOLOGY_IRI": "https://example.com/myonto#",
    "GIT_REPOSITORY": "myorg/myrepo",
    "GIT_BASE_URL": "github.com",
    "GITHUB_REPOSITORY": "myorg/myrepo",
    "BUILD_DIR": "build",
    "REFERENCE_SUBSECTIONS": "all",
    "REFERENCE_IMPORTED": "false",
    "REFERENCE_RECURSIVE": "true",
    "REFERENCE_IRI_REGEX": "https://example.com/myonto#",
}


def test_get_config_path(tmp_path):
    assert get_config_path(tmp_path) == tmp_path / CONFIG_FILENAME


def test_load_config(tmp_path):
    config_file = tmp_path / CONFIG_FILENAME
    config_file.write_text(yaml.safe_dump(SAMPLE_DEFAULTS))
    assert load_config(config_file) == SAMPLE_DEFAULTS


def test_create_config(tmp_path):
    config_file = tmp_path / CONFIG_FILENAME
    create_config(config_file, SAMPLE_DEFAULTS)
    loaded = load_config(config_file)
    for key in REQUIRED_CONFIG_KEYS:
        assert loaded[key] == SAMPLE_DEFAULTS[key]
    assert "GITHUB_REPOSITORY" not in loaded


def test_update_config_fills_missing_key(tmp_path):
    config_file = tmp_path / CONFIG_FILENAME
    partial = {
        k: v
        for k, v in SAMPLE_DEFAULTS.items()
        if k not in {"BUILD_DIR", "REFERENCE_SUBSECTIONS"}
    }
    config_file.write_text(yaml.safe_dump(partial))
    updated, added = update_config(config_file, dict(partial), SAMPLE_DEFAULTS)
    assert "BUILD_DIR" in added
    assert "REFERENCE_SUBSECTIONS" in added
    assert updated["BUILD_DIR"] == SAMPLE_DEFAULTS["BUILD_DIR"]
    assert (
        updated["REFERENCE_SUBSECTIONS"]
        == SAMPLE_DEFAULTS["REFERENCE_SUBSECTIONS"]
    )


def test_update_config_does_not_overwrite_existing_key(tmp_path):
    config_file = tmp_path / CONFIG_FILENAME
    original = {**SAMPLE_DEFAULTS, "ONTOLOGY_NAME": "OriginalName"}
    config_file.write_text(yaml.safe_dump(original))
    updated, added = update_config(
        config_file,
        dict(original),
        {**SAMPLE_DEFAULTS, "ONTOLOGY_NAME": "NewName"},
    )
    assert updated["ONTOLOGY_NAME"] == "OriginalName"
    assert "ONTOLOGY_NAME" not in added


def test_missing_required_variables_accepts_legacy_repository_key():
    config = {
        "ONTOLOGY_NAME": "MyOntology",
        "ONTOLOGY_PREFIX": "myonto",
        "ONTOLOGY_IRI": "https://example.com/myonto#",
        "GITHUB_REPOSITORY": "myorg/myrepo",
        "BUILD_DIR": "build",
    }
    assert missing_required_variables(config) == []
