
CREATE TABLE lagouspider.lagou_table(
  jobDivision varchar(50) NOT NULL,		-- 某某公司某某部门
  jobName varchar(50) NOT NULL,			-- Python开发工程师
  jobMoney varchar(30) NOT NULL,		-- 10k-16k
  salary_left varchar(10) NOT NULL,		-- 10
  salary_right varchar(10) NOT NULL,	-- 16
  jobReleaseTime date NOT NULL,			-- 2018-04-02
  jobPlace varchar(30) DEFAULT NULL,	-- 上海
  jobNeed varchar(30) DEFAULT NULL,		-- 经验3-5年
  jobEducation varchar(30) DEFAULT NULL,-- 本科及以上
  jobType varchar(30) DEFAULT NULL,		-- 全职
  jobLabel varchar(100) DEFAULT NULL,	-- 高级 Python 大数据
  jobSpeak varchar(200) DEFAULT NULL,	-- 福利好，五险一金
  city varchar(30) DEFAULT NULL,		-- 上海
  Area varchar(30) DEFAULT NULL,		-- 徐汇区
  address varchar(200) DEFAULT NULL,	-- 某某路xx号
  jobCompany varchar(50) DEFAULT NULL,	-- 某公司
  CompanyUrl varchar(300) DEFAULT NULL,	-- 公司网址
  jobDetailUrl varchar(300) NOT NULL,	-- 本职位网址
  jobClass varchar(50) DEFAULT NULL,	-- 职位分类
  CompanyDomain varchar(50) NOT NULL,	-- 公司领域
  DevelopmentStage varchar(50) NOT NULL,-- 公司融资情况
  PRIMARY KEY (jobDetailUrl)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;