import os
import random
import sys

import numpy as np
from keras.layers import LSTM, Activation, Dense, Dropout
from keras.models import Sequential, load_model
from keras.optimizers import Adam
from keras.callbacks import TensorBoard

from dataset import DataSet

SAVE_PATH = 'saves/latest.h5'

text = open('clean_posts.txt', 'r').read()
data = DataSet(text)

len_section = 50
batch_size = 64

print("Build model...")
if (os.path.exists(SAVE_PATH)):
    model = load_model(SAVE_PATH)
else:
    model = Sequential()
    model.add(LSTM(1024, return_sequences=True, input_shape=(len_section, data.char_size)))
    model.add(Dropout(0.5))
    model.add(LSTM(512))
    model.add(Dense(data.char_size))
    model.add(Activation('softmax'))

    optimizer = Adam()
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)

def sample(preds, div):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / div
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

tbCallBack = TensorBoard(write_images=True)
tbCallBack.set_model(model)

for iteration in range(1, 70000):
    if iteration % 100 == 0:
        print()
        print('-' * 80)
        print('Iteration', iteration)

    x, y = data.next_batch(batch_size, len_section)
    model.train_on_batch(x, y)

    start_index = random.randint(0, len(data.text) - len_section - 1)

    if iteration % 1000 == 0:
        model.save(SAVE_PATH)
        for diversity in [0.2, 0.5, 1.0, 1.2]:
            print()
            print('----- diversity:', diversity)

            generated = ''
            sentence = data.text[start_index: start_index + len_section]
            generated += sentence

            print('----- Generating with seed: "' + sentence + '"')
            sys.stdout.write(generated)

            for i in range(400):
                x_pred = np.zeros((1, len_section, data.char_size))
                for t, char in enumerate(sentence):
                    x_pred[0, t, data.char2id[char]] = 1.

                preds = model.predict(x_pred, verbose=0)[0]
                next_index = sample(preds, diversity)
                next_char = data.id2char[next_index]

                generated += next_char
                sentence = sentence[1:] + next_char

                sys.stdout.write(next_char)
                sys.stdout.flush()
            print()
