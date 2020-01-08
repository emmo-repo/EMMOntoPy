EMMO -- A Python API for the Euroean Materials & Modelling Ontology (EMMO)
==========================================================================
This is a Python API for EMMO based on [Owlready2], which provides an
intuitive representation of EMMO in Python.

EMMO is an ongoing effort to create an ontology that takes into
account fundamental concepts of physics, chemistry and materials
science and is designed to pave the road for semantic
interoperability.  The aim of EMMO is to be generic and provide a
common ground for describing materials, models and data that can be
adapted by all domains.

EMMO is formulated using OWL.  EMMO-python is a Python API for using
EMMO to solving real problems.  By using the excellent Python package
[Owlready2], EMMO-python provides a natural representation of
EMMO in Python.  On top of that EMMO-python provides:

  - Access by label (as well as by names, important since class and
    property names in EMMO are based on UUIDs).
  - Generation of graphs.
  - Generation of documentation.
  - Pre-inferred [OWL file](emmo/owl/emmo-inferred.owl) of EMMO.
  - ++

Some examples of what you can do with EMMO-python includes:

  - Access and query EMMO-based ontologies from your application.
  - Extend EMMO with new domain or application ontologies.  This can
    be done both statically with easy readable Python code or
    dynamically within your application.
  - Generate graphs and documentation of your ontologies.  EMMO-python
    includes `ontodoc`, which is a dedicated command line tool for this.
    You find it in the [tools/](tools) sub directory.
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
