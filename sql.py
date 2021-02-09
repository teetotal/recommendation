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

    def insert_result(self, _table, _rows):
        table = _table + "_result"
        self.execute("DROP TABLE IF EXISTS " + table)
        print("Drop Table. " + table)

        create_table = "CREATE TABLE `" + table +"` ("
        create_table += "`user` int(11) NOT NULL, `cluster` int(11) DEFAULT NULL, KEY `idx_user` (`user`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
        self.execute(create_table)
        print("Created Table. " + table)

        sql = "INSERT INTO " + table + " (user, cluster) VALUES "
        rows = ""
        count = 0
        for row in _rows:
            rows += "(" + str(count) + "," + str(row) + ")"
            count += 1

            if count % 500 == 0:
                q = sql + rows
                rows = ""
                self.execute(q)
            else:
                rows += ", "

        if len(rows) > 0:
            q = sql + rows[:-2]
            self.execute(q)
    
    def insert_result_2(self, _table, _rows):
        table = _table
        self.execute("DROP TABLE IF EXISTS " + table)
        print("Drop Table. " + table)

        create_table = "CREATE TABLE `" + table +"` ("
        create_table += "`user` varchar(25) NOT NULL, `cluster` int(11) DEFAULT NULL, KEY `idx_user` (`user`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
        self.execute(create_table)
        print("Created Table. " + table)

        sql = "INSERT INTO " + table + " (user, cluster) VALUES "
        rows = ""
        count = 0
        for row in _rows:
            rows += "('" + str(row[0]) + "', " + str(row[1]) + ")"
            count += 1

            if count % 500 == 0:
                q = sql + rows
                rows = ""
                self.execute(q)
            else:
                rows += ", "

        if len(rows) > 0:
            q = sql + rows[:-2]
            self.execute(q)
    
    def create_pivot(self, table_origin, to, item_count):
        table_name = to
        _item_count = item_count
        _table = table_origin

        self.execute("DROP TABLE IF EXISTS " + table_name)
        print("Drop Table. " + table_name)

        create_table = "CREATE TABLE `" + table_name + "` ("
        create_table += "`user` int(11) unsigned NOT NULL, "
        for i in range(_item_count + 1):
            create_table += "`item" + str(i) + "` float DEFAULT NULL, "
        
        create_table += "`cluster` int(11) DEFAULT NULL, PRIMARY KEY (`user`), KEY `cluster` (`cluster`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

        self.execute(create_table)
        print("Created Table. " + table_name)

        self.execute("insert into " + table_name +"(user, item0) select user, rating from " + _table + " where item = 0;")
        print("Inserted item id = 0")

        for i in range(_item_count + 1):
            if(i == 0):
                continue  
            self.execute("UPDATE " + table_name + " A SET A.item" + str(i) + " = ( SELECT B.rating FROM " + _table + " B WHERE B.user = A.user and B.item=" + str(i) + ");")
            print("Inserted item id = " + str(i))

    def report(self, _table, _table_cluster = None):
        table_name = _table + "_report"
        table_cluster = _table + "_result"

        if _table_cluster != None:
            table_cluster = _table_cluster

        _item_count = self.get_rows("SELECT MAX(item) FROM " + _table)[0][0]
        '''
        self.execute("DROP TABLE IF EXISTS " + table_name)
        print("Drop Table. " + table_name)

        create_table = "CREATE TABLE `" + table_name + "` ("
        create_table += "`user` int(11) unsigned NOT NULL, "
        for i in range(_item_count + 1):
            create_table += "`item" + str(i) + "` float DEFAULT NULL, "
        
        create_table += "`cluster` int(11) DEFAULT NULL, PRIMARY KEY (`user`), KEY `cluster` (`cluster`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

        self.execute(create_table)
        print("Created Table. " + table_name)

        self.execute("insert into " + table_name +"(user, item0) select user, rating from " + _table + " where item = 0;")
        print("Inserted item id = 0")

        for i in range(_item_count + 1):
            if(i == 0):
                continue  
            self.execute("UPDATE " + table_name + " A SET A.item" + str(i) + " = ( SELECT B.rating FROM " + _table + " B WHERE B.user = A.user and B.item=" + str(i) + ");")
            print("Inserted item id = " + str(i))
        '''
        self.create_pivot(_table, table_name, _item_count)
        self.execute("UPDATE " + table_name + " A SET A.cluster = ( SELECT B.cluster FROM " + table_cluster + " B WHERE B.user = A.user);")
        print("Inserted clustering")

        print("-----------------------")
        print("select cluster")
        for i in range(_item_count + 1):
            print(", avg(item" + str(i) + ")")

        print("from " + table_name + " where cluster is not null group by cluster;")

    def get_data_supervised_inference(self, items, table, limit_s = None, limit_cnt = None):
        query = "SELECT user"
        for i in range(items):
            query += ", item" + str(i)
        
        query += " FROM " + table + " ORDER BY user"
        if(limit_s != None and limit_cnt != None):
            query += " LIMIT " + str(limit_s) + ", " + str(limit_cnt)

        rows = self.get_rows(query)
        users = []
        input = []

        for row in rows:
            users.append(row[0])

            inp = []
            for r in row[1:]:
                inp.append(r)
            input.append(inp)

        users = np.array(users)
        input = np.array(input)

        return input, users
        
    def get_data_supervised(self, items, clusters, table):
        query = "SELECT B.user_origin, A.cluster"
        for i in range(items):
            query += ", A.item" + str(i)
        
        query += " FROM " + table + "_report A INNER JOIN " + table + " B ON A.user = B.user AND B.item = 0 ORDER BY A.user"
        rows = self.get_rows(query)
        users = []
        input = []
        output = []
        output_1_dim = []

        for row in rows:
            output_1_dim.append(row[1])

            out = [0] * clusters
            out[row[1]] = 1
            users.append(row[0])
            output.append(out)

            inp = []
            for r in row[2:]:
                inp.append(r)
            input.append(inp)

        users = np.array(users)
        input = np.array(input)
        output = np.array(output)

        return input, output, output_1_dim, users

    def insert_supervised(self, table, certains, uncertains):
        table_certain = table + "_certain"
        table_uncertain = table + "_uncertain"

        if(len(certains) > 0):
            self.execute("CREATE TABLE IF NOT EXISTS " + table_certain + "(`user` int(11) unsigned NOT NULL, `cluster` int(11) DEFAULT NULL, PRIMARY KEY (`user`), KEY `cluster` (`cluster`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
            cnt = 0
            insert = "INSERT INTO " + table_certain + " VALUES"
            rows = ""
            for c in certains:
                rows += "(" + str(c[0]) + ", " + str(c[1]) + "),"
                
                cnt += 1
                if((cnt % 500) == 0 ):
                    self.execute(insert + rows[:-1])
                    rows = ""
                    print("Inserting certain cluster", cnt)

            if(len(rows) > 0):
                self.execute(insert + rows[:-1])
                print("Inserting certain cluster", cnt)

            print("Inserted certain cluster", table_certain)

        if(len(uncertains) > 0):
            create_post = "(`user` int(11) unsigned NOT NULL"
            for n in range(len(uncertains[0][1])):
                create_post += ", `cluster" + str(n) + "` float DEFAULT NULL"

            self.execute("CREATE TABLE IF NOT EXISTS " + table_uncertain + create_post + ", PRIMARY KEY (`user`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
            cnt = 0
            insert = "INSERT INTO " + table_uncertain + " VALUES"
            rows = ""
            for c in uncertains:
                rows += "(" + str(c[0])

                for n in c[1]:
                    rows += ", " + str(n)
                
                rows += "),"

                
                cnt += 1
                if((cnt % 500) == 0 ):
                    self.execute(insert + rows[:-1])
                    print("Inserting uncertain cluster", cnt)
                    rows = ""
            
            if(len(rows) > 0):
                self.execute(insert + rows[:-1])
                print("Inserting uncertain cluster", cnt)
            
            print("Inserted uncertain cluster", table_uncertain)

    def get_column_names(self, table):
        return self.get_rows("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + table + "';")
        