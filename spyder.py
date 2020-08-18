import time
import requests
from bs4 import BeautifulSoup
import re
import json
import datetime
import pymysql

def Inside(ds):
    class Province:
        def __init__(self):
            self.provinceName = ''
            self.provinceShortName = ''
            self.currentConfirmedCount = 0 #现有确诊病例数
            self.confirmedCount = 0 #累计确诊
            self.suspectedCount = 0 #疑似病例
            self.curedCount = 0 #累计治愈
            self.deadCount = 0#累计死亡
            self.pub_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#时间
            self.cities = []

        def __str__(self):
            return 'provinceName:%s provinceShortName:%s currentConfirmedCount:%d \
            confirmedCount:%d suspectedCount:%d curedCount:%d deadCount :%d '%(self.provinceName,self.provinceShortName,self.currentConfirmedCount,self.confirmedCount,self.suspectedCount,self.curedCount,self.deadCount)


        def get_info_tuple(self):
            return ((self.provinceName,self.provinceShortName,self.currentConfirmedCount,self.confirmedCount, self.suspectedCount, self.curedCount,self.deadCount,self.pub_time))

    class City:
        def __init__(self):
            self.cityName = ''
            self.currentConfirmedCount = 0
            self.confirmedCount = 0
            self.suspectedCount = 0
            self.curedCount = 0
            self.deadCount = 0
            self.locationId =0
            self.province = ''
            self.pub_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#时间

        def __str__(self):
            return 'cityName:%s, currentConfirmedCount:%d, confirmedCount:%d, suspectedCount:%d,\
            curedCount:%d, deadCount:%d, locationId:%d, pub_time:%s ,province:%s '%(self.cityName, self.currentConfirmedCount, self.confirmedCount, self.suspectedCount, self.curedCount, self.deadCount, self.locationId,self.pub_time,self.province)

        def get_info_tuple(self):
            return ((self.cityName, self.currentConfirmedCount, self.confirmedCount, self.suspectedCount, self.curedCount, self.deadCount, self.locationId,self.province,self.pub_time ))



    class MyDB:
        def __init__(self,host,user,passwd,db):
            self.conn = pymysql.connect(host,user,passwd,db)
            self.cursor = self.conn.cursor()

        def get_province_list_tuple(self,all_province):
            info_tuple = []
            for item in all_province:
                info_tuple.append(item.get_info_tuple())
            return info_tuple

        def get_city_list_tuple(self,all_city):
            info_tuple = []
            for item in all_city:
                info_tuple.append(item.get_info_tuple())
            return info_tuple

        #保存省份数据
        def save_province_datas(self,all_province):

            date1 = datetime.datetime.now().strftime('%Y-%m-%d')
            sql1 = 'delete from province_daily_datas where pub_time like "%s"'%(date1 + '%')
            print(sql1)

            try:
                self.cursor.execute(sql1)
                self.conn.commit()
                print("之前省份删除成功")
            except Exception as a:
                print(a)

            sql = 'insert into province_daily_datas(provinceName,provinceShortName,currentConfirmedCount,confirmedCount,suspectedCount,curedCount,deadCount,pub_time) \
            values(%s,%s,%s,%s,%s,%s,%s,%s)'
            res = self.get_province_list_tuple(all_province)

            print("+++++++   save_province_datas, datas len:%d"%(len(res)))

            try:                     

                self.cursor.executemany(sql,res)
                self.conn.commit()
            except Exception as e:
                print(e)
                print("???")
            print("++++++++++++ save_province_datas is over")


        #保存城市数据
        def save_city_datas(self,all_city):
            date2 = datetime.datetime.now().strftime('%Y-%m-%d')
            sql2 = 'delete from city_daily_datas where pub_time like "%s"'%(date2 + '%')
            try:
                self.cursor.execute(sql2)
                print((date2+"%"))
                self.conn.commit()
                print("之前城市删除成功")
            except Exception as a:
                print(a)
            sql = 'insert into city_daily_datas(cityName,currentConfirmedCount,confirmedCount,suspectedCount,curedCount,deadCount,locationId,province,pub_time) \
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            res = self.get_city_list_tuple(all_city)

            print("+++++++   save_city_daily_datas, datas len:%d"%(len(res)))

            try:
                self.cursor.executemany(sql,res)
                self.conn.commit()
            except Exception as e:
                print(e)
                print("???")
            print("++++++++++++ save_city_daily_datas is over")     

        def __del__(self):
            if self.conn is not None:
                self.conn.close()

    class DataService:
        def __init__(self,ds):
            self.url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'
            self.db = MyDB(host = ds[0],user = ds[1],passwd = ds[2],db = ds[3])

        #抓取网页
        def fetch_html_page(self):
            res = requests.get(self.url)
            res = res.content.decode('utf-8')
            return res

        #解析网页
        def parse_html_page(self,html):
            soup = BeautifulSoup(html,'html.parser')
            tag = soup.find('script',attrs = {'id':'getAreaStat'})
            tagstr = tag.string
            self.results = re.findall('\{"provinceName":.*?"cities":.*?\]\}',tagstr)

        #提取各个省份及其城市数据
        def fetch_province_datas(self):
                all_province = []
                all_city = []
                province_name = ''

                for item in self.results:
                    province = Province()
                    obj = json.loads(item)
                    province.provinceName = obj["provinceName"]
                    #提取省份名，放入city()
                    province_name = province.provinceName

                    province.provinceShortName = obj["provinceShortName"]
                    province.currentConfirmedCount = obj["currentConfirmedCount"]
                    province.confirmedCount = obj["confirmedCount"]
                    province.suspectedCount = obj["suspectedCount"]
                    province.curedCount = obj["curedCount"]
                    province.deadCount = obj["deadCount"]

                    #提取城市数据
                    cities  = obj["cities"]
                    for cityItem in cities:
                #         print(cityItem)
                        city = City()

                        city.province = province_name
                        city.cityName = cityItem["cityName"]
                        city.currentConfirmedCount = cityItem["currentConfirmedCount"]
                        city.confirmedCount = cityItem["confirmedCount"]
                        city.suspectedCount = cityItem["suspectedCount"]
                        city.curedCount = cityItem["curedCount"]
                        city.deadCount = cityItem["deadCount"]
                        city.locationId = cityItem["locationId"]
                        all_city.append(city)
                        province.cities.append(city)
                    all_province.append(province)
                return all_province,all_city

        #业务函数
        def process_data(self):
            html = self.fetch_html_page()
            self.parse_html_page(html)
            all_province,all_city = self.fetch_province_datas()

    #         # 保存省份数据
            self.db.save_province_datas(all_province)
            # 保存城市数据
            self.db.save_city_datas(all_city)

    # 创建Dataservice对象
    ds = DataService(ds)
    ds.process_data()
    
    
    
