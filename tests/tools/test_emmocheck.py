"""Test the `emmocheck` tool."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import ModuleType
    from typing import Callable


# if True:
def test_run() -> None:
    """Check that running `emmocheck` works."""
    from ontopy.testutils import ontodir, get_tool_module

    test_file = ontodir / "models.ttl"
    emmocheck = get_tool_module("emmocheck")

    # The main() method will raise an exception on error, so it is
    # sufficient to just call it here

    status = emmocheck.main(["--skip=test_description", str(test_file)])
    assert status == 0

    # This will fail because the ontology does not contain
    # the emmo.properties elucidation, description
    # or conceptualisation.
    status = emmocheck.main([str(test_file)])
    assert status == 1
