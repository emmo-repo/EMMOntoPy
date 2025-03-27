"""This module injects some additional methods into owlready2 classes."""

# pylint: disable=protected-access
import types
from typing import TYPE_CHECKING

import owlready2
from owlready2 import AnnotationPropertyClass, ThingClass, PropertyClass
from owlready2 import Metadata, Thing, Restriction, Namespace

# pylint: disable=wrong-import-order
from ontopy.utils import (  # pylint: disable=cyclic-import
    EMMOntoPyException,
    NoSuchLabelError,
)
from ontopy.ontology import (  # pylint: disable=cyclic-import
    Ontology as OntopyOntology,
)

if TYPE_CHECKING:
    from typing import Any, Generator, Tuple


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

# Save a copy of the unpatched ThingClass.__getattr__() method.
save_getattr = ThingClass.__getattr__


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
    """Extend dir() listing of ontology classes."""
    set_dir = set(object.__dir__(self))
    props = [str(key) for key in self.namespace.world._props.keys()]
    set_dir.update(props)
    return sorted(set_dir)


def _getitem(self, name):
    """Provide item access to annotation properties."""
    prop = self.namespace.ontology.get_by_label(name)
    if isinstance(prop, AnnotationPropertyClass):
        return getattr(self, name)
    raise KeyError(f"no such annotation property: {name}")


def _setitem(self, name, value):
    """Provide item asignment for annotation properties.

    Note, this appends `value` to the property instead of replacing the
    property.  This is consistent with Owlready2, but may be little
    unintuitive.

    Example:
    >>> from emmopy import get_emmo
    >>> from owlready2 import locstr
    >>> emmo = get_emmo()
    >>> emmo.Atom['altLabel']
    [locstr('ChemicalElement', 'en')]
    >>> emmo.Atom['altLabel'] = 'Element'
    >>> emmo.Atom['altLabel'] = locstr('Atomo', 'it')
    >>> emmo.Atom['altLabel']
    [locstr('ChemicalElement', 'en'), 'Element', locstr('Atomo', 'it')]
    """

    item = _getitem(self, name)
    item.append(value)


def _delitem(self, name):
    """Provide item deletion for annotation properties.

    Note, this simply clears the named property.
    """
    item = _getitem(self, name)
    item.clear()


def _getattr(self, name):
    """Provide attribute access to annotation properties.

    This upates __getattr__ in owlready2. If name is not found as
    attribute it tries using the iriname of the annotation property.
    """
    try:
        return save_getattr(self, name)
    except AttributeError as err:
        # make sure we are using and ontopy Ontology which has get_by_label
        if isinstance(self.namespace.ontology, OntopyOntology):
            entity = self.namespace.ontology.get_by_label(name)
            # add annotation property to world._props for faster access later
            self.namespace.world._props[name] = entity

            # Try first unpatched getattr method to avoid risking
            # infinite recursion.
            try:
                return save_getattr(self, entity.name)
            except AttributeError:
                return getattr(self, entity.name)
        raise err


def get_annotations(
    self, all=False, imported=True
):  # pylint: disable=redefined-builtin
    """Returns a dict with non-empty annotations.

    If `all` is `True`, also annotations with no value are included.

    If `imported` is `True`, also include annotations defined in imported
    ontologies.
    """
    onto = self.namespace.ontology

    def extend(key, values):
        """Extend annotations with a sequence of values."""
        if key in annotations:
            annotations[key].extend(values)
        else:
            annotations[key] = values

    annotations = {
        str(get_preferred_label(a)): a._get_values_for_class(self)
        for a in onto.annotation_properties(imported=imported)
    }
    extend("comment", self.comment)
    extend("label", self.label)
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
        yield from disjoint_set
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
        for attr in "is_a", "equivalent_to":
            if hasattr(entity, attr):
                lst = getattr(entity, attr)
                if skip_classes:
                    subclass_relations.update(
                        r
                        for r in lst
                        if not isinstance(r, owlready2.ThingClass)
                    )
                else:
                    subclass_relations.update(lst)

    subclass_relations.update(self.is_a)
    return subclass_relations


is_defined = property(
    fget=lambda self: (
        hasattr(self, "equivalent_to") and bool(self.equivalent_to)
    ),
    doc="""Is true if this class is a defined class.

    For a "defined class" both necessary and sufficient conditions for
    membership in that class are given.  Hence, classes declared with
    `owl:equivalentTo` are defined classes.

    Note that this method is different from the `defined_class`
    property provided by Owlready2, who's boolean value is set by the
    user.
    """,
)


# Inject methods into ThingClass
setattr(ThingClass, "__dir__", _dir)
setattr(ThingClass, "__getitem__", _getitem)
setattr(ThingClass, "__setitem__", _setitem)
setattr(ThingClass, "__delitem__", _delitem)
setattr(ThingClass, "__getattr__", _getattr)
setattr(ThingClass, "get_preferred_label", get_preferred_label)
setattr(ThingClass, "get_parents", get_parents)
setattr(ThingClass, "get_annotations", get_annotations)
setattr(ThingClass, "disjoint_with", disjoint_with)
setattr(ThingClass, "get_indirect_is_a", get_indirect_is_a)
setattr(ThingClass, "is_defined", is_defined)


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
def keys(self) -> "Generator[str, None, None]":
    """Return a generator over annotation property names associated
    with this ontology, i.e. metadata keys."""

    namespace = self.namespace
    predicates = set(x[1] for x in namespace.get_triples(s=self.storid))
    for pred in predicates:
        try:
            pred = namespace[namespace._unabbreviate(pred)].iri
        except NoSuchLabelError:
            pred = namespace._unabbreviate(pred)

        yield pred


def items(self) -> "Generator[Tuple[str, Any], None, None]":
    """Return a dict of annotation properties as (name, value_list)
    pairs associated with this ontology, i.e. the metadata."""
    namespace = self.namespace

    for key in self.keys():
        triples = namespace._get_triples_spod_spod(
            s=self.storid, p=namespace._abbreviate(key), o=None
        )

        obj = []
        for triple in triples:
            if isinstance(triple[2], str):
                obj.append(triple[2])
            else:
                try:
                    obj.append(namespace[namespace._unabbreviate(triple[2])])
                except NoSuchLabelError:
                    obj.append(namespace._unabbreviate(triple[2]))
        yield key, obj


def has(self, name) -> bool:
    """Returns true if name"""
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
    s = "\n  ".join(
        f"{k!r}: {v!r}"
        for k, v in self.items()
        if k != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    )
    return f"Metadata(\n  {s}\n)"


def _getname(iri):
    label_startpos = iri.rfind("#") if iri.rfind("#") != -1 else iri.rfind("/")
    return iri[label_startpos + 1 :] if label_startpos != -1 else iri


def __metadata_getattr__(self, attr):
    try:
        return metadata__getattr__save(self, attr)
    except AttributeError:
        if attr in self.keys():
            return dict(self.items())[attr]
        d = {_getname(key): val for key, val in self.items()}
        return d[attr]


metadata__setattr__save = Metadata.__setattr__
metadata__getattr__save = Metadata.__getattr__
setattr(Metadata, "keys", keys)
setattr(Metadata, "items", items)
setattr(Metadata, "has", has)
setattr(Metadata, "__contains__", __contains__)
setattr(Metadata, "__iter__", __iter__)
setattr(Metadata, "__setattr__", __setattr__)
setattr(Metadata, "__repr__", __repr__)
setattr(Metadata, "__getattr__", __metadata_getattr__)
Metadata.__getitem__ = Metadata.__getattr__
Metadata.__setitem__ = Metadata.__setattr__
