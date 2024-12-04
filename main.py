import pandas as pd
import jieba
import time
import csv
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
# print(Positive)
# print(Negative)

# 导入停用词规则

stop_words = pd.read_csv('stopwords-master/cn_stopwords.txt', engine='python',
                         encoding='utf-8', names=['sw'])
print(stop_words.head(10))
# 将停用词标转化为列表
stop_lists = stop_words['sw'].to_list()
print(stop_lists)

# 分词筛选
def cut_word(text):
    '''
    进行文本分词，将文本分词后筛选除去停用词
    :param text: 文本内容
    :return: 分词后的文本列表
    '''
    word_lists = [w for w in jieba.lcut(text) if w not in stop_lists]
    return word_lists


# 情感计算统计
c = open('Emotion_features.csv', "a+", newline='', encoding='utf-8-sig')
writer = csv.writer(c)
writer.writerow(['Em0tion', 'Word', 'Num'])



# 情感计算
def emotion_caculate(text):
    '''
    文本的情感计算
    :param text:
    :return:
    '''

    # 积极的
    positive = 0
    # 消极的
    negative = 0

    ## 评分初始值
    # positive = negative =0

    # 愤怒的（数量）
    anger = 0
    # 厌恶的
    disgust = 0
    # 恐惧的
    fear = 0
    # 伤心的
    sad = 0
    # 惊讶的
    surprise = 0
    # 好的
    good = 0
    # 开心的
    happy = 0


    ## 各个情感数量初始值
    # happy = good = sad = surprise = fear = disgust = anger = 0

    # 文本中各个情绪词的数量初始列表
    # 愤怒的（数量）
    anger_lists = []
    # 厌恶的
    disgust_lists = []
    # 恐惧的
    fear_lists = []
    # 伤心的
    sad_lists = []
    # 惊讶的
    surprise_lists = []
    # 好的
    good_lists = []
    # 开心的
    happy_lists = []

    ## 文本中各个情绪词初始列表
    # happy_lists = good_lists = surprise_lists = sad_lists = fear_lists = disgust_lists = anger_lists = []

    # 文本切割
    word_lists = cut_word(text)
    # 集合去重
    word_set = set(word_lists)

    # 迭代文本分词后的情绪词
    for word in word_set:
        # 统计直接分词后的列表中这个情绪的数量
        freq = word_lists.count(word)
        tlist = []
        if word in Positive:
            positive += freq
        if word in Negative:
            negative += freq
        if word in Good:
            good += freq
            good_lists.append(word)
            tlist.append('good')
            tlist.append(word)
            tlist.append(freq)
            writer.writerow(tlist)
        if word in Happy:
            happy += freq
            happy_lists.append(word)
            tlist.append('happy')
            tlist.append(word)
            tlist.append(freq)
            writer.writerow(tlist)
        if word in Sad:
            sad += freq
            sad_lists.append(word)
            tlist.append('sad')
            tlist.append(word)
            tlist.append(freq)
            writer.writerow(tlist)
        if word in Fear:
            fear += freq
            fear_lists.append(word)
            tlist.append('fear')
            tlist.append(word)
            tlist.append(freq)

            writer.writerow(tlist)
        if word in Surprise:
            surprise += freq
            surprise_lists.append(word)
            tlist.append('surprise')
            tlist.append(word)
            tlist.append(freq)

            writer.writerow(tlist)
        if word in Anger:
            anger += freq
            anger_lists.append(word)
            tlist.append('anger')
            tlist.append(word)
            tlist.append(freq)

            writer.writerow(tlist)
        if word in Disgust:
            disgust += freq
            disgust_lists.append(word)
            tlist.append('disgust')
            tlist.append(word)
            tlist.append(freq)

            writer.writerow(tlist)

    emotion_info = {
        "length": len(word_lists),
        "positive": positive,
        "negative": negative,
        "happy": happy,
        "good": good,
        "surprise": surprise,
        "sad": sad,
        "fear": fear,
        "anger": anger,
        "disgust": disgust
    }
    # 添加标头
    indexs = ['length', 'positive', 'negative', 'happy', 'good', 'surprise', 'sad', 'fear', 'anger', 'disgust']
    return pd.Series(emotion_info, index=indexs)

