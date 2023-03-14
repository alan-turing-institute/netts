# Getting Started

## Install netts

### Latest Stable Release

To install the latest official release from PyPI:

```bash
pip install netts
```

### Development Version

If you would like the latest development version of netts install it from GitHub. This code may change at anytime.

```bash
pip install git+https://github.com/alan-turing-institute/netts
```

!!! warning
    Be aware that the development code is under active development and may change at any time.

## Install Additional Dependencies

Netts requires the Java Runtime Environment. Instructions for downloading and installing for your operating system can be found [here](https://docs.oracle.com/goldengate/1212/gg-winux/GDRAD/java.htm#BGBFHBEA).

Netts requires additional dependencies including [CoreNLP](https://stanfordnlp.github.io/CoreNLP/) and [OpenIE](https://github.com/dair-iitd/OpenIE-standalone). You can install them either directly from the netts CLI or in Python.

=== "CLI"

```bash
netts install
```

=== "Python"

```python
import netts
netts.install_dependencies()
```

!!! info
    Dependencies are large (>5GB) and may take some time to download.

### Install to an Alternative Directory

By default, the dependencies will be installed to a `netts` directory in your home directory. If you would like to install in a different location, set an environment variable called `NETTS_DIR` either on the commandline:

```bash
export NETTS_DIR={DIRECTORY}
```

or by creating a `.env` file in your working directory with these contents:

```bash
NETTS_DIR={DIRECTORY}
```

netts will create `NETTS_DIR` for you if it doesn't already exist.

To verify which directory netts will use run:

=== "CLI"

```bash
netts home
```

=== "Python"

```python
import netts
settings = netts.get_settings()
print(settings.netts_dir)
```
