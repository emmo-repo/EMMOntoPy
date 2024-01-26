from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test_save(
    tmpdir: "Path",
    testonto: "Ontology",
    repo_dir: "Path",
) -> None:
    import os
    from pathlib import Path

    # For debugging purposes tmpdir can be set to a directory
    # in the current directory: test_save_dir
    # Remember to remove the directory after testing
    debug = False
    if debug:
        tmpdir = repo_dir / "tests" / "test_save_dir"
        import os

        os.makedirs(tmpdir, exist_ok=True)

    # Save ontology in a different location
    testonto.save(tmpdir / "testonto_saved.ttl")
    # check that the file is in tmpdir
    assert (tmpdir / "testonto_saved.ttl").exists()

    # provide a format and filename
    testonto.save(tmpdir / "testonto_saved.owl", format="rdfxml")
    assert (tmpdir / "testonto_saved.owl").exists()

    # Provide only filename
    # Note that when not giving a filename and not giving a directory
    # the file will be saved in the current directory
    testonto.save(format="rdfxml")
    assert Path(testonto.name + ".rdfxml").exists()

    # check if testonto_saved.owl and testonto.rdfxml are identical files
    with open(tmpdir / "testonto_saved.owl") as f:
        owlfile = f.read()
    with open(Path(testonto.name + ".rdfxml")) as f:
        rdfxmlfile = f.read()
    assert owlfile == rdfxmlfile
    # Delete the file from the current directory
    Path(testonto.name + ".rdfxml").unlink()

    # Provide format and directory
    testonto.save(format="rdfxml", dir=tmpdir)
    assert (tmpdir / str(testonto.name + ".rdfxml")).exists()

    # Provide directory that does not exist, but add mkdir=True
    testonto.save(format="owl", dir=tmpdir / "subdir", mkdir=True)
    assert (tmpdir / "subdir" / (testonto.name + ".owl")).exists()

    # Check that file is overwritten only wityh overwrite=True, and
    # not by default (overwrite=False).
    # To do this we
    # 1. check that the file testonto.rdfxml is the same as
    # testonto_saved.owl
    # 2. save testonto to testonto.rdfxml again. Since overwrite=False
    # this should append to testonto.rdfxml
    # 3. check that testonto.owl is not the same as testonto_saved.owl
    # 4. save testonto to testonto.owl again, but with overwrite=True
    # 5. check that testonto.owl is the same as testonto_saved.owl
    # NB! this is not currently working, issue #685
    # It might be that this inetnional behaviour of save should be changed.
    # If so, the tests should change accordingly.
    # This should be addressed in issue #685

    # 1.
    with open(tmpdir / "testonto_saved.owl") as f:
        owlfile = f.read()
    with open(tmpdir / "testonto.rdfxml") as f:
        owlfile2 = f.read()
    assert owlfile == owlfile2
    # 2.
    testonto.save(format="rdfxml", dir=tmpdir)
    # 3.
    with open(tmpdir / "testonto_saved.owl") as f:
        owlfile = f.read()
    with open(tmpdir / "testonto.rdfxml") as f:
        owlfile2 = f.read()
    # assert owlfile != owlfile2 # to be uncommented when issue #685 is fixed
    # 4.
    testonto.save(format="rdfxml", dir=tmpdir, overwrite=True)
    # 5.
    with open(tmpdir / "testonto_saved.owl") as f:
        owlfile = f.read()
    with open(tmpdir / "testonto.rdfxml") as f:
        owlfile2 = f.read()
    assert owlfile == owlfile2

    # Test that the ontology is saved recursively only when desired
    testonto.save(
        format="ttl",
        dir=tmpdir / "recursively",
        mkdir=True,
        recursive=False,
    )
    assert (tmpdir / "recursively" / "testonto.ttl").exists()
    assert (tmpdir / "recursively" / "models.ttl").exists() == False

    testonto.save(
        format="ttl",
        dir=tmpdir / "recursively",
        mkdir=True,
        recursive=True,
    )
    assert (tmpdir / "recursively" / "models.ttl").exists()

    # squash merge during save is tested in test_ontology_squash.py


