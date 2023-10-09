from typing import TYPE_CHECKING
import pytest
from owlready2.entity import ThingClass
from owlready2.prop import ObjectPropertyClass, DataPropertyClass
from owlready2 import AnnotationPropertyClass

if TYPE_CHECKING:
    from pathlib import Path


def test_ontology_to_storids(testonto: "Ontology") -> None:
    """Test adding helper functions in ontopy.ontology"""
    from ontopy.ontology import DEFAULT_LABEL_ANNOTATIONS

    label_annotations = DEFAULT_LABEL_ANNOTATIONS
    assert len(testonto._to_storids(label_annotations)) == 3
    assert testonto._to_storids(None) == []
    assert testonto._to_storids([testonto.TestClass])
