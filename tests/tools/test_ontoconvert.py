"""Test the `ontoconvert` tool."""
from pathlib import Path

import pytest


@pytest.mark.parametrize("tool", ["ontoconvert"], indirect=True)
def test_run(tool, tmpdir: Path) -> None:
    """Check that running `ontoconvert` works."""
    test_file = (
        Path(__file__).resolve().parent.parent / "testonto" / "models.ttl"
    )

    tool.main([str(test_file), str(tmpdir / "test.ttl")])
