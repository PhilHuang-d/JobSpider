# -*- coding:utf-8 -*-
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from Web.DateProcessing.salary_calculation import *
from pyecharts import Geo, Radar,HeatMap
from pyecharts import Map, Bar
from pyecharts import Page, Pie

def test_aa():
    pass
#test_aa()
list_a = []

#全国招聘薪资水平热力图
def city_avg_salary():
    data = sel_place_avg_salary()
    print(data)
    geo = Geo("全国招聘薪资水平热力图", "数据来源:拉勾网", title_color="#000",
              title_pos="center", width=1120,
              height=800,background_color='#F4F3EF')
    attr, value = geo.cast(data)
    geo.add("", attr, value,
            type="heatmap", #类型热力图
            is_label_show = True,
            is_visualmap=True,
            visual_range=[0, 20],
            visual_text_color='#000'
            ,geo_normal_color="#FFFACD",
            geo_emphasis_color="#FFEC8B")
    return geo

#大类薪资水平与职位数量雷达图
def big_class_radar():
    page = Page()
    schema = [
        ("产品", 20), ("市场与销售", 20), ("技术", 20),
        ("职能", 20), ("设计", 20), ("运营", 20) ,("金融", 20)
    ]
    print("正在计算...")
    data = sel_bigClass_avg_salary()
    print(data)
    salary_list = []
    count_list = []
    for i in data:
        salary_list.append(i[1])
        count_list.append(i[2])
    v1 = [salary_list]
    v2 = [count_list]
    #平均薪资雷达图
    radar = Radar(background_color='#F4F3EF',)
    radar.config(schema)
    radar.add("平均薪资", v1, is_splitline=True, is_axisline_show=True)
    page.add(radar)
    #职位数量雷达图
    schema2 = [
        ("产品", 50000), ("市场与销售", 50000), ("技术", 50000),
        ("职能", 50000), ("设计", 50000), ("运营", 50000), ("金融", 50000)
    ]
    radar2 = Radar(background_color='#F4F3EF',)
    radar2.config(schema2)
    radar2.add("职位数量", v2, is_splitline=True, is_axisline_show=True,label_color=["#4e79a7"])
    page.add(radar2)
    return page


#小类薪资水平与职位数量饼图
def small_class_avg_salary(bigclass):
    print("正在计算...")
    data = sel_small_class_avg_salary()
    attr = []
    avg_salary_list = []
    small_class_count = []
    for i in data:
        if i[0] == "%s"%bigclass:
            attr.append(i[1])
            avg_salary_list.append(i[2])
            small_class_count.append(i[3])
    print(attr,avg_salary_list,small_class_count)
    pie = Pie("%s岗位各类别薪资(左)与职位数量(右)统计" %bigclass, title_pos='top', width=1200,background_color='#F4F3EF',)
    pie.add("平均薪资统计", attr, avg_salary_list, center=[25, 50], is_random=True,
            radius=[30, 75], rosetype='radius',is_label_show=True)
    pie.add("职位数量统计", attr, small_class_count, center=[75, 50], is_random=True,
            radius=[30, 75], rosetype='radius',is_label_show=True,legend_top='bottom')
    return pie

#python薪资水平分区统计表
def python_salary_count():
    page = Page()
    attr = ["0-4k", "4-8k", "8-12k", "12-16k", "16-20k", "20-24k","24-30k",">30k"]
    #数据处理，将列表中第一组元祖拆分添加到python_count列表中，pop掉第一个"python"字段
    data = sel_python_salary_count()
    python_count = []
    for i in data[0]:
        python_count.append(i)
    python_count.pop(0)
    print(python_count)
    pie = Pie("python薪资水平分段统计图", title_pos='center',background_color='#F4F3EF',)
    pie.add("", attr, python_count, radius=[40, 75], label_text_color=None,
             is_label_show=True, legend_orient='vertical',
             legend_pos='left')
    page.add(pie)
    bar = Bar(background_color='#F4F3EF',)
    bar.add("",attr,python_count,is_convert=True)
    page.add(bar)
    return page



