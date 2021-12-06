"""Test the `ontograph` tool."""
from pathlib import Path

import pytest


@pytest.mark.parametrize("tool", ["ontograph"], indirect=True)
def test_run(tool, tmpdir: Path) -> None:
    """Check that running `ontograph` works."""
    test_file = (
        Path(__file__).resolve().parent.parent / "testonto" / "models.ttl"
    )

    tool.main([str(test_file), str(tmpdir / "test.png")])
