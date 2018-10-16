import pymysql
import pymysql.cursors

import log_handler
from config import MYSQLDATABASES as mq


class MysqlHandler(object):
    """
    处理mysql语句
    """

    def __init__(self):
        self.db = None
        self.cur = None

    def connect_db(self):
        self.db = pymysql.connect(
            host=mq["host"],
            port=mq["port"],
            user=mq["user"],
            passwd=mq["passwd"],
            db=mq["db"],
            charset=mq["charset"],

        )
        self.cur = self.db.cursor(pymysql.cursors.DictCursor)

    def create_sql(self, table, k, v):
        self.connect_db()
        try:
            sql = 'insert into `%s` (%s) values (%s)' % \
                  (table,
                   ','.join(['`%s`' % j for j in k]),
                   ','.join(['%s'] * len(k)))
            self.cur.executemany(sql, v)
            self.db.commit()
            print("%s数据插入成功" % table)
        except Exception:
            self.db.rollback()
            msg = "insert %s sql failed" % "%s"
            return msg
        finally:
            self.close_db()

    def update_sql(self, table, k, v, condition):
        self.connect_db()
        data = ",".join(["%s='%s'" % (k[t], v[t]) for t in range(len(k))])
        sql = "update %s set %s where %s" % (
            table,
            data,
            condition
        )
        try:
            self.cur.execute(sql)
            self.db.commit()
            print("%s数据更新 %s 成功" % (table, condition))
        except Exception:
            self.db.rollback()
            msg = "update %s sql failed" % "%s"
            return msg
        self.close_db()

    def read_table(self, table, condition=None):
        self.connect_db()
        try:
            if table == "api_comicinfo":
                re = "com_id"
            else:
                re = "chap_id"
            sql = "select %s from %s" % (re, table)
            if condition:
                sql = sql + " where %s" % condition
            self.cur.execute(sql)
            data = self.cur.fetchall()
            return data
        except Exception:
            if table == "api_comicinfo":
                log_handler.write_log("%s read com_id failed" % table)
            else:
                log_handler.write_log("%s read chap_id failed" % table)
        finally:
            self.close_db()

    def close_db(self):
        self.cur.close()
        self.db.close()
