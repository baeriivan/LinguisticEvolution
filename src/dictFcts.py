import pickle, re
import os
from collections import Counter

def words(text): return re.findall(r'[A-zÀ-ÿ\-]+', text.lower())

# Creates a dictionary for a range of years from the raw articles
def create_dictionary(years, DirRead, DirWrite):
    big_text = ""
    for year in years:
        fileName = DirRead + str(year) + '.pkl'
        if os.path.exists(fileName):
            with open(fileName, 'rb') as f:
                all_art_year = pickle.load(f)
                flattened_text = ' '.join([word for all_art_month in all_art_year for article in all_art_month for word in article])
                big_text += flattened_text
        else:
            print(fileName + "doesn't exist")
    print(len(big_text))

    WORDS = Counter(words(big_text))
    fileName = DirWrite + str(years[0])+ '-' + str(years[-1]) + '-Dic.pkl'
    with open(fileName, 'wb') as f:
        pickle.dump(WORDS, f, pickle.HIGHEST_PROTOCOL)

# Loads multiple dictionaries in order to merge them later
def load_dictionaries(path, from_date, to_date):
    dictionaries = []
    if os.path.isdir(path):
        for year in range(from_date, to_date + 1):
            filePath = path + str(year) + '-' + str(year) + '-Dic.pkl'
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