from global_var import *
import numpy as np
import re


def get_first_pron(s):
    """
    :param s: string, 字书《玉篇》对某个字的注音，一种或多种
    :return: string, 返回第一种注音
    """
    if len(s) == 2:
        return s
    elif len(s) > 2:
        first_s = s.split('/')[0]
        if len(first_s) == 2:
            return first_s


def get_common_pron_id(char, res):
    """
    输入一个在《广韵》中有异读的字，返回其常见音，即在《玉篇》中排在第一个的音
    :param char: string of length 1, 待确定常见音的字
    :param res: string of length 2, 即char在《玉篇》中排在第一个的反切注音
    :return: int, 《广韵》对char的多条注音中，注的是常见音的条目的id

    例：
    - Input: 筒
    - Output: 14610
    “筒”有两个音，一个是“徒紅切”，定母东韵开一平声，idx=27；另一个是“徒弄切”，
    定母东韵开一去声，idx=14610。《玉篇》中仅有“徒棟切”，“棟”为端母东韵开一去声。
    《玉篇》所收音与14610“徒弄切”相同。
    """
    yupian_feature = []  # 记录《玉篇》反切音韵特征
    yidu_feature = {}  # 记录《广韵》异读字

    # 记录《玉篇》对char的第一个反切注音的音韵特征，即反切上字的声母，反切下字的等、呼之类
    if char2idx.get(res[0]) is not None and char2idx.get(res[1]) is not None:
        for i in char2idx[res[0]]:
            yupian_feature.append(all_table['聲紐'].iloc[i])
        for i in char2idx[res[1]]:
            yupian_feature.append(all_table['呼'].iloc[i])
            yupian_feature.append(all_table['等'].iloc[i])
            yupian_feature.append(all_table['韻部原貌-平上去入相配爲平(調整前)'].iloc[i])
            yupian_feature.append(all_table['聲調'].iloc[i])

    # 记录《广韵》对char的各反切注音的音韵特征，即反切上字的声母，反切下字的等、开合之类
    for i in char2idx[char]:
        yidu_feature[i] = []
        yidu_feature[i].append(all_table['聲紐'].iloc[i])
        yidu_feature[i].append(all_table['呼'].iloc[i])
        yidu_feature[i].append(all_table['等'].iloc[i])
        yidu_feature[i].append(all_table['韻部原貌-平上去入相配爲平(調整前)'].iloc[i])
        yidu_feature[i].append(all_table['聲調'].iloc[i])

    # 《玉篇》中常见音未必出现在《广韵》中，因此选择《广韵》中与《玉篇》常见音**最接近**的音
    # “最接近”即声母、等、开合、韵系、声调这五项中相同的最多
    highest_id = -1
    highest_sim = 0
    for key in yidu_feature:
        sim = len(set(yidu_feature[key]) & set(yupian_feature))
        if sim > highest_sim:
            highest_sim = sim
            highest_id = key
    return highest_id


def get_yidu(idx):
    """
    给定一个字的序号，返回该字释义中的另一种注音
    :param idx: 有多音字的序号
    :return: 另一种注音的反切上下字（长度为2，格式为“又xx切”），或直音法注音（长度为1，格式为“又音x”）
    例：
    - Input: 8
      ( 凍 瀧涷沾漬說文曰水出發鳩山入於河又都貢切 )
    - Output: 都貢

    - Input: 9
      ( 蝀 螮蝀虹也又音董 )
    - Output: 董
    """
    shiyi = all_table['廣韻釋義'].iloc[idx]
    if not pd.isna(all_table['釋義補充'].iloc[idx]):
        shiyi = all_table['釋義補充'].iloc[idx]
    if shiyi is not np.nan:
        shiyi = re.sub('[一二三四五六七八九十]*$', '', shiyi)
        res = re.findall(r"又(.{2})切$", shiyi)
        if len(res):
            return res[0]
        else:
            res = re.findall(r"又音(.{1})$", shiyi)
            if len(res):
                return res[0]


if __name__ == "main":
    print("调试")
    print(get_common_pron_id('筒', '徒棟'))
    print(get_yidu(8))
    print(get_yidu(9))
