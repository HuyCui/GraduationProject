from snownlp import SnowNLP
from snownlp import sentiment


#训练新的样本
def TrainNew_():
    sentiment.train('./neg.txt', './pos.txt')
    sentiment.save('sentiment.marshal')


#评论情感分析
def AnalyseComments(inputFile):
    good = 0
    bad = 0
    with open(inputFile, 'r', encoding='utf-8') as f:
        i = 1
        while True:
            row = f.readline()
            if not row:
                break
            if SnowNLP(row).sentiments > 0.6:
                good += 1
            else:
                bad += 1
            #print(str(i) +'   '+str(SnowNLP(row).sentiments))
            i += 1
        print('good:', good)
        print('bad:', bad)

def AnalyseCommentsByList(comments):
    pos = 0
    neg = 0
    for comment in comments:
        if SnowNLP(comment).sentiments > 0.6:
            pos += 1
        else:
            neg += 1
    return pos

# if __name__ == '__main__':
#     AnalyseComments('../TaoBao/tb_comments.txt')
