ATTR_TO_ABANDON = ['id', 'name', '名称', '来源']
BOT_NAME = "武小理"
MAX_LIST_NUM = 5


def build_dis_ans(dis_name: str, dis_info: dict, mask_info: list = None):
    """
    构造疾病的答案
    :param dis_name: 疾病名称
    :param dis_info: 疾病信息
    :param mask_info: 不需要展示的信息
    :return: ans 构造好的答案
    """
    if mask_info is None:
        mask_info = []
    ans = ""
    if dis_info['type'] == 'dis':
        if 'why' in dis_info and (mask_info is None or 'why' not in mask_info):
            ans += f"{dis_name}的常见病因有:" + ', '.join(dis_info['why']) + "等。"
        if 'sym' in dis_info and (mask_info is None or 'sym' not in mask_info):
            ans += f"\n{dis_name}的常见症状有:" + ', '.join(dis_info['sym']) + "等。"
        if 'subject' in dis_info and (mask_info is None or 'subject' not in mask_info):
            ans += f"\n若您{dis_name}的症状严重，请立即到医院{dis_info['subject']}就诊!"
        else:
            ans += f"\n若您{dis_name}的症状严重，请立即到医院就诊!"
        if 'plan' in dis_info and (mask_info is None or 'plan' not in mask_info):
            ans += f"\n为减轻{dis_name}症状，可以选用相关药物。"
            for sym, drugs in dis_info['plan']:
                ans += f"\n{sym}可以通过{', '.join(drugs)}等药物缓解。"
        if 'protect' in dis_info and (mask_info is None or 'protect' not in mask_info):
            ans += f"\n{BOT_NAME}提示您要注意健康，可以通过{', '.join(dis_info['protect'])}来预防{dis_name}。"
    return ans


def build_sym_ans(sym_name: str, sym_info: dict, mask_info: list = None):
    """
    构造症状答案
    :param sym_name: 症状名称
    :param sym_info: 症状信息
    :param mask_info: 不需要展示的信息
    :return: ans 构造好的答案
    """
    ans = ""
    if sym_info['type'] == 'sym':
        if 'why' in sym_info and (mask_info is None or 'why' not in mask_info):
            ans += f"{sym_name}的主要病因有: {', '.join(sym_info['why'])}"
        if 'drugs' in sym_info and (mask_info is None or 'drugs' not in mask_info):
            ans += f"症状{sym_name}可以通过: {', '.join(sym_info['drugs'])}缓解。"
        if 'subject' in sym_info and (mask_info is None or 'subject' not in mask_info):
            ans += f"\n若您{sym_name}的症状较为严重，请立即到医院{sym_info['subject']}就诊!"
        else:
            ans += f"\n若您{sym_name}的症状较为严重，请立即到医院就诊!"
        if 'test' in sym_info and (mask_info is None or 'test' not in mask_info):
            ans += f"可能需要的相关检查有: {', '.join(sym_info['test'])}"
        if 'protect' in sym_info and (mask_info is None or 'protect' not in mask_info):
            ans += f"\n{BOT_NAME}提示您要注意健康，可以通过{', '.join(sym_info['protect'])}来预防{sym_name}"
    return ans


def build_dru_ans(dru_name: str, dru_info: dict, mask_info: list = None):
    """
    构造药品答案
    :param dru_name: 药品名称
    :param dru_info: 药品信息
    :param mask_info: 不需要显示的信息
    :return: ans 构造好的答案
    """
    ans = ""
    if 'subject' in dru_info and (mask_info is None or 'subject' not in mask_info):
        ans += f"\n药品{dru_name}常用于{dru_info['subject']}。"
    if 'dis' in dru_info and (mask_info is None or 'dis' not in mask_info):
        ans += f"\n{dru_name}可以用于治疗: {', '.join(dru_info['dis'])}等疾病。"
    if 'sym' in dru_info and (mask_info is None or 'sym' not in mask_info):
        ans += f"\n{dru_name}可以用于缓解: {', '.join(dru_info['sym'])}等症状"
    if 'caution' in dru_info and (mask_info is None or 'caution' not in mask_info):
        ans += f"\n使用{dru_name}的禁忌有: {', '.join(dru_info['caution'])}。"
    return ans


