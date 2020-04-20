from Database import DBController
import time
import markdown

class LogueController:
    def get(self, arg, typ):
        funcs = {
            "id": self.getByID,
            "limit": self.getByLimit
        }
        self.arg = arg
        func = funcs[typ]
        return func()

    def getByLimit(self):
        arg = self.arg
        db = DBController()
        cur = db.cursor(True)
        sql = ("SELECT * FROM Logue LIMIT " + arg)
        cur.execute(sql)
        if (db.commit(True)):
            data = cur.fetchall()
            for i in range(len(data)):
                data[i]["contents"] = markdown.markdown(data[i]["contents"])
            return data
        return False
    
    def getByID(self):
        arg = self.arg
        db = DBController()
        cur = db.cursor(True)
        sql = ("SELECT * FROM Logue WHERE id=%s")
        cur.execute(sql, (arg))
        if (db.commit(True)):
            data = cur.fetchone()
            data["contents"] = markdown.markdown(data["contents"])
            return data
        return False

    def write(self, title, contents, typ):
        db = DBController()
        cur = db.cursor(True)
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        args = (title, contents, typ, date)
        sql = ("INSERT INTO Logue (title, contents, type, date) VALUES (%s, %s, %s, %s)");
        cur.execute(sql, args)
        return db.commit(True)

    def alter(self, id, title, contents, typ):
        db = DBController()
        cur = db.cursor()
        args = (title, contents, typ)
        sql = ("UPDATE Logue SET title=%s, contents=%s, type=%s")
        cur.execute(sql, args)
        return db.commit(True)