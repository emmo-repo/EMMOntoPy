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
    from pathlib import Path
    import sys

    original_sys_path = deepcopy(sys.path)
    original_tool_path: Path = (
        Path(__file__).resolve().parent.parent.parent / "tools" / request.param
    )
    sys.path.append(str(original_tool_path.parent.parent))

    assert (
        original_tool_path.exists()
    ), f"The requested tool ({request.param}) was not found in {original_tool_path.parent}"
    try:
        tool_path = original_tool_path.rename(
            original_tool_path.with_name(f"{request.param}.py")
        )
        yield importlib.import_module(f"tools.{request.param}")
    finally:
        if tool_path and tool_path.exists():
            tool_path.rename(tool_path.with_name(request.param))
        sys.path = original_sys_path
