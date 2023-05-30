import pandas as pd
from openpyxl import Workbook
import re
from tqdm import tqdm


# 所有声类
shenglei = list('博必普披蒲皮莫彌都他徒奴陟丑直女作子倉七作疾蘇息徐莊初崇山俟章昌船書禪古居苦去渠五魚烏於呼許胡雲餘盧力而')
n_shenglei = len(shenglei)

# 帮
s1 = '邊（布玄）布（博故）補（博古）伯百（博陌）北（博墨）博（補各）巴（伯加）晡（博孤）'
s2 = '方（府良）卑（府移）并（府盈）封（府容）分（府文）府甫（方矩）鄙（方美）必（卑吉）彼（甫委）兵（甫明）筆（鄙密）陂（彼爲）畀（必至）'
# 滂
s3 = '滂（普郎）普（滂古）匹（譬吉）譬（譬賜）'
s4 = '敷孚（芳無）妃（芳非）撫（芳武）芳（敷方）披（敷羈）峯（敷容）丕（敷悲）拂（敷勿）'
# 并
s5 = '蒲（薄胡）步捕（薄故）裴（薄回）薄（傍各）白（傍陌）傍（步光）部（蒲口）'
s6 = '房防（符方）縛（符钁）平（符兵）皮（符羈）附（符遇）符苻扶（防無）便（房連）馮（房戎）毗（房脂）弼（房密）浮（縛謀）父（扶雨）婢（便俾）'
# 明
s7 = '莫（慕各）慕（莫故）模謨摸（莫胡）母（莫厚）'
s8 = '文（無分）美（無鄙）望（巫放）無巫（武夫）明（武兵）彌（武移）亡（武方）眉（武悲）綿（武延）武（文甫）靡（文彼）'

# 端透定泥
s9 = '多（得何）得德（多則）丁（當經）都（當孤）當（都郎）冬（都宗）'
s10 = '他（託何）託（他各）土吐（他魯）通（他紅）天（他前）台（土來）湯（吐郎）'
s11 = '徒（同都）同（徒紅）特（徒則）度（徒故）杜（徒古）唐堂（徒郎）陀（徒何）'
s12 = '奴（乃都）乃（奴亥）諾（奴各）內（奴對）妳（奴蟹）那（諾何）'

# 知徹澄娘
s13 = '張（陟良）知（陟離）猪豬（陟魚）徵（陟陵）中（陟弓）追（陟隹）陟（竹力）卓（竹角）竹（張六）珍（陟鄰）'
s14 = '抽（丑鳩）癡（醜之）楮禇（丑呂）丑（敕久）恥（敕里）敕（恥力）'
s15 = '除（直魚）場（直良）池馳（直離）治持（直之）遟（直尼）佇（直呂）柱（直主）丈（直兩）直（除力）宅（場伯）墜（直類）'
s16 = '尼（女夷）拏（女加）穠（女容）女（尼呂）'

# 精-可以系联为一类
s17 = '臧（則郎）作（則落）則（子德）祖（則古）借（子夜）'
s18 = '將（即良）子（即里）資（即夷）即（子力）茲（子之）醉（將遂）姊（將几）遵（將倫）𩛠'
# 清-异读条例系联
s19 = '倉蒼（七岡）采（倉宰）麁麤（倉胡）青（倉經）千（蒼先）'
s20 = '此（雌氏）雌（此移）遷（七然）取（七庾）親（七人）七（親吉）醋（倉故）'
# 從
s21 = '才（昨哉）徂（昨胡）在（昨宰）前（昨先）藏（昨郎）昨（在各）'
s22 = '疾（秦悉）秦（匠鄰）匠（疾亮）慈（疾之）自（疾二）情（疾盈）漸（慈染）'
# 心
s23 = '蘇（素姑）素（桑故）速（桑谷）桑（息郎）先（蘇前）'
s24 = '相（息良）悉（息七）思司（息茲）斯（息移）私（息夷）雖（息遺）辛（息鄰）息（相即）須（相俞）胥（相居）寫（息姐）'
# 邪
s25 = '徐（似魚）祥詳（似羊）辭辝（似茲）似（詳里）旬（詳遵）寺（詳吏）夕（祥易）隨（旬爲）'

