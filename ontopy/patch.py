"""This module injects some additional methods into owlready2 classes."""
# pylint: disable=protected-access
import types

import owlready2
from owlready2 import ThingClass, PropertyClass, Thing, Restriction, Namespace
from owlready2 import Metadata
from ontopy.utils import EMMOntoPyException


def render_func(entity):
    """Improve default rendering of entities."""
    if hasattr(entity, "prefLabel") and entity.prefLabel:
        name = entity.prefLabel[0]
    elif hasattr(entity, "label") and entity.label:
        name = entity.label[0]
    elif hasattr(entity, "altLabel") and entity.altLabel:
        name = entity.altLabel[0]
    else:
        name = entity.name
    return f"{entity.namespace.name}.{name}"


owlready2.set_render_func(render_func)


#
# Extending ThingClass (classes)
# ==============================
def get_preferred_label(self):
    """Returns the preferred label as a string (not list).

    The following heuristics is used:
      - if prefLabel annotation property exists, returns the first prefLabel
      - if label annotation property exists, returns the first label
      - otherwise return the name
    """
    if hasattr(self, "prefLabel") and self.prefLabel:
        return self.prefLabel[0]
    if hasattr(self, "label") and self.label:
        return self.label.first()
    return self.name


def get_parents(self, strict=False):
    """Returns a list of all parents.

    If `strict` is `True`, parents that are parents of other parents are
    excluded.
    """
    if strict:
        parents = self.get_parents()
        for entity in parents.copy():
            parents.difference_update(entity.ancestors(include_self=False))
        return parents
    if isinstance(self, ThingClass):
        return {cls for cls in self.is_a if isinstance(cls, ThingClass)}
    if isinstance(self, owlready2.ObjectPropertyClass):
        return {
            cls
            for cls in self.is_a
            if isinstance(cls, owlready2.ObjectPropertyClass)
        }
    raise EMMOntoPyException(
        "self has no parents - this should not be possible!"
    )


def _dir(self):
    """Extend in dir() listing of ontology classes."""
    set_dir = set(object.__dir__(self))
    props = self.namespace.world._props.keys()
    set_dir.update(props)
    return sorted(set_dir)


def get_annotations(
    self, all=False, imported=True
):  # pylint: disable=redefined-builtin
    """Returns a dict with non-empty annotations.

    If `all` is `True`, also annotations with no value are included.

    If `imported` is `True`, also include annotations defined in imported
    ontologies.
    """
    onto = self.namespace.ontology
    annotations = {
        get_preferred_label(_): _._get_values_for_class(self)
        for _ in onto.annotation_properties(imported=imported)
    }
    if all:
        return annotations
    return {key: value for key, value in annotations.items() if value}


def disjoint_with(self, reduce=False):
    """Returns a generator with all classes that are disjoint with `self`.

    If `reduce` is `True`, all classes that are a descendant of another class
    will be excluded.
    """
    if reduce:
        disjoint_set = set(self.disjoint_with())
        for entity in disjoint_set.copy():
            disjoint_set.difference_update(
                entity.descendants(include_self=False)
            )
        for entity in disjoint_set:
            yield entity
    else:
        for disjoint in self.disjoints():
            for entity in disjoint.entities:
                if entity is not self:
                    yield entity


def get_indirect_is_a(self, skip_classes=True):
    """Returns the set of all isSubclassOf relations of self and its ancestors.

    If `skip_classes` is `True`, indirect classes are not included in the
    returned set.
    """
    subclass_relations = set()
    for entity in reversed(self.mro()):
        if hasattr(entity, "is_a"):
            if skip_classes:
                subclass_relations.update(
                    _
                    for _ in entity.is_a
                    if not isinstance(_, owlready2.ThingClass)
                )
            else:
                subclass_relations.update(entity.is_a)
    subclass_relations.update(self.is_a)
    return subclass_relations


