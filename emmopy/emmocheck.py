# -*- coding: utf-8 -*-
"""
A module for testing an ontology against conventions defined for EMMO.

A YAML file can be provided with additional test configurations.

Example configuration file:

    test_unit_dimensions:
      exceptions:
        - myunits.MyUnitCategory1
        - myunits.MyUnitCategory2

    skip:
      - name_of_test_to_skip

    enable:
      - name_of_test_to_enable

"""
import os
import sys
import re
import unittest
import itertools
import argparse
import fnmatch

import owlready2

from ontopy.ontology import World
from ontopy.patch import get_preferred_label as get_label
from ontopy import onto_path

try:
    from ontopy.colortest import ColourTextTestRunner as TextTestRunner
except ImportError:
    from unittest import TextTestRunner


class TestEMMOConventions(unittest.TestCase):
    """Base class for testing an ontology against EMMO conventions."""
    config = {}  # configurations

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


class TestSyntacticEMMOConventions(TestEMMOConventions):
    """Test syntactic EMMO conventions."""
    def test_number_of_labels(self):
        """Check that all entities have one and only one prefLabel.

        Use "altLabel" for synonyms.

        The only allowed exception is entities who's representation
        starts with "owl.".
        """
        exceptions = set((
            'terms.license',
            'terms.abstract',
            'terms.contributor',
            'terms.creator',
            'terms.publisher',
            'terms.title',
            'core.prefLabel',
            'core.altLabel',
            'core.hiddenLabel',
        ))
        exceptions.update(self.get_config(
            'test_number_of_labels.exceptions', ()))

        if 'prefLabel' in self.onto.world._props:
            for e in self.onto.get_entities():
                if repr(e) not in exceptions:
                    with self.subTest(entity=e, label=get_label(e),
                                      prefLabels=e.prefLabel):
                        if not repr(e).startswith('owl.'):
                            self.assertTrue(hasattr(e, 'prefLabel'))
                            self.assertEqual(1, len(e.prefLabel))
        else:
            self.fail('ontology has no prefLabel')

    def test_class_label(self):
        """Check that class labels are CamelCase and valid identifiers.

        For CamelCase, we are currently only checking that the labels
        start with upper case.
        """
        exceptions = set((
            '0-manifold',  # not needed in 1.0.0-beta
            '1-manifold',
            '2-manifold',
            '3-manifold',
            'C++',
        ))
        exceptions.update(self.get_config('test_class_label.exceptions', ()))

        for cls in self.onto.classes(self.check_imported):
            for label in cls.label + getattr(cls, 'prefLabel', []):
                if label not in exceptions:
                    with self.subTest(entity=cls, label=label):
                        self.assertTrue(label.isidentifier())
                        self.assertTrue(label[0].isupper())

    def test_object_property_label(self):
        """Check that object property labels are lowerCamelCase.

        Allowed exceptions: "EMMORelation"

        If they start with "has" or "is" they should be followed by a
        upper case letter.

        If they start with "is" they should also end with "Of".
        """
        exceptions = set((
            'EMMORelation',
        ))
        exceptions.update(self.get_config(
            'test_object_property_label.exceptions', ()))

        for op in self.onto.object_properties():
            if repr(op) not in exceptions:
                for label in op.label:
                    with self.subTest(entity=op, label=label):
                        self.assertTrue(label[0].islower(),
                                        'label start with lowercase')
                        if label.startswith('has'):
                            self.assertTrue(label[3].isupper(),
                                            'what follows "has" must be '
                                            'uppercase')
                        if label.startswith('is'):
                            self.assertTrue(label[2].isupper(),
                                            'what follows "is" must be '
                                            'uppercase')
                            self.assertTrue(label.endswith(('Of', 'With')),
                                            'should end with "Of" or "With"')


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

            'emmo.MultipleUnit',
            'emmo.SubMultipleUnit',
            'emmo.OffSystemUnit',
            'emmo.PrefixedUnit',
            'emmo.NonPrefixedUnit',
            'emmo.SpecialUnit',
            'emmo.DerivedUnit',
            'emmo.BaseUnit',
            'emmo.UnitSymbol',

            'emmo.SICoherentDerivedUnit',
            'emmo.SINonCoherentDerivedUnit',
            'emmo.SISpecialUnit',
            'emmo.SICoherentUnit',
            'emmo.SIPrefixedUnit',
            'emmo.SIBaseUnit',
            'emmo.SIUnitSymbol',
            'emmo.SIUnit',
        ))
        if not hasattr(self.onto, 'MeasurementUnit'):
            return
        exceptions.update(
            self.get_config('test_unit_dimension.exceptions', ()))
        regex = re.compile(
            r'^(emmo|metrology).hasPhysicalDimension.some\(.*\)$')
        classes = set(self.onto.classes(self.check_imported))
        for cls in self.onto.MeasurementUnit.descendants():
            if not self.check_imported and cls not in classes:
                continue
            # Assume that actual units are not subclassed
            if not list(cls.subclasses()) and repr(cls) not in exceptions:
                with self.subTest(cls=cls, label=get_label(cls)):
                    self.assertTrue(
                        any(regex.match(repr(r))
                            for r in cls.get_indirect_is_a()), msg=cls)

    def test_quantity_dimension(self):
        """Check that all quantities have a physicalDimension annotation.

        Note: this test will be deprecated when isq is moved to emmo/domain.

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
            'isq.SIExactConstant',

            'emmo.ModelledQuantitativeProperty',
            'emmo.MeasuredQuantitativeProperty',
            'emmo.ConventionalQuantitativeProperty',

            'emmo.QuantitativeProperty',
            'emmo.Quantity',
            'emmo.OrdinalQuantity',
            'emmo.BaseQuantity',
            'emmo.PhysicalConstant',
            'emmo.PhysicalQuantity',
            'emmo.ExactConstant',
            'emmo.MeasuredConstant',
            'emmo.DerivedQuantity',

            'emmo.ISQBaseQuantity',
            'emmo.InternationalSystemOfQuantity',
            'emmo.ISQDerivedQuantity',
            'emmo.SIExactConstant',

            'emmo.NonSIUnits',
            'emmo.StandardizedPhysicalQuantity',
            'emmo.CategorizedPhysicalQuantity',

            'emmo.AtomicAndNuclear',
            'emmo.Defined',
            'emmo.Electromagnetic',
            'emmo.FrequentlyUsed',
            'emmo.PhysicoChemical',
            'emmo.ChemicalCompositionQuantity',
            'emmo.Universal',
        ))
        if not hasattr(self.onto, 'PhysicalQuantity'):
            return
        exceptions.update(
            self.get_config('test_quantity_dimension.exceptions', ()))
        regex = re.compile(
            '^T([+-][1-9]|0) L([+-][1-9]|0) M([+-][1-9]|0) I([+-][1-9]|0) '
            '(H|Θ)([+-][1-9]|0) N([+-][1-9]|0) J([+-][1-9]|0)$')
        classes = set(self.onto.classes(self.check_imported))
        for cls in self.onto.PhysicalQuantity.descendants():
            if not self.check_imported and cls not in classes:
                continue
            if repr(cls) not in exceptions:
                with self.subTest(cls=cls, label=get_label(cls)):
                    anno = cls.get_annotations()
                    self.assertIn('physicalDimension', anno, msg=cls)
                    physdim = anno['physicalDimension'].first()
                    self.assertRegex(physdim, regex, msg=cls)

    def test_physical_quantity_dimension(self):
        """Check that all physical quantities have `hasPhysicalDimension`.

        Note: this test will fail before isq is moved to emmo/domain.

        Configurations:
            exceptions - full class names of classes to ignore.

        """
        exceptions = set((
            'emmo.ModelledQuantitativeProperty',
            'emmo.MeasuredQuantitativeProperty',
            'emmo.ConventionalQuantitativeProperty',

            'emmo.QuantitativeProperty',
            'emmo.BaseQuantity',
            'emmo.PhysicalConstant',
            'emmo.PhysicalQuantity',
            'emmo.ExactConstant',
            'emmo.MeasuredConstant',
            'emmo.DerivedQuantity',

            'emmo.ISQBaseQuantity',
            'emmo.InternationalSystemOfQuantity',
            'emmo.ISQDerivedQuantity',
            'emmo.SIExactConstant',

            'emmo.NonSIUnits',
            'emmo.StandardizedPhysicalQuantity',
            'emmo.CategorizedPhysicalQuantity',

            'emmo.AtomicAndNuclearPhysicsQuantity',
            'emmo.ThermodynamicalQuantity',
            'emmo.LightAndRadiationQuantity',
            'emmo.SpaceAndTimeQuantity',
            'emmo.AcousticQuantity',
            'emmo.PhysioChememicalQuantity',
            'emmo.ElectromagneticQuantity',
            'emmo.MechanicalQuantity',
            'emmo.CondensedMatterPhysicsQuantity',
            'emmo.ChemicalCompositionQuantity',

            'emmo.Extensive',
            'emmo.Intensive',
        ))
        if not hasattr(self.onto, 'PhysicalQuantity'):
            return
        exceptions.update(
            self.get_config('test_physical_quantity_dimension.exceptions', ()))
        classes = set(self.onto.classes(self.check_imported))
        for cls in self.onto.PhysicalQuantity.descendants():
            if not self.check_imported and cls not in classes:
                continue
            if repr(cls) not in exceptions:
                with self.subTest(cls=cls, label=get_label(cls)):
                    try:
                        class_props = cls.INDIRECT_get_class_properties()
                    except AttributeError:
                        # The INDIRECT_get_class_properties() method
                        # does not support inverse properties.  Build
                        # class_props manually...
                        class_props = set()
                        for c in cls.mro():
                            if hasattr(c, 'is_a'):
                                class_props.update(
                                    [r.property for r in c.is_a
                                     if isinstance(r, owlready2.Restriction)])

                    self.assertIn(self.onto.hasPhysicalDimension,
                                  class_props, msg=cls)

    def test_namespace(self):
        """Check that all IRIs are namespaced after their (sub)ontology.

        Configurations:
            exceptions - full name of entities to ignore.
        """
        exceptions = set((
            'owl.qualifiedCardinality',
            'owl.minQualifiedCardinality',
            'terms.creator',
            'terms.contributor',
            'terms.publisher',
            'terms.title',
            'terms.license',
            'terms.abstract',
            'core.prefLabel',
            'core.altLabel',
            'core.hiddenLabel',
            'mereotopology.Item',
            'manufacturing.EngineeredMaterial',
        ))
        exceptions.update(self.get_config('test_namespace.exceptions', ()))

        def checker(onto, ignore_namespace):
            if list(filter(onto.base_iri.strip('#').endswith,
                           self.ignore_namespace)) != []:
                print('Skipping namespace: ' + onto.base_iri)
                return
            entities = itertools.chain(onto.classes(),
                                       onto.object_properties(),
                                       onto.data_properties(),
                                       onto.individuals(),
                                       onto.annotation_properties())
            for e in entities:
                if e not in visited and repr(e) not in exceptions:
                    visited.add(e)
                    with self.subTest(
                            iri=e.iri, base_iri=onto.base_iri, entity=repr(e)):
                        self.assertTrue(
                            e.iri.endswith(e.name),
                            msg='the final part of entity IRIs must be their '
                            'name')
                        self.assertEqual(
                            e.iri, onto.base_iri + e.name,
                            msg='IRI %r does not correspond to module '
                            'namespace: %r' % (e.iri, onto.base_iri))

            if self.check_imported:
                for imp_onto in onto.imported_ontologies:
                    if imp_onto not in visited_onto:
                        visited_onto.add(imp_onto)
                        checker(imp_onto, ignore_namespace)

        visited = set()
        visited_onto = set()
        checker(self.onto, self.ignore_namespace)


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
        help='Load imported ontologies locally.  Their paths are specified '
        'in Protègè catalog files or via the --path option.  The IRI should '
        'be a file name.')
    parser.add_argument(
        '--catalog-file', default='catalog-v001.xml',
        help='Name of Protègè catalog file in the same folder as the '
        'ontology.  This option is used together with --local and '
        'defaults to "catalog-v001.xml".')
    parser.add_argument(
        '--path', action='append', default=[],
        help='Paths where imported ontologies can be found.  May be provided '
        'as a comma-separated string and/or with multiple --path options.')
    parser.add_argument(
        '--check-imported', '-i', action='store_true',
        help='Whether to check imported ontologies.')
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Verbosity level.')
    parser.add_argument(
        '--configfile', '-c',
        help='A yaml file with additional test configurations.')
    parser.add_argument(
        '--skip', '-s', action='append', default=[],
        help=('Shell pattern matching tests to skip.  This option may be '
              'provided multiple times.'))
    parser.add_argument(
        '--enable', '-e', action='append', default=[],
        help=('Shell pattern matching tests to enable that have been '
              'skipped by default or in the config file.  This option may '
              'be provided multiple times.'))
    parser.add_argument(  # deprecated, replaced by --no-catalog
        '--url-from-catalog', '-u', default=None, action='store_true',
        help=('Get url from catalog file'))
    parser.add_argument(
        '--no-catalog', action='store_false', dest='url_from_catalog',
        default=None,
        help='Whether to not read catalog file even if it exists.')
    parser.add_argument(
        '--ignore-namespace', '-n', action='append', default=[],
        help=('Namespace to be ignored. Can be given multiple '
              'times'))

    # Options to pass forward to unittest
    parser.add_argument(
        '--buffer', '-b',
        dest='unittest', action='append_const', const='-b',
        help=('The standard output and standard error streams are buffered '
              'during the test run. Output during a passing test is '
              'discarded. Output is echoed normally on test fail or error '
              'and is added to the failure messages.'))
    parser.add_argument(
        '--catch',
        dest='unittest', action='append_const', const='-c',
        help=('Control-C during the test run waits for the current test to '
              'end and then reports all the results so far. A second '
              'control-C raises the normal KeyboardInterrupt exception'))
    parser.add_argument(
        '--failfast', '-f',
        dest='unittest', action='append_const', const='-f',
        help=('Stop the test run on the first error or failure.'))
    try:
        args = parser.parse_args()
        sys.argv[1:] = args.unittest if args.unittest else []
        if args.verbose:
            sys.argv.append('-v')
    except SystemExit as e:
        os._exit(e.code)  # Exit without traceback on invalid arguments

    # Append to onto_path
    for paths in args.path:
        for path in paths.split(','):
            if path not in onto_path:
                onto_path.append(path)

    # Load ontology
    world = World(filename=args.database)
    if args.database != ':memory:' and args.iri not in world.ontologies:
        parser.error('The IRI argument should be one of the ontologies in '
                     'the database:\n  ' +
                     '\n  '.join(world.ontologies.keys()))

    onto = world.get_ontology(args.iri)
    onto.load(only_local=args.local,
              url_from_catalog=args.url_from_catalog,
              catalog_file=args.catalog_file)

    # Store settings TestEMMOConventions
    TestEMMOConventions.onto = onto
    TestEMMOConventions.check_imported = args.check_imported
    TestEMMOConventions.ignore_namespace = args.ignore_namespace

    # Configure tests
    verbosity = 2 if args.verbose else 1
    if args.configfile:
        import yaml
        with open(args.configfile, 'rt') as f:
            TestEMMOConventions.config.update(
                yaml.load(f, Loader=yaml.SafeLoader))

    # Run all subclasses of TestEMMOConventions as test suites
    status = 0
    for cls in TestEMMOConventions.__subclasses__():
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)

        # Mark tests to be skipped
        for test in suite:
            name = test.id().split('.')[-1]
            skipped = set([  # skipped by default
                'test_namespace',
                'test_physical_quantity_dimension',
            ])
            msg = {name: 'skipped by default' for name in skipped}

            # enable/skip tests from config file
            for pattern in test.get_config('enable', ()):
                if fnmatch.fnmatchcase(name, pattern):
                    skipped.remove(name)
            for pattern in test.get_config('skip', ()):
                if fnmatch.fnmatchcase(name, pattern):
                    skipped.add(name)
                    msg[name] = 'skipped from config file'

            # enable/skip from command line
            for pattern in args.enable:
                if fnmatch.fnmatchcase(name, pattern):
                    skipped.remove(name)
            for pattern in args.skip:
                if fnmatch.fnmatchcase(name, pattern):
                    skipped.add(name)
                    msg[name] = 'skipped from command line'

            if name in skipped:
                setattr(test, 'setUp',
                        lambda: test.skipTest(msg.get(name, '')))

        runner = TextTestRunner(verbosity=verbosity)
        runner.resultclass.checkmode = True
        result = runner.run(suite)
        if result.failures:
            status = 1

    return status


if __name__ == '__main__':
    status = main()
    sys.exit(status)
