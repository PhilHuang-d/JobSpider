'''

/*
Navicat MySQL Data Transfer
Source Server         : scrapystudy
Source Server Version : 50718
Source Host           : localhost:3306
Source Database       : lagouspider
Target Server Type    : MYSQL
Target Server Version : 50718
File Encoding         : 65001

*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for lagou_table
-- ----------------------------
drop table lagouspider.lagou_table_test_bf;
CREATE TABLE lagouspider.lagou_table(
  jobDivision varchar(50) NOT NULL,
  jobName varchar(50) NOT NULL,
  jobMoney varchar(30) NOT NULL,
  salary_left varchar(10) NOT NULL,
  salary_right varchar(10) NOT NULL,
  jobReleaseTime date NOT NULL,
  jobPlace varchar(30) DEFAULT NULL,
  jobNeed varchar(30) DEFAULT NULL,
  jobEducation varchar(30) DEFAULT NULL,
  jobType varchar(30) DEFAULT NULL,
  jobLabel varchar(100) DEFAULT NULL,
  jobSpeak varchar(200) DEFAULT NULL,
  city varchar(30) DEFAULT NULL,
  Area varchar(30) DEFAULT NULL,
  address varchar(200) DEFAULT NULL,
  jobCompany varchar(50) DEFAULT NULL,
  CompanyUrl varchar(300) DEFAULT NULL,
  jobDetailUrl varchar(300) NOT NULL,
  jobClass varchar(50) DEFAULT NULL,
  CompanyDomain varchar(50) NOT NULL,
  DevelopmentStage varchar(50) NOT NULL,
  PRIMARY KEY (jobDetailUrl)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

'''

'''
cookie = {
            'user_trace_token': '20180312140840-cfc26979-25bb-11e8-b1dd-5254005c3644',
            'LGUID': '20180312140840-cfc26c37-25bb-11e8-b1dd-5254005c3644',
            'index_location_city': '%E5%85%A8%E5%9B%BD',
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
'''

'''
            #//*[@id="job_detail"]
            #通过scrapy.selector的xpath,css表达式提取各个数据
            jobDivision = detail.css('.job-name .company::text').extract_first() # 公司名字+部门
            #'/html/body/div[2]/div/div[1]/div/div[1]'
            jobName = detail.css('.job-name span::text').extract()[0]        # 职位名称
            #'/html/body/div[2]/div/div[1]/div/span'
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
            city = detail.xpath('//*[@id="job_detail"]/dd[3]/div[1]/a[1]/text()').extract()[0] #上海
            Area = detail.xpath('//*[@id="job_detail"]/dd[3]/div[1]/a[2]/text()').extract()[0] #浦东新区
            address = detail.xpath('//*[@id="job_detail"]/dd[3]/div[1]/text()').extract()   # 地址
            address = address[3]                                                            # 取list中的第三个
            address = replace_spalsh2(address)                                              # 移除地址中的 ' - '
            jobCompany = detail.css('.job_company img::attr(alt)').extract()[0]             # 公司名称
            CompanyUrl = detail.css('.job_company a::attr(href)').extract()[0]              # 公司地址
            CompanyDomain = detail.xpath('//*[@id="job_company"]/dd/ul/li[1]/text()').extract()[1]    # 公司领域
            DevelopmentStage = detail.xpath('//*[@id="job_company"]/dd/ul/li[2]/text()').extract()[1] # 融资情况

'''