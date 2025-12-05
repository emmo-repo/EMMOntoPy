# Implementation notes for the Ontology Toolkit (ontokit)
This sub-directory include python modules implementing ontokit tool.

The main tool is implemented in `tools/ontokit`. It simply defines the
general options and imports the arguments from each sub-command.

Each sub-command will be implemented its own module. These sub-command
modules should at least define two functions (with `<subcmd>` replaced
with the name of the sub-command):

* `<subcmd>_arguments(subparsers)`: This function creates a parser for the
  sub-command by calling `subparsers.add_parser()` and adding the sub-command
  options to this parser.

  Additionally, this function should refer to the implementation of the
  sub-command by calling the `set_defaults(subcommand=<subcmd>_subcommand)`
  method of the sub-command parser.

* `<subcmd>_subcommand(args)`: This function implements the sub-command.
  The `args` argument is a `argparse.Namespace` object with all the
  options.
