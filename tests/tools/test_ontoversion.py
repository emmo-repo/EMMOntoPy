"""Test the `ontoversion` tool."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import ModuleType
    from typing import Callable


def test_run() -> None:
    """Check running `ontoversion` works."""
    from ontopy.testutils import ontodir, outdir, get_tool_module

    test_file = ontodir / "testonto.ttl"
    ontoversion = get_tool_module("ontoversion")

    ontoversion.main([str(test_file), "--format", "ttl"])
