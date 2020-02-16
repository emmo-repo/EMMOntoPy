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
def _get_parents(self):
    """Returns a list of all parents (in case of multiple inheritance)."""
    return [cls for cls in self.is_a if isinstance(cls, owlready2.ThingClass)]


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
setattr(owlready2.ThingClass, 'get_parents', _get_parents)
setattr(ThingClass, '__dir__', _dir)
setattr(ThingClass, 'get_annotations', get_class_annotations)
setattr(PropertyClass, 'get_annotations', get_property_annotations)
type.__setattr__(Thing, 'get_individual_annotations',
                 get_individual_annotations)
