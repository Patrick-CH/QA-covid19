# "治疗方案", "其他", "疾病表述", "病因分析", "注意事项", "功效作用", "病情诊断", "就医建议", "医疗费用", "指标解读", "后果表述"
from py2neo import Graph

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
        #  基础信息规范化
        #  NER结果    pro医疗程序, dis疾病, sym症状, ite检查科目, bod身体, dru药物, mic微生物, equ医疗设备, dep科室
        #  std  医学专科 检查科目 疾病 病毒 症状 细菌 药物
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

    def _search_data(self):
        #  std  医学专科 检查科目 疾病 病毒 症状 细菌 药物
        data = dict()
        # 查询治疗方案
        if self.intention == '治疗方案':
            dru_for_dis = dict()
            dru_for_sym = dict()

            for i in self.std_keywords['疾病']:
                gql = "MATCH (n)-[r:`适用疾病`]->(q) WHERE q.name = '{}' RETURN n".format(i)
                gql1 = "MATCH (p)-[r:`常用药物`]->(n) WHERE p.name = '{}' RETURN n".format(i)
                r = self.g.run(gql).data()
                r1 = self.g.run(gql1).data()
                temp_dru = [d['n']['name'] for d in r]
                temp_dru += [d['n']['name'] for d in r1]
                if len(temp_dru) > 0:
                    if i in dru_for_dis.keys():
                        dru_for_dis[i] += temp_dru
                    else:
                        dru_for_dis[i] = temp_dru
            if len(dru_for_dis) > 0:
                data.update({'dru_for_dis': dru_for_dis})

            for i in self.std_keywords['症状']:
                gql = "MATCH (n)-[r:`适用症状`]->(q) WHERE q.name = '{}' RETURN n".format(i)
                r = self.g.run(gql).data()
                if len(r) > 0:
                    temp_dru = [d['n']['name'] for d in r]
                    if i in dru_for_sym.keys():
                        dru_for_sym[i] += temp_dru
                    else:
                        dru_for_sym[i] = temp_dru
            if len(dru_for_sym) > 0:
                data.update({'dru_for_sym': dru_for_sym})

        # 查询疾病是什么
        elif self.intention == '疾病表述':
            exp_for_dis = dict()
            for i in self.std_keywords['疾病']:
                gql = "MATCH (n) WHERE n.name='{}' RETURN n".format(i)
                r = self.g.run(gql).data()
                if len(r) > 0:
                    temp_dis = [dict(d['n']) for d in r]
                    if i not in exp_for_dis.keys():
                        exp_for_dis[i] = dict()
                    for dis in temp_dis:
                        exp_for_dis[i].update(dis)
            if len(exp_for_dis) > 0:
                data.update({'exp_for_dis': exp_for_dis})

        # 查询病因分析
        elif self.intention == '病因分析':
            rsn_for_dis = dict()

            for i in self.std_keywords['疾病']:
                gql = "MATCH (p)-[r:`主要病因`]->(n) WHERE p.name = '{}' RETURN n".format(i)
                r = self.g.run(gql).data()
                if len(r) > 0:
                    rsn_for_dis[i] = set([d['n'].name for d in r])
                gql1 = "MATCH (n:`疾病`) WHERE EXISTS(n.`常见病因`) AND n.name = '{}' RETURN n.`常见病因`".format(i)
                r1 = self.g.run(gql1).data()
                if len(r1) > 0:
                    if i not in rsn_for_dis.keys():
                        rsn_for_dis[i] = set()
                    for j in r1:
                        rsn_for_dis[i].add(j['n.`常见病因`'])
            if len(rsn_for_dis) > 0:
                data.update({'rsn_for_dis': rsn_for_dis})

        # 查询注意事项
        elif self.intention == '注意事项':
            cau_for_dru = dict()
            cau_for_dis = dict()
            cau_for_sym = dict()

            for i in self.std_keywords['药物']:
                gql = "MATCH (n) WHERE EXISTS(n.`禁忌`) AND n.name = '{}' RETURN n.`禁忌`".format(i)
                r = self.g.run(gql).data()
                if len(r) > 0:
                    if i not in cau_for_dru.keys():
                        cau_for_dru[i] = set()
                    for j in r:
                        cau_for_dru[i].add(j['n.`禁忌`'])
            if len(cau_for_dru) > 0:
                data.update({'cau_for_dru': cau_for_dru})

            for i in self.std_keywords['疾病']:
                gql = "MATCH (n) WHERE EXISTS(n.`预防措施`) AND n.name = '{}' RETURN n.`预防措施`".format(i)
                r = self.g.run(gql).data()
                if len(r) > 0:
                    if i not in cau_for_dis.keys():
                        cau_for_dis[i] = set()
                    for j in r:
                        cau_for_dis[i].add(j['n.`预防措施`'])
            if len(cau_for_dis) > 0:
                data.update({'cau_for_dis': cau_for_dis})

            for i in self.std_keywords['症状']:
                gql = "MATCH (n) WHERE EXISTS(n.`预防措施`) AND n.name = '{}' RETURN n.`预防措施`".format(i)
                r = self.g.run(gql).data()
                if len(r) > 0:
                    if i not in cau_for_sym.keys():
                        cau_for_sym[i] = set()
                    for j in r:
                        cau_for_sym[i].add(j['n.`预防措施`'])
            if len(cau_for_sym) > 0:
                data.update({'cau_for_sym': cau_for_sym})

        # 查询功效作用
        elif self.intention == '功效作用':
            dis_for_dru = dict()
            sym_for_dru = dict()
            for i in self.std_keywords['药物']:
                gql = "MATCH (p)-[r:`适用疾病`]->(n) WHERE p.name = '{}' RETURN n.name".format(i)
                r = self.g.run(gql).data()
                if len(r) > 0:
                    if i not in dis_for_dru.keys():
                        dis_for_dru[i] = set()
                    for d in r:
                        dis_for_dru[i].add(d['n.name'])
                if len(dis_for_dru) > 0:
                    data.update({'dis_for_dru': dis_for_dru})

                gql2 = "MATCH (p)-[r:`适用症状`]->(n) WHERE p.name = '{}' RETURN n.name".format(i)
                r2 = self.g.run(gql2).data()
                if len(r2) > 0:
                    if i not in sym_for_dru.keys():
                        sym_for_dru[i] = set()
                    for d in r2:
                        sym_for_dru[i].add(d['n.name'])
                if len(sym_for_dru) > 0:
                    data.update({'sym_for_dru': sym_for_dru})

        # 查询病情诊断
        elif self.intention == '病情诊断':
            temp_data = dict()
            for i in self.std_keywords['症状']:
                gql = "MATCH (n:`疾病`)-[r:`临床症状`]->(p) WHERE p.name = '{}' RETURN n.name".format(i)
                r = self.g.run(gql).data()
                temp_dis = [j['n.name'] for j in r]
                temp_dis = set(temp_dis)
                if len(r) > 0:
                    for dis in temp_dis:
                        if dis not in temp_data.keys():
                            temp_data[dis] = 1
                        else:
                            temp_data[dis] += 1
            diss = list(temp_data.keys())
            rates = list(temp_data.values())
            rank = list(zip(diss, rates))
            rank.sort(key=lambda x: x[1], reverse=True)
            if len(rank) > 0:
                data.update({'dis_for_sym': rank})

        # 查询就医建议
        elif self.intention == '就医建议':
            dep_for_dis = dict()
            for i in (self.std_keywords['疾病'] + self.std_keywords['症状']):
                gql = "MATCH (p)-[r:`就诊科室`]->(n) WHERE p.name = '{}' RETURN n.name".format(i)
                r = self.g.run(gql).data()
                if len(r) > 0:
                    if i not in dep_for_dis.keys():
                        dep_for_dis[i] = set()
                    for j in r:
                        dep_for_dis[i].add(j['n.name'])
            for i in self.std_keywords['疾病']:
                gql = "MATCH (p) WHERE EXISTS(p.`就诊科室`) AND p.name = '{}' RETURN p.`就诊科室`".format(i)
                r = self.g.run(gql).data()
                if len(r) > 0:
                    if i not in dep_for_dis.keys():
                        dep_for_dis[i] = set()
                    for j in r:
                        dep_for_dis[i].add(j['p.`就诊科室`'])
            if len(dep_for_dis) > 0:
                data.update({'dep_for_dis': dep_for_dis})

        # 查询医疗费用
        elif self.intention == '医疗费用':
            pass

        # 查询指标解读
        elif self.intention == '指标解读':
            pass

        # 查询后果表述
        elif self.intention == '后果表述':
            dis_for_vir = dict()
            dis_for_bac = dict()
            sym_for_vir = dict()
            sym_for_bac = dict()
            sym_for_dis = dict()
            for i in self.std_keywords['病毒']:
                gql = "MATCH (p)-[r:`引起疾病`]->(n) WHERE p.name = '{}' RETURN n.name".format(i)
                gql1 = "MATCH (p)-[r:`引起症状`]->(n) WHERE p.name = '{}' RETURN n.name".format(i)
                r = self.g.run(gql).data()
                r1 = self.g.run(gql1).data()
                if len(r) > 0:
                    if i not in dis_for_vir.keys():
                        dis_for_vir[i] = set()
                    for j in r:
                        dis_for_vir[i].add(j['n.name'])
                if len(r1) > 0:
                    if i not in sym_for_vir.keys():
                        sym_for_vir[i] = set()
                    for j in r1:
                        sym_for_vir[i].add(j['n.name'])
            if len(dis_for_vir) > 0:
                data.update({'dis_for_vir': dis_for_vir})
            if len(sym_for_vir) > 0:
                data.update({'sym_for_vir': sym_for_vir})

            for i in self.std_keywords['细菌']:
                gql = "MATCH (p)-[r:`引起疾病`]->(n) WHERE p.name = '{}' RETURN n.name".format(i)
                gql1 = "MATCH (p)-[r:`引起症状`]->(n) WHERE p.name = '{}' RETURN n.name".format(i)
                r = self.g.run(gql).data()
                r1 = self.g.run(gql1).data()
                if len(r) > 0:
                    if i not in dis_for_bac.keys():
                        dis_for_bac[i] = set()
                    for j in r:
                        dis_for_bac[i].add(j['n.name'])
                if len(r1) > 0:
                    if i not in sym_for_bac.keys():
                        sym_for_bac[i] = set()
                    for j in r:
                        sym_for_bac[i].add(j['n.name'])
            if len(dis_for_bac) > 0:
                data.update({'dis_for_bac': dis_for_bac})
            if len(sym_for_bac) > 0:
                data.update({'sym_for_bac': sym_for_bac})

            for i in self.std_keywords['疾病']:
                gql = "MATCH (p)-[r:`临床症状`]->(n) WHERE p.name =~ '{}' RETURN n.name".format(i)
                r = self.g.run(gql).data()
                if len(r) > 0:
                    if i not in sym_for_dis.keys():
                        sym_for_dis[i] = set()
                    for j in r:
                        sym_for_dis[i].add(j['n.name'])
            if len(sym_for_dis) > 0:
                data.update({'sym_for_dis': sym_for_dis})

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
    kw = {'dis': ['梅毒', '败血症'], 'mic': ['表皮葡萄球菌', '腺病毒']}
    print(anss.answer_search("后果表述", kw))