text = '''
清朝乾隆年间，民间忽然传出了这样一句话，说是女子中有千般毒，最毒没落爬龟妇。那么这个爬龟妇到底是个什么东西呢？他们都会做出哪些狠毒的事呢？
仔细听完，相信你一定会满身冷汗，忍不住感叹人性的残忍。你生活在清朝，少妇在边关服役，死在了万里之外，而你那副干瘪的小生子骨根本干不动，农活养活不了自己。
并且由于年老色衰改嫁也基本无望，眼看就要被活活饿死。好在天无绝伦之路。你们当地出产一种植物，可以制成麻药。你便和其他少妇的女人搭帮结火，带着麻药走街串巷，靠给人拔牙为生，这样就完了吗？
当然不是拔一颗烂牙才能赚几个钱。倘若下手时稍微偏一拼，把旁边的好牙也弄坏，过段时间不就又有生意了吗？
倘若拔牙时偷偷给患者下药，令其伤口化脓流血，久久不遇，然后再高价卖给他特效药，不就能拔一次牙赚两份钱了吗？一开始你还犹犹豫豫的不敢下手，结果漏了马脚被患者拉着胳膊要上膛打官司。
最后呢不得不掏空，少有银两，还到你们之中。身材最好的李二姐独自去陪了一晚上，醉才逃过一劫。
事后，李二姐把胳膊抡圆了，给了你一脚轰骂道，能干就干，不能干，就滚回家去，等着饿死，听到恶字，你吓得两腿直哆嗦，站都站不稳，
而且你也发现了这世界哪有什么好人啊，被人家抓住，把柄，还不是往死里整。你从这一刻起，你心中仅存的良知和人性彻底粉碎。从这一刻起，
你正式黑化成为一名丧尽天良的爬龟妇给对方下药，这招来信还是太慢了。而且为了避免对方醒悟过来找你们算账，不得不东逃西窜流动作案，连个安稳觉都睡不成，
太不划算了，你们必须换一种思路，逮住一只蛤蟆，就要把前列腺液都给他挤出来，将骗局进行到底。你瞄准了一户条件不错的人家，于是让李二姐在拔牙的时候，
故意多与患者攀谈，闲聊，套出对方的信息。过几天自己在扮成神婆，说到他家门前，用一只刻满鬼画符的龟壳奇怪，说出对方家里有几口人，有几间房，门帘是什么颜色的？
床单是什么材料的？鸡窝在哪边？谁刚又在拿笔，甚至领男主人三天前踩死了一条蛇，女主人腰间有两颗痣都一清二楚，把对方唬得一愣一愣的，你有故弄玄虚的说，那条蛇不是寻常之物，
不做罢，超度的话必会遭到报复。男主人听见你张口就要十两银子，气得破口大骂，让你有多远？滚多远，你倒是也不生气，两手一揣慢悠悠的离去。当天夜里，
你便和姐妹们一起往他家扔了整整两麻袋毒蛇蝎子、蜈蚣蟾蜍。第二天，你又揣着手慢悠悠的走来，一屁股坐在他家门口不出所料。这时男主人顶头哈哟的，把你请进内院，
恭恭敬敬的奉上十两银子，求你做法，你却不紧不慢的数时间越长，妖气越重，越难超度。今天十两银子可不够了，得一百两男主人脸色憋得通红，后槽牙咬得咯，吱吱直响，
可最终还是敌不过心中的恐惧，冷痛交了钱，于是你便点燃艾草，将贵壳扔进火中，跳了一段鸡飞狗跳的尬舞，随后便全布妖魔一除，日后多行善事，必能夹载平安，这样就完了吗？
当然没有你假装不经意间瞟了一眼女主人怀孕九月的肚子，然后掐指一算惋惜的的，说你们家到这里呀，怕是要绝活了。这肚子里的娃娃是个女胎，以后也很难怀上男胎命中。
该男命中，该男啊男主人打惊失色，赶忙跪在地上，磕头如倒蒜。一般问你可有破解之法，出多少钱，他都愿意你摆摆手，说钱不是问题，但是想要逆天改命，改变胎儿性别，还是需要你配合才行。
你吩咐他出门向东迎着太阳的方向，就不宜叩手，连续走十日，务必要诚心祈倒，差一步都不行，差一个时辰都不行，等到把男主人支出家门。
你便如野兽一般露出了凶狠的獠牙，借着给女主人做法的功夫，落到他身后，用沾满麻药的手绢，将其麻烦再招呼其他姐妹进门，把他绳捆锁绑，拖到卧房的床上。
孕妇的胎盘可是个不可多得的好东西，好像叫什么纸和车，大户人家的少奶奶生不出孩子，全靠这东西倒要引子，听说还有延年益寿的功效，别的你不太清楚，
只知道这东西值钱很值情，非常知情，你迫不及待的扒开女主人的衣服，露出光滑的肚皮。心想这里装的哪是什么？孩子分明是白花花的影子，掏出一把锋利的小刀，
俯下身手不抖，心不跳的。在这光滑的肚皮上划开，一条长长的口齿鲜血，顿时流淌出来，女主人也被疼醒，惊恐的看着你贪婪了很多的嘴脸，奋力扭动，挣扎起来，
看着她喷涌的泪水和流淌的鲜血，你内心毫无波澜，皮笑肉不笑的说，尽量别动了，越动可就越遭罪。你把手伸进她的肚子粗暴的乱抓一通，
把血淋淋的婴儿和胎盘一并扯出，然后手起刀落，迅速剪下胎盘。女主人疼的发出咕噜咕噜的嘶吼，却因为口鼻被捂住，无法喊出声，
眼球都快被憋得爆出来了。汗水以肉眼可见的速度从额头上渗出质地刚刚滑落，那地便又凝聚好了。她被绑绑的双手拼命抓着炕洗十个指甲全被剥落，
抓着血肉抹糊，两条腿疯狂的抖动着四个人用尽吃人的力气都摁不住浑身穴位的婴儿，此时也大哭起来，你赶忙用棉被将其层层裹住，嘴里丢弃在一边，
然后招呼姐妹迅速撤离。临走前，你像一个刚刚打了肾脏的将军，一般趴在女主人的耳边说，对不起，看走眼了，你的肚子里其实是个男孩。你们把胎盘卖到王府，
换成白银之后，跳上马车，飞速逃离，此地，继续寻找下一个猎物，只留下肚子打肠撕开的怨妇，浑身沾满血污的死因，还有归来后哭到双眼流血的男主人。
当然了，天网恢恢，疏而不漏，如此丧心病狂的作案手法，怎么可能不引起朝廷重视？怎么可能不加派人手调查，又怎么可能不用激刑？伺候你们一伙人，
最终也全部落网，被押上法场。当众临时处死。那一天，全城轰动，每个人都咬牙切齿的前来，势必要亲眼看着你们这群心肠狠毒的爬龟妇接受活剐之行。
哼狠毒，你忍不住冷哼一声愤恨的想衙门强征民夫，害得无数，和你丈夫一样的男人死在边关不够狠吗？有些人为了延年益寿花重金买纸盒车，
他们难道不知道这东西是怎么来的吗？他们难道不构毒吗？要说狠毒，你这小小的爬龟妇怕是还差得远吧。
'''

# res = emotion_caculate(text)
# print(res)

# 情感计算
start_time = time.time()
emotion_df = dt['cont'].apply(emotion_caculate)
stop_time = time.time()
print(stop_time-start_time)
print(emotion_df.head())
# 输出结果
output_df = pd.concat([dt, emotion_df], axis=1)
# output_df.to_csv('管爷教做菜_em.csv', encoding="utf-8-sig", index=False)
# print(output_df.head())

# 获取 fear情绪的结果
fear_cont = output_df.sort_values(by='fear', ascending=False)
print(fear_cont)
print(fear_cont.iloc[1:5]['cont'])

# 获取negative情绪的结果
neg_cont = output_df.sort_values(by='negative',ascending=False)
print(neg_cont.iloc[1:5]['cont'])


c.close()



