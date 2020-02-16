# -*- coding: utf-8 -*-
"""
Module that appends the directory containing the corrected version of EMMO to
the ontology search path.
"""
import os

import owlready2


thisdir = os.path.abspath(os.path.realpath((os.path.dirname(__file__))))
owldir = os.path.abspath(os.path.join(thisdir, 'owl'))

if not os.path.exists(os.path.join(owldir, 'emmo-inferred.owl')):
    print('File does not exists: ', os.path.join(owldir, 'emmo-inferred.owl'))
    print('Check your EMMO-Python installation')
    exit(1)

owlready2.onto_path.append(owldir)
