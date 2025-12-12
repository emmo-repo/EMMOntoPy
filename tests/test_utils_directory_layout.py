import os
from pathlib import Path

from ontopy import get_ontology
from ontopy.utils import directory_layout


def test_emmo_directory_layout():
    thisdir = Path(__file__).resolve().parent
    ontopath = thisdir / "testonto" / "emmo" / "emmo.ttl"
    emmo = get_ontology(ontopath).load()
    layout = directory_layout(emmo)

    # Map base IRIs to ontologies for easy access to all sub-ontologies
    omap = {o.base_iri: o for o in layout.keys()}
    print(omap)
    # Base IRI of EMMO should not end with slash (/) !!!
    assert layout[omap["https://w3id.org/emmo#"]] == "emmo"

    assert (
        layout[omap["https://w3id.org/emmo/perspectives#"]]
        == "perspectives/perspectives"
    )
    assert (
        layout[omap["https://w3id.org/emmo/reference/data#"]]
        == "reference/data"
    )
    assert (
        layout[omap["https://w3id.org/emmo/disciplines#"]]
        == "disciplines/disciplines"
    )
    assert (
        layout[omap["https://w3id.org/emmo/disciplines/math#"]]
        == "disciplines/math"
    )
    assert (
        layout[omap["https://w3id.org/emmo/mereocausality#"]]
        == "mereocausality"
        # == "mereocausality/mereocausality"
    )

    # Also check dir layout for the disciplines module - should be the same as for emmo
    disciplines = omap["https://w3id.org/emmo/disciplines#"]
    layout = directory_layout(disciplines)
    assert (
        layout[omap["https://w3id.org/emmo/perspectives#"]]
        == "perspectives/perspectives"
    )
    assert (
        layout[omap["https://w3id.org/emmo/disciplines#"]]
        == "disciplines/disciplines"
    )
    assert (
        layout[omap["https://w3id.org/emmo/disciplines/math#"]]
        == "disciplines/math"
    )


def test_local_directory_layout():
    thisdir = Path(__file__).resolve().parent
    ontopath = thisdir / "testonto" / "testonto.ttl"
    onto = get_ontology(ontopath).load()
    layout = directory_layout(onto)
    omap = {o.base_iri: o for o in layout.keys()}

    assert layout[omap["http://emmo.info/models#"]] == "models"
    assert layout[omap["http://emmo.info/testonto#"]] == "testonto"


def test_local_directory_layout_recursive():
    thisdir = Path(__file__).resolve().parent
    ontopath = thisdir / "testonto" / "testonto-recursive.ttl"
    onto = get_ontology(ontopath).load()
    layout = directory_layout(onto)
    omap = {o.base_iri: o for o in layout.keys()}

    assert (
        layout[omap["http://emmo.info/models-recursive#"]] == "models-recursive"
    )
    assert (
        layout[omap["http://emmo.info/testonto-recursive#"]]
        == "testonto-recursive"
    )
