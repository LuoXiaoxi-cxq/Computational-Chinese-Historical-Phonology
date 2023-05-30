import pandas as pd
from pulp import *

global_jianhua = 1
if global_jianhua:
    all_table = pd.read_excel(r'../data/《广韵》简化版_平水韵_魏晋南北朝隋诗歌.xlsx')
else:
    all_table = pd.read_excel(r"../data/《广韵》全_便于处理版.xlsx", sheet_name="廣韻覈校版20170209")

char2idx = {}  # 用列表记录多音字的不同音
idx2char = {}
N = len(all_table)  # 8153个字头
print(f'共读入{N}个字头')

for i in range(N):
    char_name = all_table[u'廣韻字頭(覈校後)'].iloc[i]
    if char2idx.get(char_name) is None:
        char2idx[char_name] = []
    char2idx[char_name].append(i)
    idx2char[i] = char_name

all_table['韻部原貌-平上去入相配爲平(調整前)'].unique()
shengdiao_ls = ['平', '上', '去', '入']
kaihe_ls = ['開', '合']
deng_ls = ['一', '二', '三', '四']
yunxi_ls = [
    '東', '冬', '鍾', '江', '支', '脂', '之', '微', '魚', '虞', '模', '齊', '佳', '皆', '灰',
    '咍', '真', '諄', '臻', '文', '欣', '元', '魂', '痕', '寒', '桓', '刪', '山', '先', '仙',
    '蕭', '宵', '肴', '豪', '歌', '戈', '麻', '陽', '唐', '庚', '耕', '清', '青', '蒸', '登',
    '尤', '侯', '幽', '侵', '覃', '談', '鹽', '添', '咸', '銜', '嚴', '凡', '祭', '泰', '夬',
    '廢']
kaihe2idx = {'開': 0, '合': 1}
deng2idx = {'一': 0, '二': 1, '三': 2, '四': 3}
shengdiao2idx = {'平': 0, '上': 1, '去': 2, '入': 3}
yunxi2idx = {}
for i, char in enumerate(yunxi_ls):
    yunxi2idx[char] = i

if global_jianhua:
    df_xiaoyun = all_table[all_table['新小韵字序'] == 0].copy().reset_index()
else:
    df_xiaoyun = all_table[all_table['小韻內字序'] == 1].copy().reset_index()

# 得到小韵代表字df_xiaoyun
n_xiaoyun = len(df_xiaoyun)
df_xiaoyun['idx'] = range(n_xiaoyun)

inf = 10 ** 5
eps = 10 ** (-1)
NN = 300

# 定义优化问题
GuangYunYinXi = pulp.LpProblem("GuangYunYinXi", LpMinimize)
print("Finish Defining Optimization Problem!")

# 定义决策变量
var_shengmu = {i: LpVariable(name=f"var_shengmu{i}", lowBound=0, upBound=100, cat=LpInteger) for i in range(N)}
var_kaihe = {i: LpVariable(name=f"var_kaihe{i}", lowBound=0, upBound=1, cat=LpInteger) for i in range(N)}
var_deng = {i: LpVariable(name=f"var_deng{i}", lowBound=0, upBound=3, cat=LpInteger) for i in range(N)}
var_yunxi = {i: LpVariable(name=f"var_yunxi{i}", lowBound=0, upBound=60, cat=LpInteger) for i in range(N)}
var_shengdiao = {i: LpVariable(name=f"var_shengdiao{i}", lowBound=0, upBound=3, cat=LpInteger) for i in range(N)}

# 为了将反切中绝对值转换为线性函数设的变量
var_fanqie_shengmu = {i: LpVariable(name=f"var_fanqie_shengmu{i}", cat=LpBinary) for i in range(N)}
var_fanqie_kaihe = {i: LpVariable(name=f"var_fanqie_kaihe{i}", cat=LpBinary) for i in range(N)}
var_fanqie_deng = {i: LpVariable(name=f"var_fanqie_deng{i}", cat=LpBinary) for i in range(N)}
var_fanqie_yunxi = {i: LpVariable(name=f"var_fanqie_yunxi{i}", cat=LpBinary) for i in range(N)}
var_fanqie_shengdiao = {i: LpVariable(name=f"var_fanqie_shengdiao{i}", cat=LpBinary) for i in range(N)}

# 为了将归部中绝对值转换为线性函数设的变量
var_guibu_yunxi = {i: LpVariable(name=f"var_guibu_yunxi{i}", cat=LpInteger) for i in range(N)}
var_guibu_shengdiao = {i: LpVariable(name=f"var_guibu_shengdiao{i}", cat=LpInteger) for i in range(N)}

# 为了将韵图中绝对值转换为线性函数设的变量
var_yuntu_kaihe = {i: LpVariable(name=f"var_yuntu_kaihe{i}", cat=LpInteger) for i in range(N)}
var_yuntu_deng = {i: LpVariable(name=f"var_yuntu_deng{i}", cat=LpInteger) for i in range(N)}

# 为了将求异条例中绝对值转换为线性函数设的变量
var_qiuyi_shengmu = {
    i: {j: LpVariable(name=f"var_qiuyi_shengmu{i}{j}", cat=LpBinary) for j in range(i + 1, n_xiaoyun)} for i in
    range(n_xiaoyun)}

# 异读条例变量
var_yidu1 = {i: LpVariable(name=f"var_yidu1{i}", cat=LpBinary) for i in range(N)}
var_yidu2 = {i: LpVariable(name=f"var_yidu2{i}", cat=LpBinary) for i in range(N)}

print("Finish Defining Variable!")

# 定义优化目标
GuangYunYinXi += lpSum(
    var_fanqie_shengmu[i] + var_fanqie_kaihe[i] + var_fanqie_deng[i] +
    var_fanqie_yunxi[i] + var_fanqie_shengdiao[i] + var_guibu_yunxi[i] +
    var_yuntu_kaihe[i] + var_yuntu_deng[i] + var_guibu_shengdiao[i] +
    var_yidu1[i] + var_yidu2[i] for i in range(N))
print("Finish Defining Optimazation Goal!")
