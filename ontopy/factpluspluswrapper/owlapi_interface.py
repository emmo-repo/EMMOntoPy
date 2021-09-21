"""Python interface to the FaCT++ Reasoner.

This module is copied from the SimPhoNy project.

Original author: Matthias Urban
"""
import os
import subprocess
import logging
import rdflib
import tempfile
import argparse

logger = logging.getLogger(__name__)

RESULT_FILE = "_result_ontology.owl"


class OwlApiInterface():
    """Interface to the FaCT++ reasoner via OWLAPI."""

    def __init__(self):
        """Initialize the interface."""
        pass

    def reason(self, graph):
        """Generate the inferred axioms for a given Graph.

        Args:
            graph (Graph): An rdflib graph to execute the reasoner on.
        """
        with tempfile.NamedTemporaryFile("wt") as f:
            graph.serialize(f.name, format="xml")
            return self._run(f.name, command="--run-reasoner")

    def reason_files(self, *owl_files):
        """Merge the given owl and generate the inferred axioms.

        Args:
            owl_files (os.path): The owl files two merge
        """
        return self._run(*owl_files, command="--run-reasoner")

    def merge_files(self, *owl_files):
        """Merge the given owl files and its import closure.

        Args:
            owl_files (os.path): The owl files two merge
        """
        return self._run(*owl_files, command="--merge-only")

    def _run(self, *owl_files, command, output_file=None, return_graph=True):
        """Run the FaCT++ reasoner using a java command.

        Args:
            owl_files (str): Path to the owl files to load.
            command (str): Either --run-reasoner or --merge-only
            output_file (str, optional): Where the output should be stored.
                Defaults to None.
            return_graph (bool, optional): Whether the result should be parsed
                and returned. Defaults to True.

        Returns:
            rdflib.Graph: The reasoned result.
        """
        java_base = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "java")
        )
        cmd = [
            "java", "-cp",
            java_base + "/lib/jars/*",
            "-Djava.library.path="
            + java_base + "/lib/so", "org.simphony.OntologyLoader"
        ] + ["%s" % command] + list(owl_files)
        logger.info("Running Reasoner")
        logger.debug(f"Command {cmd}")
        subprocess.run(cmd, check=True)

        graph = None
        if return_graph:
            graph = rdflib.Graph()
            graph.parse(RESULT_FILE)
        if output_file:
            os.rename(RESULT_FILE, output_file)
        else:
            os.remove(RESULT_FILE)
        return graph


def reason_from_terminal():
    """Run the reasoner from terminal."""
    parser = argparse.ArgumentParser(
        description="Run the FaCT++ reasoner on the given OWL file. "
        "Catalog files are used to load the import closure. "
        "Then the reasoner is executed and the inferred triples are merged "
        "with the asserted ones. If multiple OWL files are given, they are "
        "merged beforehand"
    )
    parser.add_argument("owl_file", nargs="+",
                        help="OWL file(s) to run the reasoner on.")
    parser.add_argument("output_file",
                        help="Path to store inferred axioms to.")

    args = parser.parse_args()
    OwlApiInterface()._run(*args.owl_file, command="--run-reasoner",
                           return_graph=False, output_file=args.output_file)


if __name__ == "__main__":
    reason_from_terminal()
