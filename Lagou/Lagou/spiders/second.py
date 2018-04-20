# -*- coding: utf-8 -*-
#模块导入
import scrapy

from Lagou import settings
from Lagou.items import LagouItem
import re
import time
import pymysql
from datetime import datetime,timedelta
'''
启用爬虫：cmd下cd到scrapy项目目录 输入 scrapy crawl lagou 执行
持久化爬虫: scrapy crawl lagou -s JOBDIR=crawls/somespider-1
需要注意的问题:cookie的有效期
'''
class Lagou(scrapy.Spider):
    #name用于区别Spider，该名字必须是唯一的
    name = "lagou"
    #设置allowed_domains的含义是过滤爬取的域名，不在此允许范围内的域名就会被过滤，而不会进行爬取
    allowed_domains = ["lagou.com"]
    #包含了Spider在启动时进行爬取的url列表。 因此，第一个被获取到的页面将是其中之一。 后续的URL则从初始的URL获取到的数据中提取。
    start_urls = [
        "https://www.lagou.com/"
    ]
    #抓取页数设置，最多为30
    page = 10
    #抓取站点设置，访问settings.py中的城市大写中文名 例如：北京 为 BEIJING
    cookie_city = settings.BEIJING

    cookie = {
            'user_trace_token': '20180312140840-cfc26979-25bb-11e8-b1dd-5254005c3644',
            'LGUID': '20180312140840-cfc26c37-25bb-11e8-b1dd-5254005c3644',
            'index_location_city': cookie_city,
            'JSESSIONID': 'ABAAABAAAGFABEFB1AA3ABA9AC15D5A640EDD50973A4F1B',
            'TG-TRACK-CODE': 'index_navigation',
            'X_HTTP_TOKEN': '2b18a1425cc13ec095c9efd2830483f4',
            'SEARCH_ID': '4793ecb31d2d49539c23e753e058fded',
            '_gat': '1',
            'hideSliderBanner20180305WithTopBannerC' : '1',
            'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1520834921',
            'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1520848909',
            '_gid': 'GA1.2.1848965186.1520834921',
            '_ga': 'GA1.2.141357079.1520834921',
            'LGSID': '20180312140840-cfc26ab1-25bb-11e8-b1dd-5254005c3644',
            'PRE_UTM': '',
            'PRE_HOST': 'www.baidu.com',
            'PRE_SITE': 'https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D7awz0WxWjKxQwJ9xplXysE6LwOiAde1dreMKkGLhWzS%26wd%3D%26eqid%3D806a75ed0001a451000000035a128181',
            'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2F',
            'LGRID': '20180312180149-6153f297-25dc-11e8-b1dd-5254005c3644'
    }

    def parse(self , response):
        '''
        从起始url抓取类目
        parse()是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。 该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象。
        :param response: 起始页面html，从起始页面中的每个类目url中抓取类目url
        :return: 回调函数：遍历每个类目url的页码，生成所有类目的所有页码的request传入parse_url方法
        '''
        for item in response.xpath('//div[@class="menu_box"]/div/dl/dd/a'):
            #使用xpath表达式，提取每个类目的url与类目
            jobClass = item.xpath('text()').extract()[0]  #extract()把selector对象转化为list,然后取list中的第一个string
            jobUrl = item.xpath("@href").extract_first()  #extract_first()把selector对象转化为string
            oneItem = LagouItem()                         #继承items.py中的LagouItem()
            oneItem["jobClass"] = jobClass                #继承jobClass
            oneItem["jobUrl"] = jobUrl                    #继承jobUrl
            #每个类目下最多有30页，生成每个类目的不同页码的url，用于下一步的requests
            for i in range(self.page):
                jobUrl2 = jobUrl + str(i+1)
                try:
                    yield scrapy.Request(url=jobUrl2, cookies=self.cookie, meta = {'oneItem':oneItem},callback=self.parse_url)
                except:
                    pass

    def parse_url(self, response):
        '''
        从parse()中返回的url中抓取各个类目所有页码的页面下的招聘url
        :param response:
        :return: 回调函数：遍历每个类目招聘url下的每个招聘信息，生成的jobDetailUrl传入parse_Details()方法
        '''
        for sel2 in response.xpath('//ul[@class="item_con_list"]/li'):
            #xpath表达式，提取每个response中的职位详情url，职位发布时间
            jobDetailUrl = sel2.xpath('div[1]/div[1]/div[1]/a/@href').extract_first()
            jobReleaseTime = sel2.xpath('div[1]/div[1]/div[1]/span/text()').extract()[0]
            urlItem = LagouItem()                        #继承items.py中的LagouItem()
            urlItem["jobDetailUrl"] = jobDetailUrl       #职位详情的url
            urlItem["jobReleaseTime"] =  jobReleaseTime  #工作发布时间
            urlItem["jobClass"] = response.meta['oneItem']['jobClass']
            '''
            url去重:每个职位信息的jobDetailUrl是唯一的
            使用url_check()方法，将抓到的jobDetailUrl通过sql语句在数据库中检查。
            如果存在此url，返回True, pass，不进行下一步请求；
            如果不存在此url，返回False, 则yield scrapy.Request
            '''
            # try:                           #不启用url去重
            #     yield scrapy.Request(url=jobDetailUrl, cookies=self.cookie, meta={'urlItem': urlItem},
            #                          callback=self.parse_Details)
            # except:
            #     pass
            code = url_check(jobDetailUrl)   #启用url去重
            if code == False:
                print("不存在本职位,continue!")
                try:
                    yield scrapy.Request(url=jobDetailUrl, cookies=self.cookie, meta = {'urlItem': urlItem},callback=self.parse_Details)
                except:
                    pass
            else:
                print("已存在本职位,pass!")
                return

    def parse_Details(self, response):
        '''
        从职位详情页面抓取需要的数据
        :param response:
        :return: Item
        '''
        for detail in response.xpath('/html/body'):
            #//*[@id="job_detail"]
            #通过scrapy.selector的xpath,css表达式提取各个数据
            jobDivision = detail.css('.job-name .company::text').extract_first() # 公司名字+部门
            jobName = detail.css('.job-name span::text').extract()[0]        # 职位名称
            jobMoney = detail.css(".job_request .salary ::text").extract()[0]               # 薪资
            pattern_salary = re.compile(r'\d+')                                             # 正则匹配数字
            salary_left = pattern_salary.findall(jobMoney)[0]                               # 薪资范围下限
            salary_right = pattern_salary.findall(jobMoney)[1]                              # 薪资范围上限
            jobReleaseTime = response.meta['urlItem']['jobReleaseTime']                     # 发布时间
            jobReleaseTime = transport_time(jobReleaseTime)                                 # 转化为yyyy-mm-dd
            jobPlace = detail.xpath('div[2]/div/div[1]/dd/p[1]/span[2]/text()').extract()[0]# 城市地点
            jobPlace = replace_splash(jobPlace)                                             # 移除 /
            jobNeed = detail.xpath('div[2]/div/div[1]/dd/p[1]/span[3]/text()').extract()[0] # 经验不限
            jobNeed = replace_splash(jobNeed)                                               # 移除 /
            jobEducation = detail.xpath('div[2]/div/div[1]/dd/p[1]/span[4]/text()').extract()[0]  # 本科及以上
            jobEducation = replace_splash(jobEducation)                                     # 移除 /
            jobType = detail.xpath('div[2]/div/div[1]/dd/p[1]/span[5]/text()').extract()[0] # 全职/兼职
            jobLabel = detail.css('.position-label li::text').extract()[0]                  # 职位标签
            jobSpeak = detail.xpath('//*[@id="job_detail"]/dd[1]/p/text()').extract()[0]    # 职位诱惑
            city = detail.xpath('//*[@id="job_detail"]/dd[3]/div[1]/a[1]/text()').extract_first() #上海
            Area = detail.xpath('//*[@id="job_detail"]/dd[3]/div[1]/a[2]/text()').extract_first() #浦东新区
            address = detail.xpath('//*[@id="job_detail"]/dd[3]/div[1]/text()').extract()   # 地址
            address = address[3]                                                            # 取list中的第三个
            address = replace_spalsh2(address)                                              # 移除地址中的 ' - '
            jobCompany = detail.css('.job_company img::attr(alt)').extract()[0]             # 公司名称
            CompanyUrl = detail.css('.job_company a::attr(href)').extract()[0]              # 公司地址
            CompanyDomain = detail.xpath('//*[@id="job_company"]/dd/ul/li[1]/text()').extract()[1]    # 公司领域
            DevelopmentStage = detail.xpath('//*[@id="job_company"]/dd/ul/li[2]/text()').extract()[1] # 融资情况
            # 继承items.py中的LagouItem()
            Item = LagouItem()
            Item["jobDivision"] = jobDivision
            Item["jobName"] = jobName
            Item["jobMoney"] = jobMoney
            Item["salary_left"] = salary_left
            Item["salary_right"] = salary_right
            Item["jobReleaseTime"] = jobReleaseTime
            Item["jobPlace"] = jobPlace
            Item["jobNeed"] = jobNeed
            Item["jobEducation"] = jobEducation
            Item["jobType"] = jobType
            Item["jobLabel"] = jobLabel
            Item["jobSpeak"] = jobSpeak
            Item["city"] = city
            Item["Area"] = Area
            Item["address"] = address
            Item["jobCompany"] = jobCompany
            Item["CompanyUrl"] = CompanyUrl
            Item["jobDetailUrl"] = response.meta['urlItem']['jobDetailUrl']
            Item["jobClass"] = response.meta['urlItem']['jobClass']
            Item["CompanyDomain"] = CompanyDomain
            Item["DevelopmentStage"] = DevelopmentStage
            print(Item)
            return Item

