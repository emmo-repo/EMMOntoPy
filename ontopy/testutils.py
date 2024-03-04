"""Module primarly intended to be imported by tests.

It defines some directories and some utility functions that can be used
with and without conftest.
"""

import sys
from pathlib import Path
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader


rootdir = Path(__file__).resolve().parent.parent
testdir = rootdir / "tests"
ontodir = testdir / "testonto"
outdir = testdir / "output"
toolsdir = rootdir / "tools"


def get_tool_module(name):
    """Imports and returns the module for the EMMOntoPy tool
    corresponding to `name`."""
    if str(toolsdir) not in sys.path:
        sys.path.append(str(toolsdir))

    # For Python 3.4+
    spec = spec_from_loader(name, SourceFileLoader(name, str(toolsdir / name)))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
