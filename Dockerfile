from continuumio/miniconda3
RUN apt update && apt install -y texlive-latex-extra texlive-xetex graphviz
RUN wget https://github.com/jgm/pandoc/releases/download/2.1.2/pandoc-2.1.2-1-amd64.deb && apt install -y ./pandoc-2.1.2-1-amd64.deb
RUN pip install --upgrade pip

RUN useradd -ms /bin/bash user
COPY . /home/user/EMMO-python
RUN cd /home/user/EMMO-python && pip install -e . && cd -
RUN chown user:user -R /home/user/EMMO-python/
USER user
WORKDIR /home/user/
#ENTRYPOINT python
