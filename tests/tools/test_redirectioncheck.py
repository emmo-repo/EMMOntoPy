"""Test the `redirectioncheck` tool."""


def test_run() -> None:
    """Check that running `redirectioncheck` works."""
    from ontopy.testutils import testdir, get_tool_module

    yamlfile = testdir / "tools" / "input" / "expected_redirections.yaml"
    redirectioncheck = get_tool_module("redirectioncheck")

    # Make output more readable when running pytest with -s option
    print("\n\n")

    redirectioncheck.main([str(yamlfile), "-v"])
