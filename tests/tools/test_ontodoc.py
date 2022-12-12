"""Test the `ontodoc` tool."""
from pathlib import Path

import pytest


@pytest.mark.parametrize("tool", ["ontodoc"], indirect=True)
def test_run(tool, tmpdir: Path) -> None:
    """Check that running `ontodoc` works."""
    test_file = (
        Path(__file__).resolve().parent.parent / "testonto" / "models.ttl"
    )

    tool.main([str(test_file), str(tmpdir / "test.md")])
    tool.main(
        [str(test_file), "--format=simple-html", str(tmpdir / "test.html")]
    )
