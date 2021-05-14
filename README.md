# Cambridge Language Analysis (Netspy)
Toolbox for semantic speech graph construction.

This toolbox was built as part of an ongoing project investigating the potential of [speech markers to predict psychosis risk](https://www.turing.ac.uk/research/research-projects/towards-incoherent-speech-predictor-psychosis-risk) funded by the [Alan Turing Institute](https://www.turing.ac.uk) and led by [Sarah Morgan](https://www.neuroscience.cam.ac.uk/directory/profile.php?SarahMorgan) at the [University of Cambridge](https://www.cam.ac.uk). Tools were written by [Caroline Nettekoven](https://www.neuroscience.cam.ac.uk/directory/profile.php?caronettekoven) at the  [Cambridge Brain Mapping Unit](http://www.bmu.psychiatry.cam.ac.uk).

The algorithms in this toolbox create a semantic speech graph from transcribed speech. Speech transcripts are short paragraphs of largely raw, uncleaned speech-like text. For example:

> 'I see a man in the dark standing against a light post. It seems to be in the middle of the night; I think because the lightbulb is working. On the picture there seems to be like a park and... Or trees but in those trees there are little balls of light reflections as well. I cannot see the… Anything else because it’s very dark. But the man on the picture seems to wear a hat and, and has a jacket on and he seems to have a hoodie on as well. The picture is very, very mysterious, which I like about it, but for me I would like to understand more concept, context of the picture.'
> -- <cite>Example Transcript</cite>

Below is the semantic speech graph constructed from this text.

![Semantic speech graph example](semantic_speech_graph_example.png)
*Figure 1. Semantic Speech Graph. Nodes represents an entity mentioned by the speaker (e.g. I, man, jacket). Edges represent relations between nodes mentioned by the speaker (e.g. see, has on).*

# Pipeline
- Construct semantic graphs from transcripts by running speech_graph.py on the transcript
  - For example, create semantic graph for the fourth transcript in the dataset by running python ./speech_graph.py 3 
  - Or run speech_graph.py in bulk by running graph_tats.sh script
- Describe graphs using describe_graphs.py (Creates graphs_data.csv)
  - Plot basic graph measures using basic_graph_analysis.ipynb notebook
- Count motifs in graphs by running motifs.py (Creates motif_counts.csv)
  - Plot motif count measures using motif_analysis.ipynb notebook