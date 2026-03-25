# Implementation notes for the Ontology Toolkit (ontokit)
This sub-directory includes python modules implementing the ontokit tool.

The main tool is implemented in `tools/ontokit`. It simply defines the
general options and imports the arguments from each sub-command.

Each sub-command will be implemented in its own module. These sub-command
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

In the tools/ontokit script the following must be added:

* The sub-command must be imported as
  `from ontopy.ontokit.<subcmd> import <subcmd>_arguments` at the top.

* The `<subcmd>_arguments(subparsers)` function must be called (see under
  '# Add sub-command arguments' in the `main` function).

Notes on setting up the workflows in github actions with `ontokit setup`:
* In order for github pages to work correctly the repository must have
  the `gh-pages` branch enabled for github pages in the repository settings.

* The ontology repository must follow the `EMMO` recommendations for
  repository structure as defined in the EMMO documentation.

* The `ontokit setup` command creates a repository level
  `.ontokit_conf.yml` file if missing. This file contains the variables
  `ONTOLOGY_NAME`, `ONTOLOGY_PREFIX`, `ONTOLOGY_IRI`, `GITHUB_REPOSITORY`
  and `BUILD_DIR` used by generated workflows and by `ontokit docs`.
  `BUILD_DIR` specifies the directory from which ontology files are read
  (and where intermediate build artefacts are placed). It defaults to
  `build` but can be set to `.` to use the root directory directly.
  The generated workflow templates load all these values from
  `.ontokit_conf.yml` at runtime, making this file the single source
  of truth for ontokit configuration.


* When running `ontokit setup` a new set of `*.yml` files is created in
  .github/workflows/. These files define the workflows for continuous
  integration and deployment. If there are other workflow already present
  in this directory these will not be overwritten. Only the files created
  by ontokit will be updated. However, care should be taken that these
  workflows do not conflict with any other workflow present in the
  repository.

Notes on running `ontokit docs`:

* The `ontokit docs` command generates documentation for the ontology and
  places it in the `public` directory.
  It uses the ontology name and IRI defined in the `.ontokit_conf.yml` file to generate the documentation.
  `public` is the directory that should
  be deployed to github pages (as done in the generated `cd_ghpages.yml` workflow).


* The `ontokit docs` command relied on the presence of the `ONTOLOGY_NAME`,
  `ONTOLOGY_PREFIX`, `ONTOLOGY_IRI`, `GITHUB_REPOSITORY` and `BUILD_DIR`
  variables in the `.ontokit_conf.yml` file. If these
  variables are missing, the command will fail. You can create this file
  manually if you want to use `ontokit docs` without running `ontokit setup`.
  However, `ontokit setup` creates github workflow files as well,
  which might lead to changes in your already existing workflows.

*  For the main reference index you can control which subsections are included. The default is
  `all`.

  ```yaml
  REFERENCE_SUBSECTIONS: all
  # Or, for a subset:
  # REFERENCE_SUBSECTIONS: classes,annotation_properties,data_properties,object_properties,individuals
  ```

* It is also possible to add multiple additional reference indices in
  `.ontokit_conf.yml` with `REFERENCE_INDICES`:

  ```yaml
  REFERENCE_INDICES:
    - ontology_file: build/other-ontology.ttl
      title: Other Ontology Reference
      docfile: other-reference.rst
      iri_regex: https://example.org/other
      imported: false
      recursive: false
      subsections: all
  ```

  The `ontology_file` key is required for each entry. The generated
  `index.rst` will include all configured reference indices. Note
  that the creation of the ontology in the particular place (as here
  in build) is not done by this tool.
