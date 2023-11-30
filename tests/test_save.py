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
    testonto.save(format="rdfxml")

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
    # 1. check that the file testonto.owl is the same as
    # testonto_saved.owl
    # 2. save testonto to testonto.owl again
    # 3. check that testonto.owl is not the same as testonto_saved.owl
    # 4. save testonto to testonto.owl again, but with overwrite=True
    # 5. check that testonto.owl is the same as testonto_saved.owl
    # NB! this is not currently working, issue #685

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

    # Test that the ontology is saved recursively when deisred
    testonto.save(
        format="ttl", dir=tmpdir / "recursively", mkdir=True, recursive=True
    )
    assert (tmpdir / "recursively" / "testonto.ttl").exists()
    # Recursive save is not working . Issue #687
    # assert (tmpdir / "recursively" / "models.ttl").exists()

    # squash merge during save

    # Write catalogfile

    # append_catalog

    # catalog_filename
