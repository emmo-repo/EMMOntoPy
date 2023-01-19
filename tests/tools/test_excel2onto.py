"""Test the `ontograph` tool."""
from pathlib import Path
import os
import pytest


@pytest.mark.parametrize("tool", ["excel2onto"], indirect=True)
def test_run(tool, tmpdir: Path) -> None:
    """Check that running `excel2onto` works."""
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

    tool.main([f"--output={str(tmpdir)}/onto.ttl", "--force", str(test_file)])

    tool.main(
        [
            f"--output={str(tmpdir)}/onto.ttl",
            "--force",
            "--input_ontology=newonto.ttl",
            str(test_file2),
        ]
    )

    tool.main(
        [
            f"--output={str(tmpdir)}/ontology.ttl",
            "--force",
            "--update=False",
            str(test_file),
        ]
    )
