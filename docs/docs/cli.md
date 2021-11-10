# CLI

## CLI Arguments

When you install the netts package, you also get the `netts` commandline interface (CLI). To see all of the commands and options for the CLI, run:

```bash
netspy --help
```

Each `netts` sub command also supports the `--help` option.

## The Run Command

The `netts run` command will process a transcript (or directory of transcripts), building semantic [MultiDiGraphs](https://networkx.org/documentation/stable/reference/classes/multidigraph.html) and saving them as [pickled](https://docs.python.org/3/library/pickle.html#module-pickle) Python objects to the specified output directory. By default, netspy will also draw the graphs and save them in `.png` format next to the pickled objects.

```bash
netspy run my_transcripts output_folder
```

```text
my_transcripts/
├─ transcript_1.txt
├─ transcript_2.txt

output_folder/
├─ transcript_1.pickle
├─ transcript_1.png
├─ transcript_2.pickle
├─ transcript_2.png
```

The `netspy run`command has a few optional parameters:

### Pattern

You can pass a [glob pathname](https://docs.python.org/3/library/glob.html) to filter files to process in a directory. For example, if we only wanted to process files in `INPUT_DIR` with the suffix `_monday.txt`, we could use:

=== "CLI"

```bash
netts run DIRECTORY OUTPUT_DIR --pattern "*_monday.txt"
```

### Force

By default netts will not reprocess a file if it already exists in the output dir. If you wish to reprocess it again add the `--force` flag.

=== "CLI"

```bash
netspy run INPUT_DIR_OR_FILE OUTPUT_DIR --force
```

### Figure

By default `netspy run` will create a figures and output them to `OUTPUT_DIR`. If you don't want figures, add the `--no-figure` flag:

=== "CLI"

```bash
netspy run INPUT_DIR_OR_FILE OUTPUT_DIR --no-figure
```

You can also change the figure format, which will except any format supported by [Matplotlib](https://matplotlib.org/2.1.2/api/_as_gen/matplotlib.pyplot.savefig.html#:~:text=One%20of%20the%20file%20extensions,%2C%20ps%2C%20eps%20and%20svg.&text=If%20True%2C%20the%20axes%20patches,edgecolor%20are%20specified%20via%20kwargs.):

=== "CLI"

```bash
netspy run INPUT_DIR_OR_FILE OUTPUT_DIR --fig-format .jpeg
```
