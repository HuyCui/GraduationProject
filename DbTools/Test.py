import jieba
import random
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
from collections import Counter

def random_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
        h  = random.randint(30,250)
        s = int(100.0 * 255.0 / 255.0)
        l = int(100.0 * float(random.randint(60, 120)) / 255.0)
        return "hsl({}, {}%, {}%)".format(h, s, l)


#去除停用词
def remove_stop_words(dic):
    stop_words = []
    with open('Chinese_stopwords.txt',  'r', encoding='utf-8') as f1:
        stop_words = f1.readlines()
        stop_words=[x.strip() for x in stop_words if x.strip()!='']
    for key in list(dic.keys()):
        if key in stop_words:
            del dic[key]
    del dic['']
    del dic['\n']
    del dic[' ']
    #print(dic)
    return dic



def cut_word(commentsFile):  # 对数据分词
    with open(commentsFile, encoding='utf-8') as f:
        content_txt = f.read()
        word_list = jieba.lcut(content_txt, cut_all=True)
        #print(word_list)
        dic = {}
        for word in word_list:
            if word not in dic.keys():
                dic[word] = 1
            else:
                dic[word] = dic[word] + 1
        wl = sorted(dic.items(), key=lambda item:item[1], reverse=True)
        wl = dict(wl)
        wl = remove_stop_words(wl)
        #print(wl)
    return wl


def cut_wordByList(comments):  # 对数据分词

    content_txt = comments
    word_list = jieba.lcut(content_txt, cut_all=True)
    #print(word_list)
    dic = {}
    for word in word_list:
        if word not in dic.keys():
            dic[word] = 1
        else:
            dic[word] = dic[word] + 1
    wl = sorted(dic.items(), key=lambda item:item[1], reverse=True)
    wl = dict(wl)
    wl = remove_stop_words(wl)
    #print(wl)
    return wl


def create_word_cloud(commentsFile):  # 生成词云
    background_image = np.array(Image.open('bg.jpg'))  # 设置词云形状图片
    image_colors = ImageColorGenerator(background_image)
    # 生成词云
    wc = WordCloud(font_path='C:/Windows/Fonts/SIMLI.TTF',   # 设置字体为本地的字体，有中文必须要加
                   background_color='white',    # 设置背景的颜色，需与背景图片的颜色保持一致，否则词云的形状会有问题
                   scale=4,
                   width = 600,
                   height=600,
                   max_words=100,     # 设置最大的字数
                   max_font_size=70,   # 设置字体的最大值
                   min_font_size=10,
                   random_state=40,     # 设置有多少种随机生成状态，即有多少种配色方案
                   mask=background_image,
                   color_func=random_color_func).generate_from_text(cut_word(commentsFile))  # 设置词云的一些配置,有mask参数再设定宽高是无效的
    wc.to_file('wordc.jpg')  # 保存图片
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')  # 不显示坐标轴
    plt.show()



#根据词频生成词云
def create_word_cloud_fq(commentsFile):  # 生成词云
    background_image = np.array(Image.open('bg.jpg'))  # 设置词云形状图片
    image_colors = ImageColorGenerator(background_image)
    # 生成词云
    wc = WordCloud(font_path='C:/Windows/Fonts/SIMLI.TTF',   # 设置字体为本地的字体，有中文必须要加
                   background_color='white',    # 设置背景的颜色，需与背景图片的颜色保持一致，否则词云的形状会有问题
                   scale=4,
                   width = 600,
                   height=600,
                   max_words=100,     # 设置最大的字数
                   max_font_size=70,   # 设置字体的最大值
                   min_font_size=15,
                   random_state=40,     # 设置有多少种随机生成状态，即有多少种配色方案
                   mask=background_image,
                   color_func=random_color_func).generate_from_frequencies(cut_word(commentsFile))  # 设置词云的一些配置,有mask参数再设定宽高是无效的
    wc.to_file('wordc.jpg')  # 保存图片
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')  # 不显示坐标轴
    plt.show()


# if __name__ == '__main__':
#     create_word_cloud_fq('../TaoBao/tb_comments.txt')

