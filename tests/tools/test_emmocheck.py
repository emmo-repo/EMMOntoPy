"""Test the `emmocheck` tool."""
import pytest


@pytest.mark.parametrize("tool", ["emmocheck"], indirect=True)
def test_run(tool) -> None:
    """Check that running `emmocheck` works."""
    from pathlib import Path

    test_file = (
        Path(__file__).resolve().parent.parent / "testonto" / "models.ttl"
    )

    tool.main([str(test_file)])
