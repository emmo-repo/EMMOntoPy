"""Test the `ontoversion` tool."""


def test_run() -> None:
    """Check running `ontoversion` works."""
    from ontopy.testutils import ontodir, outdir, get_tool_module

    test_file = ontodir / "testonto.ttl"
    ontoversion = get_tool_module("ontoversion")

    ontoversion.main([str(test_file), "--format", "ttl"])
