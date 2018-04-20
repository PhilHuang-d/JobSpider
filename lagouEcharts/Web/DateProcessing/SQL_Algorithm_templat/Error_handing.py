# -*- coding:utf-8 -*-
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import pymysql
'''
有时候会在抓取的网页中出现了 cookie为深圳的页面中抓到了上海的公司，需要在数据库中作出如下处理
select *
from lagou_table
where jobPlace = "深圳"
and Area = "黄浦区";

SET SQL_SAFE_UPDATES = 0;
update lagou_table set jobPlace = "上海" where jobPlace = "深圳"
and Area = "黄浦区";
SET SQL_SAFE_UPDATES = 1;
'''
old_jobPlace = "深圳"
new_jobPlace = "上海"
Area = "黄浦区"

def place_error_handing(old_jobPlace,Area,new_jobPlace):
    '''
    深圳 - 黄浦区 -> 上海 - 黄浦区
    :param old_jobPlace:
    :param Area:
    :param new_jobPlace:
    :return:
    '''
    # 连接数据库
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': 'root',
        'db': 'lagouspider',
        'charset': 'utf8'
    }
    db = pymysql.connect(**config)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    try:
        # 执行SQL语句
        cursor.execute('''SET SQL_SAFE_UPDATES = 0''')
        cursor.execute('''update lagou_table set jobPlace = "%s" where jobPlace = "%s"
and Area = "%s"
        '''%new_jobPlace,old_jobPlace,Area)
        results = cursor.fetchall()
        print(results)
        cursor.fetchall('''SET SQL_SAFE_UPDATES = 1''')

    except:
        print("error handing")
    db.close()

place_error_handing(old_jobPlace,Area,new_jobPlace)