import codecs
from collections import defaultdict
import jieba



# 分词，去除停用词
def seg_word(sentence):
    # 分词
    seg_list = jieba.cut(sentence)
    seg_result = []
    for w in seg_list:
        seg_result.append(w)
    # 读取停用词
    stopwords = set()
    fr = codecs.open('stopwords.txt', 'r', 'utf-8')
    for word in fr:
        stopwords.add(word.strip())
    fr.close()
    # 去除停用词
    return list(filter(lambda x: x not in stopwords, seg_result))


def classify_words(word_list):
    # 读取情感字典
    sen_file = open('BosonNLP_sentiment_score.txt', 'r+', encoding='utf-8')
    # 获取字典内容
    # 去除'\n'
    sen_list = sen_file.read().splitlines()
    # 创建情感字典
    sen_dict = defaultdict()
    # 读取字典文件每一行内容，将其转换为字典对象，key为情感词，value为对应的分值
    for s in sen_list:
         # 对每一行内容根据空格分隔，索引0是情感词，1是情感分值
        if len(s.split(' ')) == 2:
            sen_dict[s.split(' ')[0]] = s.split(' ')[1]

         # 读取否定词文件
    not_word_file = open('notDic.txt', 'r+', encoding='utf-8')
     # 否定词没有分值,使用列表
    not_word_list = not_word_file.read().splitlines()

     # 读取程度副词文件
    degree_file = open('degree.txt', 'r+', encoding='utf-8')
    degree_list = degree_file.read().splitlines()
    degree_dic = defaultdict()
     # 程度副词转为字典对象，key为词，value为权值
    for d in degree_list:
        degree_dic[d.split(',')[0]] = d.split(',')[1]

     # 分类结果，词语索引为key，分值为value，否定词分值为-1
    sen_word = dict()
    not_word = dict()
    degree_word = dict()

     # 分类
    for word in word_list:
        if word in sen_dict.keys() and word not in not_word_list and word not in degree_dic.keys():
            sen_word[word] = sen_dict[word]
        elif word in not_word_list and word not in degree_dic.keys():
            not_word[word] = -1
        elif word in degree_dic.keys():
            degree_word[word] = degree_dic[word]
    sen_file.close()
    degree_file.close()
    not_word_file.close()
         # 将分类结果返回
         # 词语索引为key，分值为value，否定词分值为 - 1
    return sen_word, not_word, degree_word


def score_sentiment(sen_word, not_word, degreen_word, seg_result):
    # 权重初始化为1
    W = 1
    score = 0
    # 遍历分词结果
    for i in range(0, len(seg_result)):
        #若是程度副词
        if seg_result[i] in degreen_word.keys():
            W *= float(degreen_word[seg_result[i]])
        # 若是否定词
        elif seg_result[i] in not_word.keys():
            W *= -1
        elif seg_result[i] in sen_word.keys():
            score += float(W) * float(sen_word[seg_result[i]])
        W = 1
    return score


# 调度各函数
def sentiment_score(sentence):
    # 1.分词
    seg_list = seg_word(sentence)
    # 2.将分词结果转为dic,再分类
    sen_word, not_word, degree_word = classify_words(seg_list)
    # 3.计算得分
    score = score_sentiment(sen_word, not_word, degree_word, seg_list)
    return score


if __name__ == '__main__':
    sentence1 = input('请输入一句话：')
    score = sentiment_score(sentence1)
    print('情感值为：', score)
