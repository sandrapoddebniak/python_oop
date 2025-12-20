
import pygame  # Główna biblioteka do tworzenia gier
import sys     # Do zarządzania systemem (wyjście z gry)
import random  # Do generowania losowych wartości

# STAŁE GRY - wartości, które nie zmieniają się podczas gry
WIDTH, HEIGHT = 640, 480  # Szerokość i wysokość okna gry w pikselach
TILE_SIZE = 20            # Rozmiar czołgów i gracza w pikselach

# Zmienne globalne dla ruchu czerwonego prostokąta (demonstracja)
speed_x = 2  # Prędkość pozioma
speed_y = 1  # Prędkość pionowa

tanks = []

class Tank:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1
        self.shoot_timer = 0
        self.shoot_delay = 100
        self.health = 1
        self.max_health = 1

    def move(self):
        self.y += self.speed

    def shoot(self):
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            print(f"Tank at ({self.x},{self.y}) shoots!")

class TigerI(Tank):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 1
        self.shoot_timer = 0
        self.shoot_delay = 100
        self.health = 3
        self.max_health = 3

class TigerII(Tank):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 0.8
        self.shoot_timer = 0
        self.shoot_delay = 200
        self.health = 2
        self.max_health = 2

class Panther(Tank):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 1.5
        self.shoot_timer = 0
        self.shoot_delay = 50
        self.health = 5
        self.max_health = 5

def spawn_random_tank():
    x = random.randint(0, 800) 
    y = -50                     
    return random.choice([TigerI(x, y), TigerII(x, y), Panther(x, y)])


