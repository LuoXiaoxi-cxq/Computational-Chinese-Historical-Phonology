import pandas as pd
from pulp import *
from global_var import *
from tool_funcion import get_first_pron, get_common_pron_id, get_yidu

"""
以下添加反切约束，来自《广韵》反切求同条例
若有”A, BC切“，则AB声母相同，AC开合、等、韵系、声调相同，相当于系联
"""
print('------Start Adding Constraint on Fanqie!------')

all_shangzi = all_table['上字'].unique().tolist()
all_xiazi = all_table['下字'].unique().tolist()
duoyin_common_pron = {}  # 记录多音字的常见音
unsettled_duoyin = []

for char in all_shangzi + all_xiazi:
    # 检查用作反切上下字的某字《广韵》是否收了
    if char2idx.get(char) is None:
        print('广韵没收的字: ', char)
        continue
    else:
        # 如果该字在《广韵》中有多个读音
        if len(char2idx[char]) > 1:
            j = char2idx[char][0]
            # 如果《原本玉篇殘卷/篆隸萬象名義》收了这个字
            if not pd.isna(all_table['玉篇-原本玉篇殘卷/篆隸萬象名義'].iloc[j]):
                res1 = get_first_pron(all_table['玉篇-原本玉篇殘卷/篆隸萬象名義'].iloc[j])
                if res1 is not None:
                    common_meaning_id = get_common_pron_id(char, res1)
                    if common_meaning_id != -1:
                        duoyin_common_pron[char] = common_meaning_id
                        continue
            # 如果《宋本玉篇》收了这个字
            if not pd.isna(all_table['玉篇-宋本玉篇'].iloc[j]):
                res2 = get_first_pron(all_table['玉篇-宋本玉篇'].iloc[j])
                if res2 is not None:
                    common_meaning_id = get_common_pron_id(char, res2)
                    if common_meaning_id != -1:
                        duoyin_common_pron[char] = common_meaning_id
                        continue
                    else:
                        print(char, ' 《玉篇》中找不到该字的常见读音！')
            # 如果两个版本的《玉篇》都没收这个字，就放到unsettled_duoyin里，人工解决
            unsettled_duoyin.append(char)

"""
或许以后我会手动处理一下这些没法用《玉篇》解决的、反切上下字中的多音字
"""
print(unsettled_duoyin)
# for char in unsettled_duoyin:
#     duoyin_common_pron[char] = char2idx[char][0]

# 遍历《广韵》中每个条目，为每个字的每个音项添加反切限制
for i in range(N):
    shangzi_char = all_table['上字'].iloc[i]
    xiazi_char = all_table['下字'].iloc[i]
    if char2idx.get(shangzi_char) is None or char2idx.get(xiazi_char) is None:
        continue

    # 找反切上下字的条目序号。如果反切上下字是多音字，返回其常用音的序号。
    shangzi_idx = 0
    xiazi_idx = 0
    if len(char2idx[shangzi_char]) > 1 and duoyin_common_pron.get(shangzi_char) is not None:
        shangzi_idx = duoyin_common_pron[shangzi_char]
    else:
        shangzi_idx = char2idx[shangzi_char][0]

    if len(char2idx[xiazi_char]) > 1 and duoyin_common_pron.get(xiazi_char) is not None:
        xiazi_idx = duoyin_common_pron[xiazi_char]
    else:
        xiazi_idx = char2idx[xiazi_char][0]

    ## 添加反切限制
    # AB声母相同
    GuangYunYinXi += var_fanqie_shengmu[i] >= (var_shengmu[i] - var_shengmu[shangzi_idx]) / NN
    GuangYunYinXi += var_fanqie_shengmu[i] >= (var_shengmu[shangzi_idx] - var_shengmu[i]) / NN
    # AC开合相同
    GuangYunYinXi += var_fanqie_kaihe[i] >= (var_kaihe[i] - var_kaihe[xiazi_idx]) / NN
    GuangYunYinXi += var_fanqie_kaihe[i] >= (var_kaihe[xiazi_idx] - var_kaihe[i]) / NN
    # AC等相同
    GuangYunYinXi += var_fanqie_deng[i] >= (var_deng[i] - var_deng[xiazi_idx]) / NN
    GuangYunYinXi += var_fanqie_deng[i] >= (var_deng[xiazi_idx] - var_deng[i]) / NN
    # AC韵系相同
    GuangYunYinXi += var_fanqie_yunxi[i] >= (var_yunxi[i] - var_yunxi[xiazi_idx]) / NN
    GuangYunYinXi += var_fanqie_yunxi[i] >= (var_yunxi[xiazi_idx] - var_yunxi[i]) / NN
    # AC声调相同
    GuangYunYinXi += var_fanqie_shengdiao[i] >= (var_shengdiao[i] - var_shengdiao[xiazi_idx]) / NN
    GuangYunYinXi += var_fanqie_shengdiao[i] >= (var_shengdiao[xiazi_idx] - var_shengdiao[i]) / NN

