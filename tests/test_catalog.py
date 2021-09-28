from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test_catalog(repo_dir: "Path", tmpdir: "Path") -> None:
    from ontopy.utils import read_catalog, ReadCatalogError, write_catalog

    ontodir = repo_dir / "tests" / 'testonto'
    catalog_expected = {
        'http://emmo.info/testonto/0.1.0': str(ontodir / 'testonto.ttl'),
        'http://emmo.info/testonto/0.1.0/models': str(ontodir / 'models.ttl'),
    }

    catalog = read_catalog(str(ontodir / 'catalog-v001.xml'))
    assert catalog == catalog_expected

    catalog = read_catalog(str(ontodir))
    assert catalog == catalog_expected

    catalog = read_catalog(str(ontodir), recursive=True)
    assert catalog == catalog_expected

    catalog, catalog_paths = read_catalog(str(ontodir), return_paths=True)
    assert catalog == catalog_expected
    assert catalog_paths == set([str(ontodir)])

    catalog = read_catalog('https://raw.githubusercontent.com/emmo-repo/EMMO/master/'
                    'catalog-v001.xml')
    assert any(_.endswith('/emmo.ttl') for _ in catalog.values())

    catalog = read_catalog('https://raw.githubusercontent.com/emmo-repo/EMMO/master')
    assert any(_.endswith('/emmo.ttl') for _ in catalog.values())

    try:
        read_catalog(
            'https://raw.githubusercontent.com/emmo-repo/EMMO/does-not-exists')
    except ReadCatalogError:
        pass
    else:
        assert False, 'expected ReadCatalogError'

    try:
        read_catalog(str(ontodir / 'does-not-exists'))
    except ReadCatalogError:
        pass
    else:
        assert False, 'expected ReadCatalogError'

    catalog = read_catalog('https://raw.githubusercontent.com/emmo-repo/EMMO/master/'
                    'catalog-v001.xml', baseuri='/abc')
    assert '/abc/emmo.ttl' in catalog.values()

    tmp_catalog_path = tmpdir / "tmp-catalog.xml"
    write_catalog(catalog, output=tmp_catalog_path)
    tmp_catalog = read_catalog(str(tmp_catalog_path))
    assert tmp_catalog == catalog
