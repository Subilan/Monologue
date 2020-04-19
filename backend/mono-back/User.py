from werkzeug.security import check_password_hash, generate_password_hash
from Database import DBController

class UserManager:

    def createUser(self, username, password):
        db = DBController()
        cur = db.cursor()
        args = (username, generate_password_hash(password))
        sql = ("INSERT INTO User (username, password) VALUES (%s, %s)")
        cur.execute(sql, args)
        return db.commit(True)