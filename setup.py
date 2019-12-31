#!/usr/bin/env python3
"""Python reference API for the Europeean Materials & Modelling Ontology (EMMO).
"""
import os
import setuptools
from glob import glob


def rglob(patt):
    return [f for f in glob(patt, recursive=True) if os.path.isfile(f)]


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='emmo',
    version='1.0.0',
    author='Europeean Materials Modelling Council (EMMC)',
    author_email='jesper.friis@sintef.no',
    description = ('Python reference API for the Europeean Materials & '
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
        'Programming Language :: Python :: 3.8',
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=['emmo'],
    scripts=['tools/ontodoc'],
    package_data={'emmo': ['owl/emmo-inferred.owl', 'tests/*.py']},
    data_files=[
        ('share/EMMO-python', ['README.md', 'LICENSE.txt']),
        ('share/EMMO-python/examples', rglob('examples/**')),
        ('share/EMMO-python/demo', rglob('demo/**')),
    ],
)
