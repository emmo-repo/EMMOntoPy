# To test import of structures from the MaterialsProject
from pymatgen.ext.matproj import MPRester
with MPRester('USER_API_KEY') as m:
    structure = m.get_structure_by_material_id('mp-2018')


