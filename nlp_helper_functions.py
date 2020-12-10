# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:07:59 2019

@author: Dr Sarah E Morgan, with input from Dr Bo Wang
modified by Dr. Caro Nettekoven, 2020
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


# def remove_interjections(text):
#     interjections = ['Um', 'um', 'Uh', 'uh', 'Eh', 'eh', 'Ehm', 'Em', 'em', 'Mmm', 'mmm',
#                      'ah', 'Ah', 'Aah', 'aah', 'hmm', 'hmmm', 'Hmm', 'Hmmm', 'inaudible', 'Inaudible', '...']
#     # tokens = nltk.word_tokenize(sent2)
#     # remove interjections
#     for interj in interjections:
#         text = text.replace(' ' + interj + ' ', '')
#     #
#     return text

def remove_interjections(text):
    """
    @author: by Dr. Caro Nettekoven, 2020
    Note: The interjections removed by this funciton are specific for English. Applying this to other languages may cause problems (For example in German "um" is a presposition)
    """
    english_interjections = ['Um', 'um', 'Uh', 'uh', 'Eh', 'eh', 'Ehm', 'Em', 'em', 'Mmm', 'mmm',
                             'ah', 'Ah', 'Aah', 'aah', 'hmm', 'hmmm', 'Hmm', 'Hmmm', 'inaudible', 'Inaudible']
    #
    sent2 = expand_contractions(text)  # expand contractions
    tokens = nltk.word_tokenize(sent2)
    # remove interjections
    tokens = [w for w in tokens if not w in english_interjections]
    sent3 = ' '.join(tokens)
    return sent3


def replace_problematic_symbols(text):
    # key is problematic symbol, value is replacement symbol
    problematic_symbols = {
        '’': "'",
        # '..': " ",
        # '...': " ",
        # '....': " ",
        '…': "...",
        '\n': " "}
    #
    # replace symbols
    for symbol in problematic_symbols.keys():
        text = text.replace(symbol, problematic_symbols[symbol])
    #
    return text


files = [
    '3138838-TAT10.txt',
    '3138838-TAT13.txt',
    '3138838-TAT30.txt',
    '3138849-TAT10.txt',
    '3138849-TAT13.txt',
    '3138849-TAT24.txt',
    '3138849-TAT30.txt',
    '3138883-TAT10.txt',
    '3138883-TAT13.txt',
    '3138883-TAT24.txt',
    '3138883-TAT30.txt',
    '3138910-TAT24.txt',
    '3138910-TAT30.txt',
    '3138916-TAT10.txt',
    '3138916-TAT13.txt',
    '3138916-TAT30.txt',
    '3138932-TAT10.txt',
    '3138932-TAT13.txt',
    '3138932-TAT24.txt',
    '3138933-TAT30.txt',
    '3138949-TAT10.txt',
    '3138949-TAT13.txt',
    '3138949-TAT30.txt',
    '3143756-TAT10.txt',
    '3143756-TAT24.txt',
    '3143762-TAT13.txt',
    '3143777-TAT10.txt',
    '3143777-TAT30.txt',
    '3143815-TAT10.txt',
    '3143843-TAT10.txt',
    '3143843-TAT24.txt',
    '3143870-TAT30.txt',
    '3143876-TAT10.txt',
    '3143876-TAT24.txt',
    '3144021-TAT13.txt',
    '3144021-TAT24.txt',
    '3144041-TAT10.txt',
    '3144199-TAT10.txt',
    '3144199-TAT30.txt',
    '3144614-TAT13.txt',
    '3145067-TAT13.txt',
    '3145067-TAT30.txt',
    '3145068-TAT10.txt',
    '3145068-TAT24.txt',
    '3145068-TAT30.txt',
    '3145069-TAT24.txt',
    '3145077-TAT10.txt',
    '3145077-TAT13.txt',
    '3145077-TAT24.txt',
    '3145077-TAT30.txt',
    '3145080-TAT13.txt',
    '3145080-TAT24.txt',
    '3145081-TAT13.txt',
    '3145090-TAT24.txt',
    '3145096-TAT10.txt',
    '3145096-TAT13.txt',
    '3145096-TAT24.txt',
    '3145120-TAT10.txt',
    '3145120-TAT24.txt',
    '3145211-TAT10.txt',
    '3145712-TAT24.txt',
    '3145752-TAT10.txt',
    '3145753-TAT10.txt',
    '3145788-TAT13.txt',
    '3145826-TAT10.txt',
    '3145826-TAT13.txt',
    '3145826-TAT24.txt',
    '3145826-TAT30.txt',
    '3145833-TAT10.txt',
    '3145833-TAT13.txt',
    '3146234-TAT10.txt',
    '3146234-TAT13.txt',
    '3146234-TAT24.txt',
    '3146234-TAT30.txt',
    '3146239-TAT13.txt',
    '3147298-TAT10.txt',
    '3147298-TAT13.txt',
    '3147298-TAT24.txt',
    '3147298-TAT30.txt',
    '3260813-TAT13.txt',
    '3260813-TAT24.txt',
    '3260820-TAT30.txt',
    '3260828-TAT30.txt',
    '3260843-TAT10.txt',
    '3260843-TAT24.txt',
    '3260864-TAT13.txt',
    '3260864-TAT24.txt',
    '3260899-TAT10.txt',
    '3260899-TAT13.txt',
    '3260899-TAT24.txt',
    '3260899-TAT30.txt',
    '3261239-TAT10.txt',
    '3261239-TAT13.txt',
    '3261239-TAT30.txt',
    '3261264-TAT10.txt',
    '3261669-TAT10.txt',
    '3262013-TAT10.txt',
    '3262013-TAT13.txt',
    '3262013-TAT24.txt',
    '3262013-TAT30.txt',
    '3975918-TAT10.txt',
    '3975918-TAT13.txt',
    '3975918-TAT24.txt',
    '3975918-TAT30.txt',
    '3975975-TAT10.txt',
    '3975975-TAT13.txt',
    '3975975-TAT24.txt',
    '3975975-TAT30.txt',
    '3983090-TAT13.txt',
    '3983090-TAT24.txt',
    '3983090-TAT30.txt',
    '3983753-TAT10.txt',
    '3983753-TAT13.txt',
    '3983753-TAT24.txt',
    '3983753-TAT30.txt',
    '3984259-TAT10.txt',
    '3984259-TAT13.txt',
    '3984259-TAT24.txt',
    '3984259-TAT30.txt']
