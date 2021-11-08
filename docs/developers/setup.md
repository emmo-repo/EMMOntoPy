# Development environment

<!-- markdownlint-disable MD046 MD014 -->

This section outlines some suggestions as well as conventions used by the EMMOntoPy developers, which should be considered or followed if one wants to contribute to the package.

## Setup

!!! important "Requirements"
    This section expects you to be running on a Unix-like system (e.g., Linux) with *minimum* Python 3.6.

### Virtual environment

Since development can be messy, it is good to separate the development environment from the rest of your system's environment.

To do this, you can use a virtual environment.
There are a several different ways to create a virtual environment, but we recommend using either `virtualenv` or `venv`.

!!! tip "Virtual environment considerations"
    There are several different virtual environment setups, here we only address a very few.

    A great resource for an overview can be found in [this StackOverflow answer](https://stackoverflow.com/a/41573588/12404091){:target="_blank" rel="noopener"}.
    However, note that in the end, it is very subjective on the solution one uses and one is not necessarily "better" than another.

=== "`virtualenv` (recommended)"

    To install `virtualenv`+`virtualenvwrapper` run:

    ```console
    $ pip install virtualenvwrapper
    ```

    There is other setup, most of which only needs to be run once.
    For more information about this, see the [`virtualenvwrapper` documentation](https://virtualenvwrapper.readthedocs.io/en/latest/#introduction){:target="_blank" rel="noopener"}.

    After successfully setting up `virtualenv` through `virtualenvwrapper`, you can create a new virtual environment:

    ```console
    $ mkproject -p python3.7 emmo-python
    ```

    !!! note
        If you do not have Python 3.7 installed (or instead want to use your system's default Python version), you can leave out the extra `-p python3.7` argument.  
        Or you can choose to use another version of Python by changing this argument to another (valid) python interpreter.

    Then, if the virtual environment has not been activated automatically (you should see the name `emmo-python` in a parenthesis in your console), you can run:

    ```console
    $ workon emmo-python
    ```

    !!! tip
        You can quickly see a list of all your virtual environments by writing `workon ` and pressing ++tab++ twice.

    To deactivate the virtual environment, returning to the system/global environment again, run:

    ```console
    (emmo-python) $ deactivate
    ```

=== "`venv`"

    `venv` is a built-in package in Python, which works similar to `virtualenv`, but with fewer capabilities.

    To create a new virtual environment with `venv`, first go to the directory, where you desire to keep your virtual environment.
    Then run the `venv` module using the Python interpreter you wish to use in the virtual environment.
    For Python 3.7 this would look like the following:

    ```console
    $ python3.7 -m venv emmo-python
    ```

    A folder with the name `emmo-python` containing the environment is created.

    To activate the environment run:

    ```console
    $ ./emmo-python/activate
    ```

    or

    ```console
    $ /path/to/emmo-python/activate
    ```

    You should now see the name `emmo-python` in a parenthesis in your console, letting you know you have activated and are currently using the `emmo-python` virtual environment.

    To deactivate the virtual environment, returning to the system/global environment again, run:

    ```console
    (emmo-python) $ deactivate
    ```

!!! important "Expectation"
    From here on, all commands expect you to have activated your virtual environment, if you are using one, unless stated otherwise.

### Installation

To install the package, please do **not** install from PyPI.
Instead you should clone the repository from GitHub:

```console
$ git clone https://github.com/emmo-repo/EMMO-python.git
```

or, if you are using an SSH connection to GitHub, you can instead clone via:

```console
$ git clone git@github.com:emmo-repo/EMMO-python.git
```

Then enter into the newly cloned `EMMO-python` directory (`cd EMMO-python`) and run:

```console
$ pip install -U -e .[dev]
$ pre-commit install
```

This will install the EMMOntoPy Python package, including all dependencies and requirements for building and serving (locally) the documentation and running unit tests.

The second line installs the `pre-commit` hooks defined in the `.pre-commit-config.yaml` file.
`pre-commit` is a tool that runs immediately prior to you creating new commits (`git commit`), and checks all the changes, automatically updates the API reference in the documentation and much more.
Mainly, it helps to ensure that the package stays nicely formattet, safe, and user-friendly for developers.

#### Non-Python dependencies

There are a few non-Python dependencies that EMMOntoPy relies on as well.
These can be installed by running (on a Debian system):

```console
$ sudo apt-get update && sudo apt-get install -y graphviz openjdk-11-jre-headless
```

If you are on a non-Debian system (Debian, Ubuntu, ...), please check which package manager you are using and find packages for `graphviz` and `openjdk` minimum version 11.

## Test the installation

It is good practice to test the integrity of the installation and that all necessary dependencies are correctly installed.

You can run unit tests, to check the integrity of the Python functionality, by running:

```console
$ pytest
```

If all has installed and is running correctly, you should not have any failures, but perhaps some warnings (deprecation warnings) in the test summary.
