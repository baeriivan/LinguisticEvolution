import pickle
import os, sys, re

from bs4 import BeautifulSoup
from nltk.corpus import stopwords

# Cleaner function to create .pkl files from the raw xml files
# Perform some cleaning (remove stop words, punctuation and other characters)
def clean_years(DIR_XML_DATA, DIR_OUTPUT_PKL, year_start, year_end, useStopWords = False):

    #DATA_DIR = 'data/raw'
    year = year_start

    # At first, we used the stopwords to clean the data but we decided to keep them because the removal
    # of the stopwords induces errors with the t-SNE.
    if useStopWords:
        stop = set(stopwords.words('french'))
        stop.update(['ils', 'les', 'plus', 'cette', 'comme', 'tout', 'fait', 'être', 'aussi', 'faire',
                    'tous', 'dont', 'sans', 'jusqu', 'entre', 'après', 'très', 'après', 'leurs', 'encore',
                    'eft', 'sous', 'ici', 'deux', 'toutes', 'chez', 'dit', 'peut', 'fur', 'font', 'fera',
                    'avoir', 'fon', 'fes', 'cet', 'ceux', 'feront', 'quelques', 'contre', 'dès', 'autres',
                    'celle', 'esl', 'depuis', 'autre', 'autres', 'toute', 'déjà', 'élé'])
    else:
        stop = set()

    if not os.path.exists(DIR_OUTPUT_PKL):
        os.makedirs(DIR_OUTPUT_PKL)

    while year <= year_end:
        pathR = os.path.join(DIR_XML_DATA, str(year))
        fileNameW = str(year) + '.pkl'
        pathW = os.path.join(DIR_OUTPUT_PKL, fileNameW)
        
        rawTexts, articles_total = loadData(pathR)

        if articles_total > 0:
            articles = processArticles(rawTexts, stop)

            with open(pathW, 'wb') as f:
                pickle.dump(articles, f, pickle.HIGHEST_PROTOCOL)

        print('Year %s done' % year)
        year += 1

# Load the texts and some metadata for the articles from the xml files. The metadata are not used (see below)
def loadData(path):
    raw_texts = []
    labels = []
    articles_tot = 0
    if os.path.isdir(path):
        for fname in sorted(os.listdir(path)):
            fpath = os.path.join(path, fname)
            if sys.version_info < (3,):
                f = open(fpath)
            else:
                f = open(fpath, encoding='utf-8')
            xmldata=BeautifulSoup(f.read(), 'xml')

            articlesID = xmldata.find_all('id')
            titles = xmldata.find_all('name')
            dates = xmldata.find_all('issue_date')
            words_count = xmldata.find_all('word_count')
            textes = xmldata.find_all('full_text')
            textes = [raw_text.text for raw_text in textes]

            # The metadata are not currently used but we can analyze them to
            # imporove the efficienty of the cleaning by discarding unrelevant
            # articles from the start.
            metaData = [ articlesID, titles, dates, words_count ]
            labels.append(metaData)

            raw_texts.append(textes)
            articles_tot += len(articlesID)
            print('%s articles processed' % articles_tot)
            f.close()
        
    print('Found %s texts.' % len(raw_texts))
    return raw_texts, articles_tot

# Process the articles by year and remove numbers, punctuation, stopwords and very small words
def processArticles(raw_texts, stop):
    all_articles_by_year = []
    for raw_text in raw_texts:
        all_articles_by_month = []
        for article in raw_text:
            words = re.findall(r'[A-zÀ-ÿ\-]+', article)
            words = [word.lower() for word in words if word.lower() not in stop]
            words = [word for word in words if len(word) > 2]
            all_articles_by_month.append(words)
        all_articles_by_year.append(all_articles_by_month)
    return all_articles_by_year
