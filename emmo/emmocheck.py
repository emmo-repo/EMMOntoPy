# -*- coding: utf-8 -*-
"""
A module for testing an ontology against conventions defined for EMMO.
"""
import sys
import unittest
import re
import itertools
import argparse

from .ontology import get_ontology

try:
    from .colortest import ColourTextTestRunner as TextTestRunner
except ImportError:
    from unittest import TextTestRunner


class TestEMMOConventions(unittest.TestCase):
    """Test against basic conventions."""
    iri = 'emmo-inferred'

    def setUp(self):
        self.onto = get_ontology(self.iri)
        self.onto.load()

    def test_num_labels(self):
        """Check that all entities has one label.

        The only allowed exception is entities who's representation
        starts with "owl."."""
        for e in itertools.chain(self.onto.classes(),
                                 self.onto.object_properties(),
                                 self.onto.data_properties(),
                                 self.onto.individuals(),
                                 self.onto.annotation_properties()):
            with self.subTest(e=e):
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

    @unittest.skip("skipping checking unit dimensions")
    def test_unit_dimension(self):
        """Check that all units have a physical dimension."""
        patt = re.compile(r'Inverse\(units.hasReferenceUnit\).only\([^)]+\)')
        print()
        for cls in self.onto.MeasurementUnit.descendants():
            # Assume that actual units are not subclassed
            if not list(cls.subclasses()):
                with self.subTest(cls=cls):
                    print('---', cls)
                    for r in cls.is_a:
                        print('    ', repr(r), patt.match(repr(r)))
                    #self.assertTrue(
                    #    any(patt.match(repr(r)) for r in cls.is_a), msg=cls)


def main():
    """Run all checks on ontology `iri`.  Default is 'emmo-inferred'."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--iri', '-i',
        help='File name or URI to the ontology to test.')
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Verbosity level.')
    args, argv = parser.parse_known_args()

    verbosity = 2 if args.verbose else 1

    if args.iri:
        TestEMMOConventions.iri = args.iri
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEMMOConventions)
    runner = TextTestRunner(verbosity=verbosity)
    unittest.main(module=__name__, argv=sys.argv + argv, testRunner=runner)


if __name__ == '__main__':
    run()
