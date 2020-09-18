#!/usr/bin/env python3
"""
Python reference API for the Europeean Materials & Modelling Ontology (EMMO).
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
        r'(\[[^]]+\])\(([^:)]+)\)', rf'\1(%s\2)' % baseurl, f.read())

# Read requirements from requirements.txt file
with open(os.path.join(rootdir, 'requirements.txt'), 'rt') as f:
    requirements = f.read().split()

# Retrieve emmo-package version
with open(os.path.join(rootdir, 'emmo/__init__.py')) as handle:
    for line in handle:
        match = re.match(r"__version__ = '(.*)'", line)
        if match is not None:
            VERSION = match.group(1)
            break
    else:
        raise RuntimeError(f'Could not determine package version from {handle.name} !')


setuptools.setup(
    name='EMMO',
    version=VERSION,
    author='Jesper Friis, Francesca Lønstad Bleken, Bjørn Tore Løvfall',
    author_email='jesper.friis@sintef.no',
    description=('Python reference API for the Europeean Materials & '
                 'Modelling Ontology'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/emmo-repo/EMMO-python',
    license='BSD',
    python_requires='>=3.6.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=requirements,
    packages=['emmo'],
    scripts=['tools/ontodoc', 'tools/ontograph', 'tools/emmocheck'],
    package_data={'emmo': ['tests/*.py']},
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