def Outside(ds):
    class Country:
        def __init__(self):
            self.countryName = ''
            self.currentConfirmedCount = 0 # 现有确诊病例数
            self.confirmedCount = 0 # 累计确诊
            self.confirmedCountRank = 0 # 累计确诊排名
            self.curedCount = 0  # 累计治愈
            self.deadCount = 0 # 累计死亡
            self.deadCountRank = 0 # 累计死亡排名
            self.deadRate = 0.0 # 死亡率
            self.deadRateRank = 0 # 死亡率排名
            self.updatedTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        def get_info_tuple(self):
            return (self.countryName, self.currentConfirmedCount, self.confirmedCount, self.confirmedCountRank, self.curedCount, self.deadCount, self.deadCountRank, self.deadRate, self.deadRateRank,self.updatedTime)
        def __str__(self):
            return 'countryName:%s,currentConfirmedCount:%d,confirmedCount:%d,\
    confirmedCountRankt:%d,curedCount:%d,deadCount:%d,deadCountRank:%d,deadRate:%d,deadRateRank:%d,updatedTime:%s' % (self.countryName, self.currentConfirmedCount, self.confirmedCount, self.confirmedCountRank, self.curedCount, self.deadCount, self.deadCountRank, self.deadRate, self.deadRateRank,self.updatedTime)

    class MyDB:
        def __init__(self, host, user, passwd, db):

            self.conn = pymysql.connect(host, user, passwd, db)
            self.cursor = self.conn.cursor()



        def get_country_list_tuple(self, all_country):
            info_tuple = []
            for item in all_country:
                info_tuple.append(item.get_info_tuple())
            return info_tuple

        # 保存数据
        def save_country_datas(self, all_country):
            date=datetime.datetime.now().strftime('%Y-%m-%d')
            sql='delete from country_daily_datas where pub_time like "%s"'%(date+"%")
            try:
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                print(e)

            sql = 'insert into country_daily_datas(countryName,currentConfirmedCount,\
    confirmedCount,confirmedCountRank,curedCount,deadCount,deadCountRank,deadRate,deadRateRank,pub_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            res = self.get_country_list_tuple(all_country)

            print('+++ save_country_datas, data len: %d' % len(res))
            try:
                self.cursor.executemany(sql, res)
                self.conn.commit()
            except Exception as e:
                print(e)
            print('+++ save_country_datas is over.')
        def show_country_datas(self):
                self.cursor.execute('select * from country_daily_datas')


        def __del__(self):
            if self.conn is not None:
                self.conn.close()


    def forign_data_search(ds):
        db = MyDB(host = ds[0],user = ds[1],passwd = ds[2],db = ds[3])
        res = requests.get('https://ncov.dxy.cn/ncovh5/view/pneumonia')# 爬取页面
        res = res.content.decode('utf-8') # 重新解码
        soup = BeautifulSoup(res, 'html.parser')# 构建soup对象
        tag = soup.find('script', attrs={'id':'getListByCountryTypeService2true'}) # Tag# 使用soup对象查找实时播报新闻标签
        tagStr = tag.string# 获取内容
        results = re.findall('\{"id".*?"showRank".*?\}', tagStr) # length: 34, [str, str, ....]# 使用正则表达式匹配
        all_country = []
        for item in results:
            country=Country() 
            obj = json.loads(item) # obj -> dict
            country.countryName = obj['provinceName']
            country.currentConfirmedCount = int(obj['currentConfirmedCount'])
            country.confirmedCount = int(obj['confirmedCount'])
            country.curedCount = int(obj['curedCount'])
            country.deadCount = int(obj['deadCount'])
            country.deadRate = float(obj['deadRate'])
            country.updatedTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                country.deadCountRank = int(obj['deadCountRank'])
                country.deadRateRank = int(obj['deadRateRank'])
                country.confirmedCountRank = int(obj['confirmedCountRank'])
            except KeyError:
                country.deadCountRank = 0
                country.deadRateRank = 0
                country.confirmedCountRank = 0
            finally:
                all_country.append(country)

        db.save_country_datas(all_country)
        
    forign_data_search(ds)
    
