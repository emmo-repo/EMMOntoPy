"""EMMOntoPy esceptions and warnings, and utilities to check dependencies."""

# pylint: disable=import-outside-toplevel, invalid-name

import shutil
import warnings


class EMMOntoPyException(Exception):
    """A BaseException class for EMMOntoPy"""


class EMMOntoPyWarning(Warning):
    """A BaseWarning class for EMMOntoPy"""


class IncompatibleVersion(EMMOntoPyWarning):
    """An installed dependency version may be incompatible with a functionality
    of this package - or rather an outcome of a functionality.
    This is not critical, hence this is only a warning."""


class UnknownVersion(EMMOntoPyException):
    """Cannot retrieve version from a package."""


class IndividualWarning(EMMOntoPyWarning):
    """A warning related to an individual, e.g. punning."""


class NoSuchLabelError(LookupError, AttributeError, EMMOntoPyException):
    """Error raised when a label cannot be found."""


class AmbiguousLabelError(LookupError, AttributeError, EMMOntoPyException):
    """Error raised when a label is ambiguous."""


class LabelDefinitionError(EMMOntoPyException):
    """Error in label definition."""


class EntityClassDefinitionError(EMMOntoPyException):
    """Error in ThingClass definition."""


class ReadCatalogError(IOError):
    """Error reading catalog file."""


class ExcelError(EMMOntoPyException):
    """Raised on errors in Excel file."""


class ManchesterError(EMMOntoPyException):
    """Raised on invalid Manchester notation."""


# Utilities for checking dependencies


# Check java avilability for reasoner
def _require_java():

    # --- Java availability check ---
    if shutil.which("java") is None:
        _JAVA_AVAILABLE = False
        warnings.warn(
            "Java runtime not found on PATH. "
            "Reasoning features in emmo.graph_utils will not be available.",
            UserWarning,
            stacklevel=2,
        )
    else:
        _JAVA_AVAILABLE = True

    if not _JAVA_AVAILABLE:
        raise RuntimeError(
            "Java is required for this feature. "
            "Please install Java (e.g. OpenJDK) and ensure 'java' "
            "is on your PATH."
        )


# check graphviz


def _check_graphviz():

    try:
        import graphviz  # pylint: disable=unused-import

        _GRAPHVIZ_AVAILABLE = True
    except ImportError:
        _GRAPHVIZ_AVAILABLE = False
        warnings.warn(
            "Graphviz (Python package) not installed. "
            "Graph-related features in emmo.graph_utils will not be available.",
            UserWarning,
            stacklevel=2,
        )

    if shutil.which("dot") is None:
        _GRAPHVIZ_AVAILABLE = False
        warnings.warn(
            "Graphviz executable 'dot' not found on PATH. "
            "Graph rendering features will not be available.",
            UserWarning,
            stacklevel=2,
        )

    if not _GRAPHVIZ_AVAILABLE:
        raise RuntimeError("Graphviz is required for this feature. ")
