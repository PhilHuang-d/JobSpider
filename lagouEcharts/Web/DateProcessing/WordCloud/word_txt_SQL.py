# -*- coding:utf-8 -*-
import pymysql

def word_txt(key):
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': 'root',
        'db': 'lagouspider',
        'charset': 'utf8'
    }
    db = pymysql.connect(**config)
    fileObject = open('source/%s.txt'%key, 'w')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    cursor.execute('''
        select %s from lagou_table;
        '''%key)
    # 获取所有记录列表
    results = cursor.fetchall()
    for word in results:
        fileObject.write(txt_handle(str(word)))
        fileObject.write('\n')
    fileObject.close()
    # 关闭数据库连接
    db.close()

def txt_handle(txt):
    txt = txt.replace("'","")
    txt = txt.replace("(","")
    txt = txt.replace(")","")
    txt = txt.replace(",","")
    txt = txt.replace("，","")
    txt = txt.replace("、","")
    txt = txt.replace(";","")
    txt = txt.replace("；","")
    txt = txt.replace("n","")
    txt = txt.replace("\\","")
    return txt

if __name__ == '__main__':
    word_txt("jobSpeak")
    word_txt("CompanyDomain")
