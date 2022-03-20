ATTR_TO_ABANDON = ['id', 'name', '名称', '来源']


def build_answer(intention, data):
    ans = ""
    # 查询治疗方案
    if intention == '治疗方案':
        # dru_for_dis, dru_for_sym
        if 'dru_for_dis' in data.keys():
            for k in data['dru_for_dis'].keys():
                ans += f"治疗{k}的药物有:\t" + "\t".join(list(data['dru_for_dis'][k])) + '\n'
        if 'dru_for_sym' in data.keys():
            for k in data['dru_for_sym'].keys():
                ans += f"治疗{k}的药物有:\t" + "\t".join(list(data['dru_for_sym'][k])) + '\n'

    # 查询疾病是什么
    elif intention == '疾病表述':
        # exp_for_dis
        if 'exp_for_dis' in data.keys():
            for k in data['exp_for_dis'].keys():
                ans += f"为您查询到{k}具有以下特点：\n"
                for attr in data['exp_for_dis'][k].keys():
                    if attr not in ATTR_TO_ABANDON:
                        ans += f"\t{attr}:\t{data['exp_for_dis'][k][attr]}\n"

    # 查询病因分析
    elif intention == '病因分析':
        #  rsn_for_dis
        if 'rsn_for_dis' in data.keys():
            for k in data['rsn_for_dis']:
                ans += f"{k}可能的病因有:\n"
                for rsn in data['rsn_for_dis'][k]:
                    ans += f'\t{rsn}\n'

    # 查询注意事项
    elif intention == '注意事项':
        # cau_for_dru,  cau_for_dis, cau_for_sym
        if 'cau_for_dru' in data.keys():
            for k in data['cau_for_dru'].keys():
                ans += f"使用药品{k}的注意事项有:\n"
                for j in data['cau_for_dru'][k]:
                    ans += f'\t{j}\n'

    # 查询功效作用
    elif intention == '功效作用':
        # dis_for_dru sym_for_dru
        if 'dis_for_dru' in data.keys():
            for k in data['dis_for_dru'].keys():
                ans += f"{k} 的功效有：\n"
                for j in data['dis_for_dru'][k]:
                    ans += f'\t治疗 {j}\n'
        if 'sym_for_dru' in data.keys():
            for k in data['sym_for_dru'].keys():
                ans += f"{k} 的功效有：\n"
                for j in data['sym_for_dru'][k]:
                    ans += f'\t缓解 {j}'

    # 查询病情诊断
    elif intention == '病情诊断':
        # data.update({'dis_for_sym': rank})
        if 'dis_for_sym' in data:
            ans += "可能造成您所述症状的疾病有:\n"
            if len(data['dis_for_sym']) > 5:
                for x, y in data['dis_for_sym'][:5]:
                    ans += f'\t{x}\n'
                ans += "\t等等..."
            else:
                for x, y in data['dis_for_sym']:
                    ans += f'\t{x}\n'

    # 查询就医建议
    elif intention == '就医建议':
        # dep_for_dis
        if 'dep_for_dis' in data:
            for k in data['dep_for_dis']:
                ans += f"由于您有 {k} 建议您于 " + '\t'.join(list(data['dep_for_dis'][k])) + " 就诊\n"

    # 查询医疗费用
    elif intention == '医疗费用':
        pass

    # 查询指标解读
    elif intention == '指标解读':
        pass

    # 查询后果表述
    elif intention == '后果表述':
        # dis_for_vir  dis_for_bac  sym_for_vir sym_for_bac sym_for_dis
        if 'dis_for_vir' in data:
            for vir in data['dis_for_vir']:
                ans += f"病毒 {vir} 引起的疾病有:\n"
                for j in data['dis_for_vir'][vir]:
                    ans += f'\t{j}\n'

        if 'dis_for_bac' in data:
            for bac in data['dis_for_bac']:
                ans += f"细菌 {bac} 引起的疾病有:\n"
                for j in data['dis_for_bac'][bac]:
                    ans += f'\t{j}\n'

        if 'sym_for_vir' in data:
            for vir in data['sym_for_vir']:
                ans += f"病毒 {vir} 引起的症状有:\n"
                for j in data['sym_for_vir'][vir]:
                    ans += f'\t{j}\n'

        if 'sym_for_bac' in data:
            for bac in data['sym_for_bac']:
                ans += f"细菌 {bac} 引起的症状有:\n"
                for j in data['sym_for_bac'][bac]:
                    ans += f'\t{j}\n'

        if 'sym_for_dis' in data:
            for dis in data['sym_for_dis']:
                ans += f"疾病 {dis} 引起的症状有:\n"
                for j in data['sym_for_dis'][dis]:
                    ans += f'\t{j}\n'

    return ans
