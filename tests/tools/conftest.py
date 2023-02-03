"""Pytest fixtures for the `tools` dir only."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from types import ModuleType
    from typing import Callable


@pytest.fixture(scope="module", autouse=True)
def rename_tools() -> None:
    """Add a `.py` extension to all tools.

    Run prior to all tests in this module.
    First, rename all tools (adding a `.py` suffix) to make them importable as a
    module. Then stop executing this fixture for a while (yield) and run all the tests
    in the module. Then after they're done, rename the tools back (remove the `.py`
    suffix) and also return `sys.path` to its original state prior to running the
    tests.
    To make the importability work, the `tools` folder had to be added to the
    `sys.path`.
    """
    from copy import deepcopy
    import os
    from pathlib import Path
    import shutil
    import sys

    original_sys_path = deepcopy(sys.path)
    tools_path: Path = Path(__file__).resolve().parent.parent.parent / "tools"

    if str(tools_path) not in sys.path:
        sys.path.append(str(tools_path))

    # Add ".py" suffix to all tools
    for (
        dirpath,
        dirnames,
        filenames,
    ) in os.walk(tools_path):
        if dirpath != str(tools_path):
            continue

        if dirnames:
            for dirname in dirnames:
                if dirname == "__pycache__":
                    shutil.rmtree(
                        Path(dirpath) / "__pycache__", ignore_errors=True
                    )

        for filename in filenames:
            filepath = Path(dirpath) / filename
            assert (
                filepath.suffix == ""
            ), f"A suffix was found (not expected) for file: {filepath}"

            filepath.rename(filepath.with_suffix(".py"))

    yield

    # Remove ".py" suffix from all tools
    for (
        dirpath,
        dirnames,
        filenames,
    ) in os.walk(tools_path):
        if dirpath != str(tools_path):
            continue

        if dirnames:
            for dirname in dirnames:
                if dirname == "__pycache__":
                    shutil.rmtree(
                        Path(dirpath) / "__pycache__", ignore_errors=True
                    )

        for filename in filenames:
            filepath = Path(dirpath) / filename
            assert (
                filepath.suffix == ".py"
            ), f"A suffix was NOT found (not expected) for file: {filepath}"

            filepath.rename(filepath.with_suffix(""))

    sys.path = original_sys_path


@pytest.fixture
def get_tool() -> "Callable[[str], ModuleType]":
    """Import a tool as a module.

    Requires the fixture `rename_tools` to have been run already.
    """
    import importlib
    from pathlib import Path
    import sys

    def _get_tool(name: str) -> "ModuleType":
        """Import and return named tool."""
        tool_path: Path = (
            Path(__file__).resolve().parent.parent.parent / "tools" / name
        ).with_suffix(".py")
        assert (
            str(tool_path.parent) in sys.path
        ), f"'tools' dir not found in sys.path. Did `rename_tools` fixture run?\nsys.path: {sys.path}"

        assert (
            tool_path.exists()
        ), f"The requested tool ({name}) was not found in {tool_path.parent}."

        return importlib.import_module(name)

    return _get_tool
