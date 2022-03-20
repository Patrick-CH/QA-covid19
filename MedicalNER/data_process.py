import json
import re
import pandas as pd
import numpy as np


class DataProcessor:
    def __init__(self, train_path="D:/workspace/PycharmProjects/Covid-19-QA/data/CMeEE/CMeEE_train.json",
                 test_path="D:/workspace/PycharmProjects/Covid-19-QA/data/CMeEE/CMeEE_test.json"):
        self.train_x, self.train_y, self.test_x, self.test_y, self.types = [], [], [], [], ['O']
        with open(train_path, "r", encoding='UTF-8') as f:
            self.train_data = json.loads(f.read())
        with open(test_path, "r", encoding='UTF-8') as f:
            self.test_data = json.loads(f.read())

    def process(self):
        if self.train_data and self.test_data:
            self.train_x, self.train_y = self.process_data(self.train_data)
            self.test_x, self.test_y = self.process_data(self.test_data)
            maxL = max([len(i) for i in self.train_x])
            print(maxL)
            with open("/data/tags_ner.json", "w", encoding='UTF-8') as f:
                f.write(json.dumps(self.types))
            print("数据读取完成")
        else:
            print("数据读取失败")

    def process_data(self, data):
        x, y = [], []
        for i in data:
            temp_y = np.zeros(128)
            for e in i['entities']:
                if e['type'] not in self.types:
                    self.types.append(e['type'])
                temp_y[e['start_idx']:e['end_idx'] + 1] = self.types.index(e['type'])
            if len(i['text']) > 128:
                ls = re.split("[。，;\\n]", i['text'])
                for sub_s in ls:
                    sub_temp_y = temp_y[:len(sub_s)]
                    temp_y = temp_y[len(sub_s):]
                    if len(sub_s) < 128:
                        self.train_x.append(sub_s + ' ' * (128-len(sub_s)))
                        yit = np.zeros(128)
                        yit[:len(sub_temp_y)] = sub_temp_y
                        self.train_y.append(yit)
            else:
                x.append(i['text'])
                y.append(temp_y)
        return x, y


if __name__ == '__main__':
    d = DataProcessor()
    d.process()
