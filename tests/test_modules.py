from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test_modules(tmpdir: "Path") -> None:
    from ontopy import get_ontology
    from ontopy.graph import (
        plot_modules,
        get_module_dependencies,
        check_module_dependencies,
    )

    iri = 'http://emmo.info/emmo/1.0.0-alpha2'
    emmo = get_ontology(iri)
    emmo.load()

    modules = get_module_dependencies(emmo)

    plot_modules(modules, filename=tmpdir / 'modules.png')
    check_module_dependencies(modules)
