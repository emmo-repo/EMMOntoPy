from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
    from ontopy.ontology import Ontology


def test_basic(emmo: "Ontology") -> None:
    from ontopy import get_ontology
    from ontopy.utils import LabelDefinitionError

    emmo.sync_reasoner()

    onto = get_ontology("onto.owl")
    onto.imported_ontologies.append(emmo)
    onto.base_iri = "http://emmo.info/examples/test#"

    # Add entity directly
    onto.new_entity("Hydrogen", emmo.Atom)

    with pytest.raises(LabelDefinitionError):
        onto.new_entity("Hydr ogen", emmo.Atom)

    with onto:

        # Add entity using python classes
        class Oxygen(emmo.Atom):
            """Oxygen atom."""

        class H2O(emmo.Molecule):
            """Water molecule."""

            emmo.hasSpatialDirectPart.exactly(2, onto.Hydrogen)
            emmo.hasSpatialDirectPart.exactly(1, Oxygen)

        # Create some
        H1 = onto.Hydrogen()
        H2 = onto.Hydrogen()
        O = Oxygen()
        water = H2O()
        water.hasSpatialDirectPart = [H1, H2, O]

    name_prefix = "myonto_"
    onto.sync_attributes(name_policy="sequential", name_prefix=name_prefix)
    assert f"{onto.base_iri}{name_prefix}0" in onto
    assert f"{onto.base_iri}{name_prefix}6" in onto

    name_prefix = "onto_"
    onto.sync_attributes(name_policy="uuid", name_prefix=name_prefix)
    assert water.name.startswith("onto_")
    # A UUID is 32 chars long + 4 `-` chars = 36 chars
    assert len(water.name) == len(name_prefix) + 36
