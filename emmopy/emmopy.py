"""# `emmopy.emmopy`

Automagically retrieve the EMMO utilizing
[`ontopy.get_ontology`][ontopy.get_ontology].
"""
from typing import Optional, TYPE_CHECKING

from ontopy import get_ontology

if TYPE_CHECKING:
    from ontopy.ontology import Ontology


def get_emmo(inferred: Optional[bool] = True) -> "Ontology":
    """Returns the current version of emmo.

    Args:
        inferred: Whether to import the inferred version of emmo or not.
            Default is True.

    Returns:
        The loaded emmo ontology.

    """
    name = "emmo-inferred" if inferred in [True, None] else "emmo"
    return get_ontology(name).load(prefix_emmo=True)
