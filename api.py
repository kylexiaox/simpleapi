#coding=utf-8
from flask import Flask,request
import logging
import time
import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB



#日志
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

## database config

class Config(object) :
    DBHOST = 'localhost'
    DBPORT = 3306
    DBUSER = 'root'
    DBPWD = ''
    DBNAME = 'ayana'
    DBCHAR = 'utf8'




app = Flask(__name__)
#app.config.from_object('config')


@app.route('/r',methods=['POST'])
def record():
    try:
        ip = request.remote_addr
        choices = request.form['choices']
        user_type = request.form['user_type']
        user_interest = request.form['user_interest']
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        user_phone = request.form['user_phone']
        logging.info("accept the request with params: ip: "+ip+" choices: "+choices+" user_type :"+user_type+" user_interest :"+user_interest+" user_name :"+user_name+" user_email :"+user_email+" user_phone :"+user_phone)
        db = Mysql()
        db.insert_record(ip,choices,user_type,user_interest,user_name,user_email,user_phone)
        return "{success: true}"

    except StandardError, e:
        logging.error(e.name)
        return "{success: false; error_message:"+e.name+"}"





class Mysql(object):
    """
        MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现
        获取连接对象：conn = Mysql.getConn()
        释放连接对象;conn.close()或del conn
    """
    #连接池对象
    __pool = None
    def __init__(self):
        """
        数据库构造函数，从连接池中取出连接，并生成操作游标
        """
#        self._conn = MySQLdb.connect(host=Config.DBHOST , port=Config.DBPORT , user=Config.DBUSER , passwd=Config.DBPWD ,
#                              db=Config.DBNAME,use_unicode=False,charset=Config.DBCHAR,cursorclass=DictCursor)
        self._conn = Mysql.__getConn()
        self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn():
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        if Mysql.__pool is None:
            __pool = PooledDB(creator=MySQLdb, mincached=1, maxcached=20,
                              host=Config.DBHOST, port=Config.DBPORT, user=Config.DBUSER, passwd=Config.DBPWD,
                              db=Config.DBNAME, use_unicode=False, charset=Config.DBCHAR, cursorclass=DictCursor)
        return __pool.connection()

    def insert_record(self,ip,choices,user_type,user_interest,user_name,user_email,user_phone):
        sql = 'insert into records(ip,choices,user_type,user_interest,user_name,user_email,user_phone,insert_time) values (%s,%s,%s,%s,%s,%s,%s,now())'
        values = [ip,choices,user_type,user_interest,user_name,user_email,user_phone]
        self._cursor.execute(sql,values)
        self._conn.commit()
        return

if __name__ == '__main__':
    app.run(port=23333,debug=True,threaded=True)
