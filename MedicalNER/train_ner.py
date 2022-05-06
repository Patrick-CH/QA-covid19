import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from tensorflow.python.keras.layers import Bidirectional, LSTM
from tensorflow.python.keras.losses import CategoricalCrossentropy
from tensorflow.python.keras.optimizer_v2.adam import Adam

from MedicalNER.CRF import CRF
from data_process import DataProcessor

tfhub_handle_preprocess = "D:/workspace/PycharmProjects/Covid-19-QA/pretrained_model/bert_zh_preprocess_3"
tfhub_handle_encoder = "D:/workspace/PycharmProjects/Covid-19-QA/pretrained_model/bert_zh_L-12_H-768_A-12_4"


def build_classifier_model(tag_num):
    # 定义模型
    text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='inputs')
    preprocessing_layer = hub.KerasLayer(tfhub_handle_preprocess, name='preprocessing')
    encoder_inputs = preprocessing_layer(text_input)
    encoder = hub.KerasLayer(tfhub_handle_encoder, trainable=True, name='BERT_encoder')
    outputs = encoder(encoder_inputs)
    sequence_output = outputs["sequence_output"]
    sequence_output = Bidirectional(LSTM(128, return_sequences=True))(sequence_output)
    # sequence_output = Bidirectional(LSTM(128, return_sequences=True))(sequence_output)
    sequence_output = Bidirectional(LSTM(64))(sequence_output)
    net = tf.keras.Model(text_input, sequence_output)
    print("define model done!")
    return net


if __name__ == '__main__':
    dp = DataProcessor()
    dp.process()
    train_x = tf.constant(dp.train_x)
    train_y = tf.constant(dp.train_y)
    print(train_x.shape, train_y.shape)
    model = build_classifier_model(len(dp.types))
    model.summary()
    model.compile(Adam(3e-4, epsilon=1e-8), loss="CategoricalCrossentropy", metrics=['accuracy'])
    history = model.fit(train_x, train_y, epochs=5, batch_size=4, validation_split=0.2)
    model.save_model("model\\bert_ner_v0")
    sentences = tf.constant(dp.train_x[:3])
    print(model(sentences))
