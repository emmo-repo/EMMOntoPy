# -*- coding: utf-8 -*-
import sys

__version__ = '0.1.0'

# Ensure correct Python version
if sys.version_info < (3, 6):
    raise RuntimeError('ontopy requires Python 3.6 or later')

# Ensure ontopy is imported before owlready2...
if 'owlready2' in sys.modules.keys() and "emmopy" not in sys.modules.keys():
    raise RuntimeError('ontopy must be imported before owlready2')

# Monkey patch Owlready2 by injecting some methods
from . import patch

# Import World and get_ontology(), which are our main entry points
from .ontology import World, get_ontology

# Global list of ontology search paths
from owlready2 import onto_path


__all__ = ("patch", "World", "get_ontology", "onto_path")
