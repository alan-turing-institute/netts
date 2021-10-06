### Processing transcripts

Netspy takes speech transcripts and converts them into a semantic graph. Imagine we have the following short transcript in a file called `transcript.txt`:

> There are two… There is a young girl and who and seems to be maid, sitting on a couch. The little girl seems to be upset, she’s looking away and she looks very dismissive.

<details>
Create this example file by running the following command in a terminal
```bash
echo "There are two… There is a young girl and who and seems to be maid, sitting on a couch. The little girl seems to be upset, she’s looking away and she looks very dismissive." > transcript.txt
```
</details>

We can the process the file

=== "CLI"

    ```bash
    netspy run transcript.txt OUTPUT_DIR
    ```
=== "Python"

    ```python
    import netspy

    with open("transcript.txt") as f:
        transcript = f.read()

    graph = netspy.SpeechGraph(transcript).process()
    ```


where `OUTPUT_DIR` is the name of a directory to output files to. If it does not exist netspy will create it.

<details>
The Python example does not save to directory
```
</details>


The CLI also allows you to process a directory of transcripts:

=== "CLI"

    ```bash
    netspy run DIRECTORY OUTPUT_DIR
    ```

where `DIRECTORY` is the name of the directory you wish to output to.

### CLI Arguments

The command `netspy run` has a few optional parameters:

#### Pattern
You can pass a [glob pathname](https://docs.python.org/3/library/glob.html) to filter files to process in a directory. For example if we only wanted to process files with the suffix `_monday.txt`:

=== "CLI"

    ```bash
    netspy run DIRECTORY OUTPUT_DIR --pattern "*_monday.txt"
    ```

#### Force

By default netspy will not reprocess a file if it already exists in the output dir. If you wish to reprocess it again add the `--force` flag.

=== "CLI"

    ```bash
    netspy run DIRECTORY OUTPUT_DIR --force
    ```

#### Figure
By default `netspy run` will create a figure and output it to `OUTPUT_DIR`. If you don't want a figure add the `--no-figure` flag

=== "CLI"

    ```bash
    netspy run DIRECTORY OUTPUT_DIR --no-figure
    ```

You can also change the figure format, which will except any format supported by [Matplotlib](https://matplotlib.org/2.1.2/api/_as_gen/matplotlib.pyplot.savefig.html#:~:text=One%20of%20the%20file%20extensions,%2C%20ps%2C%20eps%20and%20svg.&text=If%20True%2C%20the%20axes%20patches,edgecolor%20are%20specified%20via%20kwargs.):

=== "CLI"

    ```bash
    netspy run DIRECTORY OUTPUT_DIR --fig-format .jpeg
    ```
