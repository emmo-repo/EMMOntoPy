#!/usr/bin/env python
import sys
import os

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from ontopy.utils import read_catalog, ReadCatalogError  # noqa: E402, F401
from ontopy.utils import write_catalog  # noqa: E402, F401


ontodir = os.path.join(thisdir, 'testonto')
d_expected = {
    'http://emmo.info/testonto/0.1.0': os.path.join(
        ontodir, 'testonto.ttl'),
    'http://emmo.info/testonto/0.1.0/models': os.path.join(
        ontodir, 'models.ttl'),
}

d = read_catalog(os.path.join(ontodir, 'catalog-v001.xml'))
assert d == d_expected

d = read_catalog(ontodir)
assert d == d_expected

d = read_catalog(ontodir, recursive=True)
assert d == d_expected

d, p = read_catalog(ontodir, return_paths=True)
assert d == d_expected
assert p == set([ontodir])

d = read_catalog('https://raw.githubusercontent.com/emmo-repo/EMMO/master/'
                 'catalog-v001.xml')
assert any(v.endswith('/emmo.ttl') for v in d.values())

d = read_catalog('https://raw.githubusercontent.com/emmo-repo/EMMO/master')
assert any(v.endswith('/emmo.ttl') for v in d.values())

try:
    read_catalog(
        'https://raw.githubusercontent.com/emmo-repo/EMMO/does-not-exists')
except ReadCatalogError:
    pass
else:
    assert False, 'expected ReadCatalogError'

try:
    read_catalog(os.path.join(ontodir, 'does-not-exists'))
except ReadCatalogError:
    pass
else:
    assert False, 'expected ReadCatalogError'

d = read_catalog('https://raw.githubusercontent.com/emmo-repo/EMMO/master/'
                 'catalog-v001.xml', baseuri='/abc')
assert '/abc/emmo.ttl' in d.values()


write_catalog(d, 'tmp-catalog.xml')
d2 = read_catalog('tmp-catalog.xml')
assert d2 == d
