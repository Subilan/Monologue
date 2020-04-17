import pymysql;
import time;
from flask import jsonify

class DBController:
    def getInstance(self):
        return pymysql.connect(
            host = "localhost",
            user = "root",
            password = "subilan1999",
            database = "Monologue",
            charset = "utf8mb4"
        )

    def getLogues(self, data_range = "0,10"):
        db = self.getInstance()
        cur = db.cursor()
        sql = ("SELECT * FROM Logue LIMIT " + data_range)
        try:
            cur.execute(sql)
            db.commit()
            data = cur.fetchall()
        except Exception:
            print(Exception)
            self.connect.rollback()
            return False
        finally:
            db.close()
            cur.close()
        return jsonify(data)

    def writeLogue(self, title, contents):
        db = self.getInstance()
        cur = db.cursor()
        extdate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        date = time.strftime("%Y-%m-%d", time.localtime())
        sql = ("INSERT INTO Logue (title, contents, date, extdate) VALUES ('{t}', '{c}', '{d}', '{ed}')")
        sql = sql.format(t = title, c = contents, d = date, ed = extdate)
        try:
            cur.execute(sql)
            db.commit()
        except Exception:
            print(Exception)
            self.connect.rollback()
            return False
        finally:
            cur.close()
            db.close()
        return True