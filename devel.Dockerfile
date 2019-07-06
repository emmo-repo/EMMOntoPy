from continuumio/miniconda3

RUN apt update && apt install -y texlive-latex-extra pandoc gcc gcj-jre
RUN conda install -c conda-forge graphviz
RUN pip install Cython pydot ase Owlready2==0.10

RUN useradd -ms /bin/bash user
USER user
WORKDIR /home/user/
ENV PYTHONPATH "/home/user/emmo/:${PYTHONPATH}"

