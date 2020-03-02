#!/usr/bin/env python3
"""\
Python reference API for the Europeean Materials & Modelling Ontology (EMMO).
"""
import os
import re
import setuptools
from glob import glob

import emmo


def rglob(patt):
    return [f for f in glob(patt, recursive=True) if os.path.isfile(f)]


# Read long description from README.md file replacing references to local
# files to github urls
baseurl = 'https://raw.githubusercontent.com/emmo-repo/EMMO-python/master/'
with open("README.md", "r") as f:
    long_description = re.sub(
        r'(\[[^]]+\])\(([^:)]+)\)', rf'\1(%s\2)' % baseurl, f.read())


setuptools.setup(
    name='EMMO',
    version=emmo.VERSION,
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
    install_requires=[
        'Cython',
        'Owlready2>=0.22',
        'pydot',
        'graphviz',
        'PyYAML',
    ],
    packages=['emmo'],
    scripts=['tools/ontodoc', 'tools/ontograph'],
    package_data={'emmo': ['owl/emmo-inferred.owl', 'tests/*.py']},
    data_files=[
        ('share/EMMO-python', ['README.md', 'LICENSE.txt']),
        ('share/EMMO-python/examples', rglob('examples/**')),
        ('share/EMMO-python/demo', rglob('demo/**')),
    ],
)
