from abc import ABC, abstractmethod
from datetime import date
class Material(ABC):
    def __init__(self, title: str):
        self.title = title
        self.is_available = True
        self.reserved_by = None

    @abstractmethod
    def material_type(self):
        pass

    def __str__(self):
        status = "available" if self.is_available else "borrowed"
        return f"{self.material_type()}: {self.title} ({status})"
    
class Book(Material):
    def material_type(self):
        return "Book"


class Ebook(Material):
    def material_type(self):
        return "Ebook"


class Audiobook(Material):
    def material_type(self):
        return "Audiobook"


class Magazine(Material):
    def material_type(self):
        return "Magazine"

class User(ABC):
    def __init__(self, name: str):
        self.name = name
        self.borrowed = []

    @abstractmethod
    def max_borrow_limit(self):
        pass

    @abstractmethod
    def fine_per_day(self):
        pass

    def __str__(self):
        return f"{self.name} ({self.__class__.__name__})"

class Student(User):
    def max_borrow_limit(self):
        return 5

    def fine_per_day(self):
        return 1


class Employee(User):
    def max_borrow_limit(self):
        return 10

    def fine_per_day(self):
        return 0.5


class Guest(User):
    def max_borrow_limit(self):
        return 2

    def fine_per_day(self):
        return 2

class Borrow:
    def __init__(self, user: User, material: Material, days: int):
        self.user = user
        self.material = material
        self.days = days
        self.borrow_date = date.today()

    def calculate_fine(self, days_late: int):
        return days_late * self.user.fine_per_day()

class Library:
    def __init__(self):
        self.materials = []
        self.borrows = []

    def add_material(self, material: Material):
        self.materials.append(material)

    def borrow_material(self, user: User, material: Material, days: int):
        if not material.is_available:
            print("Material not available")
            return

        if len(user.borrowed) >= user.max_borrow_limit():
            print("Borrow limit reached")
            return

        material.is_available = False
        borrow = Borrow(user, material, days)
        self.borrows.append(borrow)
        user.borrowed.append(borrow)

        print(f"{user.name} borrowed {material.title}")

    def return_material(self, user: User, material: Material, days_late=0):
        material.is_available = True

        borrow = next(b for b in user.borrowed if b.material == material)
        user.borrowed.remove(borrow)
        self.borrows.remove(borrow)

        fine = borrow.calculate_fine(days_late)
        print(f"{material.title} returned. Fine: {fine} PLN")

    def reserve_material(self, user: User, material: Material):
        if material.is_available:
            print("Material is available – no need to reserve")
        else:
            material.reserved_by = user
            print(f"{material.title} reserved by {user.name}")
library = Library()

book = Book("Kwiaty dla Algernoona")
ebook = Ebook("Klara i Słońce")

student = Student("Anna")
guest = Guest("Tomek")

library.add_material(book)
library.add_material(ebook)

library.borrow_material(student, book, 14)
library.borrow_material(guest, ebook, 7)

library.return_material(student, book, days_late=3)
