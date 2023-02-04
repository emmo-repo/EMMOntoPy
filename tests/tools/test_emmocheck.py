"""Test the `emmocheck` tool."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import ModuleType
    from typing import Callable


def test_run(get_tool: "Callable[[str], ModuleType]") -> None:
    """Check that running `emmocheck` works.

    Parameters:
        get_tool: Local module fixture to load a named tool as a module.
            See the current folder's `conftest.py` file.

    """
    from pathlib import Path

    test_file = (
        Path(__file__).resolve().parent.parent / "testonto" / "models.ttl"
    )
    emmocheck = get_tool("emmocheck")

    emmocheck.main([str(test_file)])
