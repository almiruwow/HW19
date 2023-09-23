from flask import request
from flask_restx import Resource, Namespace
from implemented import user_service
from dao.model.user import UserSchema

users_ns = Namespace('users')


@users_ns.route('/')
class UsersView(Resource):
    def get(self):
        user = user_service.get_all()
        return UserSchema(many=True).dump(user)

    def post(self):
        json_data = request.json
        user_service.create(json_data)

        return '', 201


@users_ns.route('/<int:uid>')
class UsersViews(Resource):
    def get(self, uid):
        user = user_service.get_one(uid)
        return UserSchema().dump(user)

    def put(self, uid):
        json_data = request.json
        json_data['id'] = uid
        user_service.update(json_data)
        return '', 204

    def delete(self, uid):
        user_service.delete(uid)

        return '', 204
