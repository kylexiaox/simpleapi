#!/usr/bin/env python
# encoding: utf-8

"""
@author: Xiang Xiao
@contact: btxiaox@gmail.com
@site:
@file: DBConfig.py
@time: 30/1/18 01:26
"""

from flask import Flask,request
import urllib2
import logging
import subprocess
import time
import json
from Mysql import Mysql

#log
logging.basicConfig(level=logging.NOTSET,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='records.log'
               # filemode='w'
                    )

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


app = Flask(__name__)
db = Mysql()


@app.route('/r',methods=['POST'])
def record():
    try:
        ip = request.headers['X-Forwarded-For']
        url = 'http://ip.taobao.com/service/getIpInfo.php?ip=%s' % (ip)
        urlobject = urllib2.urlopen(url)
        urlcontent = urlobject.read()
        res = json.loads(urlcontent)
        city = res['data']['city']
        choices = request.form['choices']
        user_type = request.form['user_type']
        user_interest = request.form['user_interest']
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        user_phone = request.form['user_phone']
        channel = request.form['channel']
        logging.info("accept the request with params: ip: "+ip+" choices: "+choices+" user_type :"+user_type+" user_interest :"+user_interest+" user_name :"+user_name+" user_email :"+user_email+" user_phone :"+user_phone+" channel :"+channel)
        # the insert sql
        sql = 'insert into records(ip,choices,user_type,user_interest,user_name,user_email,user_phone,city,channel,insert_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,now())'
        # the insert value tuple
        values = [ip, choices, user_type, user_interest, user_name, user_email, user_phone,city,channel]
        if db.insert_one(sql,values):
            return "{success: true}"
        else:
            return "{success: false}"
    except StandardError, e:
        logging.error(e.args)
        return "{success: false; error_message:"+str(e.args)+"}"


@app.route('/log',methods=['GET'])
def log():
    ip = request.headers['X-Forwarded-For']
    sql = "insert into logs(ip,insert_time) values (%s,now())"
    values = [ip]
    if db.insert_one(sql,values):
        return "{success: true}"
    else:
        return "{success: false}"

@app.route('/pullfromgithub',methods=['POST'])
def pull():
    cmd = subprocess.Popen("git pull", shell=True, cwd='/data/freelancing-ayana/',)
    if cmd.wait() == 0:
        return "{success: true}"
    else:
        return "{success: false}"






if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=23334,
        debug=False,
        threaded=True)
