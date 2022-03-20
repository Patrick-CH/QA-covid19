import json
import numpy as np
import tensorflow as tf
import tensorflow_text as text


class QuestionClassifier:
    def __init__(self):
        # 加载模型
        self.model = tf.keras.models.load_model("D:/workspace/PycharmProjects/Covid-19-QA/model/QClasssifiervV1")
        # 读取分类名称
        with open("D:/workspace/PycharmProjects/Covid-19-QA/data/qic_idx.json", "r", encoding='UTF-8') as f:
            data = json.loads(f.read())
            self.qic_s = data
        print("read diseases file done!")

    def predict(self, q):
        # 预测句子的分类
        test_examples = np.array([q])
        p = self.model(test_examples)
        r = np.argmax(p, axis=1)
        return self.qic_s[r[0]]

    def evaluate(self):
        di = {}
        labels = ["治疗方案", "其他", "疾病表述", "病因分析", "注意事项", "功效作用", "病情诊断", "就医建议", "医疗费用", "指标解读", "后果表述"]
        for i in labels:
            di[i] = {"TP": 0, "FP": 0, "TN": 0, "FN": 0}
        with open("D:/workspace/PycharmProjects/Covid-19-QA/data/KUAKE-QIC/KUAKE-QIC_dev.json", "r", encoding="UTF-8") as f:
            test_data = json.loads(f.read())
        if test_data:
            t, f = 0, 0
            for q in test_data:
                result = self.predict(q["query"])
                if result == q["label"]:
                    t += 1
                    di[result]["TP"] += 1
                    for i in labels:
                        if i != result:
                            di[i]["TN"] += 1
                else:
                    f += 1
                    di[q["label"]]["FN"] += 1
                    di[result]["FP"] += 1
                    for i in labels:
                        if i != q["label"] and i != result:
                            di[i]["TN"] += 1
            for i in di.keys():
                precision = di[i]["TP"] / (di[i]["TP"] + di[i]["FP"])
                recall = di[i]["TP"] / (di[i]["TP"] + di[i]["FN"])
                f1 = 2 * precision * recall / (precision + recall)
                print(i + ":\tprecision: %.2f\trecall: %.2f\tf1: %.2f" % (precision * 100, recall * 100, f1 * 100))
            print("acc:\t%.2f" % (t * 100 / (t + f)))
