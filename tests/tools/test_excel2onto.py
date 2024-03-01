"""Test the `ontograph` tool."""

from typing import TYPE_CHECKING
import pytest


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_run() -> None:
    """Check that running `excel2onto` works.

    Parameters:
        get_tool: Local module fixture to load a named tool as a module.
            See the current folder's `conftest.py` file.
        tmpdir: A generic pytest fixture to generate a temporary directory, which will
            exist only for the lifetime of this test function.

    """
    from ontopy.testutils import ontodir, outdir, testdir, get_tool_module

    test_file = testdir / "test_excelparser" / "onto.xlsx"
    test_file2 = testdir / "test_excelparser" / "onto_update.xlsx"
    excel2onto = get_tool_module("excel2onto")

    outfile = outdir / "onto.ttl"
    if outfile.exists():  # consider to add an --overwrite option to excel2onto
        outfile.unlink()
    excel2onto.main([f"--output={outfile}", "--force", str(test_file)])

    # Append to outfile
    excel2onto.main(
        [
            f"--output={outdir}/onto.ttl",
            "--force",
            "--input_ontology=newonto.ttl",
            str(test_file2),
        ]
    )

    outfile = outdir / "ontology.ttl"
    if outfile.exists():
        outfile.unlink()
    excel2onto.main(
        [
            f"--output={outfile}",
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
