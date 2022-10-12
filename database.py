import psycopg2
import psycopg2.extras

import configparser

'''
conn      : connection
cur       : cursor
connected : connection status
'''

class Database():
    def __init__(self, **kwargs):

        config = configparser.ConfigParser()
        config.read("config.ini")
        self.config = config["DATABASE"]

        if kwargs.get("pass") != None:kwargs["password"] = kwargs["pass"]
        if kwargs.get("db") != None:kwargs["database"] = kwargs["db"]
        if kwargs.get("username") != None:kwargs["user"] = kwargs["username"]
        self.kwargs = kwargs
        self.connect(**kwargs)

    def connect(self, **kwargs):
        try:
            self.conn = psycopg2.connect(
                host = self.config['host'] if kwargs.get("host") == None else kwargs["host"],
                port = self.config['port'] if kwargs.get("port") == None else kwargs["port"],
                user = self.config['user'] if kwargs.get("user") == None else kwargs["user"],
                password = self.config['pass'] if kwargs.get("password") == None else kwargs["password"],
                database = self.config['db'] if kwargs.get("database") == None else kwargs["database"])
            self.connected = True
            print("Connected!")
        except:
            self.conn = None
            self.connected = False
            print("Not connected")

        if self.conn != None:
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
    
    def reconnect(self):
        if not self.connected:
            try:
                self.connect(**self.kwargs)
            except:
                return -1
            return 1
        else:
            print("Already connected")
        return 0

    def close(self):
        if self.connected:
            try:
                self.conn.close()
                self.connected = False
            except:
                return -1
            return 1
        else:
            print("Already closed")
        return 0

    def execute(self, query, value = None):
        self.cur.execute(query%value)

if __name__ == "__main__":
    # db = Database(host="", port="", db="", user="", pass="")
    db = Database()
    if db.connected:
        db.close()
        db.close()
        print(db.connected)
        db.reconnect()
        print(db.connected)
    else:
        print('a')
