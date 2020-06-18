#!/usr/bin/python3
# coding: utf-8
# 处理csv文件
# author：cuihui
import csv

def wirte2csv(fileName, data):
    fields = ['comment', 'score']
    with open('../CommentData/'+fileName+'.csv', 'a+', newline='',encoding='utf-8-sig') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(data)
        csvfile.close()


def writeDetail2Csv(fileName, data):
    fields = ['comment']
    with open('./Detail/'+fileName+'.csv', 'a+', newline='',encoding='utf-8-sig') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        # print(data)
        for line in data:
            csvwriter.writerow([line])
        csvfile.close()


def readFromCsv(fileName):
    data = []
    with open('../CommentData/'+fileName, 'r') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            data.append(row)
        del(data[0])
        return data

# if __name__ == '__main__':
#     wirte2csv('测试', [['fafa', 4], ['fagada', 5]])

