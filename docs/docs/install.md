
### Install with pip

```bash
pip install netspy
```

### Development Version

If you would like the latest development version of netspy install it from GitHub. This code may change at anytime.

```bash
pip install git+https://github.com/alan-turing-institute/netspy
```


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

> Dependencies are large (>5Gb) and may take some time to download.

### Install to alternative directory

By default these will install to a `netspy` directory in your home directory. If you would like to install in a different location set an environment variable called `NETSPY_DIR`.

```bash
export NETSPY_DIR={DIRECTORY}
```

or create a file in the netspy root directory called `.env`

```bash
NETSPY_DIR={DIRECTORY}
```

> netspy will create the `NETSPY_DIR` if it does not exist.

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
