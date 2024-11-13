import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
import json
import pickle

lemmatizer = WordNetLemmatizer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def lemmatize(word):
    return lemmatizer.lemmatize(word.lower())

def bag_of_words(sentence, words):
    sentence_words = [lemmatize(word) for word in tokenize(sentence)]
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1
    return bag
