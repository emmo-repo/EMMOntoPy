"""Test the `ontograph` tool."""

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path
    from types import ModuleType
    from typing import Callable


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_run(get_tool: "Callable[[str], ModuleType]", tmpdir: "Path") -> None:
    """Check that running `excel2onto` works.

    Parameters:
        get_tool: Local module fixture to load a named tool as a module.
            See the current folder's `conftest.py` file.
        tmpdir: A generic pytest fixture to generate a temporary directory, which will
            exist only for the lifetime of this test function.

    """
    from pathlib import Path

    test_file = (
        Path(__file__).resolve().parent.parent
        / "test_excelparser"
        / "onto.xlsx"
    )
    test_file2 = (
        Path(__file__).resolve().parent.parent
        / "test_excelparser"
        / "onto_update.xlsx"
    )
    excel2onto = get_tool("excel2onto")

    excel2onto.main(
        [f"--output={str(tmpdir)}/onto.ttl", "--force", str(test_file)]
    )

    excel2onto.main(
        [
            f"--output={str(tmpdir)}/onto.ttl",
            "--force",
            "--input_ontology=newonto.ttl",
            str(test_file2),
        ]
    )

    excel2onto.main(
        [
            f"--output={str(tmpdir)}/ontology.ttl",
            "--force",
            "--update=False",
            str(test_file),
        ]
    )

    # Test Error raised if ontology to be updated does not exist
    with pytest.raises(
        FileNotFoundError,
        match="The output ontology to be updated does not exist",
    ):
        excel2onto.main([f"--output=onto_not_created.ttl", str(test_file)])
