# -*- coding: utf-8 -*-
import sys
import warnings

__version__ = '2.0.0'

warnings.warn(
    message="The EMMO package is deprecated. Use EMMOntoPy instead.",
    category=DeprecationWarning,
)

# Ensure correct Python version
if sys.version_info < (3, 6):
    raise RuntimeError('emmo requires Python 3.6 or later')

# Ensure emmo is imported before owlready2...
if 'owlready2' in sys.modules.keys():
    raise RuntimeError('emmo must be imported before owlready2')

# Monkey patch Owlready2 by injecting some methods
from . import patch  # noqa: E402, F401

# Import World and get_ontology(), which are our main entry points
from .ontology import World, get_ontology  # noqa: E402, F401

# Global list of ontology search paths
from owlready2 import onto_path  # noqa: E402, F401
