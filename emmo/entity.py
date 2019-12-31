# -*- coding: utf-8 -*-
"""This module injects some additional methods into owlready2.ThingClass."""
from owlready2 import ThingClass, PropertyClass, Thing


def _dir(self):
    """Extend in dir() listing of ontology classes."""
    s = set(object.__dir__(self))
    props = self.__class__.namespace.world._props.keys()
    s.update(props)
    #s.update('INDIRECT_' + p for p in props)
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


# Inject methods to ThingClass
setattr(ThingClass, '__dir__', _dir)
setattr(ThingClass, 'get_annotations', get_class_annotations)
setattr(PropertyClass, 'get_annotations', get_property_annotations)
type.__setattr__(Thing, 'get_individual_annotations', get_individual_annotations)
