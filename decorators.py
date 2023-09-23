from flask import request, abort
import jwt
from constants import SECRET, ALGO


def auth_required(func):
    def wrapper(*args, **kwargs):

        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split('Bearer ')[-1]

        try:
            jwt.decode(token, SECRET, algorithms=[ALGO])
        except Exception as e:
            print('Ошибка при декодировании токена', e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):

        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split('Bearer ')[-1]
        role = None

        try:
            decode = jwt.decode(token, SECRET, algorithms=[ALGO])
            role = decode.get('role', 'user')
        except Exception as e:
            print('Ошибка при декодировании токена', e)
            abort(401)

        if role != 'admin':
            abort(403)

        return func(*args, **kwargs)

    return wrapper