# 莊初崇山俟
s26 = '莊（側羊）爭（側莖）阻（側呂）鄒（側鳩）簪（側吟）側仄（阻力）'
s27 = '初（楚居）楚（創舉）瘡創（初良）測（初力）叉（初牙）厠（初吏）芻（測隅）'
s28 = '鋤鉏（士魚）牀（士莊）犲（士皆）崱（士力）士仕（鉏里）崇（鋤弓）査（鉏加）雛鶵（仕于）助（牀據）'
s29 = '山（所間）疏踈（所葅）砂沙（所加）生（所庚）色（所力）數（所矩）所（疏舉）史（疏士）'
s30 = '牀（士莊）俟（牀史）'

# 章昌船書禪
s31 = '之（止而）止（諸市）章（諸良）征（諸盈）諸（章魚）煑（章與）支（章移）職（之翼）正（之盛）旨（職雉）占（職廉）脂（旨移）'
s32 = '昌（尺良）尺赤（昌石）充（昌終）處（昌與）叱（昌栗）'
s33 = '神（食鄰）乘（食陵）食（乘力）實（神質）'
s34 = '書舒（傷魚）傷商（式陽）施（式支）失（式質）矢（式視）試（式吏）式識（賞職）賞（書兩）詩（書之）釋（施隻）始（詩止）'
s35 = '時（市之）殊（市朱）常嘗（市羊）蜀（市玉）市（時止）植殖寔（常職）署（常恕）臣（植鄰）承（署陵）是氏（承紙）視（承矢）成（是征）'

# 見
s36 = '古（公戶）公（古紅）過（古臥）各（古落）格（古伯）兼（古甜）姑（古胡）佳（古膎）詭（過委）乖（古懷）'
s37 = '居（九魚）九（舉有）俱（舉朱）舉（居許）規（居隋）吉（居質）紀（居里）幾（居履）'
# 溪
s38 = '康（苦岡）枯（苦胡）牽（苦堅）空（苦紅）謙（苦兼）口（苦后）楷（苦駭）客（苦格）恪（苦各）苦（康杜）可（枯我）'
s39 = '去（丘據）丘（去鳩）墟袪（去魚）詰（去吉）窺（去隨）羌（去羊）欽（去金）傾（去營）起（墟里）綺（墟彼）豈（袪豨）區驅（豈俱）曲（丘玉）卿（去京）棄（詰利）乞（去訖）'
# 群
s40 = '渠（強魚）強（巨良）求（巨鳩）巨（其呂）具（其遇）臼（其九）衢（其俱）其（渠之）奇（渠羈）曁（具冀）跪（渠委）狂（巨王）'
# 疑
s41 = '五（疑古）俄（五何）吾（五乎）研（五堅）'
s42 = '魚（語居）疑（語其）牛（語求）語（魚巨）宜（魚羈）擬（魚紀）危（魚爲）玉（魚欲）遇（牛具）虞愚（遇俱）'

# 影-烏於
s43 = '烏（哀都）哀（烏開）安（烏寒）煙（烏前）鷖（烏奚）愛（烏代）'
s44 = '於（央居）央（於良）憶（於力）伊（於脂）依衣（於希）憂（於求）一（於悉）乙（於筆）謁（於歇）紆（憶俱）挹（伊入）委（於詭）握（於角）'
# 曉-呼許
s45 = '呼（荒烏）荒（呼光）虎（呼古）馨（呼刑）火（呼果）海（呼改）呵（虎何）花（呼瓜）'
s46 = '香（許良）朽（許久）羲（許羈）休（許尤）況（許訪）許（虛呂）興（虛陵）喜（虛里）虛（朽居）'
# 匣-胡雲
s47 = '胡乎（戶吴）侯（戶鉤）戸（侯古）下（胡雅）黃（胡光）何（胡歌）懷（戶乖）獲（胡麥）'
s48 = '于（羽俱）羽雨（王矩）云雲（王分）王（雨方）韋（雨非）永（于憬）有（雲久）榮（永兵）爲（薳支）洧（榮美）筠（爲赟）薳（韋委）'
# 餘
s49 = '余餘予（以諸）夷（以脂）以（羊已）羊（與章）弋翼（與職）與（余呂）營（余傾）移（弋支）悅（弋雪）'

