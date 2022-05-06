import jieba
from py2neo import Graph

from QuestionParser import QuestionParser
from question_classifier import QuestionClassifier
from AnswerSearch import AnswerSearcher
from AnswerBuild import build_answer


class ChatBot:
    def __init__(self):
        self.questionClassifier = QuestionClassifier()
        self.questionParser = QuestionParser()
        self.answerSearcher = AnswerSearcher()
        print("chat bot 加载完成")

    def answer(self, q):
        # pro医疗程序, dis疾病, sym症状, ite检查科目, bod身体, dru药物, mic微生物, equ医疗设备, dep科室
        key_words = self.questionParser.parse(q)
        intention = self.questionClassifier.classify(q, [x for x in key_words.keys() if len(key_words[x]) > 0])
        print(intention)
        ans = ''
        for it in intention:
            data = self.answerSearcher.answer_search(it, key_words)
            ans += build_answer(it, data)
        if len(ans) == 0:
            ans = "抱歉我无法解答您的问题\n"
        return ans


if __name__ == '__main__':
    bot = ChatBot()
    s = input('请输入您的问题\n')
    while s != 'exit':
        print(bot.answer(s))
        s = input('请输入您的问题\n')
