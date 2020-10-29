# -*- coding: utf-8 -*-
"""This module injects some additional methods into owlready2 classes."""
from types import MethodType

import owlready2
from owlready2 import ThingClass, PropertyClass, Thing, Restriction


# Improve default rendering of entities
def render_func(entity):
    if hasattr(entity, 'prefLabel') and entity.prefLabel:
        name = entity.prefLabel[0]
    elif hasattr(entity, 'label') and entity.label:
        name = entity.label[0]
    elif hasattr(entity, 'altLabel') and entity.altLabel:
        name = entity.altLabel[0]
    else:
        name = entity.name
    return "%s.%s" % (entity.namespace.name, name)


owlready2.set_render_func(render_func)



#
# Extending ThingClass (classes)
#
def get_preferred_label(self):
    """Returns the preferred label as a string (not list).

    The following heuristics is used:
      - if prefLabel annotation property exists, returns the first prefLabel
      - if label annotation property exists, returns the first label
      - otherwise return the name
    """
    if hasattr(self, 'prefLabel') and self.prefLabel:
        return self.prefLabel[0]
    elif hasattr(self, 'label') and self.label:
        return self.label.first()
    else:
        return self.name


def get_parents(self, strict=False):
    """Returns a list of all parents.  If `strict` is true, parents that are
    parents of other parents are excluded."""
    if strict:
        s = self.get_parents()
        for e in s.copy():
            s.difference_update(e.ancestors(include_self=False))
        return s
    elif isinstance(self, ThingClass):
        return {cls for cls in self.is_a
                if isinstance(cls, ThingClass)}
    elif isinstance(self, owlready2.ObjectPropertyClass):
        return {cls for cls in self.is_a
                if isinstance(cls, owlready2.ObjectPropertyClass)}
    else:
        assert 0


def _dir(self):
    """Extend in dir() listing of ontology classes."""
    s = set(object.__dir__(self))
    props = self.namespace.world._props.keys()
    s.update(props)
    return sorted(s)


def get_class_annotations(self, all=False, imported=True):
    """Returns a dict with non-empty annotations.

    If `all` is true, also annotations with no value are included.

    If `imported` is true, also include annotations defined in
    imported ontologies.
    """
    onto = self.namespace.ontology
    d = {get_preferred_label(a): a._get_values_for_class(self)
         for a in onto.annotation_properties(imported=imported)}
    if all:
        return d
    else:
        return {k: v for k, v in d.items() if v}


def disjoint_with(self, reduce=False):
    """Returns a generator with all classes that are disjoint with `self`.
    If `reduce` is true, all classes that are a descendant of another class
    will be excluded."""
    if reduce:
        s = set(self.disjoint_with())
        for e in s.copy():
            s.difference_update(e.descendants(include_self=False))
        for e in s:
            yield e
    else:
        for d in self.disjoints():
            for e in d.entities:
                if e is not self:
                    yield e


def get_indirect_is_a(self, skip_classes=True):
    """Returns the set of all isSubclassOf relations of self and its
    ancestors.  If `skip_classes` is true, indirect classes are not
    included in the returned set.
    """
    s = set()
    for e in reversed(self.mro()):
        if hasattr(e, 'is_a'):
            if skip_classes:
                s.update(r for r in e.is_a
                         if not isinstance(r, owlready2.ThingClass))
            else:
                s.update(e.is_a)
    s.update(self.is_a)
    return s


#
# Extending PropertyClass (properties)
#
def get_property_annotations(self, all=False, imported=True):
    """Returns a dict with non-empty property annotations.

    If `all` is true, also annotations with no value are included.

    If `imported` is true, also include annotations defined in
    imported ontologies.
    """
    onto = self.namespace.ontology
    d = {get_preferred_label(a): a._get_values_for_class(self)
         for a in onto.annotation_properties(imported=imported)}
    if all:
        return d
    else:
        return {k: v for k, v in d.items() if v}


#
# Extending Thing (individuals)
#
def get_individual_annotations(self, all=False, imported=True):
    """Returns a dict with non-empty individual annotations.

    If `all` is true, also annotations with no value are included.

    If `imported` is true, also include annotations defined in
    imported ontologies.
    """
    onto = self.namespace.ontology
    d = {get_preferred_label(a): a._get_values_for_individual(self)
         for a in onto.annotation_properties(imported=imported)}
    if all:
        return d
    else:
        return {k: v for k, v in d.items() if v}


#
# Extending Restruction
#
def get_typename(self):
    return owlready2.class_construct._restriction_type_2_label[self.type]


# Inject methods into Owlready2 classes
setattr(ThingClass, '__dir__', _dir)
setattr(ThingClass, 'get_preferred_label', get_preferred_label)
setattr(ThingClass, 'get_parents', get_parents)
setattr(ThingClass, 'get_annotations', get_class_annotations)
setattr(ThingClass, 'disjoint_with', disjoint_with)
setattr(ThingClass, 'get_indirect_is_a', get_indirect_is_a)

setattr(PropertyClass, 'get_preferred_label', get_preferred_label)
setattr(PropertyClass, 'get_parents', get_parents)
setattr(PropertyClass, 'get_annotations', get_property_annotations)

setattr(Restriction, 'get_typename', get_typename)

# Method names for individuals must be different from method names for classes
type.__setattr__(Thing, 'get_preflabel', get_preferred_label)
type.__setattr__(Thing, 'get_individual_annotations', get_individual_annotations)
