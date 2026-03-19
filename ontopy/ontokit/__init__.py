"""Ontopy subpackage for creating workflows and documenting ontologies."""

from importlib import import_module

__all__ = ["docs", "setup"]


def __getattr__(name):
    """Lazily expose submodules for tooling such as mkdocstrings.

    It will import the `docs` module when a user does `import ontokit.docs`.
    Similar for the other modules.
    """
    if name in __all__:
        module = import_module(f"{__name__}.{name}")
        globals()[name] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
