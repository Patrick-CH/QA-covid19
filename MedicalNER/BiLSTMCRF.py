import tensorflow as tf
import tensorflow_addons as tfa
import numpy as np
import matplotlib.pyplot as plt
import tqdm
from keras.layers import Bidirectional, Dropout, LSTM, Embedding
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.optimizers import Adam
from MedicalNER.CRF import CRF


class MyBiLSTMCRF:
    def __init__(self, vocabSize, maxLen, tagSum, sequenceLengths=None, vecSize=256, learning_rate=0.001):
        self.vocabSize = vocabSize
        self.vecSize = vecSize
        self.maxLen = maxLen
        self.tagSum = tagSum
        self.sequenceLengths = sequenceLengths
        self.LEARNING_RATE = learning_rate
        self.BATCH_SIZE = 32
        self.buildBiLSTMCRF()

    def buildBiLSTMCRF(self):
        myModel = Sequential()
        myModel.add(tf.keras.layers.Embedding(self.vocabSize + 1, self.vecSize, trainable=False, input_length=128))
        myModel.add(Bidirectional(LSTM(128, return_sequences=True)))
        myModel.add(Bidirectional(LSTM(128, return_sequences=True)))
        myModel.add(Bidirectional(LSTM(128, return_sequences=True)))
        myModel.add(Bidirectional(LSTM(128, return_sequences=True)))
        myModel.add(Dropout(0.3))
        crf = CRF(self.tagSum, name='crf_layer')
        myModel.add(crf)
        myModel.compile(Adam(learning_rate=self.LEARNING_RATE), loss={'crf_layer': crf.get_loss}, metrics=['accuracy'])
        self.myBiLSTMCRF = myModel

    def fit(self, x, y, epochs=100):
        if len(y.shape) == 3:
            y = np.argmax(y, axis=-1)
        if self.sequenceLengths is None:
            self.sequenceLengths = [row.shape[0] for row in y]
        log_dir = "../logs"
        tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

        history = self.myBiLSTMCRF.fit(x, y, epochs=epochs, validation_split=0.2,
                                       batch_size=self.BATCH_SIZE, callbacks=[tensorboard_callback])

        acc = history.history['accuracy']
        val_acc = history.history['val_accuracy']

        loss = history.history['loss']
        val_loss = history.history['val_loss']
        epochs_range = history.epoch

        plt.figure(figsize=(8, 8))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, acc, label='Training Accuracy')
        plt.plot(epochs_range, val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.title('Training and Validation Accuracy')

        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, loss, label='Training Loss')
        plt.plot(epochs_range, val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.title('Training and Validation Loss')
        plt.show()

        return history

    def predict(self, X):
        preYArr = self.myBiLSTMCRF.predict(X)
        return preYArr

    def save_model(self, save_path):
        self.myBiLSTMCRF.save(save_path)
