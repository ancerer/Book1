class User():
    def __init__(self, firstname, lastname):
        self.first_name = firstname
        self.second_name = lastname
        self.university = ''
        self.age = 0
        self.login_attempts = 0



    def descirbe_user(self):
        pass

    def greet_user(self):
        pass

    def increment_login_attempts(self):
        self.login_attempts += 1
        print(self.login_attempts)

    def reset_login_attempts(self):
        self.login_attempts = 0
        print((self.login_attempts))

class Unit(User):
    def __init__(self, firstname, lastname):
        super().__init__(self, firstname, lastname)




X = User('Y', 'P')
X.increment_login_attempts()
X.increment_login_attempts()
X.increment_login_attempts()
X.reset_login_attempts()