#!/usr/bin/env python  
# encoding: utf-8  

""" 
@author: Xiang Xiao
@contact: btxiaox@gmail.com
@site:  
@file: Mysql.py 
@time: 30/1/18 01:27
"""

import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
from DBConfig import Config


class Mysql(object):
    """
        MYSQL database pooled object;
        to get the connection: conn = Mysql.__getConn()
        to release the connection: conn.close()
    """
    __pool = None

    def __init__(self):
        """
        constructor，initial the connection the cursor
        """
        #        self._conn = MySQLdb.connect(host=Config.DBHOST , port=Config.DBPORT , user=Config.DBUSER , passwd=Config.DBPWD ,
        #                              db=Config.DBNAME,use_unicode=False,charset=Config.DBCHAR,cursorclass=DictCursor)
        self._conn = Mysql.__getConn()
        self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn():
        """
        :summary: static methods, get connection from the pool
        :return: MySQLdb.connection
        """
        if Mysql.__pool is None:
            __pool = PooledDB(creator=MySQLdb, mincached=1, maxcached=20,
                              host=Config.DBHOST, port=Config.DBPORT, user=Config.DBUSER, passwd=Config.DBPWD,
                              db=Config.DBNAME, use_unicode=False, charset=Config.DBCHAR, cursorclass=DictCursor)
        return __pool.connection()

    def insert_one(self, sql, values):
        """
        methods for insert one record
        :param sql:
        :param values:
        :return:
        """
        try:
            self._cursor.execute(sql, values)
            self._conn.commit()
            return True
        except StandardError, e:
            raise e
            return False

    def query_all(self, sql, param=None):
        """

         get all data from table
        :param self:
        :param sql:
        :param param: conditionsal query
        :return:            """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = False
        return result,count
