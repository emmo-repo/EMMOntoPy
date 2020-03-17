# -*- coding: utf-8 -*-
"""A module adding additional functionality to owlready2. The main additions
includes:
  - Visualisation of taxonomy and ontology as graphs (using pydot, see
    ontograph.py).

The class extension is defined within.

If desirable some of this may be moved back into owlready2.
"""
import os
import itertools
import inspect
import warnings
from collections import defaultdict

import owlready2

from .utils import asstring
from .ontograph import OntoGraph  # FIXME: depricate...
from .owldir import owldir


class NoSuchLabelError(LookupError, AttributeError):
    """Error raised when a label cannot be found."""
    pass


# owl categories
categories = (
    'annotation_properties',
    'data_properties',
    'object_properties',
    'classes',
    'individuals',
)


def get_ontology(base_iri='emmo-inferred', verbose=False):
    """Returns a new Ontology from `base_iri`.

    If `verbose` is true, a lot of dianostics is written.
    """
    if base_iri in owlready2.default_world.ontologies:
        onto = owlready2.default_world.ontologies[base_iri]
    elif base_iri + '#' in owlready2.default_world.ontologies:
        onto = owlready2.default_world.ontologies[base_iri + '#']
    else:
        if os.path.exists(base_iri):
            iri = base_iri
        elif os.path.exists(base_iri + '.owl'):
            iri = base_iri + '.owl'
        elif os.path.exists(os.path.join(owldir, base_iri)):
            iri = os.path.join(owldir, base_iri)
        elif os.path.exists(os.path.join(owldir, base_iri + '.owl')):
            iri = os.path.join(owldir, base_iri + '.owl')
        else:
            iri = base_iri
        if iri[-1] not in '/#':
            iri += '#'
        onto = Ontology(owlready2.default_world, iri)
    onto._verbose = verbose
    return onto


