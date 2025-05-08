import random

class Person:
    def __init__(self, id):
        self.id = id
        self.status = "susceptible"  # susceptible, infected, recovered, deceased
        self.days_infected = 0
        self.immune_days = 0
        
        # Pozycja osoby w przestrzeni 2D
        self.x = random.uniform(0, 100)
        self.y = random.uniform(0, 100)
        # Prędkość ruchu
        self.speed = random.uniform(0.5, 2.0)
        self.direction = random.uniform(0, 2 * 3.14159)
    
    def move(self, bounds=(100, 100)):
        # Losowa zmiana kierunku ruchu
        if random.random() < 0.1:
            self.direction = random.uniform(0, 2 * 3.14159)
            
        # Ruch w wybranym kierunku
        self.x += self.speed * (0.5 if self.status == "infected" else 1.0) * \
                 random.uniform(0.8, 1.2) * (random.random() - 0.5 + 0.5 * 
                 (0 if random.random() > 0.5 else 1)) * 2
        self.y += self.speed * (0.5 if self.status == "infected" else 1.0) * \
                 random.uniform(0.8, 1.2) * (random.random() - 0.5 + 0.5 * 
                 (0 if random.random() > 0.5 else 1)) * 2
        
        # Odbicie od granic
        if self.x < 0:
            self.x = 0
            self.direction = 3.14159 - self.direction
        elif self.x > bounds[0]:
            self.x = bounds[0]
            self.direction = 3.14159 - self.direction
            
        if self.y < 0:
            self.y = 0
            self.direction = -self.direction
        elif self.y > bounds[1]:
            self.y = bounds[1]
            self.direction = -self.direction
            
        # Osoby zmarłe się nie poruszają
        if self.status == "deceased":
            self.speed = 0
