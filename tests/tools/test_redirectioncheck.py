"""Test the `redirectioncheck` tool."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
    from types import ModuleType
    from typing import Callable


def test_run(get_tool: "Callable[[str], ModuleType]") -> None:
    """Check that running `redirectioncheck` works.

    Parameters:
        get_tool: Local module fixture to load a named tool as a module.
            See the current folder's `conftest.py` file.

    """
    from pathlib import Path

    yamlfile = (
        Path(__file__).resolve().parent / "input" / "expected_redirections.yaml"
    )
    redirectioncheck = get_tool("redirectioncheck")

    # Make output more readable when running pytest with -s option
    print("\n\n")

    redirectioncheck.main([str(yamlfile), "-v"])
