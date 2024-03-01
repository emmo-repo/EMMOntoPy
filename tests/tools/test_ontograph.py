"""Test the `ontograph` tool."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
    from types import ModuleType
    from typing import Callable


def test_run() -> None:
    """Check that running `ontograph` works."""
    from ontopy.testutils import ontodir, outdir, get_tool_module

    test_file = ontodir / "models.ttl"
    ontograph = get_tool_module("ontograph")

    ontograph.main([str(test_file), str(outdir / "test.png")])
