from Functions import parseMarkdown, getDateString
from Database import DBController

class VoteController:
    def create(self, title, desc, items, multiple):
        db = DBController()
        cur = db.cursor()
        date = getDateString()
        args = (title, desc, date, items, multiple)
        sql = ("INSERT INTO Vote (title, description, date, items, multiple) VALUES (%s, %s, %s, %s, %s)")
        cur.execute(sql, args)
        return db.commit(True)

    def update(self, data, id):
        db = DBController()
        cur = db.cursor()
        args = (data, id)
        sql = ("UPDATE Vote SET data=%s WHERE id=%s")
        cur.execute(sql, args)
        return db.commit(True)

    def alter(self, title, desc, items, id, multiple):
        db = DBController()
        cur = db.cursor()
        args = (title, desc, items, multiple, id)
        sql = ("UPDATE Vote SET title=%s, description=%s, items=%s, multiple=%s WHERE id=%s")
        cur.execute(sql, args)
        return db.commit(True)
    
    def delete(self, id):
        if not id:
            return False
        db = DBController()
        cur = db.cursor()
        sql = ("DELETE FROM Vote WHERE id=%s" % id)
        cur.execute(sql)
        return db.commit(True)

    def get(self, id, markdown):
        if not id:
            return False
        db = DBController()
        cur = db.cursor(True)
        sql = ("SELECT * FROM Vote WHERE id=%s" % id)
        cur.execute(sql)
        if (db.commit(True)):
            data = cur.fetchone()
            if (data != None):
                if (markdown):
                    data["desc"] = parseMarkdown(data["desc"])
                return data
        return False