from flask import request
from flask_restx import Namespace, Resource
from implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class Auth(Resource):
    def post(self):
        data_json = request.json

        username = data_json.get('username')
        password = data_json.get('password')

        if None in [username, password]:
            return "", 400

        tokens = auth_service.generate_token(username, password)

        return tokens

    def put(self):
        data = request.json

        token = data.get('refresh_token')

        tokens = auth_service.token_update(token)

        return tokens