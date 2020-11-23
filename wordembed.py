# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:07:59 2019

@author: Dr Sarah E Morgan, with input from Dr Bo Wang
"""

from __future__ import division
import itertools
import numpy as np
from collections import Counter
from sklearn.decomposition import PCA

import nltk
import re
import string
from contractions import CONTRACTION_MAP
import sklearn
import gensim

###### Train model: # https://github.com/eyaler/word2vec-slim
model = gensim.models.KeyedVectors.load_word2vec_format('c:/Users/sarah/Documents/Research/speech/Corpora/w2v_googlenews/GoogleNews-vectors-negative300-SLIM.bin.gz', binary=True)
#model.similarity(w1="Mother",w2="Father")
#model.most_similar(positive="polite",topn=3)
embedding_size = 300

def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
        if contraction_mapping.get(match)\
        else contraction_mapping.get(match.lower())
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

def process_sent(sent):
    
    stop_words = nltk.corpus.stopwords.words('english')
    newStopWords = ['Um','um','Uh','uh','Eh','eh','Ehm','Em','em','Mmm','mmm','ah','Ah','Aah','aah','hmm','hmmm','Hmm','Hmmm','inaudible','Inaudible']
    stop_words.extend(newStopWords)
    
    sent2 = expand_contractions(sent) # expand contractions
    tokens = nltk.word_tokenize(sent2)
    tokens = [t.lower() for t in tokens if t not in string.punctuation] # remove punctuation
    tokens = [w for w in tokens if not w in stop_words] # remove stopwords
    sent3 = ' '.join(tokens)
    return sent3

def map_word_frequency(document):
    return Counter(itertools.chain(*document))

def sentence2vec(tokenised_sentence_list, embedding_size, word_emb_model, a = 1e-3):

    """
    Computing weighted average of the word vectors in the sentence;
    remove the projection of the average vectors on their first principal component.
    Borrowed from https://github.com/peter3125/sentence2vec; now compatible with python 2.7
    """

    word_counts = map_word_frequency(tokenised_sentence_list)
    sentence_set=[]

    for sentence in tokenised_sentence_list:
        vs = np.zeros(embedding_size)
        sentence_length = len(sentence)
        for word in sentence:
            a_value = a / (a + word_counts[word]) # smooth inverse frequency, SIF
            try:
                vs = np.add(vs, np.multiply(a_value, word_emb_model[word])) # vs += sif * word_vector
            except:
                pass
        vs = np.divide(vs, sentence_length) # weighted average
        sentence_set.append(vs)

    # calculate PCA of this sentence set

    pca = PCA(n_components=embedding_size)
    pca.fit(np.array(sentence_set))
    u = pca.explained_variance_ratio_  # the PCA vector
    u = np.multiply(u, np.transpose(u))  # u x uT

    if len(u) < embedding_size:
        for i in range(embedding_size - len(u)):
            u = np.append(u, 0)  # add needed extension for multiplication below

	# resulting sentence vectors, vs = vs - u x uT x vs
    sentence_vecs = []
    for vs in sentence_set:
        sub = np.multiply(u,vs)
        sentence_vecs.append(np.subtract(vs, sub))

    return sentence_vecs
    
    
def wordvec_features(embedding):
    mymatrix=sklearn.metrics.pairwise.cosine_similarity(embedding) # matrix is the similarity matrix
    nosent=len(mymatrix) # no. of sentences- BEWARE- sentences with no relevant words aren't included.
    
    incoh=0
    for index in range(0,nosent-1):
        incoh += (mymatrix[index,1+index])/(len(range(0,nosent-1)))
    
    mymatrix0=mymatrix
    np.fill_diagonal(mymatrix0, 0) # sets diagonal to zero in mymatrix0
    maxoffdiag=np.max(mymatrix0) # max off-diagonal (repetition measure)
    
    return incoh, maxoffdiag


def meas_coh(text):

    sentences=nltk.tokenize.sent_tokenize(text)
    
    sentences_process=[]
    for sent in sentences:
        sent=process_sent(sent)
        sentences_process.append(sent)
        
    sentences_process = [x for x in sentences_process if x]# Removes any empty sentences (i.e. sentences which only had stopwords)
    
    if len(sentences_process)>1:
        sentences2=[sentence.split() for sentence in sentences_process]
        if all(x==sentences2[0] for x in sentences2): # if all sentences are the same, return nan
            wordvec_result = float('NaN'), float('NaN')
        else:
            embedding = sentence2vec(sentences2, embedding_size, model)
            if np.nansum(np.nansum(embedding))==0: # Sometimes embedding might be all zeros/nans.
                wordvec_result = float('NaN'), float('NaN')
            else:
                wordvec_result = wordvec_features(embedding)
    else:
        wordvec_result = float('NaN'), float('NaN') # if only one sentence, return nan

    return wordvec_result