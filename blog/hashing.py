from passlib.context import CryptContext


class Hashing:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def encrypt(self, pwd):
        return self.pwd_context.hash(pwd)

    def verify(self, plain_pwd, hashed_pwd):
        return self.pwd_context.verify(plain_pwd, hashed_pwd)
