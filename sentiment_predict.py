import pandas as pd
import glob
from pathlib import Path
import re
import numpy as np
import nltk
nltk.download('movie_reviews')


def load_reviews(file):
    df = pd.DataFrame(columns = ['review','sentiment'])  
    neg = glob.glob(file + '/neg/*.txt')
    pos = glob.glob(file + '/pos/*.txt')
    for i in neg:
        review = open(i,"r").read()
        df = df.append({'review':review,'sentiment':'neg'},ignore_index = True)       
    for i in pos:
        review = open(i,"r").read()
        df = df.append({'review':review,'sentiment':'pos'},ignore_index =True)
    return df


# This is the default directory and will need to be changed.
df = load_reviews(str(Path.home()) + '/nltk_data/corpora/movie_reviews')





# Here in, we tokenize every row of reviews in the dataset.
nltk.download('punkt')
for i in range(len(df['review'])):
    df['review'][i] = nltk.word_tokenize(df['review'][i])
    


# Here in, we download the stopwords and filter the words which are not in stop words.
nltk.download('stopwords')
from nltk.corpus import stopwords
stopWords = set(stopwords.words("english"))



for i in range(len(df['review'])):
    df['review'][i] = [word for word in df['review'][i] if word not in stopWords]




nltk.download('wordnet')
import nltk.stem  as stem

# Here we attempt to lemmatize every row of the dataset.
wordnet_lemmatizer = stem.WordNetLemmatizer()
for i in range(len(df['review'])):
    df['review'][i] = [wordnet_lemmatizer.lemmatize(word) for word in df['review'][i]]


for i in range(len(df['review'])):
    df['review'][i] = " ".join(df['review'][i])


# Here we convert the arrays into vectors which will be used further by the machine learning model.
X_train = df.review.to_numpy()
Y_train = df.sentiment.to_numpy()


from sklearn.feature_extraction.text import TfidfVectorizer
vec = TfidfVectorizer()
X_vectorized = vec.fit_transform(X_train)

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB()
clf.fit(X_vectorized, Y_train)



def predict_sentiment(text):
    text = nltk.word_tokenize(text)
    words = [w for w in text if w not in stopWords]
    words = [wordnet_lemmatizer.lemmatize(w) for w in words]
    text = " ".join(words) 
    text = [text]
    test_vector = vec.transform(text)
    predicted = clf.predict(test_vector)
    return predicted[0]

