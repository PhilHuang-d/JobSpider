# -*- coding:utf-8 -*-
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from flask import Flask, render_template
from Web.lagou_echarts.test import *
from Web.DateProcessing.form_calculation import *
REMOTE_HOST = "https://pyecharts.github.io/assets/js"
#Flask程序初始化
app = Flask(__name__)
'''
CMD强制关闭服务器
sudo lsof -i:5000
sudo kill "PID"
'''
#app.route修饰器定义路由
@app.route("/")
@app.route("/index")
def city_avg_html():
    url_count = sel_count()
    avg_salary = sel_salary()
    company_count = sel_company()
    three_days_newjob = sel_threeday_newjob()
    city_avg = city_avg_salary()
    return render_template('index.html', myechart=city_avg.render_embed(),host=REMOTE_HOST,
                           script_list=city_avg.get_js_dependencies(),var1 = url_count,var2 = avg_salary,var3=company_count,var4=three_days_newjob)

@app.route("/table")
def company_top100_table_html():
    top100 = tbody_html()
    return render_template('table.html',var1 = top100)

@app.route("/search")
def search_job_html():
    url = "https://www.lagou.com/jobs/list_"
    return render_template('search.html',var1 = url)

@app.route("/jobspeak")
def jobspeak_wordcloud():
    return render_template('jobSpeak.html')

@app.route("/companydomain")
def companydomain_wordcloud():
    return render_template('companydomain.html')

@app.route("/jobClass")
def bigClass_radar_html():
    bigClass_radar_html = big_class_radar()
    return render_template('jobClass.html', myechart=bigClass_radar_html.render_embed(),host=REMOTE_HOST,
                           script_list=bigClass_radar_html.get_js_dependencies())

@app.route("/jishu")
def jishu():
    jishu = small_class_avg_salary("技术")
    return render_template('jobClass.html', myechart=jishu.render_embed(),host=REMOTE_HOST,
                           script_list=jishu.get_js_dependencies())
@app.route("/chanpin")
def chanpin():
    chanpin = small_class_avg_salary("产品")
    return render_template('jobClass.html', myechart=chanpin.render_embed(),host=REMOTE_HOST,
                           script_list=chanpin.get_js_dependencies())
@app.route("/sheji")
def sheji():
    sheji = small_class_avg_salary("设计")
    return render_template('jobClass.html', myechart=sheji.render_embed(),host=REMOTE_HOST,
                           script_list=sheji.get_js_dependencies())
@app.route("/yunying")
def yunying():
    yunying = small_class_avg_salary("运营")
    return render_template('jobClass.html', myechart=yunying.render_embed(),host=REMOTE_HOST,
                           script_list=yunying.get_js_dependencies())
@app.route("/shichang_xiaoshou")
def shichang_xiaoshou():
    shichang_xiaoshou = small_class_avg_salary("市场与销售")
    return render_template('jobClass.html', myechart=shichang_xiaoshou.render_embed(),host=REMOTE_HOST,
                           script_list=shichang_xiaoshou.get_js_dependencies())
@app.route("/zhineng")
def zhineng():
    zhineng = small_class_avg_salary("职能")
    return render_template('jobClass.html', myechart=zhineng.render_embed(),host=REMOTE_HOST,
                           script_list=zhineng.get_js_dependencies())
@app.route("/jinrong")
def jinrong():
    jinrong = small_class_avg_salary("金融")
    return render_template('jobClass.html', myechart=jinrong.render_embed(),host=REMOTE_HOST,
                           script_list=jinrong.get_js_dependencies())

@app.route("/houduankaifa")
def houduankaifa():
    houduankaifa = backend_development_avg_salary()
    return render_template('python.html', myechart=houduankaifa.render_embed(),host=REMOTE_HOST,
                           script_list=houduankaifa.get_js_dependencies())

@app.route("/rengongzhineng")
def rengongzhineng():
    rengongzhineng = Artificial_intelligence_avg_salary()
    return render_template('python.html', myechart=rengongzhineng.render_embed(),host=REMOTE_HOST,
                           script_list=rengongzhineng.get_js_dependencies())

@app.route("/python")
def python_salary_html():
    python_salary = python_salary_count()
    return  render_template('python.html', myechart=python_salary.render_embed(),host=REMOTE_HOST,
                           script_list=python_salary.get_js_dependencies())

@app.route("/salary/shanghai")
def sh_left_salary_html():
    sh = salary_shanghai_map()
    return render_template('city.html', myechart=sh.render_embed(),host=REMOTE_HOST,
                           script_list=sh.get_js_dependencies())

@app.route("/salary/beijing")
def bj_left_salary_html():
    bj = salary_beijing_map()
    return render_template('city.html', myechart=bj.render_embed(),host=REMOTE_HOST,
                           script_list=bj.get_js_dependencies())

@app.route("/salary/chengdu")
def cd_left_salary_html():
    cd = salary_chengdu_map()
    return render_template('city.html', myechart=cd.render_embed(),host=REMOTE_HOST,
                           script_list=cd.get_js_dependencies())

@app.route("/salary/shenzhen")
def sz_left_salary_html():
    sz = salary_shenzhen_map()
    return render_template('city.html', myechart=sz.render_embed(),host=REMOTE_HOST,
                           script_list=sz.get_js_dependencies())

@app.route("/salary/hangzhou")
def hz_left_salary_html():
    hz = salary_hangzhou_map()
    return render_template('city.html', myechart=hz.render_embed(),host=REMOTE_HOST,
                           script_list=hz.get_js_dependencies())

@app.route("/salary/guangzhou")
def gz_left_salary_html():
    gz = salary_guangzhou_map()
    return render_template('city.html', myechart=gz.render_embed(),host=REMOTE_HOST,
                           script_list=gz.get_js_dependencies())

@app.route("/salary/nanjing")
def nj_left_salary_html():
    nz = salary_nanjing_map()
    return render_template('city.html', myechart=nz.render_embed(),host=REMOTE_HOST,
                           script_list=nz.get_js_dependencies())

@app.route("/salary/wuhan")
def wh_left_salary_html():
    wh = salary_wuhan_map()
    return render_template('city.html', myechart=wh.render_embed(),host=REMOTE_HOST,
                           script_list=wh.get_js_dependencies())

@app.route("/salary/xian")
def xa_left_salary_html():
    xa = salary_xian_map()
    return render_template('city.html', myechart=xa.render_embed(),host=REMOTE_HOST,
                           script_list=xa.get_js_dependencies())

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500

#启动服务器
if __name__ == '__main__':
    app.run(debug=True)