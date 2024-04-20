from base_class import BaseClass

class CorrectSubclass(BaseClass):
    def __init__(self):
        super().__init__()
        print("CorrectSubclass initialized")

    def another_method(self):
        print("Another method of CorrectSubclass")
