import random
from models.person import Person

class DiseaseSimulation:
    def __init__(self, config):
        self.config = config
        self.population = []
        self.stats_history = []
        self.initialize_population()
    
    def initialize_population(self):
        # Tworzenie populacji
        self.population = [Person(i) for i in range(self.config["population_size"])]
        
        # Losowe wybranie początkowo zarażonych osób
        initially_infected = random.sample(self.population, self.config["initial_infected"])
        for person in initially_infected:
            person.status = "infected"
        
        # Zapisanie początkowych statystyk
        self.record_stats()
    
    def run_simulation(self):
        for day in range(self.config["simulation_days"]):
            self.simulate_day()
            self.record_stats()
            print(f"Dzień {day+1} zakończony")
        
        return self.stats_history
    
    def simulate_day(self):
        # Symulacja interakcji między ludźmi
        for person in self.population:
            # Poruszanie się osób
            person.move()
            
            if person.status == "infected":
                # Zarażona osoba może zarażać innych
                contacts_today = self.config["contacts_per_day"]
                if self.config["social_distancing"]:
                    contacts_today = int(contacts_today * 0.5)  # Redukcja kontaktów
                
                # Kontakt zależy od odległości między osobami
                for other in self.population:
                    if other.status == "susceptible" and other.id != person.id:
                        # Obliczenie odległości między osobami
                        distance = ((person.x - other.x)**2 + (person.y - other.y)**2)**0.5
                        
                        # Prawdopodobieństwo zarażenia maleje z kwadratem odległości
                        infection_chance = self.config["infection_rate"] * (10 / (distance + 1))**2
                        
                        if distance < 5 and random.random() < infection_chance:
                            other.status = "infected"
                
                # Aktualizacja stanu choroby
                person.days_infected += 1
                
                # Możliwość wyzdrowienia lub śmierci
                if random.random() < self.config["mortality_rate"]:
                    person.status = "deceased"
                elif random.random() < self.config["recovery_rate"]:
                    person.status = "recovered"
                    person.immune_days = self.config["immunity_period"]
                    person.days_infected = 0
            
            # Aktualizacja odporności
            elif person.status == "recovered":
                if person.immune_days > 0:
                    person.immune_days -= 1
                else:
                    person.status = "susceptible"  # Utrata odporności
    
    def record_stats(self):
        susceptible = sum(1 for p in self.population if p.status == "susceptible")
        infected = sum(1 for p in self.population if p.status == "infected")
        recovered = sum(1 for p in self.population if p.status == "recovered")
        deceased = sum(1 for p in self.population if p.status == "deceased")
        
        self.stats_history.append({
            "susceptible": susceptible,
            "infected": infected,
            "recovered": recovered,
            "deceased": deceased,
            "day": len(self.stats_history)
        })