'''
数据处理方法
'''
# 移除'/广州 / 经验3-5年 / 本科及以上 /'中的/
def replace_splash(value):
    return value.replace("/", "").strip()

# 移除地址中的 ' - '
def replace_spalsh2(value):
    return value.replace("-","").strip()

# 日期转换 将"1天前发布 ／ 2018-03-20  ／ 12：00 发布" 转化成yyyy-mm-dd的格式
def transport_time(word):
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    result = re.search(r'\d+',word).group(0)
    d = datetime.now()
    new_date = d - timedelta(days=int(result))
    new_date = new_date.strftime('%Y-%m-%d')
    if re.search(r'[\：|\:]',word):
        return today
    elif re.search(r'\-',word):
        return word
    else:
        return new_date

# MYSQL  url去重

def url_check(url):
    config = {
        'host': settings.MYSQL_HOST,
        'port': settings.MYSQL_PORT,
        'user': settings.MYSQL_USER,
        'passwd': settings.MYSQL_PWD,
        'db': settings.MYSQL_DB,
        'charset': settings.MYSQL_CHARSET
    }
    db = pymysql.connect(**config)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    print("正在检查url:%s" % url)
    try:
        # 执行SQL语句 查询此
        cursor.execute('''
        select jobDetailUrl
        from lagou_table
        where jobDetailUrl = "%s"
        ''' % url)
        # 获取所有记录列表
        results = cursor.fetchall()
        if results:
            #如果此url已经在数据库中，返回的是此url，则终止下一步抓取
            print("True,break!")
            db.close()
            return True
        else:
            #如果此url不在数据库中，返回的是(),则进行下一步抓取
            print("False,url is crawling!")
            db.close()
            return False
    except:
        print("Error: unable to fecth data")
        db.close()


