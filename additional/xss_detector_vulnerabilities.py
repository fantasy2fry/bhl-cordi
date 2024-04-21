class Computer:
    def __init__(self, name):
        self.name = name

    def display(self):
        print(f"Computer name: {self.name}")


class Zebra:
    def __init__(self, name):
        self.name = name

    def display(self):
        print(f"Zebra name: {self.name}")

    def render(self):
        return f"<p>{self.name}</p>"  # Potencjalna podatność XSS


class Animal:
    def __init__(self, name):
        self.name = name

    def display(self):
        print(f"Animal name: {self.name}")

    def render(self):
        return f"<p>{self.name}</p>"  # Potencjalna podatność XSS


computer = Computer("<script>alert('Hello XSS!');</script>")
computer.display()

zebra = Zebra("<script>alert('Hello XSS!');</script>")
zebra.display()
print(zebra.render())  # To jest potencjalnie podatne na atak XSS

animal = Animal("<script>alert('Hello XSS!');</script>")
animal.display()
print(animal.render())  # To również jest potencjalnie podatne na atak XSS
