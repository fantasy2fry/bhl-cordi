class User:
    shared_data = []

    def __init__(self, name):
        self.name = name
        self.user_data = []

    def add_shared_data(self, data):
        User.shared_data.append(data)
