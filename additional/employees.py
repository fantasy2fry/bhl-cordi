from abc import ABC, abstractmethod

class Employee(ABC):
    @abstractmethod
    def work(self):
        pass

    @abstractmethod
    def report(self):
        pass

class Developer(Employee):
    def work(self):
        print("Developing software...")

# Nie implementuje metody 'report', więc powinno być zgłoszone jako brakująca implementacja

class Manager(Employee):
    def report(self):
        print("Reporting to stakeholders...")

# Nie implementuje metody 'work', więc powinno być zgłoszone jako brakująca implementacja
