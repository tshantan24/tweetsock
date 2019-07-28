import os
import re
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf
from string import punctuation
from model.train import pre_process, encode_and_pad
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
    padded_tweets = encode_and_pad(tweets_processed, tokenizer, max_sent_len)
    predictions = trained_model.predict_classes(padded_tweets)

    rep_per = sum(predictions)
    dem_per = len(predictions) - sum(predictions)

    if rep_per > dem_per:
        return 1
    else:
        return 0