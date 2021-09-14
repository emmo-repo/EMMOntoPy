# Adapted from https://github.com/meshy/colour-runner by Charlie Denton
# License: MIT
#
from unittest.result import TestResult
from unittest.runner import TextTestRunner
from unittest.util import strclass

from blessings import Terminal
from pygments import formatters, highlight
from pygments.lexers import Python3TracebackLexer as Lexer


class ColourTextTestResult(TestResult):
    """
    A test result class that prints colour formatted text results to a stream.

    Based on https://github.com/python/cpython/blob/3.3/Lib/unittest/runner.py
    """
    formatter = formatters.Terminal256Formatter()
    lexer = Lexer()
    separator1 = '=' * 70
    separator2 = '-' * 70
    indent = ' ' * 4
    # if `checkmode` is true, simplified output will be generated with
    # no traceback
    checkmode = False
    _terminal = Terminal()
    colours = {
        None: str,
        'error': _terminal.bold_red,
        'expected': _terminal.blue,
        # 'fail': _terminal.bold_yellow,
        'fail': _terminal.bold_magenta,
        'skip': str,
        'success': _terminal.green,
        'title': _terminal.blue,
        'unexpected': _terminal.bold_red,
    }

    _test_class = None

    def __init__(self, stream, descriptions, verbosity):
        super(ColourTextTestResult, self).__init__(
            stream, descriptions, verbosity)
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions

    def getShortDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return self.indent + doc_first_line
        return self.indent + test._testMethodName

    def getLongDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return '\n'.join((str(test), doc_first_line))
        return str(test)

    def getClassDescription(self, test):
        test_class = test.__class__
        doc = test_class.__doc__
        if self.descriptions and doc:
            return doc.split('\n')[0].strip()
        return strclass(test_class)

    def startTest(self, test):
        super(ColourTextTestResult, self).startTest(test)
        pos = 0
        if self.showAll:
            if self._test_class != test.__class__:
                self._test_class = test.__class__
                title = self.getClassDescription(test)
                self.stream.writeln(self.colours['title'](title))
            descr = self.getShortDescription(test)
            self.stream.write(descr)
            pos += len(descr)
            self.stream.write(' ' * (70 - pos))
            # self.stream.write(' ' * (self._terminal.width - 10 - pos))
            # self.stream.write(' ... ')
            self.stream.flush()

    def printResult(self, short, extended, colour_key=None):
        colour = self.colours[colour_key]
        if self.showAll:
            self.stream.writeln(colour(extended))
        elif self.dots:
            self.stream.write(colour(short))
            self.stream.flush()

    def addSuccess(self, test):
        super(ColourTextTestResult, self).addSuccess(test)
        self.printResult('.', 'ok', 'success')

    def addError(self, test, err):
        super(ColourTextTestResult, self).addError(test, err)
        self.printResult('E', 'ERROR', 'error')

    def addFailure(self, test, err):
        super(ColourTextTestResult, self).addFailure(test, err)
        self.printResult('F', 'FAIL', 'fail')

    def addSkip(self, test, reason):
        super(ColourTextTestResult, self).addSkip(test, reason)
        if self.checkmode:
            self.printResult('s', 'skipped', 'skip')
        else:
            self.printResult('s', 'skipped {0!r}'.format(reason), 'skip')

    def addExpectedFailure(self, test, err):
        super(ColourTextTestResult, self).addExpectedFailure(test, err)
        self.printResult('x', 'expected failure', 'expected')

    def addUnexpectedSuccess(self, test):
        super(ColourTextTestResult, self).addUnexpectedSuccess(test)
        self.printResult('u', 'unexpected success', 'unexpected')

    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        colour = self.colours[flavour.lower()]

        for test, err in errors:
            if self.checkmode and flavour == 'FAIL':
                self.stream.writeln(self.separator1)
                title = '%s: %s' % (flavour, test.shortDescription())
                self.stream.writeln(colour(title))
                self.stream.writeln(str(test))
                if self.showAll:
                    self.stream.writeln(self.separator2)
                    lines = str(err).split('\n')
                    i = 1
                    for line in lines[1:]:
                        if line.startswith(' '):
                            i += 1
                        else:
                            break
                    self.stream.writeln(highlight(
                        '\n'.join(lines[i:]), self.lexer, self.formatter))
            else:
                self.stream.writeln(self.separator1)
                title = '%s: %s' % (flavour, self.getLongDescription(test))
                self.stream.writeln(colour(title))
                self.stream.writeln(self.separator2)
                self.stream.writeln(highlight(err, self.lexer, self.formatter))


class ColourTextTestRunner(TextTestRunner):
    """A test runner that uses colour in its output"""
    resultclass = ColourTextTestResult
