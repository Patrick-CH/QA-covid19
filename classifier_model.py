import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from tensorflow.python.keras.optimizer_v2.adam import Adam


class ClassifierModel:
    def __init__(self):
        # 定义路径
        self.tfhub_handle_preprocess = "pretrained_model/bert_zh_preprocess_3"
        self.tfhub_handle_encoder = "pretrained_model/bert_zh_L-12_H-768_A-12_4"
        self.diseases_file = "data/diseases.json"
        self.qic_file = "data/qic_idx.json"
        self.model_save_path = "model/QClasssifiervV1"
        # 训练参数
        self.lr = 1e-3
        self.batch_size = 32
        self.epochs = 20
        # 其他变量初始化
        self.net = None
        self.qic_s = []
        self.diseases = []
        self.train_x = []
        self.train_y = []
        self.maxLen = 0

    def read_class_file(self, dataset_name):
        # 读取分类名称
        if dataset_name == "test":
            with open(self.diseases_file, "r", encoding='UTF-8') as f:
                data = json.loads(f.read())
                self.diseases = data['diseases']
        elif dataset_name == "qic":
            with open(self.qic_file, "r", encoding='UTF-8') as f:
                data = json.loads(f.read())
                self.qic_s = data
        print("read diseases file done!")

    def build_classifier_model(self, class_num):
        # 定义模型
        text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='inputs')
        preprocessing_layer = hub.KerasLayer(self.tfhub_handle_preprocess, name='preprocessing')
        encoder_inputs = preprocessing_layer(text_input)
        encoder = hub.KerasLayer(self.tfhub_handle_encoder, trainable=False, name='BERT_encoder')
        outputs = encoder(encoder_inputs)
        net = outputs['pooled_output']
        net = tf.keras.layers.Dropout(0.1)(net)
        net = tf.keras.layers.Dense(class_num, activation=None, name='classifier')(net)
        self.net = tf.keras.Model(text_input, net)
        print("define model done!")

    def load_data(self, dataset_name):
        # 加载数据
        train_x = []
        train_y = []
        if dataset_name == "test":
            df = pd.read_csv("data/test.csv")
            for index, line in df.iterrows():
                temp_y = np.zeros(len(self.diseases))
                temp_y[self.diseases.index(line["category"])] = 1
                train_x.append(line["query1"])
                train_y.append(temp_y)
                train_x.append(line["query2"])
                train_y.append(temp_y)
        elif dataset_name == "qic":
            with open("data/KUAKE-QIC/KUAKE-QIC_train.json", "r", encoding='UTF-8') as f:
                data = json.loads(f.read())
            if data:
                for i in data:
                    train_x.append(i["query"])
                    if i["label"] not in self.qic_s:
                        self.qic_s.append(i["label"])
                    temp_y = np.zeros(11)
                    temp_y[self.qic_s.index(i["label"])] = 1
                    train_y.append(temp_y)
            with open("data/qic_idx.json", "w", encoding="UTF-8") as f:
                f.write(json.dumps(self.qic_s, ensure_ascii=False))
        else:
            print("name err")
            exit(-1)
        self.train_x = np.array(train_x)
        self.train_y = np.array(train_y)
        self.maxLen = max([len(i) for i in train_x])
        print("maxLen:\t", self.maxLen)
        print(len(train_x), len(train_y))
        print("load data done!")

    def train(self):
        # 编译模型
        loss = tf.keras.losses.BinaryCrossentropy(from_logits=True)
        metrics = tf.metrics.Accuracy()
        self.net.compile(optimizer=Adam(self.lr), loss=loss, metrics=metrics)
        self.net.summary()
        # 训练模型
        history = self.net.fit(self.train_x, self.train_y, epochs=self.epochs, validation_split=0.2,
                               batch_size=self.batch_size)

        # 训练过程可视化
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

        # 模型保存
        self.net.save(self.model_save_path)

    def run(self, dataset_name):
        if dataset_name == "test":
            class_num = 10
        else:
            class_num = 11
        self.read_class_file(dataset_name)
        self.load_data(dataset_name)
        self.build_classifier_model(class_num)
        self.train()


if __name__ == '__main__':
    model = ClassifierModel()
    model.run("qic")
