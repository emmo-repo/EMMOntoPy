# EMMOntoPy Docker

## Clone project

```bash
git clone git@github.com:emmo-repo/EMMOntoPy.git
```

## Build Docker image

```bash
cd EMMOntoPy
docker build -t emmo .
```

## Run Docker container

```bash
docker run -it emmo
```

## Notes

* Your Docker container may run out of memory while executing the HermiT reasoner (`sync_reasoner`).
  Append `--memory=2GB` to `docker run` in order to align the memory limit with the Java runtime environment.

  It is recommended to instead use the FaCT++ reaonser (now default).

* Uncomment the last line in the Dockerfile, if you wish to start directly in the Python interpreter.

## Dockerfile for mounting EMMOntoPy as volume (mount.Dockerfile)

### Build Docker image (mount.DockerFile)

```bash
docker build -t emmomount -f mount.Dockerfile .
```

### Run Docker container (mount.Dockerfile)

In a unix terminal (Linux)

```bash
docker run --rm -it -v $(pwd):/home/user/EMMOntoPy emmomount
```

In PowerShell (Windows 10):

```PowerShell
docker run --rm -it -v ${PWD}:/home/user/EMMOntoPy emmomount
```

To install EMMOntoPy package inside container:

```bash
cd EMMOntoPy
pip install .
```

### Notes on mounting on Windows

* Allow for mounting of C: in Docker (as administrator).
  Docker (rightclick in system tray) -> Settings -> Shared Drives -> tick of C -> Apply.

* Run the following command in PowerShell:

  ```PowerShell
  Set-NetConnectionProfile -interfacealias "vEthernet (DockerNAT)" -NetworkCategory Private
  ```

* If mounting does not succeed Reset Credentials (Docker -> Settings -> Shared Drives)  and repeat the steps above.
