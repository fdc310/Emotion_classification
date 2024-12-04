from pyecharts import options as opts

from pyecharts.charts import WordCloud

from pyecharts.globals import SymbolType

word = [
    ("背包问题", 10000),
    ("大整数", 6100),
    ("Karatsuba乘法算法", 4300),
    ("穷举搜索", 4000),
    ("傅里叶变换", 2400),
    ("状态树遍历", 2200),
    ("剪枝", 1800),
    ("Gale-shapley", 1400),
    ("最大匹配与匈牙利算法", 1000),
    ("线索模型", 860),
    ("关键路径算法", 840),
    ("最小二乘法曲线拟合", 520),
    ("二分逼近法", 550),
    ("牛顿迭代法", 500),
    ("Bresenham算法", 462),
    ("粒子群优化", 366),
    ("A*算法", 273),
    ("估值函数", 260),

]

def wordcloud_base() -> WordCloud:
    c = (
        WordCloud().add("", word, word_size_range=[20, 100], shape='diamond')
        .set_global_opts(title_opts=opts.TitleOpts(title='WordCloud词云'))
    )
    return c

wordcloud_base().render("词云图.html")