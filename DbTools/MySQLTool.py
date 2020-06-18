#!/usr/bin/python3
# coding: utf-8
# 处理MySql中的数据
# author：cuihui
import pymysql
from xpinyin import Pinyin

class DbTool:
    # 获取数据库连接
    db = None
    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root',
                             password='usbw', port=3306, db='GoodsComment')


    # 创建一张表
    def creataTable(self, keyword):
        cursor = self.db.cursor()
        p = Pinyin()
        key_ = p.get_pinyin(keyword, '')
        if cursor.execute("SHOW TABLES LIKE '%" + key_ + "%'") == 0:
            sql = 'Create Table ' + key_ + ' ( commid INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT, ' \
                                           'comment CHAR(200) , score INT(1))'
            cursor.execute(sql)
            self.db.commit()

    # 存入评论 list comm_list二维列表
    def saveComments(self, tableName, comm_list):
        p = Pinyin()
        tableName = p.get_pinyin(tableName, '')
        cursor = self.db.cursor()
        cursor.execute("select count('commid') from "+tableName)
        id = cursor.fetchall()
        id = id[0][0] #获取当前表的长度
        for comment in comm_list:
            sql = "Insert into "+tableName+"(`commid`, `comment`, `score`) " \
                                           "values('%d','%s', '%d')" %(id+1, comment[0], int(comment[1]))
            #print(sql)
            id+=1
            cursor.execute(sql)
        self.db.commit()


    #获取全部的评论
    def getAllComments(self, tableName):
        p = Pinyin()
        tableName = p.get_pinyin(tableName, '')
        sql = 'select * from '+tableName
        cursor = self.db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        commList = []
        for row in results:
            commList.append([row[1], row[2]])
        return commList

    def getNum(self):
        sql = "select table_name from information_schema.tables " \
              "where table_schema='goodscomment' and table_type='base table'"
        cursor = self.db.cursor()
        cursor.execute(sql)
        count = 0
        tableName = []
        for row in cursor.fetchall():
            tableName.append(row[0])
        for table in tableName:
            cursor.execute("select count('commid') from " + table)
            count += cursor.fetchall()[0][0]
        print('目前共有数据'+str(count)+'条')
        return count



    def closeConn(self):
        self.db.close()



if __name__ == '__main__':
    dbtool = DbTool()
    dbtool.getNum()
