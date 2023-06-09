from typing import TYPE_CHECKING
import pytest
from ontopy.utils import (
    NoSuchLabelError,
    LabelDefinitionError,
    EntityClassDefinitionError,
)
from owlready2.entity import ThingClass
from owlready2.prop import ObjectPropertyClass, DataPropertyClass
from owlready2 import AnnotationPropertyClass

if TYPE_CHECKING:
    from pathlib import Path


def test_new_entity(testonto: "Ontology") -> None:
    """Test adding entities to ontology"""

    # Add entity directly
    testonto.new_entity("FantasyClass", testonto.TestClass)

    # Test that new entity is found by both version of get_by_label
    assert testonto.get_by_label("FantasyClass") == testonto.FantasyClass
    print(testonto.get_by_label_all("*"))
    assert testonto.get_by_label_all("FantasyClass") == {testonto.FantasyClass}

    testonto.sync_attributes()
    # Test that after sync_attributes, the entity is not counted more than once
    assert testonto.get_by_label_all("FantasyClass") == {testonto.FantasyClass}

    with pytest.raises(LabelDefinitionError):
        testonto.new_entity("Fantasy Class", testonto.TestClass)

    testonto.new_entity(
        "AnotherClass", testonto.TestClass, entitytype=ThingClass
    )
    testonto.new_entity(
        "hasSubObjectProperty",
        testonto.hasObjectProperty,
        entitytype=ObjectPropertyClass,
    )
    testonto.new_entity(
        "hasSubDataProperty",
        testonto.hasDataProperty,
        entitytype=DataPropertyClass,
    )
    testonto.new_entity(
        "hasSubAnnotationProperty",
        testonto.hasAnnotationProperty,
        entitytype=AnnotationPropertyClass,
    )

    testonto.sync_attributes()
    testonto.new_entity(
        "AnotherClass2", testonto.AnotherClass, entitytype="class"
    )
    testonto.new_entity(
        "hasSubObjectProperty2",
        testonto.hasSubObjectProperty,
        entitytype="object_property",
    )
    testonto.new_entity(
        "hasSubDataProperty2",
        testonto.hasSubDataProperty,
        entitytype="data_property",
    )
    testonto.new_entity(
        "hasSubAnnotationProperty2",
        testonto.hasSubAnnotationProperty,
        entitytype="annotation_property",
    )

    with pytest.raises(EntityClassDefinitionError):
        testonto.new_entity("FantasyClass", testonto.hasObjectProperty)

    with pytest.raises(EntityClassDefinitionError):
        testonto.new_entity(
            "hasSubProperty",
            testonto.hasObjectProperty,
            entitytype="data_property",
        )

    with pytest.raises(EntityClassDefinitionError):
        testonto.new_entity(
            "hasSubProperty",
            testonto.hasObjectProperty,
            entitytype=AnnotationPropertyClass,
        )

    with pytest.raises(EntityClassDefinitionError):
        testonto.new_entity(
            "hasSubProperty",
            testonto.hasObjectProperty,
            entitytype="nonexistingpropertytype",
        )
    testonto.new_class("AnotherClass3", (testonto.AnotherClass,))
    testonto.new_object_property(
        "hasSubObjectProperty3", testonto.hasObjectProperty
    )
    testonto.new_data_property("hasSubDataProperty3", testonto.hasDataProperty)
    testonto.new_annotation_property(
        "hasSubAnnotationProperty3", testonto.hasAnnotationProperty
    )