def OutsideSummary(dsin):
    class OutsideSummary:
        def __init__(self):
            self.currentConfirmedCount = 0
            self.confirmedCount = 0
            self.suspectedCount = 0
            self.curedCount = 0
            self.deadCount = 0
            self.suspectedIncr = 0
            self.currentConfirmedIncr = 0
            self.confirmedIncr = 0
            self.curedIncr = 0
            self.deadIncr = 0
            self.updatedTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


        def get_info_tuple(self):
            return (self.currentConfirmedCount, self.confirmedCount, self.suspectedCount, self.curedCount,
                     self.deadCount, self.suspectedIncr, self.currentConfirmedIncr, self.confirmedIncr, self.curedIncr,
                     self.deadIncr, self.updatedTime)


        def __str__(self):
            return 'currentConfirmedCount:%s, confirmedCount:%s, suspectedCount:%s, curedCount:%s, deadCount:%s, suspectedIncr:%s, currentConfirmedIncr:%s, confirmedIncr:%s, curedIncr:%s, deadIncr:%s, updatedTime:%s' % (
            self.currentConfirmedCount, self.confirmedCount, self.suspectedCount, self.curedCount, self.deadCount,
            self.suspectedIncr, self.currentConfirmedIncr, self.confirmedIncr, self.curedIncr, self.deadIncr, self.updatedTime)

    # 数据库实体类

    #数据库实体类
    import pymysql
    class MyDB:
        def __init__(self, host, user, passwd, db):
            self.conn = pymysql.connect(host, user, passwd, db)
            self.cursor = self.conn.cursor()


        def get_outsideSummary_list_tuple(self, outsideSummary):
            info_tuple = []
            info_tuple.append(outsideSummary.get_info_tuple())
            return info_tuple


        # 保存数据
        def save_outsideSummary_datas(self, outsideSummary):
            date=datetime.datetime.now().strftime('%Y-%m-%d')
            print('+++ [MyDB] delete from outsideSummary_realtime_datas') 
            self.cursor.execute('delete from outsidesummary_realtime_datas where updatedTime like "%s"'%(date+'%'))
            self.conn.commit()

            sql = 'insert into outsidesummary_realtime_datas(currentConfirmedCount,confirmedCount,suspectedCount,curedCount,deadCount,suspectedIncr,currentConfirmedIncr,confirmedIncr,curedIncr,deadIncr,updatedTime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            res = self.get_outsideSummary_list_tuple(outsideSummary)
            print('+++ save_outsideSummary_datas, data len: %d' % len(res))
            try:
                self.cursor.executemany(sql, res)
                self.conn.commit()
            except Exception as e:
                print(e)
            print('+++ save_outsideSummary_datas is over.')


        def __del__(self):
            if self.conn is not None:
                self.conn.close()

    # 业务逻辑类

    #业务逻辑类
    import datetime
    import requests
    import re
    from bs4 import BeautifulSoup
    import json



    class DataService:
        def __init__(self,ds):
            self.db = MyDB(host = ds[0],user = ds[1],passwd = ds[2],db = ds[3])


    # 爬取页面
    res = requests.get('https://ncov.dxy.cn/ncovh5/view/pneumonia')

    # 重新解码
    res = res.content.decode('utf-8')

    # 构建soup对象
    soup = BeautifulSoup(res, 'html.parser')

    # 使用soup对象查找国外疫情数据标签
    tag = soup.find('script', attrs={'id': 'getStatisticsService'})

    # 转成字符串
    tagstr = tag.string
    # 使用正则表达式查找所有内容
    result = re.findall('\{"currentConfirmedCount".*?"deadIncr".*?\}', tagstr)

    # 获取国外疫情数据

    obj = json.loads(result[0])



    #print(obj)
    def fetch_outside_summary(obj):
        outsideSummary = OutsideSummary()
        outsideSummary.currentConfirmedCount = int(obj['currentConfirmedCount'])
        outsideSummary.confirmedCount = int(obj['confirmedCount'])
        outsideSummary.suspectedCount = int(obj['suspectedCount'])
        outsideSummary.curedCount = int(obj['curedCount'])
        outsideSummary.deadCount = int(obj['deadCount'])
        outsideSummary.suspectedIncr = int(obj['suspectedIncr'])
        outsideSummary.currentConfirmedIncr = int(obj['currentConfirmedIncr'])
        outsideSummary.confirmedIncr = int(obj['confirmedIncr'])
        outsideSummary.curedIncr = int(obj['curedIncr'])
        outsideSummary.deadIncr = int(obj['deadIncr'])
        outsideSummary.updatedTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return outsideSummary



    # 创建Dataservice对象
    ds = DataService(dsin)
    outsideSummary=fetch_outside_summary(obj)
    ds.db.save_outsideSummary_datas(outsideSummary)
    
