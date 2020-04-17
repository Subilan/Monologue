from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource, request
from flask_cors import CORS
from werkzeug.exceptions import abort
from Database import DBController

app = Flask(__name__)
api = Api(app);
CORS(app);

class CommitAPI(Resource):
    def post(self):
        json = request.get_json(force = True)
        db = DBController()
        result = db.writeLogue(json["title"], json["contents"])
        if (result):
            return True
        else:
            abort(500)
            return False

class GetAPI(Resource):
    def get(self):
        arg = request.args.get("limit")
        db = DBController()
        result = db.getLogues(arg)
        return {result: result}, 200

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

api.add_resource(CommitAPI, '/api/commit', endpoint = 'commit')
api.add_resource(GetAPI, '/api/get', endpoint = 'get')

if __name__ == '__main__':
    app.run(debug = True);