#后端开发各个城市薪资水平热力图
def backend_development_avg_salary():
    print("正在计算后端开发各个城市薪资......")
    data = sel_backend_development_avg_salary()
    print(data)
    x_axis =  city_list
    y_axis = Backend_development_list
    avg_salary_list = []
    for x in range(9):
        for y in range(12):
            for i in data:
                if i["avg_salary"] == None:
                    i["avg_salary"] = '0'
                avg_salary_list.append([x,y,i["avg_salary"]])
    #print(avg_salary_list[::109])  防止3次循环产生的笛卡尔积 需要隔 x * y 中取数
    avg_salary_list = avg_salary_list[::109]
    heatmap = HeatMap("各地后端开发薪资水平",background_color='#F4F3EF',)
    heatmap.add("", x_axis, y_axis, avg_salary_list, is_visualmap=True,
                visual_text_color="#000", visual_orient='horizontal',visual_range=[0,30]
            ,visual_range_text= ['0', '30k'])
    return heatmap

#人工智能开发各个城市薪资水平热力图
def Artificial_intelligence_avg_salary():
    print("正在计算人工智能开发各个城市薪资......")
    data = sel_Artificial_intelligence_avg_salary()
    print(data)
    x_axis =  city_list
    y_axis = Artificial_intelligence_list
    avg_salary_list = []
    for x in range(9):
        for y in range(8):
            for i in data:
                if i["avg_salary"] == None:
                    i["avg_salary"] = '0'
                avg_salary_list.append([x,y,i["avg_salary"]])
    #print(avg_salary_list[::73])  #防止3次循环产生的笛卡尔积 需要隔 (x * y)+1中取数
    avg_salary_list = avg_salary_list[::73]
    heatmap = HeatMap("各地人工智能开发薪资水平",background_color='#F4F3EF',)
    heatmap.add("", x_axis, y_axis, avg_salary_list, is_visualmap=True,
                visual_text_color="#000", visual_orient='horizontal',visual_range=[0,30]
            ,visual_range_text= ['0', '30k'])
    return heatmap

#生成各地区最低薪资均值的可视化界面
def salary_shanghai_map():
    '''
    上海各地区最低薪资均值
    :return:html
    '''
    print("正在生成上海各地区最低薪资均值......")
    page = Page()
    s = sel_area_left_salary()
    value = []
    attr = []
    for i in s:
        if i['city'] == "上海":
            Area = i['Area']
            Area = Area.replace("县","区")
            area_left_salary = i['area_left_salary']
            value.append(area_left_salary)
            attr.append(Area)
    print(value)
    print(attr)
    map = Map("上海各地区最低薪资均值", width=1120, height=600,background_color='#F4F3EF',)
    map.add("", attr, value, maptype='上海',  is_label_show=True, is_visualmap=True, visual_range=['0','15']
            ,visual_range_text= ['0', '15k'],visual_text_color='#000')
    page.add(map)
    bar = Bar("上海各地区最低薪资均值",background_color='#F4F3EF')
    bar.add("上海", attr, value, is_stack=True,xaxis_interval=0,xaxis_label_textsize=11,is_datazoom_show=True
            , xaxis_rotate=30, datazoom_range=[0, 50], is_random=True, datazoom_type='both')
    page.add(bar)
    #page.render("salary_shanghai_map.html")
    print("上海各地区最低薪资均值生成完毕！！")
    return page

def salary_beijing_map():
    '''
    北京各地区最低薪资均值
    :return: html
    '''
    print("正在生成北京各地区最低薪资均值......")
    page = Page()
    s = sel_area_left_salary()
    value = []
    attr = []
    for i in s:
        if i['city'] == "北京":
            Area = i['Area']
            Area = Area.replace("县","区")
            area_left_salary = i['area_left_salary']
            value.append(area_left_salary)
            attr.append(Area)
    print(value)
    print(attr)
    map = Map("北京各地区最低薪资均值", width=1120, height=600,background_color='#F4F3EF',)
    map.add("", attr, value, maptype='北京',  is_label_show=True, is_visualmap=True, visual_range=['0','15']
            ,visual_range_text= ['0', '15k'],visual_text_color='#000')
    page.add(map)
    bar = Bar("北京各地区最低薪资均值",background_color='#F4F3EF',)
    bar.add("北京", attr, value, is_stack=True,xaxis_interval=0,xaxis_label_textsize=11,is_datazoom_show=True
            ,xaxis_rotate=30,datazoom_range=[0,50],is_random=True,datazoom_type='both')
    page.add(bar)
    #page.render("salary_beijing_map.html")
    print("北京各地区最低薪资均值生成完毕！！")
    return page

