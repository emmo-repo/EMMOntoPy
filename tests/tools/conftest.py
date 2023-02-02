"""Pytest fixtures for the `tools` dir only."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from types import ModuleType
    from typing import Any, Dict


@pytest.fixture
def tool(request: "Dict[str, Any]") -> "ModuleType":
    """Import a tool as a module."""
    from copy import deepcopy
    import importlib
    import os
    from pathlib import Path
    import sys

    original_sys_path = deepcopy(sys.path)
    original_tool_path: Path = (
        Path(__file__).resolve().parent.parent.parent / "tools" / request.param
    )
    if str(original_tool_path.parent) not in sys.path:
        sys.path.append(str(original_tool_path.parent))

    content_parent = "\n".join(
        str(_) for _ in os.walk(original_tool_path.parent)
    )
    assert (
        original_tool_path.exists()
    ), f"The requested tool ({request.param}) was not found in {original_tool_path.parent}.\nContents:\n{content_parent}"
    tool_path = None
    try:
        tool_path = original_tool_path.rename(
            original_tool_path.with_suffix(".py")
        )
        yield importlib.import_module(request.param)
    finally:
        if tool_path and tool_path.exists():
            tool_path.rename(tool_path.with_suffix(""))
        sys.path = original_sys_path
