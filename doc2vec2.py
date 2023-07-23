import gensim 
import codecs as cd 
import pandas as pd
pd.set_option('display.max_rows',None) 
from gensim.models.doc2vec import Doc2Vec 
import MeCab
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from numpy import *
import sys   
sys.setrecursionlimit(100000)

dird=os.path.dirname(os.path.abspath(__file__))
model = Doc2Vec.load('jawiki.doc2vec.dbow300d.model')

m = MeCab.Tagger("-Ochasen")

def mecab_sep(text):
    node = m.parseToNode(text)

    words_list = []

    while node:
        words_list.append(node.surface)
        node = node.next

    return words_list[1:-1]

def calc_vecs_d2v(docs):
    vecs = []
    for d in docs:
        vecs.append(model.infer_vector(mecab_sep(d)))
    return vecs


target_docs=[]

###内積類似度

def v2cv(target_docs,input_doc):
    print(input_doc)
    print(target_docs)
    all_docs = [input_doc]+[target_docs]
    #all_docs = [input_doc]+target_docs
    all_docs_vecs = calc_vecs_d2v(all_docs)

    similarity = np.dot([all_docs_vecs[0]],np.array(all_docs_vecs[1:]).T)
    #similarity = cosine_similarity([all_docs_vecs[0]],all_docs_vecs[1:])
    print(similarity)
    print(similarity.shape)

    return similarity[0]
