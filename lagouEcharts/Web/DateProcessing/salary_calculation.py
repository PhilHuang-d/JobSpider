# -*- coding:utf-8 -*-
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import pymysql
from Web.DateProcessing.SQL_Algorithm_templat.salary_algorithm import *
'''
此处代码为连接数据库，查询各个需求的统计数据，返回数据列表，供echarts模块使用
需要使用的列表：城市列表，后台开发，人工智能开发
'''
#数据库配置
HOST = '127.0.0.1'
PORT = 3306
USER = 'root'
PASSWD = 'root'
DB = 'lagouspider'
CHARSET = 'utf8'


#数据关键字list
city_list = ["上海", "北京", "杭州", "成都", "深圳", "广州", "南京", "武汉", "西安"]
Backend_development_list = ["java", "c++","PHP", "python","数据挖掘", "C", "C#","Hadoop","区块链","ruby","Delphi","node.js"]
Artificial_intelligence_list = ["深度学习","机器学习","图像处理","图像识别","语音识别","机器视觉","算法工程师","自然语言处理"]

def sel_place_avg_salary():
    '''
    计算所有城市的所有职位平均薪资 的 均值
    :return:list
    '''
    #连接数据库
    config = {
        'host': HOST,
        'port': PORT,
        'user': USER,
        'passwd': PASSWD,
        'db': DB,
        'charset': CHARSET
    }
    db = pymysql.connect(**config)
    salary_list = []
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    print("正在计算各个城市薪资均值......")
    try:
        # 执行SQL语句
        cursor.execute(all_city())
        # 获取所有记录列表
        results = cursor.fetchall()
        for i in results:
            #遍历所有记录，依次添加到salary_list
            salary_list.append(i)
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    #print(salary_list)
    return salary_list

def sel_backend_development_avg_salary():
    '''
    计算后端开发平均薪资
    :return:
    '''
    # 打开数据库连接
    config = {
        'host': HOST,
        'port': PORT,
        'user': USER,
        'passwd': PASSWD,
        'db': DB,
        'charset': CHARSET
    }
    db = pymysql.connect(**config)
    salary_list = []
    num = 0
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    for city in city_list:
        for jobClass in Backend_development_list:
            try:
               # 执行SQL语句
               cursor.execute(select_avg_salary(city,jobClass))
               # 获取所有记录列表
               results = cursor.fetchall()
               for row in results:
                    #print(city,jobClass,row[0])
                    salary_list.append({'num': num,'city': city,'jobClass': jobClass,'avg_salary':row[0]})
                    num += 1
            except:
               print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    #print(salary_list)
    return salary_list

def sel_Artificial_intelligence_avg_salary():
    '''
    计算人工智能开发平均薪资
    :return:
    '''
    # 打开数据库连接
    config = {
        'host': HOST,
        'port': PORT,
        'user': USER,
        'passwd': PASSWD,
        'db': DB,
        'charset': CHARSET
    }
    db = pymysql.connect(**config)
    salary_list = []
    num = 0
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    for city in city_list:
        for jobClass in Artificial_intelligence_list:
            try:
               # 执行SQL语句
               cursor.execute(select_avg_salary(city,jobClass))
               # 获取所有记录列表
               results = cursor.fetchall()
               for row in results:
                    #print(city,jobClass,row[0])
                    salary_list.append({'num': num,'city': city,'jobClass': jobClass,'avg_salary':row[0]})
                    num += 1
            except:
               print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    return salary_list

def sel_area_left_salary():
    '''
        计算某地各地区最低薪资平均值
        :return:
        '''
    # 打开数据库连接
    config = {
        'host': HOST,
        'port': PORT,
        'user': USER,
        'passwd': PASSWD,
        'db': DB,
        'charset': CHARSET
    }
    db = pymysql.connect(**config)
    salary_list = []
    num = 0
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    for city in city_list:
        try:
            # 执行SQL语句
            cursor.execute(select_area_left_salary(city))
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                # print(city,jobClass,row[0])
                salary_list.append({'num': num, 'city': city, 'Area': row[1],'area_left_salary': row[0]})
                num += 1
        except:
            print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    #print(salary_list)
    return salary_list

def sel_small_class_avg_salary():
    #查询各个小类薪资均值与职位数量，返回list
    config = {
        'host': HOST,
        'port': PORT,
        'user': USER,
        'passwd': PASSWD,
        'db': DB,
        'charset': CHARSET
    }
    db = pymysql.connect(**config)
    salary_list = []
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    print("正在计算小类薪资均值......")
    try:
        # 执行SQL语句
        cursor.execute(select_smallClass_avg_salary())
        # 获取所有记录列表
        results = cursor.fetchall()
        for i in results:
            #i[1] = float(i[1])
            salary_list.append(i)
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    #print(salary_list)
    return salary_list

def sel_bigClass_avg_salary():
    config = {
        'host': HOST,
        'port': PORT,
        'user': USER,
        'passwd': PASSWD,
        'db': DB,
        'charset': CHARSET
    }
    db = pymysql.connect(**config)
    big_salary_list = []
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    print("正在计算大类薪资均值与职位数量......")
    try:
        # 执行SQL语句
        cursor.execute(select_bigClass_avg_salary())
        # 获取所有记录列表
        results = cursor.fetchall()
        for i in results:
            big_salary_list.append(i)
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    #print(big_salary_list)
    return big_salary_list

def sel_python_salary_count():
    config = {
        'host': HOST,
        'port': PORT,
        'user': USER,
        'passwd': PASSWD,
        'db': DB,
        'charset': CHARSET
    }
    db = pymysql.connect(**config)
    smallClass_salary_count = []
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    print("正在计算python薪资区间统计......")
    try:
        # 执行SQL语句
        cursor.execute(select_smallClass_salary_count_SQL("python"))
        # 获取所有记录列表
        results = cursor.fetchall()
        for i in results:
            smallClass_salary_count.append(i)
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    #print(smallClass_salary_count)
    return smallClass_salary_count

