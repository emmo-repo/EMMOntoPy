"""Test the `ontoconvert` tool."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
    from types import ModuleType
    from typing import Callable


if True:
    # def test_run(get_tool: "Callable[[str], ModuleType]", tmpdir: "Path") -> None:
    """Check that running `ontoconvert` works.

    Parameters:
        get_tool: Local module fixture to load a named tool as a module.
            See the current folder's `conftest.py` file.
        tmpdir: A generic pytest fixture to generate a temporary directory,
            which will exist only for the lifetime of this test function.
    """
    import re
    from pathlib import Path
    import sys
    import importlib

    testdir = Path(__file__).resolve().parent.parent
    ontodir = testdir / "testonto"
    outdir = testdir / "output"
    toolsdir = testdir.parent / "tools"

    # ontoconvert = get_tool("ontoconvert")

    sys.path.append(str(toolsdir))
    ontoconvert = importlib.machinery.SourceFileLoader(
        "ontoconvert", str(toolsdir / "ontoconvert")
    ).load_module()

    # Test 1
    ontoconvert.main(
        [str(ontodir / "models.ttl"), str(outdir / "test_ontoconvert1.ttl")]
    )
    output1 = (outdir / "test_ontoconvert1.ttl").read_text()
    assert re.search("@prefix : <http://emmo.info/models#>", output1)
    assert re.search("<http://emmo.info/models> .* owl:Ontology", output1)
    assert re.search("testclass .* owl:Class", output1)

    # Test 2 - squash
    ontoconvert.main(
        [
            "-asw",
            "--iri=https://w3id.org/ex/testonto",
            "--base-iri=https://w3id.org/ex/testonto#",
            str(ontodir / "testonto.ttl"),
            str(outdir / "test_ontoconvert2.ttl"),
        ]
    )
    output2 = (outdir / "test_ontoconvert2.ttl").read_text()
    assert re.search("@prefix : <https://w3id.org/ex/testonto#>", output2)
    assert re.search("<https://w3id.org/ex/testonto> .* owl:Ontology", output2)
    assert re.search("testclass .* owl:Class", output2)
