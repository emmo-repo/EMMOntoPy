# Visualise an ontology using pyctoscape in Jupyter Notebook

## Installation instructions

In a terminal, run:

```shell
cd /path/to/env/dirs
python -m venv cytopy  # cytopy is my name, you can choose what ouy want
source cytopy/bin/activate
cd /dir/to/EMMO-python/
pip install -e .
pip install jupyterlab
python -m ipykernel install --user --name=cytopy
pip install ipywidgets
pip install nodejs # Note requires that node.js and npm has already been isntalled!
pip install ipycytoscape pydotplus networkx
pip install --upgrade setuptools
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

## Test the notebook

In a terminal, run:

```shell
jupyter-lab
```

That should start jupyter kernel and open a new tab in your browser.
In the side pane, select `team40.ipynb` and run the notebook.
