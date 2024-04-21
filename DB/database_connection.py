import mysql.connector 

class DatabaseConnection:
    def __init__(self):
        self.MYSQL_HOST = 'localhost'
        self.MYSQL_USER = 'root'
        self.MYSQL_PASSWORD = 'ahojahoj'
        self.MYSQL_DB = 'omegadbdva'

    def connect(self):
        connection = mysql.connector.connect(
            host=self.MYSQL_HOST,
            user=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            database=self.MYSQL_DB
        )
        return connection
