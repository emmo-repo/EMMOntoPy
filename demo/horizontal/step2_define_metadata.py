#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""\
Step 2 - define metadata for the ASE Atoms class
------------------------------------------------
In this step we define metadata for the Atoms class in the Atomistic
Simulation Environment (ASE).  This metadata is defined in the file
atoms.json.

The actual definition are provided in atoms.json.  Below we use the
dlite.classfactory() to create a subclass of ASE Atoms that also
exposes the attributes as dlite properties. The subclass DLiteAtoms
adds some methods for handling some special attributes.

"""
import ase
from ase.spacegroup import Spacegroup

import dlite


# Create an ASE Atoms subclass that also inherits from dlite atoms.json
BaseAtoms = dlite.classfactory(ase.Atoms, url='json://atoms.json?mode=r#')


class DLiteAtoms(BaseAtoms):
    """ASE Atoms class extended as a dlite entity."""

    def _dlite_get_info(self):
        d = self.info.copy()
        sg = Spacegroup(d.get('spacegroup', 'P 1'))
        d['spacegroup'] = sg.symbol
        return [(k, str(v)) for k, v in d.items()]

    def _dlite_set_info(self, value):
        self.info.update(value)
        self.info['spacegroup'] = Spacegroup(self.info['spacegroup'])

    def _dlite_get_celldisp(self):
        return self.get_celldisp()[:, 0]
