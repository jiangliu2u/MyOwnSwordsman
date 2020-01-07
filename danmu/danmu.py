import jieba,re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
jieba.load_userdict("dict.txt")
words = []  # 所有单词
two_words = []  # 大于或等于两个单词
p = re.compile(r'\/\{\w{2}',re.S)
with open("11.txt", 'r', encoding="utf-8") as f:
    for line in f.readlines():
        danmu = line.split(",")
        if len(danmu)<3:
            continue
        seg = danmu[2]
        seg = seg.replace("6","")
        seg = p.sub("",seg)
        # seg = danmu[2].decode('utf-8').encode('utf-8')  # 中文解编码
        seg1 = seg.strip()
        seg_list = jieba.lcut(seg1, cut_all=False)  # jieba分词
        words.extend(seg_list)
print("此文章总共分得"+str(len(words))+"个词")
for i in words:  # 以词语长度分类
    if len(i) >= 2:
        words.remove(i)
        if i =="哈哈" or i =="哈哈哈哈"or i =="哈哈哈" or i =="你们"or i =="不是"or i =="什么"or i =="没有"or i =="就是"or i =="这个"or i =="一个":
            continue
        two_words.append(i)
print("此文章大于两个字的词语有" + str(len(two_words)) + "个")
print("此文章一个字的词语有" + str(len(words)) + "个")
c = Counter(words)
c1 = Counter(two_words)
wc = WordCloud(scale=16,font_path='font.ttf',background_color='white').generate_from_frequencies(c1) # wordcloud自带的xxx.ttf 并不支持中文，在网上下载一个引用即可
plt.figure()
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()