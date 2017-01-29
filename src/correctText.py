from dictFcts import *
from helpers import *
import pickle
from nltk.corpus import stopwords

# arbitrary values to remove words with less than these occurences
occs_merged1  = [5,5,5,10,10,10,10,10]
occs_merged2  = [15,15,15,25,25,50,50,50]
occs_merged3  = [50,50,50,100,100,100,200,200]

# Creating cleaned dictionaries by removing the less frequent occurences
year = 1810
fileName = 'data/dico/10yearsGDL/'+ str(year) + '-' + str(year + 10) + '.pkl'
dico_10years = load_dictionary(fileName)
dico_10year_merged1 = clean_dict_by_occ(dico_10years, occs_merged1)
dico_10year_merged2 = clean_dict_by_occ(dico_10years, occs_merged2)
dico_10year_merged3 = clean_dict_by_occ(dico_10years, occs_merged3)


def words(text): return re.findall(r'[A-zÀ-ÿ\-]+', text.lower())
# Functions to perform spellchecking on a single word given a dicitonary
def spellChecker(word, dictionary):
    WORDS = dictionary

    def P(word, N=sum(WORDS.values())):
        "Probability of the word"
        return WORDS[word] / N

    def correction(word):
        "Most probable spelling correction for word."
        return max(candidates(word.lower()), key=P)

    def candidates(word):
        "Generate possible spelling corrections for word."
        return (known([word]) or known(edits1(word)) or [word])

    def known(words):
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in WORDS)

    def edits1(word):
        "All edits that are one edit away from `word`."
        letters = 'abcdefghijklmnopqrstuvwxyzéèêàâîïùüöä '
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        splits2 = [(word[:i], word[(i + 1):]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        doubless = [L + c + c + R[1:] for L, R in splits2 for c in 's']
        return set(deletes + transposes + replaces + inserts + doubless)

    return correction(word)

stop = set(stopwords.words('french'))
stop.update(['ils', 'les', 'plus', 'cette','comme', 'tout',
             'fait', 'être', 'aussi', 'faire', 'tous', 'dont',
             'sans', 'jusqu', 'entre', 'après','très', 'après',
             'leurs', 'encore','sous', 'ici', 'deux', 'toutes',
             'chez', 'dit', 'peut', 'avoir','cet', 'ceux',
             'quelques', 'contre','dès', 'autres', 'celle',
             'depuis', 'autre', 'autres', 'toute', 'déjà', 'test'])

# Check each word of a text given a dictionary
def useDict(text_data, dictionary):
    list_words = []
    for word in text_data:
        if word in stop:
            list_words.append(word)
        else:
            list_words.append(spellChecker(word, dictionary))
    return list_words

# Clean all the articles using the combinations of 3 dictionaries
def cleanArticles(text_data, merged_1, merged_2, merged_3):
    list_merged1 = useDict(text_data, merged_1)
    list_merged2 = useDict(list_merged1, merged_2)
    list_merged3 = useDict(list_merged2, merged_3)
    return list_merged3

# Main script to clean articles
year_s = 1840
year_e = 1850
testYears = range(year_s,year_e)
testData = loadYears('data/raw/GDL_pkl/', testYears)

articles = []
i = 0
for article in testData:
    if i%100 == 0:
        print(str(i) + ' articles cleaned, ' + str(len(testData)-i) + ' remaining')
    article = cleanArticles(article, dico_10year_merged1, dico_10year_merged2, dico_10year_merged3)
    articles.append(article)
    i+=1

with open('data/cleanedData/' + str(year_s) + '-' + str(year_e) + '.pkl', 'wb') as f:
    pickle.dump(articles, f, pickle.HIGHEST_PROTOCOL)

print(year_s)
