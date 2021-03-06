"""Contains various functions to create models from pkl files.
    The pickle files 
"""

import os
import numpy as np
import pickle
from gensim.models import Word2Vec
from scipy.linalg import orthogonal_procrustes

"""Given the pickle path (.pkl), load the data. Refer to the cleaning of data to understand
    the format of the pickle files.
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
    It returns 2 models after applying the orthogonal Procrustes algorithm for aligning the axes of both model.    
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
    TransM, _ = orthogonal_procrustes(np.asarray(A), np.asarray(B), check_finite=False) 

    # apply the transofrmation matrix to the first model matrix
    Z = np.matmul(A, TransM)

    # create the 2 models manually (by first creating a text file and reading it).
    # it would be most efficient not to have to store the results on files like this.
    constructModel(np.asarray(Z), labels, "tmpZ.model.txt")
    constructModel(np.asarray(B), labels, "tmpB.model.txt")
    
    modelZ_ = Word2Vec.load_word2vec_format('tmpZ.model.txt', binary=False)
    modelB_ = Word2Vec.load_word2vec_format('tmpB.model.txt', binary=False)
    
    return modelZ_, modelB_

"""Construct a model from the matrix and the labels. (Note that a file will be created,
    so make sure not to overwrite something that matters.)
"""
def constructModel(M, labels, filename):
    f = open(filename,'w')
    f.write(str(M.shape[0])+ " "+ str(M.shape[1])+"\n")
    for i in range(0, len(labels)):
        f.write(labels[i] + " " + ' '.join(str(cell) for cell in list(M[i]))+"\n")
    f.close()
    
