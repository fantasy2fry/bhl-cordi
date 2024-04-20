class LivingBeing:
    pass


class Animal(LivingBeing):
    pass


class Mammal(Animal):
    pass


class Primate(Mammal):
    pass


class Human(Primate):
    pass


class Person(Human):
    def speak(self):
        print("Hello, I am a person.")


# Użycie klasy
person = Person()
person.speak()
