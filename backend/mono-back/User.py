from werkzeug.security import check_password_hash, generate_password_hash
from Database import DBController

class UserManager:
    def __init__(self, username):
        self.username = username
        super().__init__()

    def createUser(self, password):
        db = DBController()
        cur = db.cursor()
        args = (self.username, generate_password_hash(password))
        sql = ("INSERT INTO User (username, password) VALUES (%s, %s)")
        cur.execute(sql, args)
        return db.commit(True)

    def exists(self):
        db = DBController()
        cur = db.cursor()
        cur.execute("SELECT * FROM User WHERE username=%s", (self.username));
        result = cur.fetchone()
        return result != None