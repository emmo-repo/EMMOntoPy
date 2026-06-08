# Testing and tooling

## Unit testing

The [PyTest](https://pytest.org) framework is used for testing the EMMOntoPy package.
It is a unit testing framework with a plugin system, sporting an extensive plugin library as well as a sound fixture injection system.

To run the tests locally install the package with the `dev` extra (see the [developer's setup guide](setup.md)) and run:

```console
$ pytest
=== test session starts ===
...
```

To understand what options you have, run `pytest --help`.

## Targeted checks for ontology reference docs

For local verification of index/reference generation used by
`ontodoc_rst` and `ontokit`, run this focused test:

```console
pytest -rP tests/test_ontokit.py::test_animal_html_reference_doc
```

Why this command is useful:

- `-rP` shows captured output for passing tests.
- The test prints the generated local HTML path (`index.html`) so you can
    open it in a browser and inspect the rendered reference docs.
- It validates both writing RST reference files and building HTML with Sphinx.

## Tools

Several tools are used to maintain the package, keeping it secure, readable, and easing maintenance.

### Mypy

[Mypy](http://mypy-lang.org/) is a static type checker for Python.

**Documentation**: [mypy.readthedocs.io](https://mypy.readthedocs.io/)

The signs of this tool will be found in the code especially through the `typing.TYPE_CHECKING` boolean variable, which will be used in the current way:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
```

Since `TYPE_CHECKING` is `False` at runtime, the `if`-block will not be run as part of running the script or module or if importing the module.
However, when Mypy runs to check the static typing, it forcefully runs these blocks, considering `TYPE_CHECKING` to be `True` (see the [`typing.TYPE_CHECKING` section](https://mypy.readthedocs.io/en/stable/runtime_troubles.html#typing-type-checking) in the Mypy documentation).

This means the imports in the `if`-block are meant to *only* be used for static typing, helping developers to understand the intention of the code as well as to check the invoked methods make sense (through Mypy).
