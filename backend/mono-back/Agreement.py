from Database import DBController
from Functions import parseMarkdown, getDateString

class AgreementController:
    def __init__(self):
        self.db = DBController()
        pass

    def get(self, id, markdown):
        db = self.db
        cur = db.cursor(True)
        sql = ("SELECT * FROM Agreement WHERE id=%s" % id)
        cur.execute(sql)
        if (db.commit(True)):
            result = cur.fetchone()
            if markdown:
                result["contents"] = parseMarkdown(result["contents"])
            return result
        return False

    def write(self, title, content, disagreement):
        db = self.db
        cur = db.cursor()
        date = getDateString()
        args = (title, content, disagreement, date)
        sql = ("INSERT INTO Agreement (title, contents, disagreement, date) VALUES (%s, %s, %s, %s)")
        cur.execute(sql, args)
        if (db.commit(True)):
            return True
        return False

    def delete(self, id):
        if not id:
            return False
        db = self.db
        cur = db.cursor()
        cur.execute("DELETE FROM Agreement WHERE id=%s", id)
        return db.commit(True)

    def alter(self, id, title, content, disagreement):
        db = self.db
        cur = db.cursor()
        args = (title, content, disagreement, id)
        sql = ("UPDATE Agreement SET title=%s, contents=%s, disagreement=%s WHERE id=%s")
        cur.execute(sql, args)
        return db.commit(True)