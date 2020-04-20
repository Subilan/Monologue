from flask import Flask, jsonify, make_response, request, session, escape
from flask_restful import Api, Resource
from flask_cors import CORS
from werkzeug.exceptions import abort
from datetime import timedelta
from Database import DBController
from Auth import AuthManager
from Logue import LogueController

app = Flask(__name__)
api = Api(app)
CORS(app)
app.secret_key = "jkshbfawugfagr78f3q4r7rq4tfg4g23o7yr39o563498fi387ty8ygr7tdwsacghjsdvbdxzvesfdiolhg;waprurq2;3p[u5r0piq82r90831-=8410184-32857[q2385-u20pfqyu-34t8q[urgfvq3-['ig3='rgiqre-'ugu='rug0wer8a0w78d8g9s7gu934yu930y5ihi3h4ihihegj'egisdahfhsiahfhhufewfwtr7wfgharege"
app.permanent_session_lifetime = timedelta(days = 7)

class LogueAPI(Resource):
    def get(self):
        method = request.args.get("method")
        markdown = request.args.get("markdown")
        if not markdown or markdown == 'true':
            markdown = True
        else:
            markdown = False
        arg = request.args.get(method)
        logue = LogueController()
        result = logue.get(arg, method, markdown)
        return result

    def post(self):
        json = request.get_json(force = True)
        self.json = json
        funcs = {
            "submit": self.submit,
            "alter": self.alter
        }
        func = funcs[json["method"]]
        return func()

    def submit(self):
        json = self.json
        logue = LogueController()
        result = logue.write(json["title"], json["contents"], json["type"])
        return result

    def alter(self):
        json = self.json
        logue = LogueController()
        result = logue.alter(json["id"], json["title"], json["contents"], json["type"])
        return result

class AuthAPI(Resource):
    def login(self):
        json = self.json
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
        func = funcs[json["method"]]
        return func()

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

api.add_resource(LogueAPI, '/api/logue', endpoint = 'logue')
api.add_resource(AuthAPI, '/api/auth', endpoint = 'auth')

if __name__ == '__main__':
    app.run(debug = True);