from werkzeug.security import generate_password_hash, check_password_hash
from Database import DBController

class AuthManager:
    def __init__(self, username):
        ins = DBController()
        cur = ins.cursor()
        sql = ("SELECT password FROM User WHERE username='{u}'").format(u = username)
        cur.execute(sql)
        self._password = cur.fetchone()[0]
        ins.close()
        pass

    @property
    def password(self):
        return self._password

    def check(self, userpwd):
        return check_password_hash(self.password, userpwd)