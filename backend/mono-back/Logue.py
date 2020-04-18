from Database import DBController
import time

class LogueController:
    def get(self, data_range = "0,10"):
        db = DBController()
        cur = db.cursor(True)
        sql = ("SELECT * FROM Logue LIMIT " + data_range)
        try:
            cur.execute(sql)
            db.commit()
            data = cur.fetchall()
        except Exception:
            print(Exception)
            db.rollback()
            return False
        finally:
            db.close()
        return data

    def write(self, title, contents, typ):
        db = DBController()
        cur = db.cursor(True)
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        args = (title, contents, typ, date)
        sql = ("INSERT INTO Logue (title, contents, type, date) VALUES ('%s', '%s', '%s', '%s')");
        try:
            cur.execute(sql, args)
            db.commit()
        except Exception:
            print(Exception)
            db.rollback()
            return False
        finally:
            db.close()
        return True