"""
以下使用归部信息添加约束
"""
print('------Start Adding Constraint on GuiBu!------')

for i in range(N):
    yunxi = yunxi2idx[all_table['韻部原貌-平上去入相配爲平(調整前)'].iloc[i]]
    shengdiao = shengdiao2idx[all_table['聲調'].iloc[i]]
    GuangYunYinXi += var_guibu_yunxi[i] >= (var_yunxi[i] - yunxi) / NN
    GuangYunYinXi += var_guibu_yunxi[i] >= (yunxi - var_yunxi[i]) / NN
    GuangYunYinXi += var_guibu_shengdiao[i] >= (var_shengdiao[i] - shengdiao) / NN
    GuangYunYinXi += var_guibu_shengdiao[i] >= (shengdiao - var_shengdiao[i]) / NN

"""
以下使用韵图信息添加约束
"""
print('------Start Adding Constraint on YunTu!------')

for i in range(N):
    kaihe = kaihe2idx[all_table['呼'].iloc[i]]
    deng = deng2idx[all_table['等'].iloc[i]]
    GuangYunYinXi += var_yuntu_kaihe[i] >= (var_kaihe[i] - kaihe) / NN
    GuangYunYinXi += var_yuntu_kaihe[i] >= (kaihe - var_kaihe[i]) / NN
    GuangYunYinXi += var_yuntu_deng[i] >= (var_deng[i] - deng) / NN
    GuangYunYinXi += var_yuntu_deng[i] >= (deng - var_deng[i]) / NN

"""
以下使用求异条例添加约束，求异条例只对小韵代表字进行操作
"""
print('------Start Adding Constraint on QiuYi!------')
for yunxi in yunxi_ls:
    for shengdiao in shengdiao_ls:
        # df_tmp里是韵系和声调都相同（即韵相同）的小韵代表字(df_xiaoyun见global_var.py)
        df_tmp = df_xiaoyun[(df_xiaoyun['韻部原貌-平上去入相配爲平(調整前)'] == yunxi) & (df_xiaoyun['聲調'] == shengdiao)]
        all_xiazi = df_tmp['下字'].unique()
        for xiazi in all_xiazi:
            # df_same_xiazi里是同一韵中反切下字相同的所有条目
            df_same_xiazi = df_tmp[df_tmp['下字'] == xiazi]
            tmp_L = len(df_same_xiazi)
            for i in range(tmp_L):
                for j in range(i + 1, tmp_L):
                    # 同一韵中，如果反切下字相同而反切上字不同，反切上字的声母必不同
                    if df_same_xiazi['上字'].iloc[i] != df_same_xiazi['上字'].iloc[j]:
                        # idx_i 和 idx_j 是待使用求异条例的两个反切上字在所有小韵中的序号，用来索引绝对值辅助变量var_qiuyi_shengmu
                        idx_i = df_same_xiazi['idx'].iloc[i]
                        idx_j = df_same_xiazi['idx'].iloc[j]
                        # idx_i 和 idx_j 是待使用求异条例的两个反切上字在所有小韵中的序号
                        if global_jianhua:
                            idx_ii = df_same_xiazi['新字序'].iloc[i] - 1
                            idx_jj = df_same_xiazi['新字序'].iloc[j] - 1
                        else:
                            idx_ii = df_same_xiazi['廣韻字序'].iloc[i] - 1
                            idx_jj = df_same_xiazi['廣韻字序'].iloc[j] - 1

                        # 添加限制：df_same_xiazi['上字'].iloc[i] 和 df_same_xiazi['上字'].iloc[j] 的声母不同
                        GuangYunYinXi += ((var_shengmu[idx_jj] - var_shengmu[idx_ii]) <= -eps + inf *
                                          var_qiuyi_shengmu[idx_i][idx_j])
                        GuangYunYinXi += (var_shengmu[idx_jj] - var_shengmu[idx_ii]) >= eps - inf * (
                                1 - var_qiuyi_shengmu[idx_i][idx_j])
"""
以下使用异读条例添加约束
"""
print('------Start Adding Constraint on YiDu!------')

