class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def is_authenticated(self):
        return True

    @staticmethod
    def is_active(self):
        return True

    @staticmethod
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def checkpassword(self, user_password):
        if self.password == user_password:
            return self.password
