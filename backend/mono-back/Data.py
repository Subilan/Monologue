from Database import DBController

class DataManager:
    def get(self, component, name):
        fullname = component + "." + name
        funcs = {
            "logue.length": self.getLogueLength
        }
        func = funcs[fullname]
        return func()

    def getLogueLength(self):
        db = DBController()
        cur = db.cursor()
        cur.execute("SELECT COUNT(*) FROM Logue")
        result = cur.fetchone()[0]
        db.close()
        return result