# EMMOntoPy

*Python API for the Elemental Multiperspective Material Ontology ([EMMO]).*

<!-- markdownlint-disable MD033 -->

![CI tests](https://github.com/emmo-repo/EMMO-python/workflows/CI%20Tests/badge.svg)
[![PyPI version](https://badge.fury.io/py/EMMOntoPy.svg)](https://badge.fury.io/py/EMMOntoPy)

> ***Note**: EMMOntoPy is a continuation of the EMMO-python project and the associated `emmo` Python package.
> To see the legacy versions go to [PyPI](https://pypi.org/project/EMMO/).*

This package is based on [Owlready2] and provides an intuitive representation of [EMMO] in Python.
It is available on [GitHub][EMMOntoPy] and on [PyPI][PyPI:EMMOntoPy] under the open source [BSD 3-Clause license](LICENSE.txt).

The Elemental Multiperspective Material Ontology (EMMO) is an ongoing effort to create an ontology that takes into account fundamental concepts of physics, chemistry and materials science and is designed to pave the road for semantic interoperability.
The aim of EMMO is to be generic and provide a common ground for describing materials, models and data that can be adapted by all domains.

EMMO is formulated using OWL.
EMMOntoPy is a Python API for using EMMO to solving real problems.
By using the excellent Python package [Owlready2], EMMOntoPy provides a natural representation of EMMO in Python.
On top of that EMMOntoPy provides:

- Access by label (as well as by names, important since class and property names in EMMO are based on UUIDs).
- Test suite for EMMO-based ontologies.
- Generation of graphs.
- Generation of documentation.
- Command-line tools:
  - [`emmocheck`](docs/tools-instructions.md#emmocheck):
    Checks an ontology against EMMO conventions.
  - [`ontoversion`](docs/tools-instructions.md#ontoversion):
    Prints ontology version number.
  - [`ontograph`](docs/tools-instructions.md#ontograph):
    Vertasile tool for visualising (parts of) an ontology.
  - [`ontodoc`](docs/tools-instructions.md#ontodoc):
    Documents an ontology.
  - [`ontoconvert`](docs/tools-instructions.md#ontoconvert):
    Converts between ontology formats.

Some examples of what you can do with EMMOntoPy includes:

- Access and query RDF-based ontologies from your application.
  This includes several different flavors of RDF (OWL, **Turtle (`ttl`)**, and more).
- Access and query EMMO-based ontologies from your application.
- Extend EMMO with new domain or application ontologies.
  This can be done both statically with easy readable Python code or dynamically within your application.
- Generate graphs and documentation of your ontologies.
  EMMOntoPy includes `ontodoc`: A dedicated command line tool for this.
  You find it in the [tools/](tools) sub directory.
- Check that an EMMO-based domain or application ontology adhere to the conventions of EMMO.
- Interactively explore an ontology in any Python interpreter, e.g., [IPython].
  Tab-completion makes exploration easy and fast.
  Below is an example of an IPython session where we check the relations of `Matter` in EMMO utilizing the `emmopy.get_emmo` function:

  ```ipython
  In [1]: from emmopy import get_emmo

  In [2]: emmo = get_emmo()

  In [3]: emmo.Matter
  Out[3]: physicalistic.Matter

  In [4]: emmo.Matter.is_a
  Out[4]:
  [physicalistic.Physicalistic,
    physical.Physical,
    mereotopology.hasPart.some(physicalistic.Massive),
    physical.hasTemporalPart.only(physicalistic.Matter)]
  ```

## Documentation and examples

The [Owlready2 documentation][Owlready2-doc] is a good starting point.
The EMMOntoPy package also has its own [dedicated documentation](https://emmo-repo.github.io/EMMO-python).

This includes a few examples and demos:

- [demo/vertical](demo/vertical/README.md) shows an example of how EMMO may be used to achieve vertical interoperability.
  The file [define-ontology.py](demo/vertical/define_ontology.py) provides a good example for how an EMMO-based application ontology can be defined in Python.

- [demo/horizontal](demo/horizontal/README.md) shows an example of how EMMO may be used to achieve horizontal interoperability.
  This demo also shows how you can use EMMOntoPy to represent your ontology with the low-level metadata framework [DLite].
  In addition to achieve interoperability, as shown in the demo, DLite also allow you to automatically generate C or Fortran code base on your ontology.

- [examples/emmodoc](examples/emmodoc/README.md) shows how the documentation of EMMO is generated using the `ontodoc` tool.

## Installation

Install with

```console
pip install EMMOntoPy
```

### Required Dependencies

- [Python] 3.6 or later.
- [Owlready2] v0.23 or later.

### Optional Dependencies

- [Graphviz]: Needed for graph generation.
  With support for generation pdf, png and svg figures for tests and generation of documentation automatically (`ontodoc`).
- [pandoc]: Only used for generated documentation from markdown to nicely formatted html or pdf.
  Tested with v2.1.2.
- [pdfLaTeX] or [XeLaTeX] and the `upgreek` LaTeX package (included in `texlive-was` on RetHat-based distributions and `texlive-latex-extra` on Ubuntu) for generation of pdf documentation.
  If your ontology contains exotic unicode characters, we recommend XeLaTeX.

- Java.
  Needed for reasoning.

- Optional Python packages:
  - [graphviz]: Generation of documentation and graphs.
  - [PyYAML]: Required for generating documentation with pandoc.
  - [blessings]: Clean output for `emmocheck`.
  - [Pygments]: Coloured output for `emmocheck`.
  - [rdflib]: Required for `ontoversion`-tool.
  - [semver]: Required for `ontoversion`-tool.
  - [pydot]: Used for generating graphs.
    Will be deprecated.

See [docs/docker-instructions.md](docs/docker-instructions.md) for how to build a docker image.

### Known issues

- **Invalid serialising to turtle:** Due to rdflib issue [#1043](https://github.com/RDFLib/rdflib/issues/1043) `ontoconvert` may produce invalid turtle output (if your ontology contains real literals using scientific notation without a dot in the mantissa).
  This issue was fixed after the release of rdflib 5.0.0.
  Hence, install the latest rdflib from PyPI (`pip install --upgrade rdflib`) or directly from the source code repository: [GitHub](https://github.com/RDFLib/rdflib) if you need to serialise to turtle.

### Attributions and credits

EMMOntoPy is maintained by [EMMC-ASBL](https://emmc.eu/).
It has mainly been developed by [SINTEF](https://www.sintef.no/), specifically:

- Jesper Friis ([jesper-friis](https://github.com/jesper-friis))
- Francesca L. Bleken ([francescalb](https://github.com/francescalb))
- Casper W. Andersen ([CasperWA](https://github.com/CasperWA))
- Bjørn Tore Løvfall ([lovfall](https://github.com/lovfall))

### Contributing projects

- [EMMC-CSA](https://emmc.info/about-emmc-csa/);
  Grant Agreement No: 723867
  <img src="https://i2.wp.com/emmc.info/wp-content/uploads/2018/10/emmc_logo-low.jpg?fit=1701%2C1701&ssl=1" width="50">
- [MarketPlace](https://www.the-marketplace-project.eu/);
  Grant Agreement No: 760173
  <img src="https://www.the-marketplace-project.eu/content/dam/iwm/the-marketplace-project/images/MARKETPLACE_LOGO_300dpi.png" width="120">
- [OntoTrans](https://ontotrans.eu/project/);
  Grant Agreement No: 862136
  <img src="https://ontotrans.eu/wp-content/uploads/2020/05/ot_logo_rosa_gro%C3%9F.svg" width="81.625">
- [BIG-MAP](https://www.big-map.eu/);
  Grant Agreement No: 957189
  <img src="https://avatars1.githubusercontent.com/u/72801303?s=200&v=4" width="50">
- [OpenModel](https://www.open-model.eu/);
  Grant Agreement No: 953167
  <img src="https://www.open-model.eu/en/jcr:content/stage/stageParsys/stage_slide_383467607/image.img.jpg/1630120770165/OpenModel-Logob.jpg" width="110">

[EMMOntoPy]: https://github.com/emmo-repo/EMMO-python/
[Owlready2]: https://pypi.org/project/Owlready2/
[Owlready2-doc]: https://owlready2.readthedocs.io/
[EMMO]: https://emmo-repo.github.io
[PyPI:EMMOntoPy]: https://pypi.org/project/EMMOntoPy/
[Python]: https://www.python.org/
[IPython]: https://ipython.org/
[DLite]: https://github.com/SINTEF/dlite/
[pydot]: https://pypi.org/project/pydot/
[Graphviz]: https://www.graphviz.org/
[pandoc]: http://pandoc.org/
[XeLaTeX]: https://www.overleaf.com/learn/latex/XeLaTeX/
[pdfLaTeX]: https://www.latex-project.org/
[graphviz]: https://pypi.org/project/graphviz
[PyYAML]: https://pypi.org/project/PyYAML/
[blessings]: https://pypi.org/project/blessings/
[Pygments]: https://pypi.org/project/Pygments/
[semver]: https://pypi.org/project/semver/
[rdflib]: https://pypi.org/project/rdflib/
