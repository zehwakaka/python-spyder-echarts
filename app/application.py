from flask import Flask,render_template,jsonify
from mydb import MyDB


app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html', name='Jerry')

#国内各省份现有确诊病例数饼图Top5
@app.route('/province_top5_curconfirm')
def toget_province_currentConfirmedCount_top5():
    mydb=MyDB('localhost','root','kfq991122','covid19')
    results=mydb.get_province_currentConfirmedCount_top5()#results:list
    return jsonify(privinces=[x[0]for x in results],curConfirms=[x[1]for x in results])


#国内各省份累计确诊病例数柱状图Top15
@app.route('/province_top15_curconfirm')
def toget_province_confirmedCount_top15():
    mydb = MyDB('localhost', 'root', 'kfq991122', 'covid19')
    results = mydb.get_province_confirmedCount_top15()
    return jsonify(privincestop15=[x[0]for x in results],curConfirmstop15=[x[1]for x in results])


#国内国内每日确诊人数（折线图用
@app.route('/home_daily_datas')
def toget_home_daily_datas():
    mydb = MyDB('localhost', 'root', 'kfq991122', 'covid19')
    results = mydb.get_home_daily_datas()
    return jsonify(curConfirm=[x[0]for x in results],time=[x[1]for x in results])

#中国地图
@app.route('/get_province_currentConfirmedCount')
def get_province_currentConfirmedCount():

    mydb = MyDB('localhost', 'root', 'kfq991122', 'covid19')
    results = mydb.get_province_currentConfirmedCount()
    return jsonify(provinceShortName=[x[0] for x in results],currentConfirmedCount=[x[1] for x in results],pub_date=results[0][2])

#省份
@app.route('/get_province_daily_datas')
def get_province_daily_datas():

    mydb = MyDB('localhost', 'root', 'kfq991122', 'covid19')
    results = mydb.get_province_daily_datas()
    return jsonify(provinceName=[x[0] for x in results],provinceShortName=[x[1] for x in results],currentConfirmedCount=[x[2] for x in results],confirmedCount=[x[3] for x in results],suspectedCount=[x[4] for x in results],curedCount=[x[5] for x in results],deadCount=[x[6] for x in results])



# 国内疫情概况表1
@app.route('/get_home_realtime_datas')
def get_home_realtime_datas():

    mydb = MyDB('localhost', 'root', 'kfq991122', 'covid19')
    results = mydb.get_home_realtime_datas()
    return jsonify(curConfirm =[x[0] for x in results] ,curConfirmRelative=[x[1] for x in results],asymptomatic=[x[2] for x in results], asymptomaticRelative=[x[3] for x in results], \
    unconfirmed=[x[4] for x in results], unconfirmedRelative=[x[5] for x in results], icu=[x[6] for x in results], icuRelative=[x[7] for x in results],confirmed=[x[8] for x in results],confirmedRelative=[x[9] for x in results],\
    overseasInput=[x[10] for x in results],overseasInputRelative=[x[11] for x in results],cured=[x[12] for x in results],curedRelative=[x[13] for x in results],died=[x[14] for x in results],diedRelative=[x[15] for x in results])

#国外疫情概况表2
@app.route('/get_outside_realtime_datas')
def get_outside_realtime_datas():

    mydb = MyDB('localhost', 'root', 'kfq991122', 'covid19')
    results = mydb.get_outside_realtime_datas()
    return jsonify(confirmedCount=[x[0] for x in results],currentConfirmedCount=[x[1] for x in results],confirmedIncr=[x[2] for x in results],curedCount=[x[3] for x in results],curedIncr=[x[4] for x in results],deadCount=[x[5] for x in results],deadIncr=[x[6] for x in results])



if __name__ == "__main__":
    app.run()