def InsideSummary(ds):

    class class_InsideSummary:
        def __init__(self):
            self.curConfirm = 0  # 现有确诊
            self.curConfirmRelative = 0  # 较昨日新增确诊
            self.asymptomatic = 0  # 无症状感染
            self.asymptomaticRelative = 0  # 较昨日新增无症状感染
            self.unconfirmed = 0  # 现有疑似
            self.unconfirmedRelative = 0  # 较昨日疑似新增
            self.icu = 0  # 现有重症
            self.icuRelative = 0  # 较昨日重症病例新增
            self.confirmed = 0  # 累计确诊
            self.confirmedRelative = 0  # 较昨日累计确诊新增
            self.overseasInput = 0  # 累计境外输入
            self.overseasInputRelative = 0  # 较昨日累计境外输入新 增
            self.cured = 0  # 累计治愈
            self.curedRelative = 0  # 较昨日累计治愈新增
            self.died = 0  # 累计死亡
            self.diedRelative = 0  # 较昨日累计死亡新增
            self.updatedTime = 0  # 发布时间

        # 返回元组
        def get_inside_summary_tuple(self):
            return ((self.curConfirm, self.curConfirmRelative, self.asymptomatic, self.asymptomaticRelative, \
                     self.unconfirmed, self.unconfirmedRelative, self.icu, self.icuRelative, self.confirmed, \
                     self.confirmedRelative, self.overseasInput, self.overseasInputRelative, self.cured,
                     self.curedRelative, \
                     self.died, self.diedRelative, self.updatedTime))

        # 输出接口
        def __str__(self):
            return '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (
                self.curConfirm, self.curConfirmRelative, self.asymptomatic, self.asymptomaticRelative,
                self.unconfirmed,
                self.unconfirmedRelative, self.icu, self.icuRelative, self.confirmed, self.confirmedRelative,
                self.overseasInput, self.overseasInputRelative, self.cured, self.curedRelative, self.died,
                self.diedRelative,
                self.updatedTime)


    def get_text():# 爬取国内疫情数据文本
        print(1)
        res = requests.get('https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5')
        res = res.content.decode('utf-8')
        dict = json.loads(res)  # str->dict
        # 规范数据
        for key in dict:
            try:
                dict[key] = dict[key].replace('\\', '')
                key = key.replace('\\', '')
            except:
                pass
        data = json.loads(dict['data'])

        return data




    # 国内疫情数据赋值
    def fetch_inside_summary():
        print(2)

        dataf=get_text()
        insideSummary = class_InsideSummary()
        insideSummary.curConfirm = int(dataf['chinaTotal']['nowConfirm'])
        insideSummary.curConfirmRelative = int(dataf['chinaAdd']['nowConfirm'])
        insideSummary.asymptomatic = int(dataf['chinaTotal']['noInfect'])
        insideSummary.asymptomaticRelative = int(dataf['chinaAdd']['noInfect'])
        insideSummary.unconfirmed = int(dataf['chinaTotal']['suspect'])
        insideSummary.unconfirmedRelative = int(dataf['chinaAdd']['suspect'])
        insideSummary.icu = int(dataf['chinaTotal']['nowSevere'])
        insideSummary.icuRelative = int(dataf['chinaAdd']['nowSevere'])
        insideSummary.confirmed = int(dataf['chinaTotal']['confirm'])
        insideSummary.updatedTime = dataf['lastUpdateTime']
        insideSummary.confirmedRelative = int(dataf['chinaAdd']['confirm'])
        insideSummary.overseasInput = int(dataf['chinaTotal']['importedCase'])
        insideSummary.overseasInputRelative = int(dataf['chinaAdd']['importedCase'])
        insideSummary.cured = int(dataf['chinaTotal']['heal'])
        insideSummary.curedRelative = int(dataf['chinaAdd']['heal'])
        insideSummary.died = int(dataf['chinaTotal']['dead'])
        insideSummary.diedRelative = int(dataf['chinaAdd']['dead'])

        return insideSummary




    # 保存国内疫情概况数据
    def insert(res,ds):
        print(3)
        # 创建连接，并且返回连接对象
        conn = pymysql.connect(host = ds[0],user = ds[1],passwd = ds[2],db = ds[3])
        # 创建游标对象
        cursor = conn.cursor()
        date = data['lastUpdateTime']
        sql = 'delete from home_realtime_datas where updatedTime like "%s"' % (date + '%')
        print('delete old_insidesummary_datas successful')
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print(e)
        sql = 'insert into home_realtime_datas(curConfirm,curConfirmRelative,asymptomatic,asymptomaticRelative,unconfirmed,unconfirmedRelative,icu,icuRelative,confirmed,confirmedRelative,overseasInput,overseasInputRelative,cured,curedRelative,died,diedRelative,updatedTime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql, res)
            conn.commit()
            print("+++ save_insidesummary_datas successful")
            print('+++ save_outsideSummary_datas, data len: %d' % len(res))
        except Exception as e:
            print(e)
            print('+++ save_insidesummary_datas fail.')
        print('+++ save_insidesummary_datas is over.')
        cursor.close()
        conn.close()


########InsideSummary__main__####################
    data = get_text()
    print(9)
    insert(fetch_inside_summary().get_inside_summary_tuple(),ds)
    
ds=['localhost','root','20Z00t10x28_my','covid19']
while(True):
    Inside(ds)
    InsideSummary(ds)
    Outside(ds)
    OutsideSummary(ds)
    time.sleep(3600)