# 來
s50 = '盧（落胡）來（落哀）賴（落蓋）落洛（盧各）勒（盧則）郎（魯當）魯（郎古）練（郎甸）'
s51 = '力（林直）林（力尋）呂（力舉）良（呂張）離（呂支）里（良士）連（力延）縷（力主）'
# 日
s52 = '如（人諸）汝（人渚）儒（人朱）人（如鄰）而（如之）仍（如乘）兒（汝移）耳（而止）'

names = locals()
fanqie2shenglei = {}


for i in range(n_shenglei):
    ls_fanqie = list(re.sub(r'（.+?）', '', names['s' + str(i + 1)]))
    for char in ls_fanqie:
        fanqie2shenglei[char] = shenglei[i]

fanqie2shenglei['戶'] = '胡'
fanqie2shenglei['㚷'] = '女'  # 娘
fanqie2shenglei['褚'] = '丑'  # 徹
fanqie2shenglei['暨'] = '渠'  # 群
fanqie2shenglei['疎'] = '山'
fanqie2shenglei['弃'] = '去'  # 溪
fanqie2shenglei['兹'] = '子'
fanqie2shenglei['烟'] = '烏'  # 影
fanqie2shenglei['几'] = '居'  # 見
fanqie2shenglei['迍'] = '陟'
fanqie2shenglei['豺'] = '崇'
fanqie2shenglei['查'] = '崇'
fanqie2shenglei['廁'] = '初'

df_res = pd.read_excel(r'../result/202305简化_广韵建模1_建模结果_广韵反切_归部_韵图介音_异读.xlsx', sheet_name='结果')
N = len(df_res)
df_res.insert(df_res.shape[1], '声类', 0)
# 给计算结果加上声类，便于比较
for i in tqdm(range(N)):
    shangzi = df_res['上字'].iloc[i]
    df_res['声类'].iloc[i] = fanqie2shenglei[shangzi]

df_res.to_excel('../result/202305结果分析_广韵反切_归部_韵图介音_异读.xlsx', index=False)
writer2 = pd.ExcelWriter('../result/202305结果分析_广韵反切_归部_韵图介音_异读.xlsx', mode="a", engine="openpyxl")

# 分析声类
res_shengmu_ls = df_res['声母'].unique().tolist()
ans_shengmu_ls = df_res['声母-标准'].unique().tolist()
ans_shenglei_ls = shenglei

ls = []
for res_shengmu in res_shengmu_ls:
    tmp_ls = [str(res_shengmu)]
    for ans_shengmu in ans_shengmu_ls:
        df_intersetion = df_res[(df_res['声母'] == res_shengmu) & (df_res['声母-标准'] == ans_shengmu)]
        tmp_ls.append(len(df_intersetion))
    ls.append(tmp_ls)
df_shengmu_analyze = pd.DataFrame(ls, columns=['计算出的声母结果'] + ans_shengmu_ls)
df_shengmu_analyze.head()

df_shengmu_analyze.to_excel(writer2, sheet_name='声母结果分析', index=False)

ls = []
for res_shengmu in res_shengmu_ls:
    tmp_ls = [str(res_shengmu)]
    for ans_shenglei in ans_shenglei_ls:
        df_intersetion = df_res[(df_res['声母'] == res_shengmu) & (df_res['声类'] == ans_shenglei)]
        tmp_ls.append(len(df_intersetion))
    ls.append(tmp_ls)

df_shenglei_analyze = pd.DataFrame(ls, columns=['计算出的声母结果'] + ans_shenglei_ls)
df_shenglei_analyze.to_excel(writer2, sheet_name='声类结果分析', index=False)

df_yunxi_analyze = df_res[df_res['韵系'] != df_res['韵系-标准']]
df_yunxi_analyze.to_excel(writer2, sheet_name='韵系结果分析', index=False)

df_shengdiao_analyze = df_res[df_res['声调'] != df_res['声调-标准']]
df_shengdiao_analyze.to_excel(writer2, sheet_name='声调结果分析', index=False)

df_kaihe_analyze = df_res[df_res['开合'] != df_res['开合-标准']]
df_kaihe_analyze.to_excel(writer2, sheet_name='开合结果分析', index=False)

df_deng_analyze = df_res[df_res['等'] != df_res['等-标准']]
df_deng_analyze.to_excel(writer2, sheet_name='等结果分析', index=False)

writer2.close()
