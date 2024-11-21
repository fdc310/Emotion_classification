import pandas as pd

'''
问题：read_excel将NA解析为空值
原因：pandas 读取文本的时候会默认（na_values）将如下字符串作为空值处理：

‘’, ‘#N/A’, ‘#N/A N/A’, ‘#NA’, ‘-1.#IND’, ‘-1.#QNAN’, ‘-NaN’, ‘-nan’, ‘1.#IND’, ‘1.#QNAN’, ‘<NA>’, ‘N/A’, ‘NA’, ‘NULL’, ‘NaN’, ‘n/a’, ‘nan’, ‘null’。

解决：设置keep_default_na的值为False,关闭默认空值（na_values）,源文件是什么值就是什么值

'''
df = pd.read_excel('SentimentAnalysisDictionary/情感词汇本体/情感词汇本体.xlsx', keep_default_na=False)

print(df.head(10))

dt = pd.read_csv("data/ms/UID325085719443416_管爷教做菜_喜欢作品.list", sep="|", names=['url',  'ch', 'cont'])

print(dt.head(10))
# 幸福的
Happy = []
# 好的
Good = []
# 惊讶的
Surprise = []
# 愤怒的
Anger = []
# 伤心的
Sad = []
# 恐惧的
Fear = []
# 厌恶的
Disgust = []

# 迭代表中数据，将7种情绪归类(df.iterrows是迭代遍历表中每一行)
for idx,row in df.iterrows():
    if row['情感分类'] in ['PA', 'PE']:
        Happy.append(row['词语'])
    if row['情感分类'] in ['PD', 'PH', 'PG', 'PB', 'PK']:
        Good.append(row['词语'])
    if row['情感分类'] in ['PC']:
        Surprise.append(row['词语'])
    if row['情感分类'] in ['NB', 'NJ', 'NH', 'PF']:
        Sad.append(row['词语'])
    if row['情感分类'] in ['NI', 'NC', 'NG']:
        Fear.append(row['词语'])
    if row['情感分类'] in ['NE', 'ND', 'NN', 'NK', 'NL']:
        Disgust.append(row['词语'])
    if row['情感分类'] in ['NA']:
        Anger.append(row['词语'])
# 计算积极的和消极的规则
Positive = Happy+Good+Surprise
Negative = Anger + Sad + Fear + Disgust
print('情绪词语列表整理完成')
print(Positive)
print(Negative)