# Inject methods into ThingClass
setattr(ThingClass, "__dir__", _dir)
setattr(ThingClass, "get_preferred_label", get_preferred_label)
setattr(ThingClass, "get_parents", get_parents)
setattr(ThingClass, "get_annotations", get_annotations)
setattr(ThingClass, "disjoint_with", disjoint_with)
setattr(ThingClass, "get_indirect_is_a", get_indirect_is_a)


#
# Extending PropertyClass (properties)
# ====================================
setattr(PropertyClass, "get_preferred_label", get_preferred_label)
setattr(PropertyClass, "get_parents", get_parents)
setattr(PropertyClass, "get_annotations", get_annotations)


#
# Extending Thing (individuals)
# =============================
# Method names for individuals must be different from method names for classes
type.__setattr__(Thing, "get_preflabel", get_preferred_label)
type.__setattr__(Thing, "get_individual_annotations", get_annotations)


#
# Extending Restriction
# =====================
def get_typename(self):
    """Get restriction type label/name."""
    return owlready2.class_construct._restriction_type_2_label[self.type]


setattr(Restriction, "get_typename", get_typename)


#
# Extending Namespace
# ===================
orig_namespace_init = Namespace.__init__


def namespace_init(self, world_or_ontology, base_iri, name=None):
    """__init__ function for the `Namespace` class."""
    orig_namespace_init(self, world_or_ontology, base_iri, name)
    if self.name.endswith(".ttl"):
        self.name = self.name[:-4]


setattr(Namespace, "__init__", namespace_init)


#
# Extending Metadata
# ==================
def keys(self):
    """Return a generator over annotation property names associates
    with this ontology."""
    namespace = self.namespace
    for annotation in namespace.annotation_properties():
        if namespace._has_data_triple_spod(
            s=namespace.storid, p=annotation.storid
        ):
            yield annotation


def items(self):
    """Return a generator over annotation property (name, value_list)
    pairs associates with this ontology."""
    namespace = self.namespace
    for annotation in namespace.annotation_properties():
        if namespace._has_data_triple_spod(
            s=namespace.storid, p=annotation.storid
        ):
            yield annotation, getattr(self, annotation.name)


def has(self, name):
    """Returns true if `name`"""
    return name in set(self.keys())


def __contains__(self, name):
    return self.has(name)


def __iter__(self):
    return self.keys()


def __setattr__(self, attr, values):
    metadata__setattr__save(self, attr, values)
    # Make sure that __setattr__() also updates the triplestore
    lst = self.__dict__[attr]
    if lst:
        namespace = self.namespace
        annotation = {
            _.name: _ for _ in owlready2.AnnotationProperty.__subclasses__()
        }
        if attr in annotation:
            prop = annotation[attr]
        else:
            with namespace.ontology:
                prop = types.new_class(attr, (owlready2.AnnotationProperty,))
        onto, data = owlready2.to_literal(lst[0])
        namespace._set_data_triple_spod(
            namespace.storid, prop.storid, onto, data
        )
        for entity in lst[1:]:
            onto, data = owlready2.to_literal(entity)
            namespace._set_data_triple_spod(
                namespace.storid, prop.storid, onto, data
            )


def __repr__(self):
    result = ["Metadata("]
    for annotation, values in self.items():
        sep = f"\n{' ' * (len(annotation.name) + 4)}"
        result.append(
            f"  {annotation.name}=[{sep.join(repr(_) for _ in values)}],"
        )
    result.append(")")
    return "\n".join(result)


metadata__setattr__save = Metadata.__setattr__
setattr(Metadata, "keys", keys)
setattr(Metadata, "items", items)
setattr(Metadata, "has", has)
setattr(Metadata, "__contains__", __contains__)
setattr(Metadata, "__iter__", __iter__)
setattr(Metadata, "__setattr__", __setattr__)
setattr(Metadata, "__repr__", __repr__)
Metadata.__getitem__ = Metadata.__getattr__
Metadata.__setitem__ = Metadata.__setattr__
