
#!/Users/CN/Documents/Projects/Cambridge/language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  setup_stanfordnlp.py
#
# Description:
#               First steps according to stanza tutorial
#               Tutorial: https://stanfordnlp.github.io/stanza/client_usage.html
#
# Author:       Caroline Nettekoven, 2020
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# to activate python environment, run:
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate
import stanza
import pandas as pd
import sys
sys.path.append(
    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/')

# Import useful functions
from parts_of_language import extract_pol
from lemma import extract_lemma


# Create text pipeline
nlp = stanza.Pipeline()
nlp = stanfordnlp.Pipeline(processors=",pos")


# Create a text pipeline
doc = nlp("""In daily life we must constantly adapt our movements 
to changes in the environment or changes in our body. 
To adapt movements is a fundamental property of the central nervous system.""")

doc = nlp("""Uh this has a kind of hypo  coughing. Maybe a big dagger. I don’t imagine what they’re doing on the  down and by, what’s clearly happening. Yeah I don't, I don’t know yeah. """)
# For some reason, including the word adaptation into the sentence leads to an error? Unclear why.


# Tokenization
doc.sentences[0].print_tokens()

# Lemmatization: extract lemma
extract_lemma(doc)

# Parts of language (pol) tagging
extract_pol(doc)

# Dependency extraction: Get dependency relations for all of the words of a specific sentence:
doc.sentences[0].print_dependencies()


for sentence in doc.sentences:
    for word in sentence.words:
        print(word.text, word.lemma, word.pos)

for sentence in doc.sentences:
    print(sentence.ents)
    print(sentence.dependencies)


# The following example iterate over all English sentences and words, and print the word information one by one:

for i, sent in enumerate(doc.sentences):
    print("[Sentence {}]".format(i + 1))
    print("Text\tLemma\tPoS\tHead\tDeprel")
    for word in sent.words:
        print("{0}\t{1}\t{2}\t{3}\t{4}".format(
            word.text, word.lemma, word.pos, word.head, word.deprel))
    print("")

# Install CoreNLP
stanza.install_corenlp(dir="/Users/CN/stanza_resources/stanza_corenlp")
stanza.download_corenlp_models(
    model='english', version='4.1.0')


from stanza.server import CoreNLPClient
text = "Chris Manning is a nice person. Chris wrote a simple sentence. He also gives oranges to people."
with CoreNLPClient(
        annotators=['tokenize', 'ssplit', 'pos', 'lemma',
                    'ner', 'parse', 'depparse', 'coref'],
        timeout=30000,
        memory='16G') as client:
    ann = client.annotate(text)
# --> The CoreNLP server will be automatically started in the background upon the instantiation of the client.

# get the first sentence
sentence = ann.sentence[0]

# get the constituency parse of the first sentence
constituency_parse = sentence.parseTree
print(constituency_parse)
constituency_parse.child[0].value

print(sentence.basicDependencies)


# get the first token of the first sentence
token = sentence.token[0]
print(token.value, token.pos, token.ner)

# get an entity mention from the first sentence
print(sentence.mentions[0].entityMentionText)

# access the coref chain in the input text
print(ann.corefChain)
