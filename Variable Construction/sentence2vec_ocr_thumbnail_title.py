# -*- coding: utf-8 -*-
"""
Sentence2vec - ocr text (thumbnail images) & title text
Reference: 'https://github.com/PrincetonML/SIF', 'https://github.com/peter3125/sentence2vec'
  Copyright 2016-2018 Peter de Vocht

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
Requirement:
  use the spacy large model's vectors for testing semantic relatedness
  this assumes you've already installed the large model, if not download it and pip install it:
  wget https://github.com/explosion/spacy-models/releases/tag/en_core_web_lg-2.0.0
  pip install en_core_web_lg-2.0.0.tar.gz
"""

import spacy
import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

nlp = spacy.load('en_core_web_lg')            

# an embedding word with associated vector
class Word:
    def __init__(self, text, vector):
        self.text = text
        self.vector = vector

    def __str__(self):
        return self.text + ' : ' + str(self.vector)

    def __repr__(self):
        return self.__str__()

# a sentence, a list of words
class Sentence:
    def __init__(self, word_list):
        self.word_list = word_list

    # return the length of a sentence
    def len(self) -> int:
        return len(self.word_list)

    def __str__(self):
        word_str_list = [word.text for word in self.word_list]
        return ' '.join(word_str_list)

    def __repr__(self):
        return self.__str__()


# todo: get a proper word frequency for a word in a document set
# or perhaps just a typical frequency for a word from Google's n-grams
def get_word_frequency(word_text):
    return 0.0001  # set to a low occurring frequency - probably not unrealistic for most words, improves vector values


# A SIMPLE BUT TOUGH TO BEAT BASELINE FOR SENTENCE EMBEDDINGS
# Sanjeev Arora, Yingyu Liang, Tengyu Ma
# Princeton University
# convert a list of sentence with word2vec items into a set of sentence vectors
def sentence_to_vec(sentence_list: List[Sentence], embedding_size: int, a: float=1e-3):
    sentence_set = []
    for sentence in sentence_list:
        vs = np.zeros(embedding_size)  # add all word2vec values into one vector for the sentence
        sentence_length = sentence.len()
        for word in sentence.word_list:
            a_value = a / (a + get_word_frequency(word.text))  # smooth inverse frequency, SIF
            vs = np.add(vs, np.multiply(a_value, word.vector))  # vs += sif * word_vector

        vs = np.divide(vs, sentence_length)  # weighted average
        sentence_set.append(vs)  # add to our existing re-calculated set of sentences

    # calculate PCA of this sentence set
    pca = PCA()
    pca.fit(np.array(sentence_set))
    u = pca.components_[0]  # the PCA vector
    u = np.multiply(u, np.transpose(u))  # u x uT

    # pad the vector?  (occurs if we have less sentences than embeddings_size)
    if len(u) < embedding_size:
        for i in range(embedding_size - len(u)):
            u = np.append(u, 0)  # add needed extension for multiplication below

    # resulting sentence vectors, vs = vs -u x uT x vs
    sentence_vecs = []
    for vs in sentence_set:
        sub = np.multiply(u,vs)
        sentence_vecs.append(np.subtract(vs, sub))

    return sentence_vecs

import os
import pandas as pd

os.chdir('D:\\youtube')
df = pd.read_csv("ocr.csv")
video_id_list = df.video_id.tolist()

titles = df.title
tit_list = titles.values.tolist()
df.th_text = df.th_text.fillna("")

ocrtxt = df.th_text
ocr_list = ocrtxt.values.tolist()

tit_sentences=[]
for line in tit_list:
    tit_sentences.append(line.strip().split(' '))

ocr_sentences=[]
for line in ocr_list:
    ocr_sentences.append(line.strip().split(' '))
    
tit_sentence_list = []
for sentence in tit_sentences:
    word_list = []
    for word in sentence:
        token = nlp.vocab[word]
        if token.has_vector:  # ignore OOVs
            word_list.append(Word(word, token.vector))
    if len(word_list) > 0:  # did we find any words (not an empty set)
        tit_sentence_list.append(Sentence(word_list))
    else:
        tit_sentence_list.append(Sentence([Word('',0)]))

ocr_sentence_list = []
for sentence in ocr_sentences:
    word_list = []
    for word in sentence:
        token = nlp.vocab[word]
        if token.has_vector:  # ignore OOVs
            word_list.append(Word(word, token.vector))
    if len(word_list) > 0:  # did we find any words (not an empty set)
        ocr_sentence_list.append(Sentence(word_list))
    else:
        ocr_sentence_list.append(Sentence([Word('',0)]))
    
if __name__ == '__main__':

    embedding_size = 300   # dimension of spacy word embeddings
    
    tit_vectors = sentence_to_vec(tit_sentence_list, embedding_size)  # all vectors converted together
    ocr_vectors = sentence_to_vec(ocr_sentence_list, embedding_size)  # all vectors converted together
    
    simil_list = []
    for i,x in enumerate(tit_sentence_list):
        simil_list.append( cosine_similarity([tit_vectors[i], ocr_vectors[i]])[0,1] )

simil_df = pd.DataFrame(
    {'video_id': video_id_list,
     'th_tit_dist': simil_list
    })

simil_df.to_csv("simildf.csv")