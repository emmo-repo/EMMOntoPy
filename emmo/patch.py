# -*- coding: utf-8 -*-
"""This module injects some additional methods into owlready2 classes."""
import owlready2
from owlready2 import ThingClass, PropertyClass, Thing


# Improve default rendering of entities
def render_func(entity):
    name = entity.label[0] if len(entity.label) == 1 else entity.name
    return "%s.%s" % (entity.namespace.name, name)


owlready2.set_render_func(render_func)


#
# Extending ThingClass (classes)
#
def _get_parents(self, strict=False):
    """Returns a list of all parents.  If `strict` is true, parents that are
    parents of other parents are excluded."""
    if strict:
        s = self.get_parents()
        for e in s.copy():
            s.difference_update(e.ancestors(include_self=False))
        return s
    elif isinstance(self, owlready2.ThingClass):
        return {cls for cls in self.is_a
                if isinstance(cls, owlready2.ThingClass)}
    elif isinstance(self, owlready2.ObjectPropertyClass):
        return {cls for cls in self.is_a
                if isinstance(cls, owlready2.ObjectPropertyClass)}
    else:
        assert 0


def _dir(self):
    """Extend in dir() listing of ontology classes."""
    s = set(object.__dir__(self))
    props = self.__class__.namespace.world._props.keys()
    s.update(props)
    return sorted(s)


def get_class_annotations(self, all=False):
    """Returns a dict with non-empty annotations.

    If `all` is true, also annotations with no value are included."""
    onto = self.namespace.ontology
    d = {a.label.first(): a._get_values_for_class(self)
         for a in onto.annotation_properties()}
    d.update({k: v._get_values_for_class(self)
              for k, v in self.__class__.namespace.world._props.items()})
    if all:
        return d
    else:
        return {k: v for k, v in d.items() if v and k != 'label'}


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


def get_indirect_is_a(self):
    """Returns the set of all isSubclassOf relations of self and its
    ancestors."""
    s = set()
    for e in self.mro():
        if hasattr(e, 'is_a'):
            s.update(e.is_a)
    return s


#
# Extending PropertyClass (properties)
#
def get_property_annotations(self, all=False):
    """Returns a dict with non-empty property annotations.

    If `all` is true, also annotations with no value are included."""
    onto = self.namespace.ontology
    d = {a.label.first(): a._get_values_for_class(self)
         for a in onto.annotation_properties()}
    d.update({k: v._get_values_for_class(self)
              for k, v in self.__class__.namespace.world._props.items()})
    if all:
        return d
    else:
        return {k: v for k, v in d.items() if v and k != 'label'}


#
# Extending Thing (individuals)
#
def get_individual_annotations(self, all=False):
    """Returns a dict with non-empty individual annotations.

    If `all` is true, also annotations with no value are included."""
    onto = self.namespace.ontology
    props = self.__class__.__class__.namespace.world._props
    d = {a.label.first(): a._get_values_for_class(self)
         for a in onto.annotation_properties()}
    d.update({k: v._get_values_for_individual(self)
              for k, v in props.items()})
    if all:
        return d
    else:
        return {k: v for k, v in d.items() if v and k != 'label'}


# Inject methods into Owlready2 classes
setattr(ThingClass, '__dir__', _dir)
setattr(ThingClass, 'get_parents', _get_parents)
setattr(ThingClass, 'get_annotations', get_class_annotations)
setattr(ThingClass, 'disjoint_with', disjoint_with)
setattr(ThingClass, 'get_indirect_is_a', get_indirect_is_a)
setattr(PropertyClass, 'get_parents', _get_parents)
setattr(PropertyClass, 'get_annotations', get_property_annotations)
type.__setattr__(Thing, 'get_individual_annotations',
                 get_individual_annotations)
