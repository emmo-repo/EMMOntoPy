# -*- coding: utf-8 -*-
"""
A module for testing an ontology against conventions defined for EMMO.

A yaml file can be provided with additional test configurations.

Example configuration file:

    test_unit_dimensions:
      exceptions:
        - myunits.MyUnitCategory1
        - myunits.MyUnitCategory2
"""
import os
import sys
import re
import unittest
import itertools
import argparse

from .ontology import World

try:
    from .colortest import ColourTextTestRunner as TextTestRunner
except ImportError:
    from unittest import TextTestRunner


class TestEMMOConventions(unittest.TestCase):
    """Base class for testing an ontology against EMMO conventions."""
    config = {}  # configurations


class TestSyntacticEMMOConventions(TestEMMOConventions):
    """Test syntactic EMMO conventions."""
    def test_number_of_labels(self):
        """Check that all entities have one and only one label.

        The only allowed exception is entities who's representation
        starts with "owl."."""
        for e in itertools.chain(self.onto.classes(),
                                 self.onto.object_properties(),
                                 self.onto.data_properties(),
                                 self.onto.individuals(),
                                 self.onto.annotation_properties()):
            with self.subTest(e=e, labels=e.label):
                if not repr(e).startswith('owl.'):
                    self.assertEqual(1, len(e.label))

    def test_class_label(self):
        """Check that labels are CamelCase.

        For now we just we just check that they start with upper case."""
        for cls in self.onto.classes():
            for label in cls.label:
                self.assertTrue(label[0].isupper() or label[0].isdigit())

    def test_object_property_label(self):
        """Check that object property labels are lowerCamelCase.

        Allowed exceptions: "EMMORelation"

        If they start with "has" or "is" they should be followed by a
        upper case letter.

        If they start with "is" they should also end with "Of".
        """
        for op in self.onto.object_properties():
            for label in op.label:
                if label == 'EMMORelation':
                    continue
                self.assertTrue(label[0].islower())
                if label.startswith('has'):
                    self.assertTrue(label[3].isupper())
                if label.startswith('is'):
                    self.assertTrue(label[2].isupper())
                    self.assertTrue(label.endswith('Of'))


class TestFunctionalEMMOConventions(TestEMMOConventions):
    """Test functional EMMO conventions."""
    def test_unit_dimension(self):
        """Check that all measurement units have a physical dimension.

        Configurations:
            exceptions - full class names of classes to ignore.
        """
        exceptions = set((
            'metrology.MultipleUnit',
            'metrology.SubMultipleUnit',
            'metrology.OffSystemUnit',
            'metrology.PrefixedUnit',
            'metrology.NonPrefixedUnit',
            'metrology.SpecialUnit',
            'metrology.DerivedUnit',
            'metrology.BaseUnit',
            'metrology.UnitSymbol',
            'siunits.SICoherentDerivedUnit',
            'siunits.SINonCoherentDerivedUnit',
            'siunits.SISpecialUnit',
            'siunits.SICoherentUnit',
            'siunits.SIPrefixedUnit',
            'siunits.SIBaseUnit',
            'siunits.SIUnitSymbol',
            'siunits.SIUnit',
        ))
        exceptions.update(
            self.get_config('test_unit_dimension.exceptions', ()))
        regex = re.compile(r'^metrology.hasPhysicsDimension.only\(.*\)$')
        classes = set(self.onto.classes())
        for cls in self.onto.MeasurementUnit.descendants():
            if not self.check_imported and cls not in classes:
                continue
            # Assume that actual units are not subclassed
            if not list(cls.subclasses()) and repr(cls) not in exceptions:
                with self.subTest(cls=cls):
                    self.assertTrue(
                        any(regex.match(repr(r))
                            for r in cls.get_indirect_is_a()), msg=cls)

    def test_quantity_dimension(self):
        """Check that all quantities have units (defined via dimensionality).

        Configurations:
            exceptions - full class names of classes to ignore.
        """
        exceptions = set((
            'properties.ModelledQuantitativeProperty',
            'properties.MeasuredQuantitativeProperty',
            'properties.ConventionalQuantitativeProperty',
            'metrology.QuantitativeProperty',
            'metrology.Quantity',
            'metrology.OrdinalQuantity',
            'metrology.BaseQuantity',
            'metrology.PhysicalConstant',
            'metrology.PhysicalQuantity',
            'metrology.ExactConstant',
            'metrology.MeasuredConstant',
            'metrology.DerivedQuantity',
            'isq.ISQBaseQuantity',
            'isq.InternationalSystemOfQuantity',
            'isq.ISQDerivedQuantity',
            'siunits.SIExactConstant',
            'units-extension.AtomAndNuclearPhysicsDerivedQuantity',
        ))
        exceptions.update(
            self.get_config('test_quantity_dimension.exceptions', ()))
        regex = re.compile(
            r'^metrology.hasReferenceUnit.only\(metrology.'
            r'hasPhysicsDimension.only\(.*\)\)$')
        classes = set(self.onto.classes())
        for cls in self.onto.Quantity.descendants():
            if not self.check_imported and cls not in classes:
                continue
            if repr(cls) not in exceptions:
                with self.subTest(cls=cls):
                    self.assertTrue(
                        any(regex.match(repr(r))
                            for r in cls.get_indirect_is_a()), msg=cls)

    def test_namespace(self):
        """Check that all IRIs are namespaced after their (sub)ontology.

        Configurations:
            exceptions - full name of entities to ignore.
        """
        exceptions = set((
            'mereotopology.Item',
            'owl.qualifiedCardinality',
            'owl.minQualifiedCardinality',
        ))
        exceptions.update(self.get_config('test_namespace.exceptions', ()))

        def checker(onto):
            for e in itertools.chain(onto.classes(),
                                     onto.object_properties(),
                                     onto.data_properties(),
                                     onto.individuals(),
                                     onto.annotation_properties()):
                if e not in visited and repr(e) not in exceptions:
                    visited.add(e)
                    with self.subTest(
                            iri=e.iri, base_iri=onto.base_iri, entity=str(e)):
                        self.assertTrue(
                            e.iri.endswith(e.name),
                            msg='the final part of entity IRIs must be their '
                            'name')
                        self.assertEqual(
                            e.iri[:-len(e.name)], onto.base_iri,
                            msg='IRI %r does not correspond to module '
                            'namespace: %r' % (e.iri, onto.base_iri))

            if self.check_imported:
                for imp_onto in onto.imported_ontologies:
                    checker(imp_onto)

        visited = set()
        checker(self.onto)

    def get_config(self, string, default=None):
        """Returns the configuration specified by `string`.

        If configuration is not found in the configuration file, `default`
        is returned.

        Sub-configurations can be accessed by separating the components with
        dots, like "test_namespace.exceptions".
        """
        c = self.config
        try:
            for token in string.split('.'):
                c = c[token]
        except KeyError:
            return default
        return c


