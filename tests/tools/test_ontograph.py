"""Test the `ontograph` tool."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
    from types import ModuleType
    from typing import Callable


def test_run(get_tool: "Callable[[str], ModuleType]", tmpdir: "Path") -> None:
    """Check that running `ontograph` works.

    Parameters:
        get_tool: Local module fixture to load a named tool as a module.
            See the current folder's `conftest.py` file.
        tmpdir: A generic pytest fixture to generate a temporary directory, which will
            exist only for the lifetime of this test function.

    """
    from pathlib import Path

    test_file = (
        Path(__file__).resolve().parent.parent / "testonto" / "models.ttl"
    )
    ontograph = get_tool("ontograph")

    ontograph.main([str(test_file), str(tmpdir / "test.png")])
