import os
from pathlib import Path

from ontopy import get_ontology
from ontopy.utils import directory_layout


def test_emmo_directory_layout():
    emmo = get_ontology(
        "https://raw.githubusercontent.com/emmo-repo/EMMO/1.0.0-beta4/emmo.ttl"
    ).load()
    layout = directory_layout(emmo)

    # Map base IRIs to ontologies for easy access to all sub-ontologies
    omap = {o.base_iri: o for o in layout.keys()}
    print(omap)
    # Base IRI of EMMO should not end with slash (/) !!!
    assert layout[omap["http://emmo.info/emmo/"]] == "emmo"

    assert (
        layout[omap["http://emmo.info/emmo/perspectives#"]]
        == "perspectives/perspectives"
    )
    assert (
        layout[omap["http://emmo.info/emmo/perspectives/data#"]]
        == "perspectives/data"
    )
    assert (
        layout[omap["http://emmo.info/emmo/disciplines#"]]
        == "disciplines/disciplines"
    )
    assert (
        layout[omap["http://emmo.info/emmo/disciplines/math#"]]
        == "disciplines/math"
    )
    assert (
        layout[omap["http://emmo.info/emmo/mereocausality#"]]
        == "mereocausality/mereocausality"
    )

    # Also check dir layout for the disciplines module - should be the same as for emmo
    disciplines = omap["http://emmo.info/emmo/disciplines#"]
    layout = directory_layout(disciplines)
    assert (
        layout[omap["http://emmo.info/emmo/perspectives#"]]
        == "perspectives/perspectives"
    )
    assert (
        layout[omap["http://emmo.info/emmo/perspectives/data#"]]
        == "perspectives/data"
    )
    assert (
        layout[omap["http://emmo.info/emmo/disciplines#"]]
        == "disciplines/disciplines"
    )
    assert (
        layout[omap["http://emmo.info/emmo/disciplines/math#"]]
        == "disciplines/math"
    )
    assert (
        layout[omap["http://emmo.info/emmo/mereocausality#"]]
        == "mereocausality/mereocausality"
    )


def test_local_directory_layout():
    thisdir = Path(__file__).resolve().parent
    ontopath = thisdir / "testonto" / "testonto.ttl"
    onto = get_ontology(ontopath).load()
    layout = directory_layout(onto)
    omap = {o.base_iri: o for o in layout.keys()}

    assert layout[omap["http://emmo.info/models#"]] == "models"
    assert layout[omap["http://emmo.info/testonto#"]] == "testonto"
