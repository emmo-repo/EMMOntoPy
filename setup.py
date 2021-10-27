#!/usr/bin/env python3
"""
Python reference API for the Europeean Materials & Modelling Ontology (EMMO).
"""
import setuptools


setuptools.setup(
    name='EMMO',
    version="2.0.0",
    author='Jesper Friis, Francesca Lønstad Bleken, Bjørn Tore Løvfall',
    author_email='jesper.friis@sintef.no',
    description=('Python reference API for the Europeean Materials & '
                 'Modelling Ontology'),
    long_description=(
        """Use [`EMMOntoPy`](https://pypi.org/project/EMMOntoPy) instead."""
    ),
    long_description_content_type="text/markdown",
    url='https://github.com/emmo-repo/EMMO-python',
    license='BSD',
    python_requires='>=3.6.0',
    classifiers=['Development Status :: 7 - Inactive'],
    install_requires=["EMMOntoPy"],
)
