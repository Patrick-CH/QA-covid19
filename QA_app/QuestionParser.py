import jieba


class QuestionParser:
    def __init__(self):
        pass

    def parse(self, q: str):
        """
        解析问题q中的实体
        :param q: 问题
        :return: {'pro':[], 'dis':[], 'sym':[], 'ite':[], 'bod':[], 'dru':[], 'mic':[], 'equ':[], 'dep'[]}
                其中，pro医疗程序, dis疾病, sym症状, ite检查科目, bod身体, dru药物, mic微生物, equ医疗设备, dep科室
        """
        key_words = {'dis': list(jieba.cut(q, use_paddle=True)), 'sym': list(jieba.cut(q, use_paddle=True)),
                     'mic': list(jieba.cut(q, use_paddle=True)), 'dru': list(jieba.cut(q, use_paddle=True))}
        return key_words