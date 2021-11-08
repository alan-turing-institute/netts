# CLI

## CLI Arguments

The command `netts run` has a few optional parameters:

### Pattern

You can pass a [glob pathname](https://docs.python.org/3/library/glob.html) to filter files to process in a directory. For example if we only wanted to process files with the suffix `_monday.txt`:

=== "CLI"

```bash
netts run DIRECTORY OUTPUT_DIR --pattern "*_monday.txt"
```

### Force

By default netts will not reprocess a file if it already exists in the output dir. If you wish to reprocess it again add the `--force` flag.

=== "CLI"

```bash
netts run DIRECTORY OUTPUT_DIR --force
```

### Figure

By default `netts run` will create a figure and output it to `OUTPUT_DIR`. If you don't want a figure add the `--no-figure` flag

=== "CLI"

```bash
netts run DIRECTORY OUTPUT_DIR --no-figure
```

You can also change the figure format, which will except any format supported by [Matplotlib](https://matplotlib.org/2.1.2/api/_as_gen/matplotlib.pyplot.savefig.html#:~:text=One%20of%20the%20file%20extensions,%2C%20ps%2C%20eps%20and%20svg.&text=If%20True%2C%20the%20axes%20patches,edgecolor%20are%20specified%20via%20kwargs.):

=== "CLI"

```bash
netts run DIRECTORY OUTPUT_DIR --fig-format .jpeg
```
