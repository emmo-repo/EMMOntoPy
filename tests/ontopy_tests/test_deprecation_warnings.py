from typing import TYPE_CHECKING
import pytest
from owlready2.entity import ThingClass
from owlready2.prop import ObjectPropertyClass, DataPropertyClass
from owlready2 import AnnotationPropertyClass

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.filterwarnings(
    "ignore:Ontology.add_label_annotations() is deprecated. Direct modify the `label_annotations` attribute instead."
)
def test_deprecation_warnings() -> None:
    """Test functionalities will be removed and currently have depracation warnings"""
    from ontopy import get_ontology
    from ontopy.ontology import DEFAULT_LABEL_ANNOTATIONS

    testonto = get_ontology("http://domain_ontology/new_ontology")

    testonto.add_label_annotation(DEFAULT_LABEL_ANNOTATIONS[0])

    testonto.remove_label_annotation(DEFAULT_LABEL_ANNOTATIONS[0])
