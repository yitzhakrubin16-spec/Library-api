import mysql.connector

class DBManager:
    def __init__(self, config: dict = {"host":"localhost",
                                 "port": 3306,
                                 "user": "root",
                                 "password":"secret",
                                 "database":"library_db"}):
        self.config = config

        self._connection = None

    def get_connection(self):
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
    
    def create_tables(self):
        connection = self.get_connection()
        self.cursor = connection.cursor(dictionary=True)
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS books 
                            (id INT AUTO_INCREMENT PRIMARY KEY,
                            title VARCHAR(50) NOT NULL,
                            author VARCHAR(50) NOT NULL,
                            genre ENUM('Fiction','Non-Fiction','Science','History','Other') NOT NULL,
                            is_available BOOL NOT NULL DEFAULT TRUE,
                            borrowed_by_member_id INT DEFAULT NULL);""")
                                                
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS members 
                            (id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(50) NOT NULL,
                            email VARCHAR(255) UNIQUE NOT NULL,
                            is_active BOOL NOT NULL DEFAULT TRUE,
                            total_borrows INT NOT NULL DEFAULT 0);""")
                            
        connection.commit()
        self.cursor.close()
        return