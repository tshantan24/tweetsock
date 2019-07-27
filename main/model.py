import os
import re
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf
from string import punctuation
from tensorflow.keras import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences
from django.contrib.staticfiles.templatetags.staticfiles import static
from tensorflow.keras.layers import Dense, Dropout, LSTM, Activation, Embedding, Bidirectional

TOKENIZER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'main/trained/tokenizer.pickle')
META_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'main/trained/meta.csv')
WEIGHTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'main/trained/weights.h5')

PUNCTUATION = punctuation + "—\n\t"
regex = re.compile('[%s]' % re.escape(PUNCTUATION))

with open(TOKENIZER_PATH, 'rb') as handle:
    tokenizer = pickle.load(handle)

meta = pd.read_csv(META_PATH, index_col=0)
vocab_size = meta.loc['Model 1', 'Vocab Size']
max_sent_len = meta.loc['Model 1', 'Max Sent Length']
emb_dim = meta.loc['Model 1', 'Emb Dim']


def remove_punctuations(sentence):
    return regex.sub('', sentence)


def de_Emojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')


def pre_process(X, **kwargs):
    # Replaces special characters
    X = X.str.replace(r"http\S+", "")
    X = X.str.replace(r"http", "")
    X = X.str.replace(r"@\S+", "")
    X = X.str.replace('&amp;', "and")
    X = X.str.replace('\xa0', " ")
    X = X.str.replace('\u2003', " ")
    X = X.str.replace(r"\\u\S+", "")

    X = X.apply(remove_punctuations)
    X = X.str.replace(r"@", "at")
    X = X.apply(de_Emojify)
    X = X.str.lower()
    
    #Removes null values
    ind = list(X[X==""].index)
    x = X.drop(ind)
    
    if 'Y' in kwargs:
        y = kwargs['Y'].drop(ind)
        return x, y
        
    return x


def encode_and_pad(X):
    encoded_x = tokenizer.texts_to_sequences(X)
    padded_x = pad_sequences(encoded_x, maxlen=max_sent_len, padding='post')
    return padded_x


def get_model():

    model = Sequential([
        Embedding(input_dim=vocab_size, output_dim=emb_dim, input_length=max_sent_len, trainable=False),
        Bidirectional(LSTM(64, return_sequences=False, recurrent_activation='sigmoid')),
        Dropout(0.5),
        Dense(2, activation='softmax')
    ])
    model.load_weights(WEIGHTS_PATH)
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# trained_model = get_model()
# print(trained_model.summary())

def predict(tweets):

    trained_model = get_model()
    print(trained_model.summary())

    tweets_processed = pre_process(tweets)
    padded_tweets = encode_and_pad(tweets_processed)
    predictions = trained_model.predict_classes(padded_tweets)

    rep_per = sum(predictions)
    dem_per = len(predictions) - sum(predictions)

    if rep_per > dem_per:
        return 1
    else:
        return 0