# Simple working tests without pytest getting in the way - feel free to change to pytest
def test_save_emmo(
    tmpdir: "Path",
    repo_dir: "Path",
) -> None:
    import os
    from pathlib import Path

    from ontopy import get_ontology

    # For debugging purposes tmpdir can be set to a directory
    # in the current directory: test_save_dir
    # Remember to remove the directory after testing
    debug = False
    if debug:
        tmpdir = repo_dir / "tests" / "test_save_dir"
        import os

        os.makedirs(tmpdir, exist_ok=True)
    emmo = get_ontology(
        "https://raw.githubusercontent.com/emmo-repo/EMMO/1.0.0-beta4/emmo.ttl"
    ).load()

    # Since version is missing in some imported ontologies (at least in periodic_table)
    # we need to fix that.
    # Note that ths is fix of an error in EMMO-1.0.0-beta4
    version = emmo.get_version()
    # for onto in emmo.indirectly_imported_ontologies():
    #    try:
    #        onto.get_version(as_iri=True)
    #    except TypeError:
    #        onto.set_version(version)
    #    # print(onto, onto.get_version(as_iri=True))

    emmo.save(
        format="turtle",
        dir=tmpdir / "emmosaved",
        recursive=True,
        mkdir=True,
        write_catalog_file=True,
    )
    assert set(os.listdir(tmpdir / "emmosaved")) == {
        "catalog-v001.xml",
        "disciplines",
        "emmo.ttl",
        "mereocausality",
        "multiperspective",
        "perspectives",
    }

    assert set(os.listdir(tmpdir / "emmosaved" / "disciplines")) == {
        "materials.ttl",
        "math.ttl",
        "computerscience.ttl",
        "chemistry.ttl",
        "unitsextension.ttl",
        "catalog-v001.xml",
        "isq.ttl",
        "periodictable.ttl",
        "metrology.ttl",
        "siunits.ttl",
        "disciplines.ttl",
        "manufacturing.ttl",
        "models.ttl",
    }


def test_save_emmo_domain_ontology(
    tmpdir: "Path",
    repo_dir: "Path",
) -> None:
    import os
    from pathlib import Path
    from ontopy.utils import directory_layout
    from ontopy import get_ontology

    # For debugging purposes tmpdir can be set to a directory
    # in the current directory: test_save_dir
    # Remember to remove the directory after testing
    debug = True
    if debug:
        tmpdir = repo_dir / "tests" / "test_save_dir"
        import os

        os.makedirs(tmpdir, exist_ok=True)

    # This test was created with the domain-electrochemistry ontology which imports
    # emmo submodules as well as chameo.
    # Also, it is important that the version domain-electrochemistry has base_iri
    # starting with https://w3id.org/emmo/
    # while emmo and chameo start with https://w3id.org/emmo/
    # For faster tests a dummyontology was created.
    # onto = get_ontology('https://raw.githubusercontent.com/emmo-repo/domain-electrochemistry/master/electrochemistry.ttl').load()
    onto = get_ontology(
        repo_dir / "tests" / "testonto" / "dummyonto_w_dummyemmo.ttl"
    ).load()

    outputdir = tmpdir / "saved_emmo_domain_ontology"
    savedfile = onto.save(
        format="rdfxml",
        dir=outputdir,
        recursive=True,
        mkdir=True,
        write_catalog_file=True,
    )
    assert get_ontology(savedfile).load()
    assert set(os.listdir(outputdir)) == {"emmo.info", "w3id.org"}
    assert set(
        os.listdir(outputdir / "emmo.info" / "emmo" / "domain" / "chameo")
    ) == {"chameo.rdfxml", "catalog-v001.xml"}
    assert set(
        os.listdir(outputdir / "emmo.info" / "emmo" / "disciplines")
    ) == {"isq.rdfxml", "catalog-v001.xml"}
    assert set(os.listdir(outputdir / "w3id.org" / "emmo" / "domain")) == {
        "dummyonto.rdfxml",
        "catalog-v001.xml",
    }

    # Test saving but giving filename. It should then be saved in the parent directory
    outputdir2 = tmpdir / "saved_emmo_domain_ontology2"
    savedfile2 = onto.save(
        format="rdfxml",
        dir=outputdir2,
        recursive=True,
        mkdir=True,
        write_catalog_file=True,
        filename="dummyonto.rdfxml",
    )
    assert get_ontology(savedfile2).load()
    assert set(os.listdir(outputdir2)) == {
        "emmo.info",
        "dummyonto.rdfxml",
        "catalog-v001.xml",
    }
    assert set(
        os.listdir(outputdir / "emmo.info" / "emmo" / "domain" / "chameo")
    ) == {"chameo.rdfxml", "catalog-v001.xml"}
    assert set(
        os.listdir(outputdir / "emmo.info" / "emmo" / "disciplines")
    ) == {"isq.rdfxml", "catalog-v001.xml"}
