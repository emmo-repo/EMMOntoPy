def test_ontodoc() -> None:
    import sys
    import os

    # Add emmo to sys path
    thisdir = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..')))
    from ontopy import get_ontology  # noqa: E402, F401
    from ontopy.ontodoc import OntoDoc, DocPP  # noqa: E402, F401


    emmo = get_ontology()
    emmo.load()

    baseiri = 'http://emmo.info/'
    iris = set(c.namespace.base_iri for c in emmo.classes())
    iris.update(set(c.namespace.base_iri for c in emmo.object_properties()))
    # iris.update(set(c.namespace.base_iri for c in emmo.annotation_properties()))

    for s in sorted(iris):
        print(s)


    inputfile = os.path.join(thisdir, 'doc.md')
    assert os.path.exists(inputfile)

    ontodoc = OntoDoc(emmo)

    with open(inputfile, 'rt') as f:
        template = f.read()
    docpp = DocPP(template, ontodoc, os.path.dirname(inputfile))
    docpp.process()
    with open('doc-output.md', 'wt') as f:
        f.write(docpp.get_buffer())
