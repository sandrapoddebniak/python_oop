from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, brand: str, model: str, price_per_day: int):
        self.brand = brand
        self.model = model
        self.price_per_day = price_per_day

    @abstractmethod
    def vehicle_type(self):
        pass
    def __str__(self):
        return f"{self.vehicle_type()}:{self.brand} {self.model} ({self.price_per_day} PLN/day)"


class Car(Vehicle):
    def vehicle_type(self):
        return "car"
car1 = Car(brand="BMW", model="X5", price_per_day=200)
car2 = Car(brand="Mercedes", model="g_wagon", price_per_day=300)
car3 = Car(brand="Mazda", model="CX5", price_per_day=400)


class Bike(Vehicle):
    def vehicle_type(self):
        return "bike"
bike1 = Bike(brand="Romet", model="aaa", price_per_day=100)
bike2 = Bike(brand="Trek", model="bbb", price_per_day=200)
bike3 = Bike(brand="Specialized", model="ccc", price_per_day=300)


class Scooter(Vehicle):
    def vehicle_type(self):
        return "scooter"
scooter1 = Scooter(brand="Vespa", model="GTS", price_per_day=200)
scooter2 = Scooter(brand="Honda", model="PCX", price_per_day=300)
scooter3 = Scooter(brand="Yamaha", model="Majesty", price_per_day=400)

class Rental:
    def __init__(self, vehicle: Vehicle, days: int):
        self.vehicle = vehicle
        self.days = days

    def total_price(self):
        return self.days * self.vehicle.price_per_day

    def __str__(self):
        return f"{self.vehicle} for {self.days} days → {self.total_price()} PLN"
    
    
class Rental_Service:
    def __init__(self):
        self.vehicles = []
        self.rentals = []

    def add_vehicle(self, vehicle: Vehicle):
        self.vehicles.append(vehicle)

    def remove_vehicle(self, vehicle: Vehicle):
        self.vehicles.remove(vehicle)

    def add_rental(self, rental: Rental):
        self.rentals.append(rental)

    def remove_rental(self, rental: Rental):
        self.rentals.remove(rental)

    def __len__(self):
        return len(self.vehicles)

    def __contains__(self, vehicle):
        return vehicle in self.vehicles

    def __str__(self):
        return (
            f"Rental Service\n"
            f"Vehicles: {len(self.vehicles)}\n"
            f"Active rentals: {len(self.rentals)}"
        )
print(bike1)