from continuumio/miniconda3

RUN apt update && apt install -y texlive-latex-extra pandoc gcc gcj-jre
RUN conda install -c conda-forge graphviz
RUN pip install Cython pydot ase Owlready2

RUN useradd -ms /bin/bash user
COPY . /home/user/EMMO-python
RUN chown user:user -R /home/user/EMMO-python/
USER user
WORKDIR /home/user/
ENV PYTHONPATH "/home/user/EMMO-python/:${PYTHONPATH}"
#ENTRYPOINT python