def salary_chengdu_map():
    '''
    成都各地区最低薪资均值
    :return:html
    '''
    print("正在生成成都各地区最低薪资均值......")
    page = Page()
    s = sel_area_left_salary()
    value = []
    attr = []
    for i in s:
        if i['city'] == "成都":
            Area = i['Area']
            area_left_salary = i['area_left_salary']
            value.append(area_left_salary)
            attr.append(Area)
    print(value)
    print(attr)
    map = Map("成都各地区最低薪资均值", background_color='#F4F3EF',width=1200, height=600)
    map.add("", attr, value, maptype='成都', is_label_show=True, is_visualmap=True, visual_range=['0','15'],visual_text_color='#000',visual_range_text= ['0', '15k'])
    page.add(map)
    bar = Bar("成都各地区最低薪资均值",background_color='#F4F3EF',)
    bar.add("成都", attr, value, is_stack=True,xaxis_interval=0,xaxis_label_textsize=11,is_datazoom_show=True
            ,xaxis_rotate=30,datazoom_range=[0,50],is_random=True,datazoom_type='both')
    page.add(bar)
    #page.render("salary_chengdu_map.html")
    print("成都各地区最低薪资均值生成完毕！！")
    return page

def salary_shenzhen_map():
    '''
    深圳各地区最低薪资均值
    :return:html
    '''
    print("正在生成深圳各地区最低薪资均值......")
    page = Page()
    s = sel_area_left_salary()
    value = []
    attr = []
    for i in s:
        if i['city'] == "深圳":
            Area = i['Area']
            if Area == "坪山新区":
                Area = Area.replace("新","").strip()
            area_left_salary = i['area_left_salary']
            value.append(area_left_salary)
            attr.append(Area)
    print(value)
    print(attr)
    map = Map("深圳各地区最低薪资均值", width=1200, height=600,background_color='#F4F3EF',)
    map.add("", attr, value, maptype='深圳',  is_label_show=True, is_visualmap=True, visual_range=['0','15'],visual_text_color='#000',visual_range_text= ['0', '15k'])
    page.add(map)
    bar = Bar("深圳各地区最低薪资均值",background_color='#F4F3EF',)
    bar.add("深圳", attr, value, is_stack=True,xaxis_interval=0,xaxis_label_textsize=11,is_datazoom_show=True
            ,xaxis_rotate=30,datazoom_range=[0,50],is_random=True,datazoom_type='both')
    page.add(bar)
    print("深圳各地区最低薪资均值生成完毕！！")
    return page

def salary_hangzhou_map():
    '''
    杭州各地区最低薪资均值
    :return:html
    '''
    print("正在生成杭州各地区最低薪资均值......")
    page = Page()
    s = sel_area_left_salary()
    value = []
    attr = []
    for i in s:
        if i['city'] == "杭州":
            Area = i['Area']
            area_left_salary = i['area_left_salary']
            value.append(area_left_salary)
            attr.append(Area)
    print(value)
    print(attr)
    map = Map("杭州各地区最低薪资均值", width=1200, height=600,background_color='#F4F3EF',)
    map.add("", attr, value, maptype='杭州',  is_label_show=True, is_visualmap=True, visual_range=['0','15'],visual_text_color='#000',visual_range_text= ['0', '15k'])
    page.add(map)
    bar = Bar("杭州各地区最低薪资均值",background_color='#F4F3EF',)
    bar.add("杭州", attr, value, is_stack=True,xaxis_interval=0,xaxis_label_textsize=11,is_datazoom_show=True
            ,xaxis_rotate=30,datazoom_range=[0,50],is_random=True,datazoom_type='both')
    page.add(bar)
    print("杭州各地区最低薪资均值生成完毕！！")
    return page

