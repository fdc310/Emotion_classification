import pandas as pd
import csv
from word_cloud import wordcloud_base


# 读取文件
'''
此处突发问题好像是因为有部分词是双情感，会在csv文件中多处两列
我的选择是跳过第二情感那三列

'''
with open('Emotion_features.csv', encoding='utf-8-sig') as f:
    data = pd.read_csv(f, on_bad_lines='skip')

# 输出前5行
print(data.head())

# 统计七种情感的数量
groupnum = data.groupby('Em0tion').size()
print(groupnum)

# 分别统计每个情感中不同情感词
# for groupname,grouplist in data.groupby('Em0tion'):
#     print(groupname, grouplist)


# 生成词云可以读取的数据形式


emotion_list = set(data['Em0tion'])
# 此处直接迭代做七个词云
for emo in emotion_list:
    i = 0
    words = []
    counts = []
    while i < len(data):
        if data['Em0tion'][i] in emo:
            key = data['Word'][i]
            value = data['Num'][i]

            n = 0
            flag = 0
            while n < len(words):
                if words[n] == key:
                    counts[n] += value
                    flag += 1
                    break
                n +=1
            if flag == 0:
                words.append(key)
                counts.append(value)
        i += 1
    # 最终结果
    result = []
    k = 0
    while k < len(words):
        result.append((words[k],  int(counts[k] * 5)))
        k += 1
    print(result)

    wordcloud_base(result).render(f'{emo}.html')







