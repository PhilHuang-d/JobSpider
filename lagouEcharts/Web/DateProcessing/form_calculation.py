# -*- coding:utf-8 -*-
import sys
import os
import datetime
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import pymysql
'''
本模块通过sql查询的数据用于html的表单页面
'''
#数据库配置
HOST = '127.0.0.1'
PORT = 3306
USER = 'root'
PASSWD = 'root'
DB = 'lagouspider'
CHARSET = 'utf8'

def handle(word):
    word = word.replace("\\n","").strip()
    return word

#计算公司职位数量Top100
def sel_company_job_count():
    config = {
        'host': HOST,
        'port': PORT,
        'user': USER,
        'passwd': PASSWD,
        'db': DB,
        'charset': CHARSET
    }
    db = pymysql.connect(**config)
    cursor = db.cursor()
    top_100 = []
    # 执行SQL语句
    cursor.execute(
'''
select jobCompany,count(jobDetailUrl) as num,CompanyDomain,DevelopmentStage,CompanyUrl
from lagou_table
group by jobCompany,CompanyDomain,DevelopmentStage,CompanyUrl
order by num desc 
limit 100;
''')
    # 获取所有记录列表
    results = cursor.fetchall()
    li = [list(i) for i in results]
    for i in li:
        x = handle(i[2])
        y = handle(i[3])
        top_100.append([i[0],str(i[1]),x,y,i[4]])
    db.close()
    return top_100

def tbody_html():
    top_100 = sel_company_job_count()
    print(top_100)
    tr_html = ''
    num = 1
    for i in top_100:
        tr = '''
        <tr>
        <td>{}</td>
        <td><a href = "{}" target ="_blank">{}</a></td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        </tr>
        '''.format(num,i[4],i[0],i[1],i[2],i[3])
        num += 1
        tr_html = tr_html + tr
    print(tr_html)
    return tr_html

tbody_html()
#计算数据总量
def sel_count():
    config = {
        'host': HOST,
        'port': PORT,
        'user': USER,
        'passwd': PASSWD,
        'db': DB,
        'charset': CHARSET
    }
    db = pymysql.connect(**config)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    try:
        # 执行SQL语句
        cursor.execute('''
        select count(jobDetailUrl)
        from lagouspider.lagou_table;
''')
        # 获取所有记录列表
        results = cursor.fetchall()
        url_count = results[0][0]
        db.close()
        return url_count
    except:
        print("Error: unable to fecth data")
        db.close()
#计算平均招聘薪资
def sel_salary():
    config = {
        'host': HOST,
        'port': PORT,
        'user': USER,
        'passwd': PASSWD,
        'db': DB,
        'charset': CHARSET
    }
    db = pymysql.connect(**config)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    try:
        # 执行SQL语句
        cursor.execute('''
        select format(avg(salary_left),2)
        from lagou_table
    ''')
        # 获取所有记录列表
        results = cursor.fetchall()
        avg_salary = results[0][0]
        db.close()
        return avg_salary
    except:
        print("Error: unable to fecth data")
        db.close()
#计算公司数量
def sel_company():
    config = {
        'host': HOST,
        'port': PORT,
        'user': USER,
        'passwd': PASSWD,
        'db': DB,
        'charset': CHARSET
    }
    db = pymysql.connect(**config)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    try:
        # 执行SQL语句
        cursor.execute('''
        select count(*)
        from(
        select jobCompany
        from lagou_table
        group by jobCompany) as tab
''')
        # 获取所有记录列表
        results = cursor.fetchall()
        avg_salary = results[0][0]
        db.close()
        return avg_salary
    except:
        print("Error: unable to fecth data")
        db.close()


#计算3日新增
#获取当前日期3天以前的日期
def GetTime():
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=3)
    n_days = now - delta
    t = n_days.strftime('%Y%m%d')
    return t

def sel_threeday_newjob():
    t = GetTime()
    config = {
        'host': HOST,
        'port': PORT,
        'user': USER,
        'passwd': PASSWD,
        'db': DB,
        'charset': CHARSET
    }
    db = pymysql.connect(**config)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    try:
        # 执行SQL语句
        cursor.execute('''
        select count(*)
        from (
        select jobName
        from lagou_table
        where jobReleaseTime > "%s") as tab
'''%t)
        # 获取所有记录列表
        results = cursor.fetchall()
        new_job = results[0][0]
        db.close()
        return str(new_job)
    except:
        print("Error: unable to fecth data")
        db.close()




