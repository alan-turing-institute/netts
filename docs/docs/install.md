# Getting Started

## Install netspy

### Latest Stable Release

To install the latest official release from PyPI:

```bash
pip install netspy
```

### Development Version

To install the latest development version, install it from GitHub:

```bash
pip install git+https://github.com/alan-turing-institute/netspy
```

Be aware that this code may change or break at anytime.

## Install Additional Dependencies

Netspy requires additional dependencies including [CoreNLP](https://stanfordnlp.github.io/CoreNLP/) and [OpenIE](https://github.com/dair-iitd/OpenIE-standalone). You can install them either directly from the netspy CLI or in Python.

=== "CLI"

```bash
netspy install
```

=== "Python"

```python
import netspy
netspy.install_dependencies()
```

Dependencies are large (>5Gb) and may take some time to download.

### Install to an Alternative Directory

By default, the dependencies will be installed to a `netspy` directory in your home directory. If you would like to install in a different location, set an environment variable called `NETSPY_DIR` either on the commandline:

```bash
export NETSPY_DIR={DIRECTORY}
```

or by creating a `.env` file in your working directory with these contents:

```bash
NETSPY_DIR={DIRECTORY}
```

netspy will create `NETSPY_DIR` for you if it doesn't already exist.

To verify which directory netspy will use run:

=== "CLI"

```bash
netspy home
```

=== "Python"

```python
import netspy
settings = netspy.get_settings()
print(settings.netspy_dir)
```