class Ontology(owlready2.Ontology, OntoGraph):
    """A generic class extending owlready2.Ontology.
    """
    def __getitem__(self, name):
        return self.__getattr__(name)

    def __getattr__(self, name):
        attr = super().__getattr__(name)
        if not attr:
            attr = self.get_by_label(name)
        return attr

    def __dir__(self):
        """Extend in dir() listing."""
        s = set(object.__dir__(self))
        for onto in [get_ontology(uri) for uri in self._namespaces.keys()]:
            s.update([cls.label.first() for cls in onto.classes()])
            s.update([cls.label.first() for cls in onto.individuals()])
            s.update([cls.label.first() for cls in onto.properties()])
            s.update([cls.name for cls in onto.classes()])
            s.update([cls.name for cls in onto.individuals()])
            s.update([cls.name for cls in onto.properties()])
            s.difference_update({None})  # get rid of possible None
        return sorted(s)

    def __contains__(self, other):
        try:
            self[other]
            return True
        except NoSuchLabelError:
            return False

    def __objclass__(self):
        # Play nice with inspect...
        pass

    def get_root_classes(self):
        """Returns a list or root classes."""
        return [cls for cls in self.classes()
                if not cls.ancestors().difference(set([cls, owlready2.Thing]))]

    def get_root_object_properties(self):
        """Returns a list of root object properties."""
        props = set(self.object_properties())
        return [p for p in props if not props.intersection(p.is_a)]

    def get_root_data_properties(self):
        """Returns a list of root object properties."""
        props = set(self.data_properties())
        return [p for p in props if not props.intersection(p.is_a)]

    def get_roots(self):
        """Returns all class, object_property and data_property roots."""
        roots = self.get_root_classes()
        roots.extend(self.get_root_object_properties())
        roots.extend(self.get_root_data_properties())
        return roots

    def get_by_label(self, label):
        """Returns entity by label.

        If several entities have the same label, only the one which is
        found first is returned.  A KeyError is raised if `label`
        cannot be found.
        """
        # Check for name in all categories in self
        for category in categories:
            method = getattr(self, category)
            for entity in method():
                if label in entity.label:
                    return entity
        # Check for special names
        d = {
                'Nothing': owlready2.Nothing,
        }
        if label in d:
            return d[label]
        # Check whether `label` matches a Python class name of any category
        lst = [cls for cls in itertools.chain.from_iterable(
            getattr(self, category)() for category in categories)
             if hasattr(cls, '__name__') and cls.__name__ == label]
        if len(lst) == 1:
            return lst[0]
        elif len(lst) > 1:
            raise NoSuchLabelError('There is more than one Python class with '
                                   'name %r' % label)
        elif label is owlready2.Thing or label == 'Thing':
            return owlready2.Thing
        # Check imported ontologies
        for onto in self.imported_ontologies:
            onto.__class__ = self.__class__  # magically change type of onto
            try:
                return onto.get_by_label(label)
            except NoSuchLabelError:
                pass
        # Fallback to check whether we have a class in the current or any
        # of the imported ontologies whos name matches `label`
        for onto in [self] + self.imported_ontologies:
            lst = [cls for cls in onto.classes() if cls.__name__ == label]
            if len(lst) == 1:
                return lst[0]
            elif len(lst) > 1:
                raise NoSuchLabelError('There is more than one class with '
                                       'name %r' % label)
        # Label cannot be found
        raise NoSuchLabelError('Ontology "%s" has no such label: %s' % (
            self.name, label))

    def get_by_label_all(self, label):
        """Like get_by_label(), but returns a list of all entities with
        matching labels.
        """
        return [entity for entity in
                itertools.chain.from_iterable(
                    getattr(self, c)() for c in categories)
                if hasattr(entity, 'label') and label in entity.label]

    def sync_reasoner(self, reasoner='HermiT', include_imported=False):
        """Update current ontology by running the given reasoner.

        Supported values for `reasoner` are 'Pellet' and 'HermiT'.

        If `include_imported` is true, the reasoner will also reason
        over imported ontologies.  Note that this may be **very** with
        the current supported reasoners (FaCT++ seems must faster).
        """
        def run(*args):
            if reasoner == 'Pellet':
                owlready2.sync_reasoner_pellet(*args)
            elif reasoner == 'HermiT':
                owlready2.sync_reasoner(*args)
            else:
                raise ValueError('unknown reasoner %r.  Supported reasoners'
                                 'are "Pellet" and "HermiT".', reasoner)
        if include_imported:
            with self:
                run()
        else:
            run([self])

    def sync_attributes(self, sync_imported=False):
        """Call method is intended to be called after you have added new
        classes (typically via Python).

        If a class, object property or individual in the current
        ontology has no label, the name of the corresponding Python class
        will be assigned as label.

        If a class, object property or individual has no comment, it will
        be assigned the docstring of the corresponding Python class.

        If `sync_imported` is true, all imported ontologies are also
        updated.
        """
        for cls in itertools.chain(self.classes(), self.object_properties()):
                                    # self.individuals()):
            if not cls.label:
                cls.label.append(cls.__name__)
            if not cls.comment and cls.__doc__:
                cls.comment.append(inspect.cleandoc(cls.__doc__))
        if sync_imported:
            for onto in self.imported_ontologies:
                onto.sync_attributes()
        # FIXME - optionally, consider to also update the class names.
        # Possible options could be:
        #   - do not change names (defalt)
        #   - set name to ``prefix + "_" + uuid`` where `prefix` is any
        #     string (e.g. "EMMO") and `uuid` is an uuid.  This is the
        #     default for EMMO.
        #   - set names to the name of the corresponding Python class
        #   - set names equal to labels

    def get_relations(self):
        """Returns a generator for all relations."""
        return self.object_properties()

    def get_annotations(self, entity):
        """Returns a dict with annotations for `entity`.  Entity may be given
        either as a ThingClass object or as a label."""
        warnings.warn('Ontology.get_annotations(cls) is deprecated.  '
                      'Use cls.get_annotations() instead.', DeprecationWarning)

        if isinstance(entity, str):
            entity = self.get_by_label(entity)
        d = {'comment': getattr(entity, 'comment', '')}
        for a in self.annotation_properties():
            d[a.label.first()] = [
                o.strip('"') for s, p, o in
                self.get_triples(entity.storid, a.storid, None)]
        return d

    def get_branch(self, root, leafs=(), include_leafs=True,
                   strict_leafs=False, exclude=None, sort=False):
        """Returns a set with all direct and indirect subclasses of `root`.
        Any subclass found in the sequence `leafs` will be included in
        the returned list, but its subclasses will not.  The elements
        of `leafs` may be ThingClass objects or labels.

        If `include_leafs` is true, the leafs are included in the returned
        list, otherwise they are not.

        If `strict_leafs` is true, any descendant of a leaf will be excluded
        in the returned set.

        If given, `exclude` may be a sequence of classes, including
        their subclasses, to exclude from the output.

        If `sort` is True, a list sorted according to depth and label
        will be returned instead of a set.
        """
        def _branch(root, leafs):
            if root not in leafs:
                branch = {root, }
                for c in root.subclasses():
                    # Defining a branch is actually quite tricky.  Consider
                    # the case:
                    #
                    #      L isA R
                    #      A isA L
                    #      A isA R
                    #
                    # where R is the root, L is a leaf and A is a direct
                    # child of both.  Logically, since A is a child of the
                    # leaf we want to skip A.  But a strait forward imple-
                    # mentation will see that A is a child of the root and
                    # include it.  Requireing that the R should be a strict
                    # parent of A solves this.
                    if root in c.get_parents(strict=True):
                        branch.update(_branch(c, leafs))
            else:
                branch = {root, } if include_leafs else set()
            return branch

        if isinstance(root, str):
            root = self.get_by_label(root)

        leafs = set(self.get_by_label(leaf) if isinstance(leaf, str)
                    else leaf for leaf in leafs)
        leafs.discard(root)

        if exclude:
            exclude = set(self.get_by_label(e) if isinstance(e, str)
                          else e for e in exclude)
            leafs.update(exclude)

        branch = _branch(root, leafs)

        # Exclude all descendants of any leaf
        if strict_leafs:
            descendants = root.descendants()
            for leaf in leafs:
                if leaf in descendants:
                    branch.difference_update(leaf.descendants(
                        include_self=False))

        if exclude:
            branch.difference_update(exclude)

        # Sort according to depth, then by label
        if sort:
            branch = sorted(sorted(branch, key=lambda x: asstring(x)),
                            key=lambda x: len(x.mro()))

        return branch

    def is_individual(self, entity):
        """Returns true if entity is an individual."""
        if isinstance(entity, str):
            entity = self.get_by_label(entity)
        return isinstance(entity, owlready2.Thing)

    # FIXME - deprecate this method as soon the ThingClass property
    #         `defined_class` works correct in Owlready2
    def is_defined(self, entity):
        """Returns true if the entity is a defined class."""
        if isinstance(entity, str):
            entity = self.get_by_label(entity)
        return hasattr(entity, 'equivalent_to') and bool(entity.equivalent_to)

    def get_graph(self, **kwargs):
        """Returns a new graph object.  See  emmo.graph.OntoGraph.

        Note that this method requires the Python graphviz package.
        """
        from .graph import OntoGraph
        return OntoGraph(self, **kwargs)

    def common_ancestors(self, cls1, cls2):
        """Return a list of common ancestors"""
        return set(cls1.ancestors()).intersection(cls2.ancestors())

    def number_of_generations(self, descendant, ancestor):
        """ Return shortest distance from ancestor to descendant"""
        if ancestor not in descendant.ancestors():
            raise ValueError('Descendant is not a descendant of ancestor')
        return self._number_of_generations(descendant, ancestor, 0)

    def _number_of_generations(self, descendant, ancestor, n):
        """Recursive help function to number_of_generations(), return
        distance between a ancestor-descendant pair (n+1)."""
        if descendant.name == ancestor.name:
            return n
        return min(self._number_of_generations(parent, ancestor, n + 1)
                   for parent in descendant.get_parents()
                   if ancestor in parent.ancestors())

    def closest_common_ancestors(self, cls1, cls2):
        """Returns a list with closest_common_ancestor for cls1 and cls2"""
        distances = {}
        for ancestor in self.common_ancestors(cls1, cls2):
            distances[ancestor] = (self.number_of_generations(cls1, ancestor) +
                                   self.number_of_generations(cls2, ancestor))
        return [ancestor for ancestor, distance in distances.items()
                if distance == min(distances.values())]

    def closest_common_ancestor(self, *classes):
        """Returns closest_common_ancestor for the given classes."""
        mros = [cls.mro() for cls in classes]
        track = defaultdict(int)
        while mros:
            for mro in mros:
                cur = mro.pop(0)
                track[cur] += 1
                if track[cur] == len(classes):
                    return cur
                if len(mro) == 0:
                    mros.remove(mro)
        assert(0)  # should never be reached...
