from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test_modules(tmpdir: "Path") -> None:
    import pytest

    pytest.importorskip("graphviz")
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
