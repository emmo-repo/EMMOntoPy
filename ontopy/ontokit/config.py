"""Helpers for reading and validating ontokit configuration."""

from pathlib import Path

import yaml

CONFIG_FILENAME = ".ontokit_conf.yml"
REQUIRED_CONFIG_KEYS = (
    "ONTOLOGY_NAME",
    "ONTOLOGY_PREFIX",
    "ONTOLOGY_IRI",
    "GIT_REPOSITORY",
    "GIT_BASE_URL",
    "BUILD_DIR",
)

OPTIONAL_CONFIG_KEYS = (
    "REFERENCE_SUBSECTIONS",
    "REFERENCE_IMPORTED",
    "REFERENCE_RECURSIVE",
    "REFERENCE_IRI_REGEX",
)

LEGACY_REPOSITORY_KEY = "GITHUB_REPOSITORY"

REFERENCE_INDICES_COMMENT = """\
# Optional settings for `ontokit docs` reference indices.
# Select subsections for the primary reference index. Default is "all".
# REFERENCE_SUBSECTIONS: all
# Example subset:
# REFERENCE_SUBSECTIONS: classes,annotation_properties,data_properties,object_properties,individuals
#
# REFERENCE_IMPORTED: false
# REFERENCE_RECURSIVE: true
# This regex is used to filter which IRIs are included in the primary reference index. Default is the ontology IRI.
# REFERENCE_IRI_REGEX: https://example.com/myonto#
#
# Optional: additional reference indices for `ontokit docs`.
# REFERENCE_INDICES:
#   - ontology_file: build/other-ontology.ttl
#     title: Other Ontology Reference
#     docfile: other-reference.rst
#     iri_regex: https://example.org/other
#     imported: false
#     recursive: false
#     subsections: all
"""


def get_config_path(root):
    """Return the path to the ontokit configuration file for `root`."""
    return Path(root) / CONFIG_FILENAME


def _as_string(value):
    """Normalise values to strings for serialisation and substitution."""
    return "" if value is None else str(value)


def _write_config_with_reference_indices_comment(path, config):
    """Write config YAML and append a commented REFERENCE_INDICES example."""
    content = yaml.safe_dump(config, sort_keys=False).rstrip()
    # Only append when REFERENCE_INDICES is not explicitly configured.
    if "REFERENCE_INDICES" not in config:
        content = f"{content}\n\n{REFERENCE_INDICES_COMMENT.rstrip()}\n"
    else:
        content = f"{content}\n"
    Path(path).write_text(content)


def load_config(path):
    """Load ontokit config from `path` and return it as a dictionary."""
    try:
        content = yaml.safe_load(Path(path).read_text())
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in {path}: {exc}") from exc

    if content is None:
        return {}
    if not isinstance(content, dict):
        raise ValueError(f"Expected a mapping in {path}, got {type(content)}")
    return content


def create_config(path, defaults):
    """Create ontokit config at `path` from default values."""
    config = {
        key: _as_string(defaults.get(key, "")) for key in REQUIRED_CONFIG_KEYS
    }
    _write_config_with_reference_indices_comment(path, config)
    return config


def update_config(path, config, defaults):
    """Add any missing required keys to `config` from `defaults` and save.

    Keys that are already present in `config` are never overwritten.
    Returns the (possibly updated) config dict and a list of keys that
    were added.
    """
    added = []
    # Normalise legacy key to new neutral key when possible.
    if (
        config.get("GIT_REPOSITORY") is None
        or str(config.get("GIT_REPOSITORY", "")).strip() == ""
    ) and str(config.get(LEGACY_REPOSITORY_KEY, "")).strip():
        config["GIT_REPOSITORY"] = _as_string(config.get(LEGACY_REPOSITORY_KEY))

    for key in REQUIRED_CONFIG_KEYS:
        value = config.get(key)
        if value is None or str(value).strip() == "":
            config[key] = _as_string(defaults.get(key, ""))
            added.append(key)
    for key in OPTIONAL_CONFIG_KEYS:
        value = config.get(key)
        if value is None or str(value).strip() == "":
            config[key] = _as_string(defaults.get(key, ""))
            added.append(key)
    if added:
        _write_config_with_reference_indices_comment(path, config)
    return config, added


def missing_required_variables(config):
    """Return required keys that are missing or empty in `config`."""
    # Accept legacy repository key as fallback for migration compatibility.
    if (
        config.get("GIT_REPOSITORY") is None
        or str(config.get("GIT_REPOSITORY", "")).strip() == ""
    ) and str(config.get(LEGACY_REPOSITORY_KEY, "")).strip():
        config = dict(config)
        config["GIT_REPOSITORY"] = config[LEGACY_REPOSITORY_KEY]

    # Legacy configs may not define this key.
    if (
        config.get("GIT_BASE_URL") is None
        or str(config.get("GIT_BASE_URL", "")).strip() == ""
    ):
        config = dict(config)
        config["GIT_BASE_URL"] = "github.com"

    missing = []
    for key in REQUIRED_CONFIG_KEYS:
        value = config.get(key)
        if value is None or str(value).strip() == "":
            missing.append(key)
    return missing


def print_config(config, stream=None):
    """Print required ontokit variables and their values."""
    out = stream.write if stream else print

    def emit(line):
        if stream:
            out(f"{line}\n")
        else:
            out(line)

    for key in REQUIRED_CONFIG_KEYS:
        emit(f"  {key}: {config.get(key, '')}")
    if LEGACY_REPOSITORY_KEY in config:
        emit(
            "  "
            f"{LEGACY_REPOSITORY_KEY}: {config.get(LEGACY_REPOSITORY_KEY, '')}"
        )
