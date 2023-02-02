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


@pytest.mark.parametrize("tool", ["ontodoc"], indirect=True)
def test_run_w_individual(tool, tmpdir: Path) -> None:
    """Check that running `ontodoc` works when there is an individual."""
    test_file = (
        Path(__file__).resolve().parent.parent
        / "testonto"
        / "testonto_w_individual.ttl"
    )

    tool.main([str(test_file), str(tmpdir / "test.md")])
    tool.main(
        [str(test_file), "--format=simple-html", str(tmpdir / "test.html")]
    )


@pytest.mark.parametrize("tool", ["ontodoc"], indirect=True)
@pytest.mark.filterwarnings(
    "ignore:Ignoring instance"
)  # currently pytest is set to accept warnings, but this might change in the future
def test_run_w_punning(tool, tmpdir: Path) -> None:
    """Check that running `ontodoc` works even if there is a punned individual.
    This will throw and extra warning as the punned individual will be ignored.
    """
    test_file = (
        Path(__file__).resolve().parent.parent
        / "testonto"
        / "testonto_w_punning.ttl"
    )

    tool.main([str(test_file), str(tmpdir / "test.md")])
    tool.main(
        [str(test_file), "--format=simple-html", str(tmpdir / "test.html")]
    )
