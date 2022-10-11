#!/usr/bin/env python3
"""
Python reference API for the
Elementary Multiperspective Material Ontology (EMMO).
"""
from glob import glob
import os
import re

import setuptools


rootdir = os.path.dirname(__file__)


def rglob(patt):
    """Recursive glob function that only returns ordinary files."""
    return [_ for _ in glob(patt, recursive=True) if os.path.isfile(_)]


def fglob(patt):
    """Glob function that only returns ordinary files."""
    return [_ for _ in glob(patt) if os.path.isfile(_) and not _.endswith("~")]


# Read long description from README.md file replacing references to local
# files to github urls
BASE_URL = "https://raw.githubusercontent.com/emmo-repo/EMMOntoPy/master/"
with open(os.path.join(rootdir, "README.md"), "rt") as handle:
    long_description = re.sub(
        r"(\[[^]]+\])\(([^:)]+)\)", rf"\1({BASE_URL}\2)", handle.read()
    )

# Read requirements from requirements.txt file
with open(os.path.join(rootdir, "requirements.txt"), "rt") as handle:
    REQUIREMENTS = [
        f"{_.strip()}"
        for _ in handle.readlines()
        if not _.startswith("#") and "git+" not in _
    ]

with open(os.path.join(rootdir, "requirements_docs.txt"), "r") as handle:
    DOCS = [
        f"{_.strip()}"
        for _ in handle.readlines()
        if not _.startswith("#") and "git+" not in _
    ]

with open(os.path.join(rootdir, "requirements_dev.txt"), "r") as handle:
    DEV = [
        f"{_.strip()}"
        for _ in handle.readlines()
        if not _.startswith("#") and "git+" not in _
    ] + DOCS

# Retrieve emmo-package version
with open(os.path.join(rootdir, "ontopy/__init__.py")) as handle:
    for line in handle:
        match = re.match(r"__version__ = ('|\")(?P<version>.*)('|\")", line)
        if match is not None:
            VERSION = match.group("version")
            break
    else:
        raise RuntimeError(
            f"Could not determine package version from {handle.name} !"
        )


setuptools.setup(
    name="EMMOntoPy",
    version=VERSION,
    author=(
        "Jesper Friis, Francesca Lønstad Bleken, Casper Welzel Andersen, "
        "Bjørn Tore Løvfall"
    ),
    author_email="jesper.friis@sintef.no",
    description=(
        "Python reference API for the Elementary Multiperspective"
        "Material Ontology."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emmo-repo/EMMOntoPy",
    license="BSD",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=REQUIREMENTS,
    extras_require={"dev": DEV, "docs": DOCS},
    packages=setuptools.find_packages(),
    scripts=[
        "tools/ontodoc",
        "tools/ontograph",
        "tools/emmocheck",
        "tools/ontoconvert",
        "tools/ontoversion",
        "tools/excel2onto",
    ],
    package_data={
        "ontopy.factpluspluswrapper.java.lib.so": ["*"],
        "ontopy.factpluspluswrapper.java.lib.jars": ["*.jar"],
        "ontopy.factpluspluswrapper.java": ["pom.xml"],
    },
    include_package_data=True,
    data_files=[
        ("share/EMMOntoPy", ["README.md", "LICENSE.txt"]),
        (
            "share/EMMOntoPy/examples/emmodoc",
            glob("examples/emmodoc/*.md")
            + glob("examples/emmodoc/*.yaml")
            + glob("examples/emmodoc/pandoc-*"),
        ),
        (
            "share/EMMOntoPy/examples/emmodoc/figs",
            fglob("examples/emmodoc/figs/*"),
        ),
        # ('share/EMMOntoPy/examples', rglob('examples/**')),
        ("share/EMMOntoPy/demo", rglob("demo/**")),
    ],
)
