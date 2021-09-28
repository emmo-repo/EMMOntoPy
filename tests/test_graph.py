from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from ontopy.ontology import Ontology

def test_graph(emmo: "Ontology", tmpdir: "Path") -> None:
        graph = emmo.get_dot_graph(relations='is_a')
        graph.write_svg(tmpdir / 'taxonomy.svg')
        graph.write_pdf(tmpdir / 'taxonomy.pdf')

        entity_graph = emmo.get_dot_graph('EMMO')
        entity_graph.write_svg(tmpdir / 'taxonomy2.svg')

        substrate_graph = emmo.get_dot_graph('Item', relations=True,
                                            leafs=('Physical'), parents='Item',
                                            style='uml')
        substrate_graph.write_svg(tmpdir / 'merotopology_graph.svg')

        property_graph = emmo.get_dot_graph('Property')
        property_graph.write_svg(tmpdir / 'property_graph.svg')

        # Update the default style
        emmo._default_style['graph']['rankdir'] = 'BT'

        relations_graph = emmo.get_dot_graph('EMMORelation')
        relations_graph.write_pdf(tmpdir / 'relation_graph.pdf')
        relations_graph.write_png(tmpdir / 'relation_graph.png')
