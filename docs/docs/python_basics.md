# Netts package

If you dont want to use the netts command line interface (CLI) or want more control over netts you can use the netts python package directly. Here we'll run through the [CLI example](/cli_basics) in Python.

Make sure you have a transcript in your working directory.

<details>
<summary>Follow along - Example transcript</summary>
To follow along create this example in a file by running the following command in a terminal

```bash
echo "I see a man and he is wearing a jacket. He is standing in the dark against a light post. On the picture there seems to be like a park and... Or trees but in those trees there are little balls of light reflections as well. I cannot see the... Anything else because it’s very dark. But the man on the picture seems to wear a hat and he seems to have a hoodie on as well. The picture is very mysterious, which I like about it, but for me I would like to understand more about the picture." > transcript.txt
```

</details>

## Process a single transcript

We can then process a single transcript using the following Python script, which we'll run through step by step.

```python hl_lines="5-7"
--8<-- "process_transcript.py"
```

First we load a `Settings` object which provides information about the netts configuration. We then check where netts will install addition dependencies, and finally download them. This can take a long time (~20min), so time to put the kettle on.

!!! info
    If the dependencies have already been installed this function will do nothing.

### Start the CoreNLP and OpenIE5 servers

```python hl_lines="9-11"
--8<-- "process_transcript.py"
```

Netts uses [Openie5](https://github.com/dair-iitd/OpenIE-standalone) and [CoreNLP](https://stanfordnlp.github.io/CoreNLP/) under the hood. These are both [Java](https://en.wikipedia.org/wiki/Java_(programming_language)) programmes that we installed in the previous step. We use a [context manager](https://book.pythontips.com/en/latest/context_managers.html) to start the servers, which makes sure they are both automatically shut down when processing finishes.

!!! warning
    The servers are extremely memory hungry, using ~8GB. If the server fails to start you probably ran out of memory and failed silently. Try on a machine with more memory.

### Process a transcript

```python hl_lines="13-22"
--8<-- "process_transcript.py"
```

Next we load our transcript into memory, create a `SpeechGraph` object and then call its `process` method, passing our two servers and a configuration object.

Here we use a default configuration object `settings.netts_config.preprocess`.

### Plot graph and save outputs

```python hl_lines="24-30"
--8<-- "process_transcript.py"
```

Finally we plot our graph, save it to file and also [pickle](https://docs.python.org/3/library/pickle.html) our graph object for further analysis later.

### Refining the plot

The network is plotted using [spring-embedding](https://en.wikipedia.org/wiki/Force-directed_graph_drawing), which tries to plot the network such that you get the least overlapping of nodes and edges with each other. This also means that each time you plot the network, it will look slightly different. If you are not happy with the way your network is plotted, try re-running the last few lines of code and look at the transcript.png image file again:

```python
fig, ax = plt.subplots()
graph.plot_graph(ax)

plt.savefig("transcript.png")
```

You can also open the figure in an interactive window by running:

```python
fig, ax = plt.subplots()
graph.plot_graph(ax)

plt.show()
```

When resizing the window, we see that the network automatically adjusts to the new window size and the nodes and edges spread out. This usually helps visualisation a lot. We therefore recommend trying out this step when processing your first few transcripts and inspecting the networks.
