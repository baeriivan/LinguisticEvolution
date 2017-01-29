"""
"""

#%matplotlib inline

import os
import numpy as np
import matplotlib.pyplot as plt
import pickle
from collections import Counter
from gensim.models import Word2Vec
import tsne
from procrustes import procrustes

"""
"""
def showEvolution(pt1, pt2, label, data1, data2, label1, label2):
    fig = plt.figure()
    #show neighbours of data1
    plt.scatter(data1[:,0], data1[:,1], c='r')
    for i in range(0,len(label1)): 
        plt.annotate(label1[i], xy=(data1[i,0], data1[i,1]), xytext=(data1[i,0], data1[i,1]))
    #show neighbours of data2
    plt.scatter(data2[:,0], data2[:,1], c='b')
    for i in range(0,len(label2)): 
        plt.annotate(label2[i], xy=(data2[i,0], data2[i,1]), xytext=(data2[i,0], data2[i,1]))
    #show old and new word
    plt.scatter(pt1[:,0], pt1[:,1], c='r')
    plt.scatter(pt2[:,0], pt2[:,1], c='b')
    plt.annotate(label, xy=(pt2[:,0], pt2[:,1]), xytext=(pt1[:,0], pt1[:,1]),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
    plt.autoscale()
    plt.xticks([])
    plt.yticks([])
    plt.show()

"""
"""
def visualizeWord(mod1, mod2, word, n):
    if word in mod1.vocab and word in mod2.vocab:
        #find old emplacement of word 
        pt1 = mod1[word]
        #find neighbours of that place
        label1 = [label for label, p in mod2.most_similar(positive=[pt1], topn=n)]
        data1 = mod2[label1]
        #print recent word
        pt2 = mod2[word]
        #print neighbours
        label2 = [label for label, p in mod2.most_similar(word, topn=n)]
        data2 = mod2[label2]
        #apply tsne on the two data before resplitting them
        res = tsne.tsne(np.concatenate([pt1.reshape(1,300), pt2.reshape(1,300), data1,data2]), no_dims=2, initial_dims=300)
        pt1 = res[0].reshape(1,2)
        pt2 = res[1].reshape(1,2)
        data1 = res[2:n+2]
        data2 = res[n+2:]
        
        showEvolution(pt1, pt2, word, data1, data2, label1, label2)
    else:
        print(word + " is not in the vocabulary.")
