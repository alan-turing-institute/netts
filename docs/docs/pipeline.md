# Pipeline

---


**Networks of Transcript Semantics (netts)** is a network algorithm that builds on state-of-the-art Natural Language Processing libraries to create speech networks that capture semantic content.
Netts takes transcripts of spoken text as input (e.g. <em>I see a man</em>) and outputs a semantic speech network.


> **_Semantic Speech Network:_**  Network that represents the semantic content of speech transcripts. In these networks, nodes are entities (e.g. <em>I</em>, <em>man</em>). Edges are relations between nodes (e.g. <em>see</em>).

<!-- __Networks of Transcript Semantics (netts)__ is a package for constructing semantic speech networks from speech transcripts. -->

<img src="/img/tool_pipeline.png" width=95% style="margin-left: auto; margin-right: auto; display: block;">

<p align="center">
    <em>Netts pipeline.</em>
</p>





Netts can capture semantic links between nodes in speech content, even when semantically these nodes are separated by several sentences.
The algorithm is robust against artefacts typical for spoken text.
As described in [Usage](basic_usage.md), netts can be used to process a single transcript or a folder of many transcripts.
With about 40 seconds processing time per speech transcript, netts takes little time to process large batches of speech transcripts and therefore is ideal for the automated construction of speech networks from large datasets.

In the following sections the netts processing pipeline is described in detail.
See figure above for an overview of the netts pipeline.

## Preprocessing
Netts first expands the most common English contractions (e.g. expanding <em>I'm</em> to <em>I am</em>).
It then removes interjections (<em>Mh</em>, <em>Uhm</em>).
Netts also removes any transcription notes (e.g. timestamps, <em>[inaudible]</em>) that were inserted by the transcriber.
The user can pass a file of transcription notes that should be removed from the transcripts before processing.
See [Configuration](configuration.md) for a step-by-step guide on passing custom transcription notes to netts for removal.
Netts does not remove stop words or punctuation to stay as close to the original speech as possible.

Netts then uses [CoreNLP](https://stanfordnlp.github.io/CoreNLP/) to perform sentence splitting, tokenization, part of speech tagging, lemmatization, dependency parsing and co-referencing on the transcript.
Netts uses the default language model implemented in CoreNLP.

We describe these Natural Language Processing steps briefly in the following.
The transcript is first split into sentences (sentence splitting).
It is then further split into meaningful entities, usually words (tokenization).
Each word is assigned a part of speech label.
The part of speech label indicates whether the word is a verb, noun, or another part of speech (part of speech tagging).
Each word is also assigned their dictionary form or lemma (lemmatization).
Next, the grammatical relationship between words is identified (dependency parsing).
Finally, any occurrences where two or more expressions in the transcript refer to the same entity are identified (co-referencing).
For example where a noun <em>man</em> and a pronoun <em>he</em> refer to the same person.

## Finding nodes and edges
Netts submits each sentence to [OpenIE5](https://github.com/dair-iitd/OpenIE-standalone) for relation extraction.
Openie5 extracts semantic relationships between entities from the sentence.
For example, performing relation extraction on the sentence <em>I see a man</em> identifies the relation <em>see</em> between the entities <em>I</em> and <em>a man</em>.
From these extracted relations, netts creates an initial list of the edges that will be present in the semantic speech network.
In the edge list, the entities are the nodes and the relations are the edge labels.

Next, netts uses the part of speech tags and dependency structure to extract edges defined by adjectives or prepositions:
For instance, <em>a man on the picture</em> contains a preposition edge where the entity <em>a man</em> and <em>the picture</em> are linked by an edge labelled <em>on</em>.
An example of an adjective edge would be <em>dark background</em>.
Here, <em>dark</em> and <em>background</em> are linked by an implicit <em>is</em>.
These adjective edges and preposition edges are added to the edge list.
During the next processing steps this edge list is further refined.

## Refining nodes and edges
After creating the edge list, netts uses the co-referencing information to merge nodes that refer to the same entity.
This is to take into account cases different words refer to the same entity.
For example in the case where the pronoun <em>he</em> is used to refer to <em>a man</em> or in the case where the synonym <em>the guy</em> is used to refer to <em>a man</em>.
Every entity mentioned in the text should be represented by a unique node in the semantic speech network.
Therefore, nodes referring to the same entity are merged by replacing the node label in the edge list with the most representative node label (first mention of the entity that is a noun).
In the example above, <em>he</em> and <em>the guy</em> would be replaced by <em>a man</em>.
Node labels are then cleaned of superfluous words such as determiners.
For example, <em>a man</em> would turn into <em>man</em>.

## Constructing network
In the final step, netts constructs a semantic speech network from the edge list using [networkx](https://networkx.org/).
The network is then plotted and saves the output.
The output consists of the networkx object, the network image and the log messages from netts.
The resulting graphs are directed and unweighted, and can have parallel edges and self-loops (as it is a [MultiDiGraph](https://networkx.org/documentation/stable/reference/classes/multidigraph.html)).
Parallel edges are two or more edges that link the same two nodes in the same direction.
A self-loop is an edge that links a node with itself.
See [here](index.md) for an example semantic speech network along with the corresponding speech transcript and stimulus picture.