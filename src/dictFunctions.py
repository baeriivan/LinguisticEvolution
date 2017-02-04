import pickle, re
import os
from collections import Counter

def words(text): return re.findall(r'[A-zÀ-ÿ\-]+', text.lower())

# Creates a dictionary for a range of years from the raw articles
def create_dictionary(years, DirRead, DirWrite):
    big_text = ""
    for year in years:
        fileName = str(year) + '.pkl'
        filePath = os.path.join(DirRead, fileName)
        if os.path.exists(filePath):
            with open(filePath, 'rb') as f:
                all_art_year = pickle.load(f)
                flattened_text = ' '.join([word for all_art_month in all_art_year for article in all_art_month for word in article])
                big_text += flattened_text
        else:
            print(filePath + "doesn't exist")
    print(len(big_text))

    if not os.path.exists(DirWrite):
        os.makedirs(DirWrite)

    WORDS = Counter(words(big_text))
    fileName = str(years[0])+ '-' + str(years[-1]) + '-Dic.pkl'
    filePath = os.path.join(DirWrite, fileName)
    with open(filePath, 'wb') as f:
        pickle.dump(WORDS, f, pickle.HIGHEST_PROTOCOL)

# Loads multiple dictionaries in order to merge them later
def load_dictionaries(path, from_date, to_date):
    dictionaries = []
    if os.path.isdir(path):
        for year in range(from_date, to_date + 1):
            filePath = os.path.join(path, str(year) + '-' + str(year) + '-Dic.pkl')
            if os.path.isfile(filePath):
                with open(filePath, 'rb') as f:
                    dictionary = pickle.load(f)
                dictionaries.append(dictionary)
            else:
                print(filePath + "doesn't exist")
    return dictionaries

# Loads a single dictionary
def load_dictionary(filePath):
    if os.path.isfile(filePath):
        with open(filePath, 'rb') as f:
            dictionary = pickle.load(f)
    return dictionary

# Merges multiple dictionaries into one
def merge_dictionaries(dictionaries, filepath):
    dictionary = Counter()
    for dict in dictionaries:
        dictionary.update(dict)

    with open(filepath, 'wb') as f:
        pickle.dump(dictionary, f, pickle.HIGHEST_PROTOCOL)

# Clean the dictionary by removing words with less than a given number of occurences and
# frequent wrong words.
def clean_dict_by_occ(dictionary, occs):
    newDictionary = dictionary.copy()
    for word in list(newDictionary):
        nb_chars = 10 if len(word) > 10 else len(word)
        if nb_chars < 3:
            del newDictionary[word]
        if newDictionary[word] < occs[nb_chars-3]:
            del newDictionary[word]
    del newDictionary['eft']
    del newDictionary['fur']
    del newDictionary['fes']
    return newDictionary

# Returns the number of words in the dictionary with less than
#  a given of number of occurences for analysis purpose
def words_with_less_than_occ(dictionary, occ):
    list_words = []
    for word in list(dictionary):
        if dictionary[word] < occ:
            list_words.append(word)
    return set(list_words)

# Returns a list of words which have a given number of occurences
def get_words_by_occ(dictionary, occ):
    list_words = []
    for word in list(dictionary):
        if dictionary[word] == occ:
            list_words.append(word)
    return list_words

def get_occs(word,dictionaries):
    list_occ = []
    for dictionary in dictionaries:
        list_occ.append(dictionary[word])
    return list_occ

def plotOccurences(word, all_dicts, param):
    list_occs = get_occs(word, all_dicts)
    if param == 'article':
        y = [a/b for a, b in zip(list_occs, nb_articles_year)]
    elif param == 'word':
        y = [a/b for a, b in zip(list_occs, nb_words_year)]
    else:
        y = list_occs
    fig, ax = plt.subplots()
    x = range(0,194)
    ax.set_xticks([0, 46, 96, 146, 193])
    ax.set_xticklabels(["1804", "1850", "1900", "1950", "1997"])
    ax.plot(x,y)

def compareWordOcc(word, all_dicts):
    plotOccurences(word, all_dicts, '')
    plotOccurences(word, all_dicts, 'article')
    plotOccurences(word, all_dicts, 'word')
