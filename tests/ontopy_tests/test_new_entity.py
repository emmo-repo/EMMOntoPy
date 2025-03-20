from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
    from pathlib import Path


def test_new_entity(testonto: "Ontology") -> None:
    """Test adding entities to ontology"""
    from ontopy.utils import (
        NoSuchLabelError,
        LabelDefinitionError,
        EntityClassDefinitionError,
    )
    from owlready2.entity import ThingClass
    from owlready2.prop import ObjectPropertyClass, DataPropertyClass
    from owlready2 import AnnotationPropertyClass

    # Add entity directly
    testonto.new_entity("FantasyClass", testonto.TestClass)

    # Test that new entity is found by both version of get_by_label
    assert testonto.get_by_label("FantasyClass") == testonto.FantasyClass
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
        "YetAnotherClass",
        testonto.TestClass,
        entitytype=ThingClass,
        preflabel="YetAnotherClass",
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

    assert (
        testonto.AnotherClass3.iri == "http://emmo.info/testonto#AnotherClass3"
    )
    testonto.new_object_property(
        "hasSubObjectProperty3", testonto.hasObjectProperty
    )

    assert (
        testonto.hasSubObjectProperty3.iri
        == "http://emmo.info/testonto#hasSubObjectProperty3"
    )
    testonto.new_data_property("hasSubDataProperty3", testonto.hasDataProperty)
    assert (
        testonto.hasSubDataProperty3.iri
        == "http://emmo.info/testonto#hasSubDataProperty3"
    )
    testonto.new_annotation_property(
        "hasSubAnnotationProperty3", testonto.hasAnnotationProperty
    )
    assert (
        testonto.hasSubAnnotationProperty3.iri
        == "http://emmo.info/testonto#hasSubAnnotationProperty3"
    )


def test_new_entity_w_preflabel() -> None:
    """Test adding entities to ontology"""
    from ontopy import get_ontology
    import owlready2

    testonto2 = get_ontology("http://domain_ontology/new_ontology")
    testonto2.new_entity(
        "NewClass",
        owlready2.Thing,
        preflabel="NewClass",
    )

    assert testonto2.NewClass.prefLabel.en == ["NewClass"]


def test_new_entity_w_iri(testonto: "Ontology") -> None:
    """Test adding entities to ontology"""
    from ontopy import get_ontology
    import owlready2

    testonto.new_entity(
        "NewClass", owlready2.Thing, iri="http://different_ontology#NewClass"
    )

    assert testonto.NewClass.iri == "http://different_ontology#NewClass"

    testonto.new_class(
        "AnotherClass",
        (testonto.NewClass,),
        iri="http://different_ontology#AnotherClass",
    )

    assert testonto.AnotherClass.iri == "http://different_ontology#AnotherClass"

    testonto.new_object_property(
        "hasSubObjectProperty",
        testonto.hasObjectProperty,
        iri="http://different_ontology#hasSubObjectProperty",
    )

    assert (
        testonto.hasSubObjectProperty.iri
        == "http://different_ontology#hasSubObjectProperty"
    )

    testonto.new_data_property(
        "hasSubDataProperty",
        testonto.hasDataProperty,
        iri="http://different_ontology#hasSubDataProperty",
    )

    assert (
        testonto.hasSubDataProperty.iri
        == "http://different_ontology#hasSubDataProperty"
    )

    testonto.new_annotation_property(
        "hasSubAnnotationProperty",
        testonto.hasAnnotationProperty,
        iri="http://different_ontology#hasSubAnnotationProperty",
    )

    assert (
        testonto.hasSubAnnotationProperty.iri
        == "http://different_ontology#hasSubAnnotationProperty"
    )
