# Pipeline


---

__Networks of Transcript Semantics (netts)__ is a package for constructing semantic speech networks from transcribed speech.

<img src="/img/tool_pipeline.png" width=95% style="margin-left: auto; margin-right: auto; display: block;">

<p align="center">
    <em>netts pipeline</em>
</p>



**Netts** is a network algorithm that builds on state-of-the-art Natural Language Processing libraries to create speech networks that capture semantic content.
Netts takes transcripts of spoken text as input (e.g. <em>I see a man</em>) and outputs the semantic speech network (Figure \ref{fig:ExampleGraph}).


> **_Semantic Speech Network:_**  Nodes are entities (e.g. <em>I</em>, <em>man</em>). Edges are relations between nodes (e.g. <em>see</em>).


The algorithm can capture information content in speech, even when semantically connected nodes are separated by several sentences.
Netts is fast (~ 40 seconds processing time per speech excerpt) and is robust against artefacts typical for transcribed speech, lending itself to the automated construction of speech networks from large datasets.
In the following we describe how netts processes a speech transcript to construct the semantic speech network.
The processing pipeline is shown in Figure \ref{fig:Pipeline}.



## Preprocessing
Netts starts by expanding the most common English contractions (e.g. expanding <em>I'm</em> to <em>I am</em>), removing interjections (<em>Mh</em>, <em>Uhm</em>) and removing any transcription notes (e.g. timestamps, <em>[inaudible]</em>) that were inserted by the transcriber.
No stop words or punctuation are removed to stay as close to the original speech as possible.
This and other processing steps are customizable in netts, e.g. with the option to pass a user-defined text file of transcription notes that should be ignored by netts.

Netts uses CoreNLP to perform sentence splitting, tokenization, part of speech tagging, lemmatization, dependency parsing and co-referencing on the transcript \cite{Manning2015} with the default language model implemented in CoreNLP.
These Natural Language Processing techniques are briefly described in the following.
The transcript is first split into sentences (sentence splitting) and further split into meaningful entities, usually words (tokenization).
Each word is then assigned a part of speech label, indicating whether it is a verb, noun, or another part of speech (part of speech tagging).
Each word is also assigned their dictionary form or lemma (lemmatization) and the grammatical relationship between words is identified (dependency parsing).
Finally, any occurrences where two or more expressions in the transcript refer to the same entity are identified (co-referencing), for example where a noun <em>man</em> and a pronoun <em>he</em> refer to the same person.

## Finding nodes and edges
Netts then submits each sentence to OpenIE5 for relation extraction \cite{Mausam2012a}, where semantic relationships between entities are extracted from the sentence.
For example, performing relation extraction on the sentence <em>I see a man</em> identifies the relation <em>see</em> between the entities <em>I</em> and <em>a man</em>.
From these extracted relations, our tool creates an initial list of the edges which should be present in the semantic speech network.
In the edge list, the entities are the nodes and the relations are the edge labels.

Next, netts uses the previously identified part of speech tags and dependency structure  to extract edges defined by adjectives or prepositions: For instance, <em>a man on the picture</em> contains a preposition edge where the entity <em>a man</em> and <em>the picture</em> are linked by an edge labelled <em>on</em>.
An example of an adjective edge would be <em>dark background</em>, where <em>dark</em> and <em>background</em> are linked by an implicit <em>is</em>.
These adjective edges and preposition edges are added to the edge list.
%- Nodes that include another edge (for example a preposition edge) get split into two nodes connected by the preposition.

This edge list is further refined during the next processing steps.

## Refining nodes and edges
After creation of the edge list, netts uses the previously identified co-referencing structure to merge nodes that refer to the same entity.
This is to account for cases where entities are referred to with different words, for example using the pronoun <em>he</em> to refer to <em>a man</em> or using the synonym <em>the guy</em> to refer to <em>a man</em>.
To ensure that every entity mentioned in the text is represented by a unique node in the semantic speech network, nodes referring to the same entity are merged by replacing the node label in the edge list with the most representative node label (first mention of the entity that is a noun).
In our example, this would mean <em>he</em> and <em>the guy</em> would be replaced by <em>a man</em>.

Node labels are then cleaned of superfluous words such as determiners, e.g. replacing <em>a man</em> with <em>man</em>.

## Constructing network
Finally, netts constructs a semantic speech network from the edge list using networkx and the network is plotted and the output consisting of the networkx object, the network image and the tool output messages saved \cite{networkx}.
The resulting graphs are directed and unweighted, and can have parallel edges and self-loops.
Parallel edges are two or more edges that link the same two nodes in the same direction.
A self-loop is an edge that links a node with itself.
An example semantic speech network is shown in Figure \ref{fig:ExampleGraph} along with the corresponding speech transcript and stimulus picture.