# -*- coding: utf-8 -*-
import sys

VERSION = '1.0.0-alpha-8'


# Ensure correct Python version
if sys.version_info < (3, 6):
    raise RuntimeError('emmo requires Python 3.6 or later')

# Ensure emmo is imported before owlready2...
if 'owlready2' in sys.modules.keys():
    raise RuntimeError('emmo must be imported before owlready2')

# Appends EMMO to the ontology search path
from . import owldir

# Monkey patch Owlready2 by injecting some methods
from . import patch

# Import get_ontology(), which is our main entry point
from .ontology import get_ontology
