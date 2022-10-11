from typing import TYPE_CHECKING
import defusedxml.ElementTree as ET
from ontopy.utils import read_catalog, ReadCatalogError, write_catalog

if TYPE_CHECKING:
    from pathlib import Path


def test_catalog(repo_dir: "Path", tmpdir: "Path") -> None:

    ontodir = repo_dir / "tests" / "catalogs_for_testing"
    catalog_expected = {
        "http://emmo.info/testonto/0.1.0": str(ontodir / "testonto.ttl"),
        "http://emmo.info/testonto/0.1.0/models": str(ontodir / "models.ttl"),
    }

    catalog = read_catalog(str(ontodir / "catalog-w-special-name.xml"))
    assert catalog == catalog_expected

    catalog = read_catalog(str(ontodir))
    assert catalog == catalog_expected

    catalog = read_catalog(str(ontodir), recursive=True)
    assert catalog == catalog_expected

    catalog, catalog_paths = read_catalog(str(ontodir), return_paths=True)
    assert catalog == catalog_expected
    assert catalog_paths == set([str(ontodir)])

    write_catalog(catalog, output="cat.xml")

    catalog = read_catalog(
        "https://raw.githubusercontent.com/emmo-repo/EMMO/master/"
        "catalog-v001.xml"
    )
    assert any(_.endswith("/emmo.ttl") for _ in catalog.values())

    catalog = read_catalog(
        "https://raw.githubusercontent.com/emmo-repo/EMMO/master"
    )
    assert any(_.endswith("/emmo.ttl") for _ in catalog.values())

    try:
        read_catalog(
            "https://raw.githubusercontent.com/emmo-repo/EMMO/does-not-exists"
        )
    except ReadCatalogError:
        pass
    else:
        assert False, "expected ReadCatalogError"

    try:
        read_catalog(str(ontodir / "does-not-exists"))
    except ReadCatalogError:
        pass
    else:
        assert False, "expected ReadCatalogError"

    catalog = read_catalog(
        "https://raw.githubusercontent.com/emmo-repo/EMMO/master/"
        "catalog-v001.xml",
        baseuri="/abc",
    )
    assert "/abc/emmo.ttl" in catalog.values()

    tmp_catalog_path = tmpdir / "tmp-catalog.xml"
    write_catalog(catalog, output=tmp_catalog_path, relative_paths=False)
    tmp_catalog = read_catalog(str(tmp_catalog_path))
    assert tmp_catalog == catalog


def test_write_catalog_choosing_relative_paths(
    repo_dir: "Path", tmpdir: "Path"
) -> None:
    ontodir = repo_dir / "tests" / "catalogs_for_testing"
    catalog1 = read_catalog(str(ontodir))
    write_catalog(
        catalog1,
        output=(tmpdir / "cat-relative-paths.xml"),
        relative_paths=True,
    )
    catalog2 = read_catalog(str(ontodir))
    write_catalog(
        catalog2,
        output=(tmpdir / "cat-absolute-paths.xml"),
        relative_paths=False,
    )

    catalog_w_absolute_paths_xml = ET.parse(tmpdir / "cat-absolute-paths.xml")
    catalog_w_relative_paths_xml = ET.parse(tmpdir / "cat-relative-paths.xml")

    catalog_w_absolute_paths_root = catalog_w_absolute_paths_xml.getroot()
    catalog_w_relative_paths_root = catalog_w_relative_paths_xml.getroot()

    absolutepaths = [
        uri.attrib["uri"] for uri in catalog_w_absolute_paths_root[0]
    ]
    relativepaths = [
        uri.attrib["uri"] for uri in catalog_w_relative_paths_root[0]
    ]

    ontodir = repo_dir / "tests" / "catalogs_for_testing"

    catalog_expected_relative_paths = {
        str("tests/catalogs_for_testing/testonto.ttl"),
        str("tests/catalogs_for_testing/models.ttl"),
    }

    catalog_expected_absolute_paths = {
        str(ontodir / "testonto.ttl"),
        str(ontodir / "models.ttl"),
    }

    assert set(absolutepaths) == set(catalog_expected_absolute_paths)
    assert set(relativepaths) == set(catalog_expected_relative_paths)

    catalog3 = read_catalog(
        "https://raw.githubusercontent.com/emmo-repo/EMMO/master/"
        "catalog-v001.xml"
    )
    write_catalog(catalog3, output=(tmpdir / "cat-with-http-paths.xml"))

    catalog_w_http_paths_xml = ET.parse(tmpdir / "cat-with-http-paths.xml")
    catalog_w_http_paths_root = catalog_w_http_paths_xml.getroot()

    paths = [uri.attrib["uri"] for uri in catalog_w_http_paths_root[0]]

    assert set(catalog3.values()) == set(paths)
