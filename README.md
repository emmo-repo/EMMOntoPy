EMMO - Python API for the European Materials & Modelling Ontology
=================================================================

![CI tests](https://github.com/emmo-repo/EMMO-python/workflows/CI%20Tests/badge.svg)
[![PyPI package](https://badge.fury.io/py/EMMO.svg)](https://pypi.org/project/EMMO/)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/emmo-repo/EMMO-python/blob/pypi-badge/LICENSE.txt)


This package is based on [Owlready2] and provides an intuitive
representation of [EMMO] in Python.
It is available on [GitHub][EMMO-python] and on [PyPI][PyPI:EMMO]
under the open source BSD 3-Clause license.

The European Materials & Modelling Ontology (EMMO) is an ongoing
effort to create an ontology that takes into account fundamental
concepts of physics, chemistry and materials science and is designed
to pave the road for semantic interoperability.  The aim of EMMO is to
be generic and provide a common ground for describing materials,
models and data that can be adapted by all domains.

EMMO is formulated using OWL.  EMMO-python is a Python API for using
EMMO to solving real problems.  By using the excellent Python package
[Owlready2], EMMO-python provides a natural representation of
EMMO in Python.  On top of that EMMO-python provides:

  - Access by label (as well as by names, important since class and
    property names in EMMO are based on UUIDs).
  - Generation of graphs.
  - Generation of documentation.
  - Test suite for EMMO-based ontologies.
  - Command-line tools (ontograph, ontodoc and emmocheck, ontoversion).

Some examples of what you can do with EMMO-python includes:

  - Access and query EMMO-based ontologies from your application.
  - Extend EMMO with new domain or application ontologies.  This can
    be done both statically with easy readable Python code or
    dynamically within your application.
  - Generate graphs and documentation of your ontologies.  EMMO-python
    includes `ontodoc`, which is a dedicated command line tool for this.
    You find it in the [tools/](tools) sub directory.
  - Check that a EMMO-based domain or application ontology ahead to the
    conventions of EMMO.
  - Interactively explore an ontology in e.g. [IPython].  Tab completion
    makes exploration easy and fast.  Below is an example of an IPython
    session where we check the relations of `Matter`:

    ```python
    >>> from emmo import get_ontology

    >>> emmo = get_ontology()
    >>> emmo.load()

    >>> emmo.Matter
    emmo-material.Matter

    >>> emmo.Matter.is_a
    [emmo-material.Type,
     emmo-mereotopology.hasPart.some(emmo-material.Massive),
     emmo-mereotopology.hasTemporalPart.only(emmo-material.Matter)]
    ```


Documentation and examples
--------------------------
The [Owlready2 documentation][Owlready2-doc] is a good starting point.

In addition EMMO-python includes a few examples and demos:
  - [demo/vertical](demo/vertical/README.md) shows an example of
    how EMMO may be used to achieve vertical interoperability.
    The file [define-ontology.py](demo/vertical/define-ontology.py)
    provides a good example for how an EMMO-based application ontology
    can be defined in Python.

  - [demo/horizontal](demo/horizontal/README.md) shows an example of
    shows an example of how EMMO may be used to achieve horizontal
    interoperability.  This demo also shows how you can use
    EMMO-python to represent your ontology with the low-level metadata
    framework [DLite]. In addition to achieve interoperability, as
    shown in the demo, DLite also allow you to automatically generate
    C or Fortran code base on your ontology.

  - [examples/emmodoc](examples/emmodoc/README.md) shows how the
    documentation of EMMO is generated using the `ontodoc` tool.


Installation
------------
Install with

    pip install EMMO

### Required Dependencies
  * [Python] 3.6 or later
  * [Owlready2] v0.23 or later


### Optional Dependencies
  * [Graphviz]: Needed for graph generation. With support for generation
    pdf, png and svg figures for tests and generation of documentation
    automatically (ontodoc).

  * [pandoc]: Only used for generated documentation from markdown to
    nicely formatted html or pdf.  Tested with v2.1.2.

  * [pdfLaTeX] or [XeLaTeX] and the `upgreek` latex
    package (included in `texlive-was` on RetHat-based distributions
    and `texlive-latex-extra` on Ubuntu) for generation of pdf
    documentation.  If your ontology contain exotic unicode characters, we
    recommend XeLaTeX.

  * Java. Needed for reasoning.

  * Optional Python packages
    - [graphviz]: Generation of documentation and graphs.
    - [PyYAML]:  Required for generating documentation with pandoc.
    - [blessings]: Clean output for emmocheck
    - [Pygments]: Coloured output for emmocheck
    - [rdflib]: Required for ontoversion-tool
    - [semver]: Required for ontoversion-tool
    - [pydot]: Used for generating graphs. Will be deprecated.

See [docs/docker-dockerinstructions.md](#docs/docker-dockerinstructions.md)
for how to build a docker image.

[EMMO-python]: https://github.com/emmo-repo/EMMO-python/
[EMMO-pypi]: https://pypi.org/project/EMMO/
[Owlready2]: https://pypi.org/project/Owlready2/
[Owlready2-doc]: https://pythonhosted.org/Owlready2/
[EMMO]: https://github.com/emmo-repo/EMMO/
[EMMO-python]: https://github.com/emmo-repo/EMMO-python/
[PyPI:EMMO]: https://pypi.org/project/EMMO/
[Python]: https://www.python.org/
[IPython]: https://ipython.org/
[DLite]: https://github.com/SINTEF/dlite/
[pydot]: https://pypi.org/project/pydot/
[Graphviz]: https://www.graphviz.org/
[pandoc]: http://pandoc.org/
[XeLaTeX]: https://www.overleaf.com/learn/latex/XeLaTeX/
[pdfLaTeX]: https://www.latex-project.org/
[graphviz]: https://pypi.org/project/
[PyYAML]: https://pypi.org/project/PyYAML/
[blessings]: https://pypi.org/project/blessings/
[Pygments]: https://pypi.org/project/Pygments/
[semver]: https://pypi.org/project/semver/
[rdflib]: https://pypi.org/project/rdflib/