def main():
    """Run all checks on ontology `iri`.  Default is 'http://emmo.info/emmo'.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'iri',
        help='File name or URI to the ontology to test.')
    parser.add_argument(
        '--database', '-d', metavar='FILENAME', default=':memory:',
        help='Load ontology from Owlready2 sqlite3 database.  The `iri` '
        'argument should in this case be the IRI of the ontology you '
        'want to check.')
    parser.add_argument(
        '--local', '-l', action='store_true',
        help='Load local versions of imported ontologies using a Protègè '
        'catalog file.')
    parser.add_argument(
        '--check-imported', '-i', action='store_true',
        help='Whether to check imported ontologies.')
    parser.add_argument(
        '--catalog-file', '-C', default='catalog-v001.xml',
        help='Path to Protègè catalog file used together with --local.  '
        'Defaults to "catalog-v001.xml".')
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Verbosity level.')
    parser.add_argument(
        '--configfile', '-c',
        help='A yaml file with additional test configurations.')

    try:
        args, argv = parser.parse_known_args()
        sys.argv[1:] = argv
    except SystemExit as e:
        os._exit(e.code)  # Exit without traceback on invalid arguments

    # Load ontology
    world = World(filename=args.database)

    if args.database != ':memory:' and args.iri not in world.ontologies:
        parser.error('The IRI argument should be one of the ontologies in '
                     'the database:\n  ' +
                     '\n  '.join(world.ontologies.keys()))

    onto = world.get_ontology(args.iri)
    catalog_file = args.catalog_file if args.local else None
    onto.load(only_local=args.local, catalog_file=catalog_file)

    # Store settings TestEMMOConventions
    TestEMMOConventions.onto = onto
    TestEMMOConventions.check_imported = args.check_imported

    # Set up and run tests
    verbosity = 2 if args.verbose else 1
    if args.configfile:
        import yaml
        with open(args.configfile, 'rt') as f:
            TestEMMOConventions.config.update(
                yaml.load(f, Loader=yaml.SafeLoader))

    unittest.TestLoader().loadTestsFromTestCase(TestEMMOConventions)
    runner = TextTestRunner(verbosity=verbosity)
    runner.resultclass.checkmode = True
    unittest.main(module=__name__, testRunner=runner)


if __name__ == '__main__':
    main()
