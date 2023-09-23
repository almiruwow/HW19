from service.user import UserService
from flask import abort
import datetime
import calendar
import jwt
from constants import SECRET, ALGO

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_token(self, username, password, is_refresh=False):

        user = self.user_service.get_by_username(username)

        if user is None:
            raise abort(404)

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                abort(400)

        data = {
            'username': user.username,
            'role': user.role
        }

        hour1 = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        data['exp'] = calendar.timegm(hour1.timetuple())
        access_token = jwt.encode(data, SECRET, algorithm=ALGO)

        days100 = datetime.datetime.utcnow() + datetime.timedelta(days=100)
        data['exp'] = calendar.timegm(days100.timetuple())
        refresh_token = jwt.encode(data, SECRET, algorithm=ALGO)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def token_update(self, refresh_token):
        data = jwt.decode(refresh_token, SECRET, algorithms=[ALGO])

        username = data.get('username')

        return self.generate_token(username, None, is_refresh=True)