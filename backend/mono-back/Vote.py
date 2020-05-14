from Functions import parseMarkdown, getDateString, getIP
from Database import DBController
import json

class VoteController:
    def create(self, title, desc, items, multiple):
        db = DBController()
        cur = db.cursor()
        date = getDateString()
        data = json.dumps([0 for i in range(len(json.loads(items)))])
        args = (title, desc, date, items, multiple, data)
        sql = ("INSERT INTO Vote (title, description, date, items, multiple, data) VALUES (%s, %s, %s, %s, %s, %s)")
        cur.execute(sql, args)
        return db.commit(True)

    def update(self, data, id):
        db = DBController()
        cur = db.cursor(True)
        cur.execute("SELECT data FROM Vote WHERE id=%s" % id)
        result = json.loads(cur.fetchone()["data"])
        for i in data:
            result[i] += 1
        newData = json.dumps(result)
        args = (newData, id)
        sql = ("UPDATE Vote SET data=%s WHERE id=%s")
        cur.execute(sql, args)
        args = (id, getIP(), getDateString(), data)
        sql = ("INSERT INTO VoteActions (id, ip, actiontime, selection) VALUES (%s, %s, %s, %s)")
        cur.execute(sql, args)
        return db.commit(True)

    def alter(self, title, desc, items, id, multiple):
        db = DBController()
        cur = db.cursor(True)
        cur.execute("SELECT data FROM Vote WHERE id=%s" % id)
        dataString = cur.fetchone()["data"]
        dataBefore = json.loads(dataString)
        dataLength = len(dataBefore)
        itemLength = len(json.loads(items))
        if dataLength == itemLength:
            data = dataString
        elif dataLength > itemLength:
            data = json.dumps([0 for i in range(itemLength)])
        elif dataLength < itemLength:
            dataBefore.extend([0 for i in range(itemLength - dataLength)])
            data = json.dumps(dataBefore)
        args = (title, desc, items, multiple, data, id)
        sql = ("UPDATE Vote SET title=%s, description=%s, items=%s, multiple=%s, data=%s WHERE id=%s")
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
                    data["description"] = parseMarkdown(data["description"])
                return data
        return False

    def duplicated(self, id):
        db = DBController()
        cur = db.cursor(True)
        sql = ("SELECT * FROM VoteActions WHERE id=%s" % id)
        cur.execute(sql)
        if (db.commit(True)):
            data = cur.fetchone()
            compareIP = data["ip"]
            ip = getIP()
            if compareIP == ip:
                return data
        return False