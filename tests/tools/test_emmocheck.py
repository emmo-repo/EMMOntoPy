"""Test the `emmocheck` tool."""


# if True:
def test_run() -> None:
    """Check that running `emmocheck` works."""
    from ontopy.testutils import ontodir, get_tool_module

    test_file = ontodir / "models.ttl"
    emmocheck = get_tool_module("emmocheck")

    emmocheck.main([str(test_file)])
