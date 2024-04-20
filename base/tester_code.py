class User:
    def __init__(self, name, age):
        self.name = name  # powinno być self._name
        self.age = age  # powinno być self._age

    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}")

    def birthday(self):
        self.age += 1
        print(f"Happy birthday {self.name}, now you are {self.age} years old!")


# Użycie klasy
user = User("John Doe", 30)
user.display_info()
user.birthday()
