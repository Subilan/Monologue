import pymysql;

class DBController:
    def __init__(self):
        self.instance = pymysql.connect(
            host = "localhost",
            user = "root",
            password = "subilan1999",
            database = "Monologue",
            charset = "utf8mb4"
        )
        super().__init__()
    
    def cursor(self, dict = False):
        if (dict):
            return self.instance.cursor(pymysql.cursors.DictCursor)
        return self.instance.cursor()

    def commit(self):
        self.instance.commit()
        return

    def close(self):
        self.instance.close()
        return

    def rollback(self):
        self.instance.rollback()
        return