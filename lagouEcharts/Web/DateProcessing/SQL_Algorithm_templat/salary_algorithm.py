# -*- coding:utf-8 -*-
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
'''--------SQL 查询语句算法模块--------'''
'''----此处代码为各个需求所用的SQL语句----'''
def all_city():
    '''
    全国薪资热力图SQL 计算方式：取6K-10中的6k计算均值
    :return:
    '''
    city_list = '''
    select jobPlace
	   ,format(avg((salary_left+salary_right)/2),2) as city_avg_salary
    from lagou_table
    group by jobPlace;
    '''
    return city_list

def place_left_salary(jobPlace):
    '''
    各地最低薪资平均值SQL 参数：地名 计算方式：取6K-10中的6k计算均值
    :param jobPlace: 地名
    :return: sql
    '''
    left_salary = '''
        select jobPlace
               ,format(avg(salary_left),2) as palce_left_salary
        from lagou_table
        where jobPlace = "%s"
    '''% jobPlace
    return left_salary

def place_avg_salary(jobPlace):
    '''
    各地平均薪资均值SQL 参数： 地名 计算方式：取6k-10k 中的6,10 相加除以2的结果计算均值
    :param jobPlace: 地名
    :return: sql
    '''
    avg_salary = '''
        select jobPlace
               ,format(avg((salary_left+salary_right)/2),2) as place_avg_salary
        from lagou_table
        where jobPlace = "%s"
    '''% jobPlace
    return avg_salary

def select_avg_salary(jobPlace,jobClass):
    '''
    查询某地某种职业类型的平均薪资 （最低薪资+最高薪资）/2
    :param jobPlace: 地名
    :param jobClass: 职业类型
    :return: sql语句
    '''
    select_avg_salary = '''
      select format(sum((salary_left+salary_right)/2)/count(salary_left),2) as avg_salary
        from lagou_table
        where jobPlace = "%s"
        and jobClass = "%s"
      ''' %(jobPlace,jobClass)
    return select_avg_salary

def select_left_salary(jobPlace,jobClass):
    '''
    查询某地某种职业类型的最低薪资  取最低薪资
    :param jobPlace: 地名
    :param jobClass: 职业类型
    :return: sql语句
    '''
    select_left_salary = '''
      select format(sum(salary_left)/count(salary_left),2) as left_salary
        from lagou_table
        where jobPlace = "%s"
        and jobClass = "%s"
      ''' %(jobPlace,jobClass)
    return select_left_salary

def select_right_salary(jobPlace,jobClass):
    '''
    查询某地某种职业类型的最高  取最高薪资
    :param jobPlace: 地名
    :param jobClass: 职业类型
    :return: sql语句
    '''
    select_right_salary = '''
      select format(sum(salary_right)/count(salary_right),2) as right_salary
        from lagou_table
        where jobPlace = "%s"
        and jobClass = "%s"
      ''' %(jobPlace,jobClass)
    return select_right_salary

def select_area_left_salary(jobPlace):
    '''
    查询某地各个地区的最低薪资平均值
    :param jobPlace: 地名
    :return: sql
    '''
    select_area_left_salary = '''
    select format(avg(salary_left),2) as sh_left_salary,Area
    from lagou_table
    where jobPlace = "%s"
    group by Area
    '''% jobPlace
    return select_area_left_salary

def select_smallClass_avg_salary():
    '''
    从大小类统计表中查询各小类的薪资水平均值与职位数量
    :return:38个小类薪资水平与职位数量
    '''
    select_smallClass_avg_salary = '''
    select 	bigClass
		,smallClass 
		,format(avg(avg_salary),2) as smallClass_avg_salary
        ,sum(job_quantity) as smallClass_count
    from lagou_table_jobClass_count
    group by bigClass,smallClass
    '''
    return select_smallClass_avg_salary

def select_bigClass_avg_salary():
    '''
    从大小类统计表中查询各大类的薪资水平与职位数量
    :return: 7大类的薪资水平与职位数量
    '''
    select_bigClass_avg_salary = '''
    select bigClass
		,format(avg(avg_salary),2) as bigClass_avg_salary
        ,sum(job_quantity) as bigClass_count
    from lagou_table_jobClass_count
    group by bigClass
    '''
    return select_bigClass_avg_salary

def select_smallClass_salary_count_SQL(smallClass):
    '''
    统计各个小类薪资区数量
    :return:
    '''
    select_smallClass_salary_count = '''
    select	jobClass
		,sum(tab1.Four)          as '0-4k'
        ,sum(tab1.Eight)		as '4-8k'
        ,sum(tab1.Twelve)		as '8-12k'
        ,sum(tab1.Sixteen)		as '12-16k'
        ,sum(tab1.Twenty)		as '16-20k'
        ,sum(tab1.Twenty-four)	as '20-24k'
        ,sum(tab1.Thirty)		as '24-30k'
        ,sum(tab1.More)			as '>30k'
    from(
    select 	jobClass
            ,jobDivision 
            ,jobName
            ,salary_left
            ,salary_right
            ,case when salary_left<4 and salary_right>0 then 1 else "" end as 'Four'
            ,case when salary_left<8 and salary_right>4 then 1 else "" end as 'Eight'
            ,case when salary_left<12 and salary_right>8 then 1 else "" end as 'Twelve'
            ,case when salary_left<16 and salary_right>12 then 1 else "" end as 'Sixteen'
            ,case when salary_left<20 and salary_right>16 then 1 else "" end as 'Twenty'
            ,case when salary_left<24 and salary_right>20 then 1 else "" end as 'Twenty-four'
            ,case when salary_left<30 and salary_right>24 then 1 else "" end as 'Thirty'
            ,case when salary_right>30 then 1 else "" end as 'More'
    from lagou_table
    where jobClass = "%s"
    ) tab1
    group by jobClass;
    '''%smallClass
    return select_smallClass_salary_count