# -*- coding: utf-8 -*-
"""
Created on Sat Jul 01 11:04:30 2017

@author: lenovo
"""
import requests
from bs4 import BeautifulSoup
import re
import MySQLdb

#reload(sys)
#sys.setdefaultencoding('utf-8')
conn=MySQLdb.connect(host='localhost',user='root',passwd='bbac2015',db='stocks'
                     ,port=3306,charset='utf8')
cur=conn.cursor()

def main():
    cur.execute("Create TABLE IF not EXISTS stocklist(\
    id char(6) UNIQUE,\
    name char(16) ,\
    amount_10000 int(11),\
    stock_link char(255),\
    xjllb_ncols int(11),\
    xjllb_data text,\
    zcfzb_ncols int(11),\
    zcfzb_data text,\
    lrb_ncols int(11),\
    lrb_data text)")
    conn.commit()
    cur.execute('truncate stocklist')
    conn.commit()
    url=("http://quote.eastmoney.com/stocklist.html")
    r = requests.get(url)
    #rc=r.raise_for_status()
    r.encoding='gbk'
    soup=BeautifulSoup(r.text,'html.parser')
    rr=soup.find_all("a",href=re.compile("http://quote.eastmoney.com/[s][hz]\d{6}.html"))
    for i in range(len(rr)):
        name_number=rr[i].string
        number=name_number[-7:-1]
        name=name_number[:-8]
        value=[number,name,0,'',0,'',0,'',0,'']
        print value
        cur.execute('insert into stocklist values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',value)
    conn.commit()
    cur.close()
    conn.close()
main()


