import base64

from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from hashlib import pbkdf2_hmac
import hmac

class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, user_id):
        return self.dao.get_one(user_id)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_d):
        user_d['password'] = self.get_hash(user_d['password'])
        return self.dao.create(user_d)

    def update(self, user_d):
        user_d['password'] = self.get_hash(user_d['password'])
        self.dao.update(user_d)

    def delete(self, uid):
        self.dao.delete(uid)

    def get_hash(self, password):
        password_hash = pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return base64.b64encode(password_hash)

    def compare_passwords(self, hash_pass, other_pass):
        decoded_digest = base64.b64decode(hash_pass)

        hash_digest = pbkdf2_hmac(
            'sha256',
            other_pass.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return hmac.compare_digest(decoded_digest, hash_digest)