def build_mic_ans(mic_name: str, mic_info: dict, mask_info: list = None):
    ans = ""
    if 'dis' in mic_info and (mask_info is None or 'dis' not in mask_info):
        ans += f"{mic_name}可能导致{', '.join(mic_info['dis'])}等疾病。"
    if 'sym' in mic_info and (mask_info is None or 'sym' not in mask_info):
        ans += f"{mic_name}可能引起{', '.join(mic_info['sym'])}等症状"
    return ans


def build_answer(intention, data):
    ans = ""
    # 查询治疗方案
    if intention == '治疗方案':
        for k in data.keys():
            if data[k]['type'] == 'dis':
                # 疾病
                ans += build_dis_ans(k, data[k])
            elif data[k]['type'] == 'sym':
                # 症状
                ans += build_sym_ans(k, data[k], mask_info=['test'])

    # 查询疾病是什么
    elif intention == '疾病表述':
        for k in data.keys():
            if data[k]['type'] == 'dis':
                # 疾病
                ans += build_dis_ans(k, data[k], mask_info=['plan'])

    # 查询病因分析
    elif intention == '病因分析':
        for k in data.keys():
            if data[k]['type'] == 'dis':
                # 疾病
                ans += build_dis_ans(k, data[k], mask_info=['plan', 'sym', 'protect'])
            elif data[k]['type'] == 'sym':
                # 症状
                ans += build_sym_ans(k, data[k], mask_info=['test', 'protect', 'drugs'])

    # 查询注意事项
    elif intention == '注意事项':
        for k in data.keys():
            if data[k]['type'] == 'dis':
                # 疾病
                ans += build_dis_ans(k, data[k], mask_info=['plan', 'sym', 'why'])
            elif data[k]['type'] == 'sym':
                # 症状
                ans += build_sym_ans(k, data[k], mask_info=['test', 'protect', 'drugs', 'why'])
            elif data[k]['type'] == 'dru':
                # 药物
                ans += build_dru_ans(k, data[k], mask_info=['dis', 'sym', 'subject'])

    # 查询功效作用
    elif intention == '功效作用':
        for k in data.keys():
            if data[k]['type'] == 'dru':
                # 药物
                ans += build_dru_ans(k, data[k])

    # 查询病情诊断
    elif intention == '病情诊断':
        if 'judge' in data:
            ans += "\n可能造成您所述症状的疾病有: "
            if len(data['judge']['rank']) > MAX_LIST_NUM:
                ans += ', '.join([x for x, y in data['judge']['rank'][:MAX_LIST_NUM]])
                ans += " 等等..."
            else:
                ans += ', '.join(data['judge']['rank'])
            ans += f"\n如果您的症状严重，请立即到医院{'、'.join(data['judge']['subjects'])}就诊!"

    # 查询就医建议
    elif intention == '就医建议':
        for k in data.keys():
            if data[k]['type'] == 'dis':
                # 疾病
                ans += build_dis_ans(k, data[k], mask_info=['why', 'plan', 'sym', 'protect'])
            elif data[k]['type'] == 'sym':
                # 症状
                ans += build_sym_ans(k, data[k], mask_info=['why', 'protect', 'drugs'])

    # 查询医疗费用
    elif intention == '医疗费用':
        pass

    # 查询指标解读
    elif intention == '指标解读':
        pass

    # 查询后果表述
    elif intention == '后果表述':
        for k in data.keys():
            if data[k]['type'] == 'dis':
                # 疾病引起症状
                ans += build_sym_ans(k, data[k], mask_info=['why', 'protect', 'subject', 'plan'])
            elif data[k]['type'] == 'mic':
                # 微生物引起疾病
                ans += build_mic_ans(k, data[k])

    return ans
