import pymysql
from datetime import datetime, timedelta
import time


class MyDB:
    def __init__(self, host, user, passwd, db):
        self.conn = pymysql.connect(host, user, passwd, db)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    # 获取当然日期
    def get_cur_date(self):
        date = datetime.today()
        curdate = date.strftime('%Y-%m-%d')
        return curdate

    # 获取前N天的日期
    def get_pren_date(self, n=1):
        predate = datetime.today() + timedelta(-n)
        predate = predate.strftime('%Y-%m-%d')
        return predate
    
    #获取国内疫情概况
    def get_home_realtime_datas(self):
        curdate = self.get_cur_date() # 获取当天的日期
        sql = "select * from home_realtime_datas where updatedTime like '%s'" % (curdate + '%')
        print('+++ sql: %s' % sql)

        results1 = []
        try:
            self.cursor.execute(sql)
            results1 = self.cursor.fetchone()

            n = 1

            while len(results1) <= 0:
                predate = self.get_pren_date(n)
                sql = "select * from home_realtime_datas where updatedTime like '%s'" % (predate + '%')
                print('+++ presql: %s' % sql)

                self.cursor.execute(sql)
                results1 = self.cursor.fetchone()
                n += 1

                if n >= 30:
                    break
                else:
                    time.sleep(1)

        except Exception as e:
            print(e)

        return results1
    #获取国外疫情概况
    def get_outside_realtime_datas(self):
        curdate = self.get_cur_date() # 获取当天的日期
        sql = "select  confirmedCount,currentConfirmedCount,confirmedIncr,curedCount,curedIncr,deadCount,deadIncr from outsidesummary_realtime_datas where updatedTime like '%s'" % (curdate + '%')
        print('+++ sql: %s' % sql)

        results = []
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()

            n = 1

            while len(results) <= 0:
                predate = self.get_pren_date(n)
                sql = "select  confirmedCount,currentConfirmedCount,confirmedIncr,curedCount,curedIncr,deadCount,deadIncr from outsidesummary_realtime_datas where updatedTime like '%s'" % (predate + '%')
                print('+++ presql: %s' % sql)

                self.cursor.execute(sql)
                results = self.cursor.fetchall()
                n += 1

                if n >= 30:
                    break
                else:
                    time.sleep(1)

        except Exception as e:
            print(e)

        return results
    #返回国内每日确诊人数（折线图用
    def get_home_daily_datas(self):
        sql = "select curConfirm,updatedTime from home_realtime_datas"
        print('+++ sql: %s' % sql)

        results1 = []
        results2=[]
        try:
            self.cursor.execute(sql)
            results1 = self.cursor.fetchall()

        except Exception as e:
            print(e)
        for i in results1:
            results2.append((i[0],i[1][5:10]))
        results2=tuple(results2)
        return results2
    # 国内各省份累计确诊病例数柱状图Top15
    def get_province_confirmedCount_top15(self):
        curdate = self.get_cur_date() # 获取当天的日期
        sql = "select  provinceShortName,confirmedCount from province_daily_datas where pub_time like '%s' order by confirmedCount desc limit 15" % (curdate + '%')
        print('+++ sql: %s' % sql)

        results1 = []
        try:
            self.cursor.execute(sql)
            results1 = self.cursor.fetchall()

            n = 1

            while len(results1) <= 0:
                predate = self.get_pren_date(n)
                sql = "select  provinceShortName,confirmedCount from province_daily_datas where pub_time like '%s' order by confirmedCount desc limit 15" % (predate + '%')
                print('+++ presql: %s' % sql)

                self.cursor.execute(sql)
                results1 = self.cursor.fetchall()
                n += 1

                if n >= 30:
                    break
                else:
                    time.sleep(1)

        except Exception as e:
            print(e)

        return results1
       #国内各省份现有确诊病例数(中国地图用No )
    def get_province_currentConfirmedCount(self):
        curdate = self.get_cur_date() # 获取当天的日期
        sql = "select provinceShortName,currentConfirmedCount,pub_time from province_daily_datas where pub_time like '%s' order by currentConfirmedCount" % (curdate + '%')
        print('+++ sql: %s' % sql)

        results1 = []
        try:
            self.cursor.execute(sql)
            results1 = list(self.cursor.fetchall())

            n = 1
            while len(results1) <= 0:
                predate = self.get_pren_date(n)
                sql = "select provinceShortName,currentConfirmedCount,pub_time from province_daily_datas where pub_time like '%s' order by currentConfirmedCount" % (predate + '%')
                print('+++ presql: %s' % sql)

                self.cursor.execute(sql)
                results1 = list(self.cursor.fetchall())
                n += 1

                if n >= 30:
                    break
                else:
                    time.sleep(1)

        except Exception as e:
            print(e)

        return results1
    #国内各省份现有确诊病例数饼图Top5
    def get_province_currentConfirmedCount_top5(self):
        curdate = self.get_cur_date() # 获取当天的日期
        sql = "select provinceShortName,currentConfirmedCount from province_daily_datas where pub_time like '%s' order by currentConfirmedCount desc limit 5" % (curdate + '%')
        print('+++ sql: %s' % sql)

        results1 = []
        try:
            self.cursor.execute(sql)
            results1 = list(self.cursor.fetchall())

            n = 1
            f = False
            while len(results1) <= 0:
                f = True
                predate = self.get_pren_date(n)
                sql = "select provinceShortName,currentConfirmedCount from province_daily_datas where pub_time like '%s' order by currentConfirmedCount desc limit 5" % (predate + '%')
                print('+++ presql: %s' % sql)

                self.cursor.execute(sql)
                results1 = list(self.cursor.fetchall())
                n += 1

                if n >= 30:
                    break
                else:
                    time.sleep(1)
            print(f)
            print(curdate)
            if(f):
                sql = "select curConfirm from home_realtime_datas where updatedTime like '%s';" % (predate + '%')
            else:
                sql = "select curConfirm from home_realtime_datas where updatedTime like '%s';" % (curdate + '%')
            self.cursor.execute(sql)
            results2 = self.cursor.fetchone()
            results1.append(("其他",results2[0]))
        except Exception as e:
            print(e)
        results1=tuple(results1)
        return results1
    #获取省疫情信息
    def get_province_daily_datas(self):
        curdate = self.get_cur_date() # 获取当天的日期
        sql = "select * from province_daily_datas where pub_time like '%s'" % (curdate + '%')
        print('+++ sql: %s' % sql)

        results1 = []
        try:
            self.cursor.execute(sql)
            results1 = self.cursor.fetchall()

            n = 1

            while len(results1) <= 0:
                predate = self.get_pren_date(n)
                sql = "select * from province_daily_datas where pub_time like '%s'" % (predate + '%')
                print('+++ presql: %s' % sql)

                self.cursor.execute(sql)
                results1 = self.cursor.fetchall()
                n += 1

                if n >= 30:
                    break
                else:
                    time.sleep(1)

        except Exception as e:
            print(e)

        return results1





mydb = MyDB('localhost', 'root', 'kfq991122', 'covid19')
results = mydb.get_home_realtime_datas()
print(results)
