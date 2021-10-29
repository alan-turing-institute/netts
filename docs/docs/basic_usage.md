# Overview

Netspy takes speech transcripts and converts them into a semantic graph. Imagine we have the following short transcript in a file called `transcript.txt`:

> I see a man in the dark standing against a light post. It seems to be in the middle of the night; I think because the lightbulb is working. On the picture there seems to be like a park and... Or trees but in those trees there are little balls of light reflections as well. I cannot see the… Anything else because it’s very dark. But the man on the picture seems to wear a hat and, and has a jacket on and he seems to have a hoodie on as well. The picture is very, very mysterious, which I like about it, but for me I would like to understand more concept, context of the picture.

<details>
<summary>Follow along</summary>
To follow along create this example in a file by running the following command in a terminal

```bash
echo "I see a man in the dark standing against a light post. It seems to be in the middle of the night; I think because the lightbulb is working. On the picture there seems to be like a park and... Or trees but in those trees there are little balls of light reflections as well. I cannot see the… Anything else because it’s very dark. But the man on the picture seems to wear a hat and, and has a jacket on and he seems to have a hoodie on as well. The picture is very, very mysterious, which I like about it, but for me I would like to understand more concept, context of the picture." > transcript.txt
```

</details>

## Create a semantic graph

We can create a semantic graph from the transcript using either the CLI of python package

=== "CLI"

```bash
netspy run transcript.txt outputs
```

=== "Python"

```python
import netspy

with open("transcript.txt") as f:
    transcript = f.read()

graph = netspy.SpeechGraph(transcript).process()

```

`netspy run` is the CLI command. The first argument `transcript.txt` is the file or directory to process, and the second argument `outputs` is the name of a directory to output the results to. If the output directory doesn't exist netspy will create it.

The output directory will contain two files:

```text
outputs/
    transcript.pickle
    transcript.png
```

The file prefix is taken from the input file (in this case <code><ins style="color: green; text-decoration-color: green;">transcript</ins>.txt</code>)

<code>transcript<ins style="color: blue; text-decoration-color: blue;">.pickle</ins></code>: A NetworkX [MiltiDiGraph](https://networkx.org/documentation/stable/reference/classes/multidigraph.html) object.

<code>transcript<ins style="color: orange; text-decoration-color:orange;">.png</ins></code>: A plot of the graph.

## Process a directory of transcripts

If you have a folder of transcripts you can process the entire folder with the CLI. For example, if you have a folder called `all_transcripts`:

```text
all_transcripts/
    transcript_1.txt
    transcript_2.txt
    ...
```

you can process it with

=== "CLI"

```bash
netspy run all_transcripts outputs
```

=== "Python"

```python
from pathlib import Path
import netspy

directory = "all_transcripts"
all_transcripts = Path(directory).glob("*.txt")

all_graphs = []
for trans in all_transcripts:
    with open(trans) as f:
        transcript = f.read()

    graph = netspy.SpeechGraph(transcript).process()
    all_graphs.append(graph)
```

## Load pickled graphs into python

If you processed transcripts with the netspy CLI you may want to load the pickled graph object into Python for further analysis.

```python
python
```
