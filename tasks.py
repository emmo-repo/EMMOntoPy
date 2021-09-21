"""Repository management tasks powered by `invoke`.

More information on `invoke` can be found at http://www.pyinvoke.org/.
"""
# pylint: disable=import-outside-toplevel,too-many-locals
import re
import sys
from typing import Tuple
from pathlib import Path

from invoke import task


TOP_DIR = Path(__file__).parent.resolve()


def update_file(filename: str, sub_line: Tuple[str, str], strip: str = None) -> None:
    """Utility function for tasks to read, update, and write files"""
    with open(filename, "r", encoding="utf8") as handle:
        lines = [
            re.sub(sub_line[0], sub_line[1], line.rstrip(strip)) for line in handle
        ]

    with open(filename, "w", encoding="utf8") as handle:
        handle.write("\n".join(lines))
        handle.write("\n")


@task(help={"ver": "EMMOntoPy version to set"})
def setver(_, ver=""):
    """Sets the EMMOntoPy version."""
    match = re.fullmatch(
        (
            r"v?(?P<version>[0-9]+(\.[0-9]+){2}"  # Major.Minor.Patch
            r"(-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?"  # pre-release
            r"(\+[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?)"  # build metadata
        ),
        ver,
    )
    if not match:
        sys.exit(
            "Error: Please specify version as "
            "'Major.Minor.Patch(-Pre-Release+Build Metadata)' or "
            "'vMajor.Minor.Patch(-Pre-Release+Build Metadata)'"
        )
    ver = match.group("version")

    update_file(
        TOP_DIR / "ontopy/__init__.py",
        (r'__version__ = ".*"', f'__version__ = "{ver}"'),
    )

    print(f"Bumped version to {ver}")


@task(
    help={
        "pre-clean": "Remove the 'api_reference' sub directory prior to (re)creation."
    }
)
def create_api_reference_docs(_, pre_clean=False):
    """Create the API Reference in the documentation"""
    import os
    import shutil

    def write_file(full_path: Path, content: str) -> None:
        """Write file with `content` to `full_path`"""
        if full_path.exists():
            with open(full_path, "r", encoding="utf8") as handle:
                cached_content = handle.read()
            if content == cached_content:
                del cached_content
                return
            del cached_content
        with open(full_path, "w", encoding="utf8") as handle:
            handle.write(content)

    package_dirs = (TOP_DIR / "emmopy", TOP_DIR / "ontopy")
    docs_api_ref_dir = TOP_DIR / "docs/api_reference"

    unwanted_subdirs = ("__pycache__",)

    pages_template = 'title: "{name}"\ncollapse_single_pages: false\n'
    md_template = "# {name}\n\n::: {py_path}\n"
    models_template = (
        md_template + f"{' ' * 4}rendering:\n{' ' * 6}show_if_no_docstring: true\n"
    )

    if docs_api_ref_dir.exists() and pre_clean:
        shutil.rmtree(docs_api_ref_dir, ignore_errors=True)
        if docs_api_ref_dir.exists():
            sys.exit(f"{docs_api_ref_dir} should have been removed!")
    docs_api_ref_dir.mkdir(exist_ok=True)

    write_file(
        full_path=docs_api_ref_dir / ".pages",
        content=pages_template.format(name="API Reference"),
    )
    library_dir = TOP_DIR

    for package_dir in package_dirs:
        for dirpath, dirnames, filenames in os.walk(package_dir):
            for unwanted_dir in unwanted_subdirs:
                if unwanted_dir in dirnames:
                    # Avoid walking into or through unwanted directories
                    dirnames.remove(unwanted_dir)

            relpath = Path(dirpath).relative_to(library_dir)

            if not (relpath / "__init__.py").exists():
                # Avoid paths that are not included in the public Python API
                continue

            # Create `.pages`
            docs_sub_dir = docs_api_ref_dir / relpath
            docs_sub_dir.mkdir(exist_ok=True)
            if str(relpath) != ".":
                write_file(
                    full_path=docs_sub_dir / ".pages",
                    content=pages_template.format(
                        name=str(relpath).rsplit("/", maxsplit=1)[-1]
                    ),
                )

            # Create markdown files
            for filename in filenames:
                if re.match(r".*\.py$", filename) is None or filename in (
                    "__init__.py",
                    "run.py",
                ):
                    # Not a Python file: We don't care about it!
                    # Or filename is `__init__.py`: We don't want it!
                    continue

                basename = filename[: -len(".py")]
                py_path = (
                    f"{relpath}/{basename}".replace("/", ".")
                    if str(relpath) != "."
                    else f"{basename}".replace("/", ".")
                )
                md_filename = filename.replace(".py", ".md")

                # For models we want to include EVERYTHING, even if it doesn't have a
                # doc-string
                template = models_template if str(relpath) == "models" else md_template

                write_file(
                    full_path=docs_sub_dir / md_filename,
                    content=template.format(name=basename, py_path=py_path),
                )


@task
def create_docs_index(_):
    """Create the documentation index page from README.md"""
    readme = TOP_DIR / "README.md"
    docs_index = TOP_DIR / "docs/index.md"

    with open(readme, encoding="utf8") as handle:
        content = handle.read()

    replacement_mapping = [
        ("docs/", ""),
        ("(LICENSE.txt)", "(LICENSE.md)"),
        ("(tools)", "(../tools)"),
    ]

    for old, new in replacement_mapping:
        content = content.replace(old, new)

    with open(docs_index, "w", encoding="utf8") as handle:
        handle.write(content)
