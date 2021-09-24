# -*- coding: utf-8 -*-
import sys
from ontopy import __version__ as __ontopy_version__

__version__ = __ontopy_version__

# Ensure correct Python version
if sys.version_info < (3, 6):
    raise RuntimeError('emmopy requires Python 3.6 or later')

# Ensure emmopy is imported before owlready2...
if 'owlready2' in sys.modules.keys() and "ontopy" not in sys.modules.keys():
    raise RuntimeError('emmopy must be imported before owlready2')

# Import functions from emmopy
from .emmopy import get_emmo


__all__ = ("get_emmo",)
