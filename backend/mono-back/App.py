from flask import Flask, jsonify, make_response, request, session, escape
from flask_restful import Api, Resource
from flask_cors import CORS
from werkzeug.exceptions import abort
from datetime import timedelta
from Database import DBController
from Auth import AuthManager
from User import UserManager
from Logue import LogueController
from Data import DataManager
from Vote import VoteController

app = Flask(__name__)
api = Api(app)
CORS(app)
app.secret_key = "jkshbfawugfagr78f3q4r7rq4tfg4g23o7yr39o563498fi387ty8ygr7tdwsacghjsdvbdxzvesfdiolhg;waprurq2;3p[u5r0piq82r90831-=8410184-32857[q2385-u20pfqyu-34t8q[urgfvq3-['ig3='rgiqre-'ugu='rug0wer8a0w78d8g9s7gu934yu930y5ihi3h4ihihegj'egisdahfhsiahfhhufewfwtr7wfgharege"
app.permanent_session_lifetime = timedelta(days = 7)

class DataAPI(Resource):
    def get(self):
        component = request.args.get("comp")
        name = request.args.get("name")
        if not component or not name:
            abort(404)
        data = DataManager()
        result = data.get(component, name)
        if not result:
            abort(404)
        return result

class LogueAPI(Resource):
    def get(self):
        method = request.args.get("method")
        markdown = request.args.get("markdown")
        if not method or method not in ["limit", "id"]:
            abort(404)
        if not markdown or markdown == 'true':
            markdown = True
        else:
            markdown = False
        arg = request.args.get(method)
        if not arg:
            abort(404)
        logue = LogueController()
        result = logue.get(arg, method, markdown)
        return result

    def post(self):
        if ("username" in session):
            self.logue = LogueController()
            json = request.get_json(force = True)
            self.json = json
            funcs = {
                "submit": self.submit,
                "alter": self.alter,
                "delete": self.delete
            }
            return funcs[json["method"]]()
        return False

    def submit(self):
        return self.logue.write(self.json.get("title"), self.json.get("contents"), self.json.get("type"))

    def alter(self):
        return self.logue.alter(self.json.get("id"), self.json.get("title"), self.json.get("contents"), self.json.get("type"))

    def delete(self):
        return self.logue.delete(self.json.get("id"))

class AuthAPI(Resource):
    def login(self):
        json = self.json
        user = UserManager(json["username"])
        if (user.exists()):
            auth = AuthManager(json["username"])
            if (auth.check(json["password"])):
                session["username"] = json["username"]
                session.permanent = True
                return True
        return False
        
    def logout(self):
        json = self.json
        if "username" in session:
            session.pop('username', None)
            return True
        return False

    def auth(self):
        if "username" in session:
            return True
        return False

    def post(self):
        json = request.get_json(force = True)
        self.json = json
        funcs = {
            "login": self.login,
            "logout": self.logout,
            "auth": self.auth
        }
        return funcs[json["method"]]()
"""
class AgreementAPI(Resource):
    def get(self):
        id = request.args.get("id")
        markdown = request.args.get("markdown")
        if not id:
            abort(404)
        if not markdown or markdown != "true":
            markdown = False
        else:
            markdown = True
        agr = AgreementController()
        result = agr.get(id, markdown)
        if result:
            return result
        return False
    
    def post(self):
        if "username" in session:
            self.agr = AgreementController()
            json = request.get_json(force = True)
            self.json = json
            funcs = {
                "submit": self.submit,
                "alter": self.alter,
                "delete": self.delete
            }
            func = funcs[json["method"]]
            return func()
        return False

    def submit(self):
        return self.agr.write(self.json.get("title"), self.json.get("contents"), self.json.get("disagreement"))
        
    def alter(self):
        return self.agr.alter(self.json.get("id"), self.json.get("title"), self.json.get("contents"), self.json.get("disagreement"))

    def delete(self):
        return self.agr.delete(self.json.get("id"))
"""

class VoteAPI(Resource):
    def get(self):
        id = request.args.get("id")
        markdown = request.args.get("markdown")
        if not markdown or markdown != "true":
            markdown = False
        else: 
            markdown = True
        vote = VoteController()
        result = vote.get(id, markdown)
        if result:
            return result
        return False

    def post(self):
        if "username" in session:
            self.vote = VoteController()
            self.json = request.get_json(force = True)
            funcs = {
                "create": self.create,
                "alter": self.alter,
                "delete": self.delete,
                "update": self.update,
                "duplicated": self.duplicated,
            }
            return funcs[self.json["method"]]()
        return False

    def create(self):
        return self.vote.create(self.json.get("title"), self.json.get("desc"), self.json.get("items"), self.json.get("multiple"))

    def alter(self):
        return self.vote.alter(self.json.get("title"), self.json.get("desc"), self.json.get("items"), self.json.get("id"), self.json.get("multiple"))

    def delete(self):
        return self.vote.delete(self.json.get("id"))

    def update(self):
        return self.vote.update(self.json.get("data"), self.json.get("id"))
    
    def duplicated(self):
        return self.vote.duplicated(self.json.get("id"))

@app.errorhandler(404)
def notFoundError(err):
    return make_response(
        jsonify({
            'error': 'NOT_FOUND',
            'code': 404
        })
    )

@app.errorhandler(500)
def internalServerError(err):
    return make_response(
        jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'code': 500
        })
    )

@app.errorhandler(401)
def unauthorizedError(err):
    return make_response(
        jsonify({
            'error': 'UNAUTHORIZED',
            'code': 401
        })
    )

api.add_resource(LogueAPI, '/api/logue', endpoint = 'logue')
api.add_resource(AuthAPI, '/api/auth', endpoint = 'auth')
api.add_resource(DataAPI, '/api/data', endpoint = 'data')
#api.add_resource(AgreementAPI, "/api/agreement", endpoint = 'agreement')
api.add_resource(VoteAPI, "/api/vote", endpoint = 'vote')

if __name__ == '__main__':
    app.run(debug = True)