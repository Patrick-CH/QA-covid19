# "治疗方案", "其他", "疾病表述", "病因分析", "注意事项", "功效作用", "病情诊断", "就医建议", "医疗费用", "指标解读", "后果表述"
from py2neo import Graph
import re
from difflib import SequenceMatcher


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


class AnswerSearcher:
    def __init__(self):
        self.std_keywords = {
            "医学专科": [],
            "检查科目": [],
            "疾病": [],
            "病毒": [],
            "症状": [],
            "细菌": [],
            "药物": []
        }
        self.extend_keywords = {
            "发病部位": []
        }
        self.intention = None
        self.keywords = None
        self.g = Graph(
            "bolt://124.223.80.199:7687",  # uri
            user="neo4j",
            password="112358")
        print("AnswerSearcher 加载成功")

    def _normalize_keywords(self):
        """
        基础信息规范化
        NER结果    pro医疗程序, dis疾病, sym症状, ite检查科目, bod身体, dru药物, mic微生物, equ医疗设备, dep科室
        :return: dict
        {
            "医学专科": [],
            "检查科目": [],
            "疾病": [],
            "病毒": [],
            "症状": [],
            "细菌": [],
            "药物": []
        }
        """
        std_similarity = 0.75

        if 'dis' in self.keywords.keys():
            temp_dis = []
            for dis in self.keywords['dis']:
                gql = "MATCH (p:`疾病`) WHERE p.name = '{}' RETURN p.name".format(dis)
                result = self.g.run(gql).data()
                if len(result) > 0:
                    temp_dis += list(set([j['p.name'] for j in result]))
                else:
                    gql = "MATCH (p:`疾病`) WHERE p.name =~ '.*{}.*' RETURN p".format(dis)
                    result = self.g.run(gql).data()
                    for d in result:
                        for k in d.keys():
                            if similarity(d[k]['name'], dis) >= std_similarity and (d[k]['name'] not in temp_dis):
                                temp_dis.append(d[k]['name'])
            self.std_keywords["疾病"] += temp_dis

        if 'sym' in self.keywords.keys():
            temp_sym = []
            for sym in self.keywords['sym']:
                gql = "MATCH (p:`症状`) WHERE p.name = '{}' RETURN p.name".format(sym)
                result = self.g.run(gql).data()
                if len(result) > 0:
                    temp_sym += list(set([j['p.name'] for j in result]))
                else:
                    gql = "MATCH (p:`症状`) WHERE p.name =~ '.*{}.*' RETURN p".format(sym)
                    result = self.g.run(gql).data()
                    for d in result:
                        for k in d.keys():
                            if similarity(d[k]['name'], sym) >= std_similarity and (d[k]['name'] not in temp_sym):
                                temp_sym.append(d[k]['name'])
            self.std_keywords["症状"] += temp_sym

        if 'pro' in self.keywords.keys():
            temp_pro = []
            for pro in self.keywords['pro']:
                gql = "MATCH (p:`检查科目`) WHERE p.name = '{}' RETURN p.name".format(pro)
                result = self.g.run(gql).data()
                if len(result) > 0:
                    temp_pro += list(set([j['p.name'] for j in result]))
                else:
                    gql = "MATCH (p:`检查科目`) WHERE p.name =~ '.*{}.*' RETURN p".format(pro)
                    result = self.g.run(gql).data()
                    for d in result:
                        for k in d.keys():
                            if similarity(d[k]['name'], pro) >= std_similarity and (d[k]['name'] not in temp_pro):
                                temp_pro.append(d[k]['name'])
            self.std_keywords["检查科目"] += temp_pro

        if 'ite' in self.keywords.keys():
            temp_ite = []
            for ite in self.keywords['ite']:
                gql = "MATCH (p:`检查科目`) WHERE p.name = '{}' RETURN p.name".format(ite)
                result = self.g.run(gql).data()
                if len(result) > 0:
                    temp_ite += list(set([j['p.name'] for j in result]))
                else:
                    gql = "MATCH (p:`检查科目`) WHERE p.name =~ '.*{}.*' RETURN p".format(ite)
                    result = self.g.run(gql).data()
                    for d in result:
                        for k in d.keys():
                            if similarity(d[k]['name'], ite) >= std_similarity and (d[k]['name'] not in temp_ite):
                                temp_ite.append(d[k]['name'])
            self.std_keywords["检查科目"] += temp_ite

        if 'equ' in self.keywords.keys():
            temp_equ = []
            for equ in self.keywords['equ']:
                gql = "MATCH (p:`检查科目`) WHERE p.name = '{}' RETURN p.name".format(equ)
                result = self.g.run(gql).data()
                if len(result) > 0:
                    temp_equ += list(set([j['p.name'] for j in result]))
                else:
                    gql = "MATCH (p:`检查科目`) WHERE p.name =~ '.*{}.*' RETURN p".format(equ)
                    result = self.g.run(gql).data()
                    for d in result:
                        for k in d.keys():
                            if similarity(d[k]['name'], equ) >= std_similarity and (d[k]['name'] not in temp_equ):
                                temp_equ.append(d[k]['name'])
            self.std_keywords["检查科目"] += temp_equ

        if 'dru' in self.keywords.keys():
            temp_dru = []
            for dru in self.keywords['dru']:
                gql = "MATCH (p:`药物`) WHERE p.name = '{}' RETURN p.name".format(dru)
                result = self.g.run(gql).data()
                if len(result) > 0:
                    temp_dru += list(set([j['p.name'] for j in result]))
                else:
                    gql = "MATCH (p:`药物`) WHERE p.name =~ '.*{}.*' RETURN p".format(dru)
                    result = self.g.run(gql).data()
                    for d in result:
                        for k in d.keys():
                            if similarity(d[k]['name'], dru) >= std_similarity and (d[k]['name'] not in temp_dru):
                                temp_dru.append(d[k]['name'])
            self.std_keywords["药物"] += temp_dru

        if 'mic' in self.keywords.keys():
            temp_bac = []
            temp_vir = []
            for mic in self.keywords['mic']:
                gql = "MATCH (p:`病毒`) WHERE p.name = '{}' RETURN p.name".format(mic)
                result = self.g.run(gql).data()
                if len(result) > 0:
                    temp_vir += list(set([j['p.name'] for j in result]))
                else:
                    gql = "MATCH (p:`病毒`) WHERE p.name =~ '.*{}.*' RETURN p".format(mic)
                    result = self.g.run(gql).data()
                    for d in result:
                        for k in d.keys():
                            if similarity(d[k]['name'], mic) >= std_similarity and (d[k]['name'] not in temp_vir):
                                temp_vir.append(d[k]['name'])

                gql = "MATCH (p:`细菌`) WHERE p.name = '{}' RETURN p.name".format(mic)
                result = self.g.run(gql).data()
                if len(result) > 0:
                    temp_vir += list(set([j['p.name'] for j in result]))
                else:
                    gql = "MATCH (p:`细菌`) WHERE p.name =~ '.*{}.*' RETURN p".format(mic)
                    result = self.g.run(gql).data()
                    for d in result:
                        for k in d.keys():
                            if similarity(d[k]['name'], mic) >= std_similarity and (d[k]['name'] not in temp_bac):
                                temp_bac.append(d[k]['name'])
            self.std_keywords["细菌"] += temp_bac
            self.std_keywords["病毒"] += temp_vir

        if 'dep' in self.keywords.keys():
            temp_dep = []
            for dep in self.keywords['dep']:
                gql = "MATCH (p:`医学专科`) WHERE p.name = '{}' RETURN p.name".format(dep)
                result = self.g.run(gql).data()
                if len(result) > 0:
                    temp_dep += list(set([j['p.name'] for j in result]))
                else:
                    gql = "MATCH (p:`医学专科`) WHERE p.name =~ '.*{}.*' RETURN p".format(dep)
                    result = self.g.run(gql).data()
                    for d in result:
                        for k in d.keys():
                            if similarity(d[k]['name'], dep) >= std_similarity and (d[k]['name'] not in temp_dep):
                                temp_dep.append(d[k]['name'])
            self.std_keywords["药物"] += temp_dep

        if 'bod' in self.keywords.keys():
            self.extend_keywords["发病部位"] += self.keywords['bod']

    def _get_dis_info(self, dis):
        """
        查询疾病信息
        :param dis: str 疾病名称
        :return: dis_info 字典，包含如下信息
        {
            'subject': 'xx科'
            'sym': ['症状1', '症状2']
            'plan': [('症状1', ['药品1', '药品2' ...]), ('症状2', ['药品5', '药品6' ...]), ...]
            'why': ['原因1', '原因2', ...],
            'protect': ['预防1', '预防2', ...]
        }
        """
        dis_info = {}

        # 查询常见症状
        gql = "MATCH (q)-[r:`临床症状`]->(n) WHERE q.name = '{}' RETURN n.name".format(dis)
        gql1 = "MATCH (p) WHERE p.name = '{}' AND EXISTS(p.`临床表现`) RETURN p.`临床表现`".format(dis)
        r = self.g.run(gql).data()
        r1 = self.g.run(gql1).data()
        temp_sym = [d['n.name'] for d in r]
        for d in r1:
            temp_sym += re.split('[，；、]', d['p.`临床表现`'])
        temp_sym = list(set(temp_sym))
        if len(temp_sym) > 0:
            dis_info['sym'] = temp_sym

        # 查询症状对应的药品
        temp_plan = []  # [(sym1, [drug1, drug2 ...]), (sym2, [drug5, drug6 ...]), ...]
        for sym in temp_sym:
            gql = "MATCH (n)-[r:`适用症状`]->(p) WHERE p.name = '{}' RETURN n.name".format(sym)
            r = self.g.run(gql).data()
            dru_ls = [j['n.name'] for j in r]
            if len(dru_ls) > 0:
                dru_ls = list(set(dru_ls))
                temp_plan.append((sym, dru_ls))
        if len(temp_plan) > 0:
            dis_info['plan'] = temp_plan

        # 查询常见病因
        gql = "MATCH (n)-[r:`引起疾病`]->(p) WHERE p.name = '{}' RETURN n.name".format(dis)
        gql1 = "MATCH (p)-[r:`主要病因`]->(n) WHERE p.name = '{}' RETURN n.name".format(dis)
        gql2 = "MATCH (n:`疾病`) WHERE EXISTS(n.`常见病因`) AND n.name = '{}' RETURN n.`常见病因`".format(dis)
        r = self.g.run(gql).data()
        r1 = self.g.run(gql1).data()
        r2 = self.g.run(gql2).data()
        temp_why = [j['n.name'] for j in r]
        temp_why += [j['n.name'] for j in r1]
        temp_why += [j['n.`常见病因`'] for j in r2]
        if len(temp_why) > 0:
            temp_why = list(set(temp_why))
            dis_info['why'] = temp_why

        # 查询就诊科室
        gql = "MATCH (q)-[r:`就诊科室`]->(n) WHERE q.name = '{}' RETURN n.name".format(dis)
        r = self.g.run(gql).data()
        if len(r) > 0:
            dis_info['subject'] = r[0]['n.name']
        else:
            gql = "MATCH (n) WHERE n.name = '{}' AND EXISTS(n.`就诊科室`) RETURN n.`就诊科室`".format(dis)
            r = self.g.run(gql).data()
            if len(r) > 0:
                dis_info['subject'] = r[0]['n.`就诊科室`']

        # 查询预防措施
        gql = "MATCH (n) WHERE EXISTS(n.`预防措施`) AND n.name = '{}' RETURN n.`预防措施`".format(dis)
        r = self.g.run(gql).data()
        protect = [j['n.`预防措施`'] for j in r]
        if len(protect) > 0:
            dis_info['protect'] = list(set(protect))

        dis_info['type'] = 'dis'
        return dis_info

    def _get_sym_info(self, sym):
        """
        查询症状信息
        :param sym: str 症状
        :return: dict
        {
            'subject': '就诊科室',
            'test': ['检查项目1', '检查项目2', ...],
            'drugs': ['药品1', '药品2', ...],
            'protect': ['预防1', '预防2', ...]
        }
        """
        sym_info = {}

        # 查询就诊科室
        gql = "MATCH (q)-[r:`就诊科室`]->(n) WHERE q.name = '{}' RETURN n.name".format(sym)
        r = self.g.run(gql).data()
        if len(r) > 0:
            sym_info['subject'] = r[0]['n.name']
        else:
            gql = "MATCH (n) WHERE n.name = '{}' AND EXISTS(n.`就诊科室`) RETURN n.`就诊科室`".format(sym)
            r = self.g.run(gql).data()
            if len(r) > 0:
                sym_info['subject'] = r[0]['n.`就诊科室`']

        # 检查项目
        gql = "MATCH (q)-[r:`检查项目`]->(n) WHERE q.name = '{}' RETURN n.name".format(sym)
        r = self.g.run(gql).data()
        tests = [j['n.name'] for j in r]
        if len(tests) > 0:
            sym_info['test'] = list(set(tests))

        # 查询常用药物
        gql = "MATCH (n)-[r:`适用症状`]->(q) WHERE q.name = '{}' RETURN n.name".format(sym)
        r = self.g.run(gql).data()
        temp_dru = [j['n.name'] for j in r]
        if len(temp_dru) > 0:
            sym_info['drugs'] = list(set(temp_dru))

        # 查询主要病因
        gql = "MATCH (q)-[r:`主要病因`]->(n:`细菌`) WHERE q.name = '{}' RETURN n.name".format(sym)
        gql1 = "MATCH (q)-[r:`主要病因`]->(n:`病毒`) WHERE q.name = '{}' RETURN n.name".format(sym)
        r = self.g.run(gql).data()
        r1 = self.g.run(gql1).data()
        temp_why = [j['n.name'] for j in r]
        temp_why += [j['n.name'] for j in r1]
        if len(temp_why) > 0:
            sym_info['why'] = list(set(temp_why))

        # 查询预防措施
        gql = "MATCH (n) WHERE EXISTS(n.`预防措施`) AND n.name = '{}' RETURN n.`预防措施`".format(sym)
        r = self.g.run(gql).data()
        protect = [j['n.`预防措施`'] for j in r]
        if len(protect) > 0:
            sym_info['protect'] = list(set(protect))

        sym_info['type'] = 'sym'
        return sym_info

    def _get_dru_info(self, drug):
        """
        查询药品信息
        :param drug: str 药品
        :return: dict
        {
            'subject': '适用科室',
            'dis': ['疾病1', '疾病2', ...],
            'sym': ['症状1', '症状2', ...],
            'caution': ['禁忌1, '禁忌2' ...],
        }
        """
        dru_info = {}

        # 查询禁忌
        gql = "MATCH (n) WHERE EXISTS(n.`禁忌`) AND n.name = '{}' RETURN n.`禁忌`".format(drug)
        r = self.g.run(gql).data()
        if len(r) > 0:
            dru_info['caution'] = list(set([j['n.`禁忌`'] for j in r]))

        # 查询适用疾病
        gql = "MATCH (p)-[r:`适用疾病`]->(n) WHERE p.name = '{}' RETURN n.name".format(drug)
        r = self.g.run(gql).data()
        if len(r) > 0:
            dru_info['dis'] = list(set([j['n.name'] for j in r]))

        # 查询适用症状
        gql = "MATCH (p)-[r:`适用症状`]->(n) WHERE p.name = '{}' RETURN n.name".format(drug)
        r = self.g.run(gql).data()
        if len(r) > 0:
            dru_info['sym'] = list(set([j['n.name'] for j in r]))

        dru_info['type'] = 'dru'
        return dru_info

    def _get_mic_info(self, micro):
        """
        查询微生物信息
        :param micro: str 细菌 / 病毒
        :return: bac_info { dis: [], sym: []}
        """
        mic_info = {}
        gql = "MATCH (p)-[r:`引起疾病`]->(n) WHERE p.name = '{}' RETURN n.name".format(micro)
        gql1 = "MATCH (p)-[r:`引起症状`]->(n) WHERE p.name = '{}' RETURN n.name".format(micro)
        r = self.g.run(gql).data()
        r1 = self.g.run(gql1).data()
        if len(r) > 0:
            temp_dis = [j['n.name'] for j in r]
            temp_dis = list(set(temp_dis))
            mic_info['dis'] = temp_dis
        if len(r1) > 0:
            temp_sym = [j['n.name'] for j in r1]
            temp_sym = list(set(temp_sym))
            mic_info['sym'] = temp_sym

        mic_info['type'] = "mic"
        return mic_info

    def _search_data(self):
        """
        查询所需要信息，
        标准查询关键词 std_keywords 医学专科 检查科目 疾病 病毒 症状 细菌 药物
        :return: dict {'疾病1': dis_info, '症状2': sym_info, ...}
        """
        data = dict()
        # 查询治疗方案
        if self.intention == '治疗方案':
            for i in self.std_keywords['疾病']:
                data[i] = self._get_dis_info(i)
            for i in self.std_keywords['症状']:
                data[i] = self._get_sym_info(i)

        # 查询疾病是什么
        elif self.intention == '疾病表述':
            for i in self.std_keywords['疾病']:
                data[i] = self._get_dis_info(i)

        # 查询病因分析
        elif self.intention == '病因分析':
            for i in self.std_keywords['疾病']:
                data[i] = self._get_dis_info(i)
            for i in self.std_keywords['症状']:
                data[i] = self._get_sym_info(i)

        # 查询注意事项
        elif self.intention == '注意事项':
            for i in self.std_keywords['疾病']:
                data[i] = self._get_dis_info(i)
            for i in self.std_keywords['症状']:
                data[i] = self._get_sym_info(i)
            for i in self.std_keywords['药物']:
                data[i] = self._get_dru_info(i)

        # 查询功效作用
        elif self.intention == '功效作用':
            for i in self.std_keywords['药物']:
                data[i] = self._get_dru_info(i)

        # 查询病情诊断
        elif self.intention == '病情诊断':
            subjects = []
            temp_data = dict()
            for i in self.std_keywords['症状'] + self.std_keywords['疾病']:
                # 查询可能的疾病
                gql = "MATCH (n:`疾病`)-[r:`临床症状`]->(p) WHERE p.name = '{}' RETURN n.name".format(i)
                r = self.g.run(gql).data()
                temp_dis = [j['n.name'] for j in r]
                temp_dis = set(temp_dis)
                if len(r) > 0:
                    for dis in temp_dis:
                        if dis not in temp_data.keys():
                            temp_data[dis] = 10
                        else:
                            temp_data[dis] += 10
                gql = "MATCH (n:`疾病`)-[r:`主要病因`]->(q)-[r1:`引起症状`]->(m) WHERE m.name = '{}' RETURN n.name".format(i)
                r = self.g.run(gql).data()
                temp_dis = [j['n.name'] for j in r]
                temp_dis = set(temp_dis)
                if len(r) > 0:
                    for dis in temp_dis:
                        if dis not in temp_data.keys():
                            temp_data[dis] = 1
                        else:
                            temp_data[dis] += 1

                # 查询科室
                gql = "MATCH (p)-[r:`就诊科室`]->(n:`医学专科`) WHERE p.name = '{}' RETURN n.name".format(i)
                r = self.g.run(gql).data()
                if len(r) > 0:
                    subjects += list(set([j['n.name'] for j in r]))

            diss = list(temp_data.keys())
            rates = list(temp_data.values())
            rank = list(zip(diss, rates))
            rank.sort(key=lambda x: x[1], reverse=True)
            if len(rank) > 0:
                data.update({'judge': {'rank': rank, 'subjects': subjects}})

        # 查询就医建议
        elif self.intention == '就医建议':
            for i in self.std_keywords['疾病']:
                data[i] = self._get_dis_info(i)
            for i in self.std_keywords['症状']:
                data[i] = self._get_sym_info(i)

        # 查询医疗费用
        elif self.intention == '医疗费用':
            pass

        # 查询指标解读
        elif self.intention == '指标解读':
            pass

        # 查询后果表述
        elif self.intention == '后果表述':
            for i in self.std_keywords['病毒']:
                data[i] = self._get_mic_info(i)
            for i in self.std_keywords['细菌']:
                data[i] = self._get_mic_info(i)
            for i in self.std_keywords['疾病']:
                data[i] = self._get_dis_info(i)

        return data

    def answer_search(self, intention, keywords):
        self.intention = intention
        self.keywords = keywords
        self.std_keywords = {
            "医学专科": [],
            "检查科目": [],
            "疾病": [],
            "病毒": [],
            "症状": [],
            "细菌": [],
            "药物": []
        }
        self._normalize_keywords()
        return self._search_data()


if __name__ == '__main__':
    anss = AnswerSearcher()
    # kw = {'dis': ['咳痰', '咳嗽', '肺炎', '梅毒'], 'sym': ['头晕', '呼吸困难'], 'pro': ['抗体检查'], 'equ': ['显微镜'], 'dru': ['头孢'],
    #       'bod': ['四肢'], 'dep': ['呼吸外科室'], 'mic': ['细菌', '病毒']}
    kw = {'dis': ['肺炎']}
    print(anss.answer_search("疾病表述", kw))
