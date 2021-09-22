# Welcome to Netspy

<p align="center">
    <em>Networks of Transcribed Speech in Python</em>
</p>

---

**Documentation**: <a href="" target="_blank"></a>

**Source Code**: <a href="https://github.com/alan-turing-institute/netspy" target="_blank">https://github.com/alan-turing-institute/netspy</a>

---

Netspy is a package and CLI for constructing semantic speech networks from speech transcripts.

## Getting started

Install development version:

```bash
pip install git+https://github.com/alan-turing-institute/netspy
```


## Install Dependencies

Netspy requires additional dependencies to run. You can install them either directly from the netspy CLI or in Python. 


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
