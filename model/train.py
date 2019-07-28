import re
import os
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf
from string import punctuation
from tensorflow.keras import Sequential
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Dense, Dropout, Activation, Embedding, CuDNNLSTM, Bidirectional

PUNCTUATION = punctuation + "—\n\t"
regex = re.compile('[%s]' % re.escape(PUNCTUATION))

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'model/data/data.csv')
TRAINING_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),"model/training/cp-{epoch:04d}.ckpt")
TOKENIZER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'main/trained/tokenizer.pickle')
META_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'main/trained/meta.csv')
WEIGHTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'main/trained/weights.h5')

def remove_punctuations(sentence):
    return regex.sub('', sentence)

def deEmojify(inputString):
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
#     X = X.str.replace(r"[^A-Za-z0-9(),!?@\'\`\"\_\n]", " ")
    X = X.apply(remove_punctuations)
    X = X.str.replace(r"@", "at")
    X = X.apply(deEmojify)
    X = X.str.lower()
    
    #Removes null values
    ind = list(X[X==""].index)
    x = X.drop(ind)
    
    if 'Y' in kwargs:
        y = kwargs['Y'].drop(ind)
        return x, y
        
    return x


def encode_and_pad(X, t):
    encoded_x = t.texts_to_sequences(X)
    padded_x = pad_sequences(encoded_x, maxlen=max_sent_len, padding='post')
    return padded_x


def train():

    #Pre-processing
    
    df = pd.read_csv(DATA_PATH)
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df.dropna(axis=0, inplace=True)
    # df.head(10)

    df['Party'] = pd.Categorical(df.Party)
    df['Party'] = pd.get_dummies(df['Party'], drop_first=True)

    X = df['Tweet']
    Y = df['Party']

    x, y = pre_process(X, Y=Y)

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=420)

    #Creating a tokenizer
    t = Tokenizer(oov_token="UNK")
    t.fit_on_texts(x)

    vocab_size = len(t.word_index) + 1
    print("Vocabulary size: {}".format(vocab_size))
    max_sent_len = len(max(x, key=len).split()) + 1
    print("Maximum sentence length: {}".format(max_sent_len))
    emb_dim = 75
    print("Embedding Dimensions: {}".format(emb_dim))

    padded_X_train = encode_and_pad(X_train, t)

    x_train, x_val, Y_train, y_val = train_test_split(padded_X_train, y_train, test_size=0.1, random_state=420)

    checkpoint_path = TRAINING_PATH
    cp_callback = ModelCheckpoint(checkpoint_path, verbose=1, save_weights_only=True, period=20)

    model = Sequential([
        Embedding(input_dim=vocab_size, output_dim=emb_dim, input_length=max_sent_len, trainable=True),
        Bidirectional(CuDNNLSTM(64, return_sequences=False)),
        Dropout(0.5),
        Dense(2, activation='softmax')
    ])

    model.save_weights(checkpoint_path.format(epoch=0))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(x_train, Y_train, epochs=200, batch_size=300, shuffle=True, callbacks = [cp_callback], validation_data=(x_val, y_val))
    model.save_weights(WEIGHTS_PATH)

    dic = {'Vocab Size': vocab_size, 'Max Sent Length': max_sent_len, 'Emb Dim': emb_dim}
    meta_df = pd.DataFrame(dic, index=['Model 1'])
    meta_df.to_csv(META_PATH)

    with open(TOKENIZER_PATH, 'wb') as handle:
        pickle.dump(t, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("Training done.")

if __name__ == "__main__":
    train()



