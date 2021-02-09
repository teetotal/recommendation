import pymysql
import numpy as np

class sql:
    def __init__(self, config):   
        self.host = config['sql']['host']
        self.user = config['sql']['user']
        self.password = config['sql']['password']
        self.db = config['sql']['db']
    
    def get_conn(self):
        #conn = pymysql.connect(host='APSEO-MYSQL', user='root', password='welcome2ea!!', db='work', charset='utf8')
        conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')
        return conn
        
    def get_rows_cf(self, query):
        conn = self.get_conn()
        curs = conn.cursor()
        print("Loading CF training data ...")
        curs.execute(query)
        rows = curs.fetchall()

        users = []
        items = []
        ratings = []
        for row in rows:
            users.append(float(row[0]))
            items.append(float(row[1]))
            ratings.append(float(row[2]))

            if (len(users) % 100000) == 0:
                print("Loaded CF training data ", len(users))

        conn.close()
        return users, items, ratings

    def get_rows(self, query):
        conn = self.get_conn()
        curs = conn.cursor()
        curs.execute(query)
        rows = curs.fetchall()
        conn.close()
        return rows
    
    def get_rows_with_names(self, query):
        conn = self.get_conn()
        curs = conn.cursor()
        curs.execute(query)
        rows = curs.fetchall()
        names = curs.description
        conn.close()
        return rows, names

    def execute(self, query):
        try:
            conn = self.get_conn()
            curs = conn.cursor()
            curs.execute(query)
            conn.commit()
            conn.close()
        except Exception as ex:
            print(query)
            raise ex

    def get_column_names(self, table):
        return self.get_rows("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + table + "';")
        