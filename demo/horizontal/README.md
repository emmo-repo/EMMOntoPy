EMMO use case for horizontal interoperability
=============================================
Horizontal interoperability is about interoperability between
different types of models and codes for a single material (i.e. one
use case, multiple models).

The key here is to show how to map between EMMO (or an EMMO-based
ontology) and another ontology (possible EMMO-based).  In this example
we use a data-driven approach based on a C-implementation of SOFT [1][2].

This is done in four steps:

  1. Generate metadata from the EMMO-based user case ontology.

     Implemented in the script
     [step1_generate_metadata.py](step1_generate_metadata.py).

  2. Define metadata for an application developed independently of EMMO.

     In this case a metadata description of the ASE Atoms class [3] is
     created in `atoms.json`.

     Implemented in the script
     [step2_define_metadata.py](step2_define_metadata.py).

  3. Instantiate the metadata defined defined in step 2 with an
     atomistic structure interface structure.

     Implemented in the script
     [step3_instantiate.py](step3_instantiate.py).

  4. Map the atomistic interface structure from the application
     representation to the common EMMO-based representation.

     Implemented in the script
     [step4_map_instance.py](step4_map_instance.py).

Essentially this demonstration shows how EMMO can be extended and how
external data can be mapped into our extended ontology (serving as a
common representational system).



Requirements for running the user case
--------------------------------------
In addition to emmo, this demo also requires:
  - [dlite][1], a C-implementation of [SOFT][2] used for handling metadata
  - [ASE][3], for reading atom structure from cif and visualisation



[1]: https://github.com/jesper-friis/DLite
[2]: https://github.com/NanoSim/SOFT5
[3]: https://wiki.fysik.dtu.dk/ase/
