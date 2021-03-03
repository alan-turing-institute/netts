# language_analysis
Scripts for language analysis project completed during my postdoc work in the Cambridge Brain Mapping Unit.

Toolbox creates semantic speech graphs from transcribed speech. Speech transcripts are short paragraphs of largely raw, uncleaned speech-like text. For example:

> 'I see a man in the dark standing against a light post. It seems to be in the middle of the night; I think because the lightbulb is working. On the picture there seems to be like a park and... Or trees but in those trees there are little balls of light reflections as well. I cannot see the… Anything else because it’s very dark. But the man on the picture seems to wear a hat and, and has a jacket on and he seems to have a hoodie on as well. The picture is very, very mysterious, which I like about it, but for me I would like to understand more concept, context of the picture.'
> -- <cite>Example Transcript</cite>

Below is the semantic speech graph constructed from this text.

![Semantic speech graph example](semantic_speech_graph_example.png)
*Figure 1. Example Speech Graph. Nodes represents an entity mentioned by the speaker (e.g. I, man, jacket). Edges represent relations between nodes mentioned by the speaker (e.g. see, has on).*

