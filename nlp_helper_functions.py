# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:07:59 2019

@author: Dr Sarah E Morgan, with input from Dr Bo Wang
"""

# from __future__ import division
import itertools
import numpy as np
# from collections import Counter
# from sklearn.decomposition import PCA

import nltk
import re
import string
from contractions import CONTRACTION_MAP
# import gensim


def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
            if contraction_mapping.get(match)\
            else contraction_mapping.get(match.lower())
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text


def process_sent(sent):

    stop_words = nltk.corpus.stopwords.words('english')
    newStopWords = ['Um', 'um', 'Uh', 'uh', 'Eh', 'eh', 'Ehm', 'Em', 'em', 'Mmm', 'mmm',
                    'ah', 'Ah', 'Aah', 'aah', 'hmm', 'hmmm', 'Hmm', 'Hmmm', 'inaudible', 'Inaudible']
    stop_words.extend(newStopWords)

    sent2 = expand_contractions(sent)  # expand contractions
    tokens = nltk.word_tokenize(sent2)
    # remove punctuation
    tokens = [t.lower() for t in tokens if t not in string.punctuation]
    tokens = [w for w in tokens if not w in stop_words]  # remove stopwords
    sent3 = ' '.join(tokens)
    return sent3
