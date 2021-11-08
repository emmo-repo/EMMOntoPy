# Development environment

<!-- markdownlint-disable MD046 -->

This section outlines some suggestions as well as conventions used by the EMMOntoPy developers, which should be considered or followed if one wants to contribute to the package.

## Setup

!!! important "Requirements"
    This section expects you to be running on a Unix-like system (e.g., Linux) with *minimum* Python 3.6.

### Virtual environment

Since development can be messy, it is good to separate the development environment from the rest of your system's environment.

To do this, you can use a virtual environment.
There are a several different ways to create a virtual environment, but we recommend using either `virtualenv`, the python native `venv` or `conda`.

=== "`virtualenv` (recommended)"

    To install `virtualenv` run:

    ```console
    pip install virtualenvwrapper
    ```

    There is other setup, most of which only needs to be run once.
    For more information about this, see the [`virtualenvwrapper` documentation](https://virtualenvwrapper.readthedocs.io/en/latest/#introduction).

    After successfully setting up `virtualenv` through `virtualenvwrapper`, you can create a new virtual environment:

    ```console
    mkproject -p python3.7 emmo-python
    ```

    !!! note
        If you do not have Python 3.7 installed (but instead have Python 3.6), you can leave out the extra `-p python3.7` argument.
        Or you can choose to use another version of Python by changing this argument to another (valid) python interpreter.

    Then, if the virtual environment has not been activated automatically (you should see the name `emmo-python` in a parenthesis in your console), you can run:

    ```console
    workon emmo-python
    ```

    To deactivate the virtual environment, returning to the system/global environment again, run:

    ```console
    deactivate
    ```
=== "`venv`"
    First go to the directory where you desire to keep you virtual environment and choosing
    the python interpreter you already have installed and wish to use run
    ```console
    python3.? -m venv emmo-python
    ```
    A subfolder with the name emmo-python containing the environment is created.
    To activate the environment
    ```console
    path/to/python-environments/emmo-python/activate
    ```
    Deactivate in the same manner as for virtualenv
=== "`conda`"

    If you are using `conda` already, simply run:

    ```console
    conda create --name emmo-python python=3.7
    ```

    !!! note
        If you do not have Python 3.7 installed (but instead have Python 3.6), you can leave out the extra `python=3.7` argument.
        Or you can choose to use another version of Python by changing this argument.

    Then, if the virtual environment has not been activated automatically (you should see the name `emmo-python` in a parenthesis in your console), you can run:

    ```console
    conda activate emmo-python
    ```

    To deactivate the virtual environment, returning to the system/global environment again, run:

    ```console
    conda deactivate
    ```

    If you are not using `conda` already, instead try the `virtualenv` solution.

    For more information about `conda`, go to [their documentation](https://conda.io).

!!! important "Expectation"
    From here on, all commands expect you have activated your virtual environment, if you are using one, unless stated otherwise.

### Installation

To install the package, please do **not** install from PyPI.
Instead you should clone the repository from GitHub:

```console
git clone https://github.com/emmo-repo/EMMO-python.git
```

or, if you are using an SSH connection to GitHub, you can instead clone via:

```console
git clone git@github.com:emmo-repo/EMMO-python.git
```

Then enter into the newly cloned `EMMO-python` directory (`cd EMMO-python`) and run:

```console
pip install -U -e .[dev]
pre-commit install
```

This will install the EMMOntoPy Python package, including all dependencies and requirements for building and serving (locally) the documentation and running unit tests.

The second line installs the `pre-commit` hooks defined in the `.pre-commit-config.yaml` file.
`pre-commit` is a tool that runs immediately prior to you creating new commits (`git commit`), and checks all the changes, automatically updates the API reference in the documentation and much more.
Mainly, it helps to ensure that the package stays nicely formattet, safe, and user-friendly for developers.

#### Non-Python dependencies

There are a few non-Python dependencies that EMMOntoPy relies on as well.
These can be installed by running (on a Debian system):

```console
sudo apt-get update && sudo apt-get install -y graphviz openjdk-11-jre-headless
```

If you are on a non-Debian system (Debian, Ubuntu, ...), please check which package manager you are using and find packages for `graphviz` and `openjdk` minimum version 11.

## Test the installation

It is good practice to test the integrity of the installation and that all necessary dependencies are correctly installed.

You can run unit tests, to check the integrity of the Python functionality, by running:

```console
pytest
```

If all has installed and is running correctly, you should not have any failures, but perhaps some warnings (deprecation warnings) in the test summary.
