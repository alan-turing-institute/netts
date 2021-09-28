### Processing single transcripts

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
    netspy run transcript.txt outputs
    ```

=== "Python"

    ```python
    import netspy

    with open("transcript.txt") as f:
        transcript = f.read()

    graph = netspy.speech_graph(transcript)
    ```
