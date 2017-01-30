"""Contains various functions to create models from pkl files.
"""

import os
import numpy as np
import pickle
from gensim.models import Word2Vec
from scipy.linalg import orthogonal_procrustes

"""Given the pickle path (.pkl), loda the data.
"""
def loadYear(pickle_path):
    with open( pickle_path, "rb" ) as f:
        BoW = pickle.load(f)
    data = []
    for m in BoW:
        for article in m:
            data.append(article)
    return data

"""Load a set of pickle files per year in a certain range (using loadYear multiple times).
"""
def loadYears(pickle_path, years):
    data = []
    for y in years:
        file = pickle_path + "/" + str(y) + ".pkl"
        if os.path.exists(file):
            tmp = loadYear(file)
            data += tmp
        else:
            print(file + " doesn't exist.")
    return data

"""Return a model from data using our best set of parameters.
"""
def createModel(data):
    # those parameters are well explained here: https://radimrehurek.com/gensim/models/word2vec.html
    # negative : state of many noisewords should be drawn
    return Word2Vec(data, size=300, window=4, min_count=50, workers=4, sg=1, negative=10)


"""Create a transformation matrix to change the axis from the first model to be oriented in the same directions as the second model. Only the words present in both datasets are kept.
"""
def createTransformationMatrix(modelA, modelB):
    # initialize the matrices
    labels = []
    A = []
    B = []
    # keep the common words and add them to the matrices
    nb_words_A = len(modelA.index2word)
    nb_words_B = len(modelA.index2word)
    for i in range(0,nb_words_A):
        word = modelA.index2word[i]
        if word in modelB.index2word:
            # add the word to the matrices (and the labels)
            labels.append(word)
            A.append(modelA[word])
            B.append(modelB[word])
    # create the transformation matrix
    #d, Z, tform = procrustes(np.asarray(B), np.asarray(A), scaling=False, reflection=True)
    TransM, _ = orthogonal_procrustes(np.asarray(A), np.asarray(B), check_finite=False) 

    #we create the entire matrix of modelA
    #label_M = []
    #M = []
    #for i in range(0,nb_words_A):
    #    word = modelA.index2word[i]
    #    M.append(modelA[word])
    #    label_M.append(word)
    #Z = np.matmul(M, TransM)
    
    Z = np.matmul(A, TransM)

    # create the 2 models manually (by first creating a text file and reading it).
    constructModel(np.asarray(Z), labels, "tmpZ.model.txt")
    constructModel(np.asarray(B), labels, "tmpB.model.txt")
    
    modelZ_ = Word2Vec.load_word2vec_format('tmpZ.model.txt', binary=False)
    modelB_ = Word2Vec.load_word2vec_format('tmpB.model.txt', binary=False)
    
    return modelZ_, modelB

"""Construct a model from the matrix and the labels. (Note that a file will be created !)
"""
def constructModel(M, labels, filename):
    f = open(filename,'w')
    f.write(str(M.shape[0])+ " "+ str(M.shape[1])+"\n")
    for i in range(0, len(labels)):
        f.write(labels[i] + " " + ' '.join(str(cell) for cell in list(M[i]))+"\n")
    f.close()
    
