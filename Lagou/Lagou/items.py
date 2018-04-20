# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy

'''
Item 是保存爬取到的数据的容器,Spider将会将爬取到的数据以 Item 对象返回。
'''
class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    '''
    Field 仅仅是内置的 dict 类的一个别名，并没有提供额外的方法或者属性。换句话说， Field 对象完完全全就是Python字典(dict)。被用来基于类属性(class attribute)的方法来支持 item声明语法 。
    '''
    jobClass = scrapy.Field()
    jobUrl = scrapy.Field()
    jobName = scrapy.Field()
    jobPlace = scrapy.Field()
    jobMoney = scrapy.Field()
    salary_left = scrapy.Field()
    salary_right = scrapy.Field()
    jobReleaseTime = scrapy.Field()
    jobNeed = scrapy.Field()
    jobEducation = scrapy.Field()
    jobDivision = scrapy.Field()
    jobType = scrapy.Field()
    jobSpeak = scrapy.Field()
    jobDetailUrl = scrapy.Field()
    jobLabel = scrapy.Field()
    city = scrapy.Field()
    Area = scrapy.Field()
    address = scrapy.Field()
    jobCompany = scrapy.Field()
    CompanyUrl = scrapy.Field()
    CompanyDomain = scrapy.Field()
    DevelopmentStage = scrapy.Field()
    # 重写get_insert_sql方法，该方法会在MyTwistedPipeline中调用，执行存储操作
    def get_insert_sql(self):
        #sql插入语句 jobDetailsUrl去重 如果已经存在此字段，则不插入数据库
        insert_sql = """
                insert into lagouspider.lagou_table(jobDivision,jobName,jobMoney,salary_left,salary_right,jobReleaseTime,jobPlace,jobNeed,jobEducation,jobType,jobLabel,jobSpeak,city,Area,address,jobCompany,CompanyUrl,jobDetailUrl
,jobClass,CompanyDomain,DevelopmentStage) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
ON DUPLICATE KEY UPDATE jobDetailUrl=VALUES(jobDetailUrl)
            """
        #将此类下的值传入params
        params = (
            self['jobDivision'], self['jobName'], self['jobMoney'],
            self['salary_left'],self['salary_right'],self['jobReleaseTime'],self['jobPlace'],
            self['jobNeed'],self['jobEducation'], self['jobType'], self['jobLabel'],
            self['jobSpeak'],self['city'], self['Area'], self['address'], self['jobCompany'],
            self['CompanyUrl'], self['jobDetailUrl'],self['jobClass'],self['CompanyDomain'],
            self['DevelopmentStage']
        )
        return insert_sql, params








