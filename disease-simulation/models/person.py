import random
import numpy as np

class Person:
    def __init__(self, id):
        self.id = id
        self.status = "susceptible"  #susceptible, infected, recovered, deceased
        self.days_infected = 0
        self.immune_days = 0
        
        #Pozycja osoby w przestrzeni 2D
        self.x = random.uniform(0, 100)
        self.y = random.uniform(0, 100)
        
        #Prędkość i kierunek ruchu
        self.speed = random.uniform(0.5, 2.0)
        self.direction = random.uniform(0, 2 * np.pi)
        
        #Atrybuty osobowości wpływające na zachowanie
        self.sociability = random.uniform(0.2, 1.0)  #Towarzyskość wpływa na liczbę kontaktów
        self.movement_pattern = random.choice(['normal', 'static', 'explorer'])  #Różne wzorce ruchu

        #Dla modelu SEIR
        self.exposed = False
        self.exposure_days = 0

        #Dla modelu sieciowego
        self.connections = []
    
    def move(self, bounds=(100, 100)):
        if self.status == "deceased":
            return  #Zmarli się nie poruszają
        
        #Prawdopodobieństwo zmiany kierunku zależy od wzorca ruchu
        direction_change_prob = {
            'normal': 0.1, 
            'static': 0.02,
            'explorer': 0.3
        }[self.movement_pattern]
        
        #Modyfikator prędkości
        speed_modifier = 1.0
        if self.status == "infected":
            speed_modifier *= 0.6  #Zarażeni poruszają się wolniej
        
        #Losowa zmiana kierunku
        if random.random() < direction_change_prob:
            #Większa zmiana dla eksploratorów, mniejsza dla statycznych
            angle_change = {
                'normal': random.uniform(-0.5, 0.5),
                'static': random.uniform(-0.2, 0.2),
                'explorer': random.uniform(-1.5, 1.5)
            }[self.movement_pattern]
            self.direction = (self.direction + angle_change) % (2 * np.pi)
        
        #Prędkość zależy od wzorca ruchu
        base_speed = {
            'normal': self.speed,
            'static': self.speed * 0.3,
            'explorer': self.speed * 1.5
        }[self.movement_pattern]
        
        #Ruch w wybranym kierunku z uwzględnieniem modyfikatorów
        dx = np.cos(self.direction) * base_speed * speed_modifier
        dy = np.sin(self.direction) * base_speed * speed_modifier
        
        #Dodanie niewielkiego losowego szumu do ruchu
        dx += random.uniform(-0.5, 0.5)
        dy += random.uniform(-0.5, 0.5)
        
        self.x += dx
        self.y += dy
        
        #Obsługa granic - odbicie lub zawracanie
        if self.x < 0:
            self.x = 0
            self.direction = np.pi - self.direction
        elif self.x > bounds[0]:
            self.x = bounds[0]
            self.direction = np.pi - self.direction
            
        if self.y < 0:
            self.y = 0
            self.direction = -self.direction
        elif self.y > bounds[1]:
            self.y = bounds[1]
            self.direction = -self.direction
