# -*- coding: utf-8 -*-
"""# `emmopy`"""
import sys
from ontopy import __version__ as __ontopy_version__

__version__ = __ontopy_version__

# Ensure correct Python version
if sys.version_info < (3, 7):
    raise RuntimeError("emmopy requires Python 3.7 or later")

# Ensure emmopy is imported before owlready2...
if "owlready2" in sys.modules and "emmopy" not in sys.modules:
    raise RuntimeError("emmopy must be imported before owlready2")

# Import functions from emmopy
from .emmopy import get_emmo  # pylint: disable=wrong-import-position


__all__ = ("get_emmo",)
