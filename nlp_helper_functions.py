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
    english_interjections = ['Um', 'um', 'Uh', 'uh', 'Eh', 'eh', 'Ehm', 'Em', 'em', 'Erm', 'erm', 'Ehhm', 'ehhm', 'Ehm', 'ehm', 'Mmm', 'mmm', 'Yeah', 'yeah',
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
        '‘': "'",
        "–": "-",
        '\n': " "}
    #
    # replace symbols
    for symbol in problematic_symbols.keys():
        text = text.replace(symbol, problematic_symbols[symbol])
    #
    return text


# instructions="Please describe what you see in this image. Please speak for the full minute! We are recording!"

tat_pilot_files = [
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


hbn_movie_files = [
    'NDARAA948VFH_MRI_recording_excerpt.txt',
    'NDARAC853DTE_MRI_recording_excerpt.txt',
    'NDARAC904DMU_MRI_recording_excerpt.txt',
    'NDARAD232HVV_MRI_recording_excerpt.txt',
    'NDARAD774HAZ_MRI_recording_excerpt.txt']


genpub_files = [
    '22895-20-task-1v8g-6375853-TAT10-3-1-converted (1).txt',
    '22895-20-task-1v8g-6375853-TAT13-9-1-converted (1).txt',
    '22895-20-task-1v8g-6375853-TAT19-4-1-converted (1).txt',
    '22895-20-task-1v8g-6375853-TAT8-6-1-converted (1).txt',
    '22895-20-task-1v8g-6376314-TAT13-2-1-converted (1).txt',
    '22895-20-task-1v8g-6376314-TAT13-2-1-converted (2).txt',
    '22895-20-task-1v8g-6376314-TAT19-8-1-converted (1).txt',
    '22895-20-task-1v8g-6377161-TAT13-8-1-converted (1).txt',
    '22895-20-task-1v8g-6377597-TAT10-2-1-converted (1).txt',
    '22895-20-task-1v8g-6377597-TAT19-6-1-converted (1).txt',
    '22895-20-task-1v8g-6377597-TAT8-9-1-converted (1).txt',
    '22895-20-task-1v8g-6378273-TAT8-5-1_otter2.ai.txt',
    '22895-20-task-1v8g-6379858-TAT19-3-1-converted_otter.ai (1).txt',
    '22895-20-task-1v8g-6380247-TAT13-5-1-converted_otter.ai (1).txt',
    '22895-20-task-1v8g-6382583-TAT10-2-1-converted (1).txt',
    '22895-20-task-1v8g-6382583-TAT13-9-1-converted (1).txt',
    '22895-20-task-1v8g-6382583-TAT19-6-1-converted (1).txt',
    '22895-20-task-1v8g-6382583-TAT8-4-1-converted (1).txt',
    '22895-20-task-1v8g-6384393-TAT10-5-1-converted (1).txt',
    '22895-20-task-1v8g-6384393-TAT13-6-1-converted (1).txt',
    '22895-20-task-1v8g-6384393-TAT19-4-1-converted (1).txt',
    '22895-20-task-1v8g-6384393-TAT8-7-1-converted (1).txt',
    '22895-20-task-1v8g-6384768-TAT10-9-1-converted (1).txt',
    '22895-20-task-1v8g-6384768-TAT13-6-1-converted (1).txt',
    '22895-20-task-1v8g-6384768-TAT19-8-1-converted (1).txt',
    '22895-20-task-1v8g-6384768-TAT8-4-1-converted (1).txt',
    '22895-20-task-7g47-6381126-TAT13-7-1-converted (1).txt',
    '22895-20-task-7jrp-6377766-TAT19-3-1-converted (1).txt',
    '22895-20-task-7jrp-6381892-TAT10-2-1-converted (1).txt',
    '22895-20-task-97yx-6376960-TAT10-9-1-converted (1).txt',
    '22895-20-task-97yx-6377906-TAT10-2-1-converted (1).txt',
    '22895-20-task-a68g-6375245-TAT13-7-1-converted (1).txt',
    '22895-20-task-a68g-6376554-TAT13-5-1-converted (1).txt',
    '22895-20-task-a68g-6376554-TAT19-4-1-converted (1).txt',
    '22895-20-task-a68g-6378790-TAT19-4-1-converted (1).txt',
    '22895-20-task-bdi6-6372490-TAT8-8-1-converted (1).txt',
    '22895-20-task-bdi6-6372650-TAT8-8-1-converted (1).txt',
    '22895-20-task-bdi6-6372877-TAT10-4-1-converted (1).txt',
    '22895-20-task-bdi6-6373908-TAT10-8-1-converted (1).txt',
    '22895-20-task-bdi6-6374267-TAT8-7-1-converted_otter.ai (1).txt',
    '22895-20-task-gv1m-6376917-TAT8-8-1-converted (1).txt',
    '22895-20-task-h57d-6380426-TAT10-2-1-converted (1).txt',
    '22895-20-task-h57d-6380859-TAT13-2-1-converted (1).txt',
    '22895-20-task-h57d-6380954-TAT30-5-1-converted (1).txt',
    '22895-20-task-hug1-6373787-TAT8-7-1-converted (1).txt',
    '22895-20-task-hug1-6376374-TAT19-3-1-converted (1).txt',
    '22895-20-task-hug1-6377809-TAT19-6-1-converted (1).txt',
    '22895-20-task-kkdc-6377033-TAT19-3-1-converted (1).txt',
    '22895-20-task-kkdc-6378756-TAT13-9-1-converted (1).txt',
    '22895-20-task-kkdc-6379040-TAT10-4-1-converted (1).txt',
    '22895-20-task-kkdc-6379040-TAT19-8-1-converted (1).txt',
    '22895-20-task-kkdc-6379040-TAT19-8-1-converted (2).txt',
    '22895-20-task-kkdc-6379040-TAT8-3-1-converted (1).txt',
    '22895-20-task-kkdc-6379084-TAT10-8-1-converted (1).txt',
    '22895-20-task-kkdc-6379853-TAT13-8-1-converted (1).txt',
    '22895-20-task-kkdc-6379853-TAT8-4-1-converted (1).txt',
    '22895-20-task-kkdc-6379856-TAT19-6-1-converted (1).txt',
    '22895-20-task-kkdc-6379888-TAT10-2-1-converted (1).txt',
    '22895-20-task-kkdc-6380693-TAT10-5-1-converted (1).txt',
    '22895-20-task-kkdc-6381092-TAT10-9-1-converted (1).txt',
    '22895-20-task-kkdc-6381092-TAT8-8-1-converted (1).txt',
    '22895-20-task-n2ru-6374166-TAT19-2-1-converted (1).txt',
    '22895-20-task-n2ru-6375350-TAT13-8-1-converted (1).txt',
    '22895-20-task-n2ru-6375904-TAT8-2-1-converted (1).txt',
    '22895-20-task-wyul-6372673-TAT10-3-1 (1).txt',
    '22895-20-task-wyul-6372673-TAT10-3-1.txt',
    '22895-20-task-wyul-6372673-TAT13-2-1 (1).txt',
    '22895-20-task-wyul-6372673-TAT19-5-1 (1).txt',
    '22895-20-task-wyul-6372673-TAT21-6-1 (1).txt',
    '22895-20-task-wyul-6372673-TAT24-4-1 (1).txt',
    '22895-20-task-wyul-6372673-TAT28-8-1 (1).txt',
    '22895-20-task-wyul-6372673-TAT30-7-1 (1).txt',
    '22895-20-task-wyul-6372673-TAT8-9-1 (1).txt',
    '22895-20-task-wyul-6374580-TAT10-3-1 (1).txt',
    '22895-20-task-wyul-6374580-TAT13-4-1 (1).txt',
    '22895-20-task-wyul-6374580-TAT19-2-1 (1).txt',
    '22895-20-task-wyul-6374580-TAT21-9-1 (1).txt',
    '22895-20-task-wyul-6374580-TAT24-6-1.txt',
    '22895-20-task-wyul-6374580-TAT28-5-1.txt',
    '22895-20-task-wyul-6374580-TAT30-8-1.txt',
    '22895-20-task-wyul-6374580-TAT8-7-1.txt',
    '22895-20-task-wyul-6375399-TAT10-3-1 (1).txt',
    '22895-20-task-wyul-6375399-TAT13-5-1 (1).txt',
    '22895-20-task-wyul-6375399-TAT19-6-1 (1).txt',
    '22895-20-task-wyul-6375399-TAT21-2-1 (1).txt',
    '22895-20-task-wyul-6375399-TAT24-8-1 (1).txt',
    '22895-20-task-wyul-6375399-TAT28-4-1 (1).txt',
    '22895-20-task-wyul-6375399-TAT30-7-1 (1).txt',
    '22895-20-task-wyul-6375399-TAT8-9-1 (1).txt',
    '22895-20-task-wyul-6378008-TAT10-7-1 (1).txt',
    '22895-20-task-wyul-6378008-TAT13-4-1 (1).txt',
    '22895-20-task-wyul-6378008-TAT19-2-1 (1).txt',
    '22895-20-task-wyul-6378008-TAT21-6-1 (1).txt',
    '22895-20-task-wyul-6378008-TAT24-5-1 (1).txt',
    '22895-20-task-wyul-6378008-TAT28-8-1 (2).txt',
    '22895-20-task-wyul-6378008-TAT30-9-1 (1).txt',
    '22895-20-task-wyul-6378008-TAT8-3-1 (1).txt',
    '22895-20-task-wyul-6378038-TAT10-5-1 (1).txt',
    '22895-20-task-wyul-6378038-TAT13-4-1 (1).txt',
    '22895-20-task-wyul-6378038-TAT19-2-1 (1).txt',
    '22895-20-task-wyul-6378038-TAT21-9-1 (1).txt',
    '22895-20-task-wyul-6378038-TAT24-6-1 (1).txt',
    '22895-20-task-wyul-6378038-TAT28-3-1 (1).txt',
    '22895-20-task-wyul-6378038-TAT30-7-1 (1).txt',
    '22895-20-task-wyul-6378038-TAT8-8-1 (1).txt',
    '22895-20-task-wyul-6378600-TAT10-5-1 (1).txt',
    '22895-20-task-wyul-6378600-TAT13-9-1 (1).txt',
    '22895-20-task-wyul-6378600-TAT19-7-1 (1).txt',
    '22895-20-task-wyul-6378600-TAT21-6-1 (1).txt',
    '22895-20-task-wyul-6378600-TAT24-3-1 (1).txt',
    '22895-20-task-wyul-6378600-TAT28-4-1 (1).txt',
    '22895-20-task-wyul-6378600-TAT30-2-1 (1).txt',
    '22895-20-task-wyul-6378600-TAT8-8-1 (1).txt',
    '22895-20-task-wyul-6378992-TAT10-3-1 (2).txt',
    '22895-20-task-wyul-6378992-TAT13-6-1 (1).txt',
    '22895-20-task-wyul-6378992-TAT19-2-1 (1).txt',
    '22895-20-task-wyul-6378992-TAT21-8-1 (1).txt',
    '22895-20-task-wyul-6378992-TAT24-4-1 (1).txt',
    '22895-20-task-wyul-6378992-TAT28-5-1 (1).txt',
    '22895-20-task-wyul-6378992-TAT30-7-1 (1).txt',
    '22895-20-task-wyul-6378992-TAT8-9-1 (1).txt',
    '22895-20-task-wyul-6379532-TAT10-7-1 (1).txt',
    '22895-20-task-wyul-6379532-TAT13-8-1 (1).txt',
    '22895-20-task-wyul-6379532-TAT19-3-1 (1).txt',
    '22895-20-task-wyul-6379532-TAT21-4-1 (1).txt',
    '22895-20-task-wyul-6379532-TAT24-6-1 (1).txt',
    '22895-20-task-wyul-6379532-TAT28-5-1 (1).txt',
    '22895-20-task-wyul-6379532-TAT30-9-1 (1).txt',
    '22895-20-task-wyul-6379532-TAT8-2-1 (1).txt',
    '22895-20-task-wyul-6379541-TAT10-8-1 (1).txt',
    '22895-20-task-wyul-6379541-TAT13-5-1 (1).txt',
    '22895-20-task-wyul-6379541-TAT19-6-1 (1).txt',
    '22895-20-task-wyul-6379541-TAT21-3-1 (1).txt',
    '22895-20-task-wyul-6379541-TAT24-4-1 (1).txt',
    '22895-20-task-wyul-6379541-TAT28-7-1 (1).txt',
    '22895-20-task-wyul-6379541-TAT30-9-1 (1).txt',
    '22895-20-task-wyul-6379541-TAT8-2-1 (1).txt',
    '22895-20-task-wyul-6381372-TAT10-8-1 (1).txt',
    '22895-20-task-wyul-6381372-TAT13-7-1 (1).txt',
    '22895-20-task-wyul-6381372-TAT19-9-1 (1).txt',
    '22895-20-task-wyul-6381372-TAT21-2-1 (1).txt',
    '22895-20-task-wyul-6381372-TAT24-5-1 (1).txt',
    '22895-20-task-wyul-6381372-TAT28-6-1 (1).txt',
    '22895-20-task-wyul-6381372-TAT30-3-1 (1).txt',
    '22895-20-task-wyul-6381372-TAT8-4-1 (1).txt',
    '22895-20-task-wyul-6383007-TAT10-8-1 (1).txt',
    '22895-20-task-wyul-6383007-TAT13-3-1 (1).txt',
    '22895-20-task-wyul-6383007-TAT19-5-1 (1).txt',
    '22895-20-task-wyul-6383007-TAT21-7-1 (1).txt',
    '22895-20-task-wyul-6383007-TAT24-4-1 (1).txt',
    '22895-20-task-wyul-6383007-TAT28-2-1 (1).txt',
    '22895-20-task-wyul-6383007-TAT30-9-1 (1).txt',
    '22895-20-task-wyul-6383007-TAT8-6-1 (1).txt',
    '22895-20-task-wyul-6383061-TAT10-4-1 (1).txt',
    '22895-20-task-wyul-6383061-TAT13-3-1 (1).txt',
    '22895-20-task-wyul-6383061-TAT19-5-1 (1).txt',
    '22895-20-task-wyul-6383061-TAT21-9-1 (1).txt',
    '22895-20-task-wyul-6383061-TAT24-6-1 (1).txt',
    '22895-20-task-wyul-6383061-TAT28-2-1 (1).txt',
    '22895-20-task-wyul-6383061-TAT30-8-1 (1).txt',
    '22895-20-task-wyul-6383061-TAT8-7-1 (1).txt',
    '22895-20-task-wyul-6386517-TAT10-3-1 (1).txt',
    '22895-20-task-wyul-6386517-TAT13-2-1 (1).txt',
    '22895-20-task-wyul-6386517-TAT19-6-1 (1).txt',
    '22895-20-task-wyul-6386517-TAT21-9-1 (1).txt',
    '22895-20-task-wyul-6386517-TAT24-5-1 (1).txt',
    '22895-20-task-wyul-6386517-TAT28-4-1 (1).txt',
    '22895-20-task-wyul-6386517-TAT30-7-1 (1).txt',
    '22895-20-task-wyul-6386517-TAT8-8-1 (1).txt',
    'BQ22895-20-task-1v8g-6376314-TAT10-5-1-converted.txt',
    'BQ22895-20-task-1v8g-6377161-TAT19-7-1-converted.txt',
    'BQ22895-20-task-7jrp-6379710-TAT19-5-1-converted (2).txt',
    'BQ22895-20-task-bdi6-6373313-TAT13-5-1-converted (2).txt',
    'BQ22895-20-task-kkdc-6378927-TAT10-2-1-converted(1).txt',
    'BQ22895-20-task-kkdc-6378927-TAT13-4-1-converted(1).txt',
    'BQ22895-20-task-kkdc-6379888-TAT10-2-1-converted (1).txt',
]
