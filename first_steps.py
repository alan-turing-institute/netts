
#!/Users/CN/Documents/Projects/Cambridge/language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  setup_stanfordnlp.py
#
# Description:
#               First steps according to analytics vidhya tutorial
#               Tutorial: https://www.analyticsvidhya.com/blog/2019/02/stanfordnlp-nlp-library-python/
#
# Author:       Caroline Nettekoven, 2020
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# to activate python environment, run:
# source /Users/CN/Documents/Projects/Cambridge/language_analysis/venv/bin/activate
import stanfordnlp
import pandas as pd
import sys
sys.path.append('/Users/CN/Documents/Projects/Cambridge/language_analysis/')

# Import useful functions
from parts_of_language import extract_pol
from lemma import extract_lemma


# Create text pipeline
nlp = stanfordnlp.Pipeline(processors = "tokenize,mwt,lemma,pos")


# Create a text pipeline
doc = nlp('In daily life we must constantly adapt our movements to changes in the environment or changes in our body. To adapt movements is a fundamental property of the central nervous system.')
# For some reason, including the word adaptation into the sentence leads to an error? Unclear why.


# Tokenization
doc.sentences[0].print_tokens()

# Lemmatization: extract lemma
extract_lemma(doc)

# Parts of language (pol) tagging
extract_pol(doc)
