# Add emmo to sys path
import os
import sys

thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from ontopy import get_ontology  # noqa: E402, F401


emmo = get_ontology()
emmo.load()
