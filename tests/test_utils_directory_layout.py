import os

from ontopy import get_ontology
from ontopy.utils import directory_layout


if True:  # Whether to check on EMMO
    emmo = get_ontology("../EMMO/emmo.ttl").load()
    layout = directory_layout(emmo)

    # Map base IRIs to ontologies for easy access to all sub-ontologies
    omap = {o.base_iri: o for o in layout.keys()}

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
        layout[omap["http://emmo.info/emmo/disciplines/units/siunits#"]]
        == "disciplines/units/siunits"
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
        layout[omap["http://emmo.info/emmo/disciplines/units/siunits#"]]
        == "disciplines/units/siunits"
    )
    assert (
        layout[omap["http://emmo.info/emmo/mereocausality#"]]
        == "mereocausality/mereocausality"
    )