def salary_guangzhou_map():
    print("正在生成广州各地区最低薪资均值......")
    page = Page()
    s = sel_area_left_salary()
    value = []
    attr = []
    for i in s:
        if i['city'] == "广州":
            Area = i['Area']
            area_left_salary = i['area_left_salary']
            value.append(area_left_salary)
            attr.append(Area)
    print(value)
    print(attr)
    map = Map("广州各地区最低薪资均值", width=1200, height=600,background_color='#F4F3EF',)
    map.add("", attr, value, maptype='广州',  is_label_show=True, is_visualmap=True, visual_range=['0','15'],visual_text_color='#000',visual_range_text= ['0', '15k'])
    page.add(map)
    bar = Bar("广州各地区最低薪资均值",background_color='#F4F3EF',)
    bar.add("广州", attr, value, is_stack=True,xaxis_interval=0,xaxis_label_textsize=11,is_datazoom_show=True
            ,xaxis_rotate=30,datazoom_range=[0,50],is_random=True,datazoom_type='both')
    page.add(bar)
    print("广州各地区最低薪资均值生成完毕！！")
    return page

def salary_nanjing_map():
    print("正在生成南京各地区最低薪资均值......")
    page = Page()
    s = sel_area_left_salary()
    value = []
    attr = []
    for i in s:
        if i['city'] == "南京":
            Area = i['Area']
            area_left_salary = i['area_left_salary']
            value.append(area_left_salary)
            attr.append(Area)
    print(value)
    print(attr)
    map = Map("南京各地区最低薪资均值", width=1200, height=600,background_color='#F4F3EF',)
    map.add("", attr, value, maptype='南京',  is_label_show=True, is_visualmap=True, visual_range=['0','15'],visual_text_color='#000',visual_range_text= ['0', '15k'])
    page.add(map)
    bar = Bar("南京各地区最低薪资均值",background_color='#F4F3EF',)
    bar.add("南京", attr, value, is_stack=True,xaxis_interval=0,xaxis_label_textsize=11,is_datazoom_show=True
            ,xaxis_rotate=30,datazoom_range=[0,50],is_random=True,datazoom_type='both')
    page.add(bar)
    print("南京各地区最低薪资均值生成完毕！！")
    return page

def salary_xian_map():
    print("正在生成西安各地区最低薪资均值......")
    page = Page()
    s = sel_area_left_salary()
    value = []
    attr = []
    for i in s:
        if i['city'] == "西安":
            Area = i['Area']
            area_left_salary = i['area_left_salary']
            value.append(area_left_salary)
            attr.append(Area)
    print(value)
    print(attr)
    map = Map("西安各地区最低薪资均值", width=1200, height=600,background_color='#F4F3EF',)
    map.add("", attr, value, maptype='西安',  is_label_show=True, is_visualmap=True, visual_range=['0','15'],visual_text_color='#000',visual_range_text= ['0', '15k'])
    page.add(map)
    bar = Bar("西安各地区最低薪资均值",background_color='#F4F3EF',)
    bar.add("西安", attr, value, is_stack=True,xaxis_interval=0,xaxis_label_textsize=11,is_datazoom_show=True
            ,xaxis_rotate=30,datazoom_range=[0,50],is_random=True,datazoom_type='both')
    page.add(bar)
    print("西安各地区最低薪资均值生成完毕！！")
    return page
def salary_wuhan_map():
    print("正在生成武汉各地区最低薪资均值......")
    page = Page()
    s = sel_area_left_salary()
    value = []
    attr = []
    for i in s:
        if i['city'] == "武汉":
            Area = i['Area']
            area_left_salary = i['area_left_salary']
            value.append(area_left_salary)
            attr.append(Area)
    print(value)
    print(attr)
    map = Map("武汉各地区最低薪资均值", width=1200, height=600,background_color='#F4F3EF',)
    map.add("", attr, value, maptype='武汉',  is_label_show=True, is_visualmap=True, visual_range=['0','15'],visual_text_color='#000',visual_range_text= ['0', '15k'])
    page.add(map)
    bar = Bar("武汉各地区最低薪资均值",background_color='#F4F3EF',)
    bar.add("武汉", attr, value, is_stack=True,xaxis_interval=0,xaxis_label_textsize=11,is_datazoom_show=True
            ,xaxis_rotate=30,datazoom_range=[0,50],is_random=True,datazoom_type='both')
    page.add(bar)
    print("武汉各地区最低薪资均值生成完毕！！")
    return page


