"""Test the `ontoversion` tool."""
import pytest


@pytest.mark.parametrize("tool", ["ontoversion"], indirect=True)
def test_run(tool) -> None:
    """Check running `ontoversion` works."""
    from pathlib import Path

    test_file = (
        Path(__file__).resolve().parent.parent / "testonto" / "testonto.ttl"
    )

    tool.main([str(test_file), "--format", "ttl"])
