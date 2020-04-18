from werkzeug.security import check_password_hash, generate_password_hash
from Database import DBController

class UserManager:

    def createUser(self, username, password):
        db = DBController()
        cur = db.cursor()
        sql = ("INSERT INTO User (username, password) VALUES ('{u}', '{p}')")
        sql = sql.format(u = username, p = generate_password_hash(password))
        try:
            cur.execute(sql)
            db.commit()
        except Exception:
            db.rollback()
            return False
        finally:
            db.close()
        return True