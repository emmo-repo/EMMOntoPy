# EMMO-python Docker

### Clone project

```bash
git clone git@github.com:emmo-repo/EMMO-python.git
```

### Build Docker image

```bash
cd EMMO-python
docker build -t emmo .
```

### Run Docker container

```bash
docker run -it emmo
```

### Notes

* Your Docker container may run out of memory while executing HermiT
  (``sync_reasoner``). Append ``--memory=2GB`` to ``docker run`` in
  order to align the memory limit with the Java runtime environment.

* Uncomment the last line in Dockerfile if you wish to start directly
  in python. 