for char in char2idx:
    # 如果恰好一个多音字有两个读音（不使用有更多读音的字）
    if len(char2idx[char]) == 2:
        i1 = char2idx[char][0]
        i2 = char2idx[char][1]
        res1 = get_yidu(i1)  # res1是i1条目的异读，可能和i2条目的反切注音相同
        if res1 is not None:
            res_char1 = res1[0]
            # 获得res1的反切上字的idx，即res_char1_idx
            if char2idx.get(res_char1) is not None:
                if len(char2idx[res_char1]) > 1 and duoyin_common_pron.get(res_char1) is not None:
                    res_char1_idx = duoyin_common_pron[res_char1]
                else:
                    res_char1_idx = char2idx[res_char1][0]
                GuangYunYinXi += var_yidu1[res_char1_idx] >= (var_shengmu[res_char1_idx] - var_shengmu[i2]) / NN
                GuangYunYinXi += var_yidu1[res_char1_idx] >= (var_shengmu[i2] - var_shengmu[res_char1_idx]) / NN

        res2 = get_yidu(i2)  # res2是i2条目的异读，可能和i1条目的反切注音相同
        if res2 is not None:
            res_char2 = res2[0]
            # 获得res2的反切上字的idx，即res_char2_idx
            if char2idx.get(res_char2) is not None:
                if len(char2idx[res_char2]) > 1 and duoyin_common_pron.get(res_char2) is not None:
                    res_char2_idx = duoyin_common_pron[res_char2]
                else:
                    res_char2_idx = char2idx[res_char2][0]
                GuangYunYinXi += var_yidu2[res_char2_idx] >= (var_shengmu[res_char2_idx] - var_shengmu[i1]) / NN
                GuangYunYinXi += var_yidu2[res_char2_idx] >= (var_shengmu[i1] - var_shengmu[res_char2_idx]) / NN

print('------Start Solving Problem!------')
solver = getSolver('GUROBI')
GuangYunYinXi.solve(solver)
print(LpStatus[GuangYunYinXi.status])

res_ls = []
for i in range(N):
    tmp_ls = []
    tmp_ls.append(idx2char[i])
    tmp_ls.append(var_shengmu[i].value())
    tmp_ls.append(kaihe_ls[int(var_kaihe[i].value())])
    tmp_ls.append(deng_ls[int(var_deng[i].value())])
    tmp_ls.append(yunxi_ls[int(var_yunxi[i].value())])
    tmp_ls.append(shengdiao_ls[int(var_shengdiao[i].value())])
    tmp_ls.append(var_fanqie_shengmu[i].value())
    tmp_ls.append(var_fanqie_kaihe[i].value())
    tmp_ls.append(var_fanqie_deng[i].value())
    tmp_ls.append(var_fanqie_yunxi[i].value())
    tmp_ls.append(var_fanqie_shengdiao[i].value())
    tmp_ls.append(var_yuntu_kaihe[i].value())
    tmp_ls.append(var_yuntu_deng[i].value())
    tmp_ls.append(var_guibu_yunxi[i].value())
    tmp_ls.append(var_guibu_shengdiao[i].value())
    tmp_ls.append(var_yidu1[i].value())
    tmp_ls.append(var_yidu2[i].value())
    res_ls.append(tmp_ls)

df_res = pd.DataFrame(res_ls,
                      columns=['字头', '声母', '开合', '等', '韵系', '声调', '反切声母', '反切开合', '反切等', '反切韵系', '反切声调', '韵图开合',
                               '韵图等', '归部韵系', '归部声调', '异读1', '异读2'])

ground_truth = all_table[['聲紐', '呼', '等', '韻部原貌-平上去入相配爲平(調整前)', '聲調', '上字', '下字']]
ground_truth.rename(columns={'聲紐': '声母-标准', '呼': '开合-标准', '韻部原貌-平上去入相配爲平(調整前)': '韵系-标准', '聲調': '声调-标准', '等': '等-标准'},
                    inplace=True)
# 给计算结果加上"标准答案"，便于比较
df_res = pd.concat([df_res, ground_truth], axis=1, join='inner')

if global_jianhua:
    df_res.to_excel('../result/202305简化_广韵建模1_建模结果_广韵反切_归部_韵图介音_异读.xlsx', sheet_name='结果', index=False)
else:
    df_res.to_excel('../result/202305广韵建模1_建模结果_广韵反切_归部_韵图介音_异读.xlsx', sheet_name='结果', index=False)

print('------end------')
print(f"当前方案共得到了{len(df_res['声母'].unique())}个声母")
