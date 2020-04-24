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
        pass
    
    def cursor(self, dict = False):
        if (dict):
            return self.instance.cursor(pymysql.cursors.DictCursor)
        return self.instance.cursor()

    def commit(self, withclose = False):
        try:
            self.instance.commit()
        except pymysql.Error as e:
            self.instance.rollback()
            return (e.args[0], e.args[1])
        finally:
            if (withclose):
                self.instance.close()
        return True

    def close(self):
        self.instance.close()
        return True

    def rollback(self):
        self.instance.rollback()
        return True