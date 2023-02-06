#!/usr/bin/env python3
"""Module for representing an EMMO-based ontology, as a collection of DLite
metadata entities.

Entities in the ontology are mapped to DLite as follows:
  - owl class (except EMMO property, see below) -> metadata entities
  - owl `hasProperty` restrictions are interpreted. The "object" entity of the
    relation is added as a SOFT property to the "subject" entity.
  - all other owl restriction -> entity + relation(s)
  - owl object property -> relations
  - owl class construct -> entity + relation(s)

TODO:
  - map restriction cardinality to collection diminsions
"""
# pylint: disable=import-error
import re

import dlite
from dlite import Instance, Dimension, Property

from ontopy import get_ontology
from ontopy.utils import asstring, get_label

import owlready2  # pylint: disable=wrong-import-order


class EMMO2Meta:
    """A class for representing EMMO or an EMMO-based ontology as a
    collection of metadata entities using DLite.

    Parameters
    ----------
    ontology : string
        URI or path to the ontology to represent.  Defaults to EMMO.
    classes : sequence
        The classes to include.  May be given either as a sequence of
        strings or a sequence of owlready2 classes.  The default is to
        include all of the ontology.
    version : string
        Default version for classes lacking a `version` annotation.
    collid : string
        Set an explicit id to the generated collection.

    Notes
    -----
    The collection UUID is accessable via the `coll.uuid` attribute.
    Use the `collid` argument to provide a human readable id to make
    it easier to later retrieve it from a storage (without having
    to remember its UUID).
    """

    def __init__(self, ontology=None, classes=None, version="0.1", collid=None):
        if ontology is None:
            self.onto = get_ontology()
            self.onto.load()
        elif isinstance(ontology, str):
            self.onto = get_ontology(ontology)
            self.onto.load()
        else:
            self.onto = ontology
        self.version = version
        self.iri = self.onto.base_iri
        self.namespace = self.onto.base_iri.rstrip("#")
        self.coll = dlite.Collection(collid)

        if classes is None:
            classes = self.onto.classes()
        elif isinstance(classes, str):
            classes = [classes]

        for cls in classes:
            self.add_class(cls)

    def get_subclasses(self, cls):
        """Returns a generator yielding all subclasses of owl class `cls`."""
        yield cls
        for subcls in cls.subclasses():
            yield from self.get_subclasses(subcls)

    def get_uri(self, name, version=None):
        """Returns uri (namespace/version/name)."""
        if version is None:
            version = self.version
        return f"{self.namespace}/{version}/{name}"

    @staticmethod
    def get_uuid(uri=None):
        """Returns a UUID corresponding to `uri`.

        If `uri` is None, a random UUID is returned.
        """
        return dlite.get_uuid(uri)

    @staticmethod
    def get_label(entity):
        """Returns a label for entity."""
        if hasattr(entity, "label"):
            return get_label(entity)
        name = repr(entity)
        label, _ = re.subn(r"emmo(-[a-z]+)?\.", "", name)
        return label

    def find_label(self, inst):
        """Returns label for class instance `inst` already added to the
        collection."""
        if hasattr(inst, "uuid"):
            uuid = inst.uuid
        else:
            uuid = dlite.get_uuid(inst)
        rel = self.coll.find_first(p="_has-uuid", o=uuid)
        if not rel:
            raise ValueError(f"no class instance with UUID: {uuid}")
        return rel.s

    def add(self, entity):
        """Adds owl entity to collection and returns a reference to the
        new metadata."""
        # if isinstance(entity, str):
        #    entity = self.onto[entity]

        if entity == owlready2.Thing:
            raise ValueError(f"invalid entity: {entity}")

        if isinstance(entity, owlready2.ThingClass):
            return self.add_class(entity)

        if isinstance(entity, owlready2.ClassConstruct):
            return self.add_class_construct(entity)

        raise ValueError(
            f'invalid entity "{entity}" of class {entity.__class__}'
        )

    def add_class(self, cls):
        """Adds owl class `cls` to collection and returns a reference to
        the new metadata."""
        if isinstance(cls, str):
            cls = self.onto[cls]
        label = get_label(cls)
        if not self.coll.has(label):
            uri = self.get_uri(label)
            dims, props = self.get_properties(cls)
            entity = Instance.create_metadata(
                uri, dims, props, self.get_description(cls)
            )
            self.coll.add(label, entity)
            for relation in cls.is_a:
                if relation is owlready2.Thing:
                    pass
                elif isinstance(relation, owlready2.ThingClass):
                    self.coll.add_relation(label, "is_a", get_label(relation))
                    self.add_class(relation)
                elif isinstance(relation, owlready2.Restriction):
                    # Correct this test if EMMO reintroduce isPropertyOf
                    if (
                        isinstance(relation.value, owlready2.ThingClass)
                        and isinstance(relation.value, self.onto.Property)
                        and issubclass(relation.property, self.onto.hasProperty)
                    ):
                        self.add_class(relation.value)
                    else:
                        self.add_restriction(relation)
                elif isinstance(relation, owlready2.ClassConstruct):
                    self.add_class_construct(relation)
                else:
                    raise TypeError(f"Unexpected is_a member: {type(relation)}")
        return self.coll.get(label)

    def get_properties(self, cls):  # pylint: disable=too-many-locals
        """Returns two lists with the dlite dimensions and properties
        correspinding to owl class `cls`."""
        dims = []
        props = []
        dimindices = {}
        propnames = set()
        types = {"Integer": "int", "Real": "double", "String": "string"}

        def get_dim(restriction, name, descr=None):
            """Returns dimension index corresponding to dimension name `name`
            for property `restriction.value`."""
            # pylint: disable=protected-access
            result = []
            restriction_type = (
                owlready2.class_construct._restriction_type_2_label[
                    restriction.type
                ]
            )
            if restriction_type in ("some", "only", "min") or (
                restriction_type in ("max", "exactly")
                and restriction.cardinality > 1
            ):
                if name not in dimindices:
                    dimindices[name] = len(dims)
                    dims.append(Dimension(name, descr))
                result = [dimindices[name]]
            return result

        for onto_class in cls.mro():  # pylint: disable=too-many-nested-blocks
            if not isinstance(onto_class, owlready2.ThingClass):
                continue
            for relation in onto_class.is_a:
                # Note that EMMO currently does not define an inverse for
                # hasProperty. If we reintroduce that, we should replace
                #
                #     not isinstance(relation.property, Inverse) and
                #     issubclass(relation.property, self.onto.hasProperty)
                #
                # with
                #
                #     ((isinstance(relation.property, Inverse) and
                #       issubclass(
                #          Inverse(relation.property), onto.isPropertyFor)
                #       ) or
                #      issubclass(relation.property, self.onto.hasProperty))
                #
                if (
                    isinstance(relation, owlready2.Restriction)
                    and not isinstance(relation.property, owlready2.Inverse)
                    and issubclass(relation.property, self.onto.hasProperty)
                    and isinstance(relation.value, owlready2.ThingClass)
                    and isinstance(relation.value, self.onto.Property)
                ):
                    name = self.get_label(relation.value)
                    if name in propnames:
                        continue
                    propnames.add(name)

                    # Default type, ndims and unit
                    if isinstance(
                        relation.value,
                        (
                            self.onto.DescriptiveProperty,
                            self.onto.QualitativeProperty,
                            self.onto.SubjectiveProperty,
                        ),
                    ):
                        ptype = "string"
                    else:
                        ptype = "double"
                    dimensions = []
                    dimensions.extend(
                        get_dim(relation, f"n_{name}s", f"Number of {name}.")
                    )
                    unit = None

                    # Update type, ndims and unit from relations
                    for relation_two in [relation] + relation.value.is_a:
                        if isinstance(relation_two, owlready2.Restriction):
                            if issubclass(
                                relation_two.property, self.onto.hasType
                            ):
                                typelabel = self.get_label(relation_two.value)
                                ptype = types[typelabel]
                                dimensions.extend(
                                    get_dim(
                                        relation_two,
                                        f"{name}_length",
                                        f"Length of {name}",
                                    )
                                )
                            elif issubclass(
                                relation_two.property, self.onto.hasUnit
                            ):
                                unit = self.get_label(relation_two.value)

                    descr = self.get_description(relation.value)
                    props.append(
                        Property(
                            name,
                            type=ptype,
                            dims=dimensions,
                            unit=unit,
                            description=descr,
                        )
                    )
        return dims, props

    def add_restriction(self, restriction):
        """Adds owl restriction to collection and returns a reference to it."""
        restriction_type = owlready2.class_construct._restriction_type_2_label[  # pylint: disable=protected-access
            restriction.type
        ]
        cardinality = restriction.cardinality if restriction.cardinality else 0
        entity = self.add_restriction_entity()
        inst = entity()
        inst.type = restriction_type
        inst.cardinality = cardinality
        label = inst.uuid
        vlabel = self.get_label(restriction.value)
        self.coll.add(label, inst)
        self.coll.add_relation(label, asstring(restriction.property), vlabel)
        print()
        print(f"*** {restriction=}")
        print(f"*** {restriction.type=}")
        print(f"*** {restriction.value=}")
        print(f"*** {label=}")
        print(f"*** {vlabel=}")
        if not self.coll.has(vlabel):
            self.add(restriction.value)
        return inst

    def add_restriction_entity(self):
        """Adds restriction metadata to collection and returns a reference
        to it."""
        uri = self.get_uri("Restriction")
        if not self.coll.has("Restriction"):
            props = [
                Property(
                    "type",
                    type="string",
                    description=(
                        "Type of restriction. Valid values for `type` are: "
                        '"only", "some", "exact", "min" and "max".'
                    ),
                ),
                Property(
                    "cardinality",
                    type="int",
                    description=(
                        'The cardinality. Unused for "only" and "some" '
                        "restrictions."
                    ),
                ),
            ]
            entity = Instance.create_metadata(
                uri,
                [],
                props,
                "Class restriction.  For each instance of a class "
                "restriction there should be a relation\n"
                "\n"
                "    (r.label, r.property, r.value.label)\n"
                "\n"
                "where `r.label` is the label associated with the "
                "restriction, `r.property` is a relation and "
                "`r.value.label` is the label of the value of the "
                "restriction.",
            )
            self.coll.add("Restriction", entity)
        return self.coll.get("Restriction")

    def add_class_construct(self, construct):
        """Adds owl class construct to collection and returns a reference to
        it."""
        ctype = construct.__class__.__name__
        entity = self.add_class_construct_entity()
        inst = entity()
        label = inst.uuid
        inst.type = ctype
        if isinstance(construct, owlready2.LogicalClassConstruct):
            args = construct.Classes
        else:
            args = [construct.Class]
        for arg in args:
            self.coll.add_relation(label, "has_argument", self.get_label(arg))
        self.coll.add(label, inst)
        return inst

    def add_class_construct_entity(self):
        """Adds class construct metadata to collection and returns a reference
        to it."""
        uri = self.get_uri("ClassConstruct")
        if not self.coll.has("ClassConstruct"):
            props = [
                Property(
                    "type",
                    type="string",
                    description=(
                        "Type of class construct. Valid values for `type` are:"
                        ' "not", "inverse", "and" or "or".'
                    ),
                ),
            ]
            entity = Instance(
                uri,
                [],
                props,
                "Class construct.  For each instance of a class "
                "construct there should be one or more relations "
                "of type\n"
                "\n"
                '    (c.label, "has_argument", c.value.label)\n'
                "\n"
                "where `c.label` is the label associated with the "
                "class construct, `c.value.label` is the label of "
                "an argument.",
            )
            self.coll.add("ClassConstruct", entity)
        return self.coll.get("ClassConstruct")

    def get_description(self, cls):
        """Returns description for OWL class `cls` by combining its
        annotations."""
        if isinstance(cls, str):
            cls = onto[cls]
        descr = []
        annotations = self.onto.get_annotations(cls)
        if "definition" in annotations:
            descr.extend(annotations["definition"])
        if "elucication" in annotations and annotations["elucidation"]:
            for _ in annotations["elucidation"]:
                descr.extend(["", "ELUCIDATION:", _])
        if "axiom" in annotations and annotations["axiom"]:
            for _ in annotations["axiom"]:
                descr.extend(["", "AXIOM:", _])
        if "comment" in annotations and annotations["comment"]:
            for _ in annotations["comment"]:
                descr.extend(["", "COMMENT:", _])
        if "example" in annotations and annotations["example"]:
            for _ in annotations["example"]:
                descr.extend(["", "EXAMPLE:", _])
        return "\n".join(descr).strip()

    def save(self, *args, **kw):
        """Saves collection to storage."""
        self.coll.save(*args, **kw)


def main():
    """Main run function."""
    emmo = EMMO2Meta()
    emmo.save("json", "emmo2meta.json", "mode=w")
    return emmo


if __name__ == "__main__":
    emmo_representative = main()
    coll = emmo_representative.coll
    onto = emmo_representative.onto
