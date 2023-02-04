"""Test the `ontodoc` tool."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path
    from types import ModuleType
    from typing import Callable


def test_run(get_tool: "Callable[[str], ModuleType]", tmpdir: "Path") -> None:
    """Check that running `ontodoc` works.

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
    ontodoc = get_tool("ontodoc")

    ontodoc.main([str(test_file), str(tmpdir / "test.md")])
    ontodoc.main(
        [str(test_file), "--format=simple-html", str(tmpdir / "test.html")]
    )


def test_run_w_individual(
    get_tool: "Callable[[str], ModuleType]", tmpdir: "Path"
) -> None:
    """Check that running `ontodoc` works when there is an individual.

    Parameters:
        get_tool: Local module fixture to load a named tool as a module.
            See the current folder's `conftest.py` file.
        tmpdir: A generic pytest fixture to generate a temporary directory, which will
            exist only for the lifetime of this test function.

    """
    from pathlib import Path

    test_file = (
        Path(__file__).resolve().parent.parent
        / "testonto"
        / "testonto_w_individual.ttl"
    )
    ontodoc = get_tool("ontodoc")

    ontodoc.main([str(test_file), str(tmpdir / "test.md")])
    ontodoc.main(
        [str(test_file), "--format=simple-html", str(tmpdir / "test.html")]
    )


@pytest.mark.filterwarnings(
    "ignore:Ignoring instance"
)  # currently pytest is set to accept warnings, but this might change in the future
def test_run_w_punning(
    get_tool: "Callable[[str], ModuleType]", tmpdir: "Path"
) -> None:
    """Check that running `ontodoc` works even if there is a punned individual.
    This will throw and extra warning as the punned individual will be ignored.

    Parameters:
        get_tool: Local module fixture to load a named tool as a module.
            See the current folder's `conftest.py` file.
        tmpdir: A generic pytest fixture to generate a temporary directory, which will
            exist only for the lifetime of this test function.

    """
    from pathlib import Path

    test_file = (
        Path(__file__).resolve().parent.parent
        / "testonto"
        / "testonto_w_punning.ttl"
    )
    ontodoc = get_tool("ontodoc")

    ontodoc.main([str(test_file), str(tmpdir / "test.md")])
    ontodoc.main(
        [str(test_file), "--format=simple-html", str(tmpdir / "test.html")]
    )
