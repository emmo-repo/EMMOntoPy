from ontopy import get_ontology
from typing import Optional


def emmo(inferred: Optional[bool] = True):
    """Returns the current version of emmo.

    Args:
        inferred: Whether to import the inferred version of emmo or not.
        Default is True.

    Returns:
        the loaded emmo ontology.
    """
    if inferred == True:
        name = 'emmo-inferred'
    else:
        name = 'emmo'
    return get_ontology(name).load()
