import pytest
from typing import TYPE_CHECKING

from ontopy.exceptions import _check_graphviz

if TYPE_CHECKING:
    from pathlib import Path

try:
    _check_graphviz()
except RuntimeError as e:
    pytest.skip(
        "Graphviz not available, skipping this test",
        allow_module_level=True,
    )


def test_modules(tmpdir: "Path") -> None:
    from ontopy import get_ontology
    from ontopy.graph import (
        plot_modules,
        get_module_dependencies,
        check_module_dependencies,
    )

    emmo = get_ontology("emmo")
    emmo.load()

    modules = get_module_dependencies(emmo)

    plot_modules(modules, filename=tmpdir / "modules.png")
    check_module_dependencies(modules)
