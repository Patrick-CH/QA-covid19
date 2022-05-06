import json
import numpy as np
import tensorflow as tf
import tensorflow_text as text


class QuestionClassifier:
    def __init__(self):
        # 加载模型
        self.model = tf.keras.models.load_model("D:/workspace/PycharmProjects/Covid-19-QA/model/QClasssifiervV1")
        # 读取分类名称
        # with open("D:/workspace/PycharmProjects/Covid-19-QA/data/qic_idx.json", "r", encoding='UTF-8') as f:
        #     data = json.loads(f.read())
        #     self.qic_s = data
        self.qic_s = ["治疗方案", "其他", "疾病表述", "病因分析", "注意事项", "功效作用", "病情诊断", "就医建议", "医疗费用", "指标解读", "后果表述"]
        print("read diseases file done!")
        self.check_qwds = ['检查', '检查项目', '查出', '检查', '测出', '试出']
        self.cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
                          '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要']
        self.prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止', '躲避', '逃避', '避开', '免得', '逃开', '避开', '避掉', '躲开', '躲掉', '绕开',
                             '怎样才能不', '怎么才能不', '咋样才能不', '咋才能不', '如何才能不',
                             '怎样才不', '怎么才不', '咋样才不', '咋才不', '如何才不',
                             '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                             '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        self.cause_qwds = ['原因', '成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致',
                           '会造成']
        self.drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
        self.rel_qwds = ['关系', '关联']
        self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现']

    '''基于特征词进行分类'''

    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False

    def classify_by_kw(self, q, types):
        question_types = set()
        # 疾病接受检查项目
        if self.check_words(self.check_qwds, q) and 'dis' in types:
            question_type = '疾病-检查'
            question_types.add(question_type)

        # 已知检查项目查相应疾病
        if self.check_words(self.check_qwds + self.cure_qwds, q) and 'ite' in types:
            question_type = '检查-疾病'
            question_types.add(question_type)

        # 症状查询
        if self.check_words(self.symptom_qwds, q) and ('dis' in types):
            question_type = '临床症状'
            question_types.add(question_type)

        # 症状预防
        if self.check_words(self.prevent_qwds, q) and 'dis' in types:
            question_type = '疾病预防'
            question_types.add(question_type)

        # 病因分析
        if self.check_words(self.cause_qwds, q) and ('dis' in types):
            question_type = '病因分析'
            question_types.add(question_type)

        # 关系查寻
        # if self.check_words(self.drug_qwds, q) and 'dis' in types:
        #     question_type = '推荐药品'
        #     question_types.add(question_type)

        return question_types

    def classify_by_model(self, q):
        # 预测句子的分类
        test_examples = np.array([q])
        p = self.model(test_examples)
        r = np.argmax(p, axis=1)
        return self.qic_s[r[0]]

    def classify(self, q: str, e_types) -> set:
        """
        对问题进行分类
        :param e_types: 实体类型
        :param q: 问题
        :return: {c1, c2...} 问题的分类
        """
        c1 = self.classify_by_model(q)
        c2 = self.classify_by_kw(q, e_types)
        if len(c2) > 0:
            return c2
        if c1 == '其他':
            return c2
        return {c1}

    def evaluate(self):
        di = {}
        labels = ["治疗方案", "其他", "疾病表述", "病因分析", "注意事项", "功效作用", "病情诊断", "就医建议", "医疗费用", "指标解读", "后果表述"]
        for i in labels:
            di[i] = {"TP": 0, "FP": 0, "TN": 0, "FN": 0}
        with open("D:/workspace/PycharmProjects/Covid-19-QA/data/KUAKE-QIC/KUAKE-QIC_dev.json", "r",
                  encoding="UTF-8") as f:
            test_data = json.loads(f.read())
        if test_data:
            t, f = 0, 0
            for q in test_data:
                result = self.classify_by_model(q["query"])
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
