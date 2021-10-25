#!/usr/bin/env python3
"""
Python reference API for the
Elementary Multiperspective Material Ontology (EMMO).
"""
import os
import re
import setuptools
from glob import glob


rootdir = os.path.dirname(__file__)


def rglob(patt):
    """Recursive glob function that only returns ordinary files."""
    return [f for f in glob(patt, recursive=True) if os.path.isfile(f)]


def fglob(patt):
    """Glob function that only returns ordinary files."""
    return [f for f in glob(patt) if os.path.isfile(f) and not f.endswith('~')]


# Read long description from README.md file replacing references to local
# files to github urls
baseurl = 'https://raw.githubusercontent.com/emmo-repo/EMMO-python/master/'
with open(os.path.join(rootdir, 'README.md'), 'rt') as f:
    long_description = re.sub(
        r'(\[[^]]+\])\(([^:)]+)\)', r'\1(%s\2)' % baseurl, f.read())

# Read requirements from requirements.txt file
with open(os.path.join(rootdir, 'requirements.txt'), 'rt') as f:
    REQUIREMENTS = [
        f"{_.strip()}"
        for _ in f.readlines()
        if not _.startswith("#") and "git+" not in _
    ]

with open(
    os.path.join(rootdir, "requirements_docs.txt"), "r", encoding="utf8"
) as handle:
    DOCS = [
        f"{_.strip()}"
        for _ in handle.readlines()
        if not _.startswith("#") and "git+" not in _
    ]

# Retrieve emmo-package version
with open(os.path.join(rootdir, 'ontopy/__init__.py')) as handle:
    for line in handle:
        match = re.match(r"__version__ = '(?P<version>.*)'", line)
        if match is not None:
            VERSION = match.group("version")
            break
    else:
        raise RuntimeError(
            f'Could not determine package version from {handle.name} !')


setuptools.setup(
    name='EMMOntoPy',
    version=VERSION,
    author=(
        'Jesper Friis, Francesca Lønstad Bleken, Casper Welzel Andersen, '
        'Bjørn Tore Løvfall'
    ),
    author_email='jesper.friis@sintef.no',
    description=('Python reference API for the Elementary Multiperspective'
                 'Material Ontology.'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/emmo-repo/EMMO-python',
    license='BSD',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=REQUIREMENTS,
    extras_require={"docs": DOCS},
    packages=setuptools.find_packages(),
    scripts=['tools/ontodoc',
             'tools/ontograph',
             'tools/emmocheck',
             'tools/ontoconvert',
             'tools/ontoversion'],
    package_data={
        'ontopy.factpluspluswrapper.java.lib.so': ['*'],
        'ontopy.factpluspluswrapper.java.lib.jars': ['*.jar'],
        'ontopy.factpluspluswrapper.java': ['pom.xml'],
    },
    include_package_data=True,
    data_files=[
        ('share/EMMO-python', ['README.md', 'LICENSE.txt']),
        (
            'share/EMMO-python/examples/emmodoc',
            glob('examples/emmodoc/*.md') +
            glob('examples/emmodoc/*.yaml') +
            glob('examples/emmodoc/pandoc-*'),
        ),
        (
            'share/EMMO-python/examples/emmodoc/figs',
            fglob('examples/emmodoc/figs/*'),
        ),
        # ('share/EMMO-python/examples', rglob('examples/**')),
        ('share/EMMO-python/demo', rglob('demo/**')),
    ],
)
