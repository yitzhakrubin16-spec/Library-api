import mysql.connector

class DBManager:
    def __init__(self, config = {"host":"localhost",
                                 "port": 3306,
                                 "user": "root",
                                 "password":"secret",
                                 "database":"library_db"}):
        self.config = config

        self._connection = None

    def connect(self):
        if self._connection:
            return self._connection
        
        self._connection = mysql.connector.connect(**self.config)
        
        return self._connection
    
    def disconnect(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None

    def is_connect(self):
        return self._connection and self._connection.is_connected()