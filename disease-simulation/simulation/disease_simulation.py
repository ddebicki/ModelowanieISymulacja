import random
from models.person import Person

class DiseaseSimulation:
    def __init__(self, config):
        self.config = config
        self.population = []
        self.stats_history = []
        self.simulation_algorithm = self._get_algorithm(config["algorithm"])
        self.initialize_population()
    
    def _get_algorithm(self, algorithm_name):
        """Wybiera odpowiedni algorytm symulacji."""
        algorithms = {
            "standard": self.standard_algorithm,
            "SIR": self.sir_algorithm,
            "SEIR": self.seir_algorithm,
            "network": self.network_algorithm
        }
        return algorithms.get(algorithm_name, self.standard_algorithm)
    
    def initialize_population(self):
        #Tworzenie populacji
        self.population = [Person(i) for i in range(self.config["population_size"])]
        
        #Losowe wybranie początkowo zarażonych osób
        initially_infected = random.sample(self.population, self.config["initial_infected"])
        for person in initially_infected:
            person.status = "infected"
        
        #Jeśli używamy modelu SEIR, dodajmy etap ekspozycji
        if self.config["algorithm"] == "SEIR":
            for person in self.population:
                person.exposed = False
                person.exposure_days = 0
        
        #Jeśli używamy modelu sieciowego, stwórzmy połączenia
        if self.config["algorithm"] == "network":
            self._create_social_network()
        
        #Zapisanie początkowych statystyk
        self.record_stats()
    
    def _create_social_network(self):
        """Tworzy sieć kontaktów społecznych dla modelu sieciowego."""
        #Dodaj atrybuty sieciowe do każdej osoby
        for person in self.population:
            person.connections = []
        
        #Generuj sieć małego świata - każdy ma stałą grupę kontaktów plus kilka losowych
        avg_connections = self.config["contacts_per_day"]
        for i, person in enumerate(self.population):
            #Stali sąsiedzi (np. rodzina, współpracownicy)
            for j in range(max(0, i-5), min(len(self.population), i+6)):
                if i != j:
                    person.connections.append(self.population[j])
            
            #Kilka losowych dalekich połączeń (znajomi, przypadkowi ludzie)
            potential_connections = [p for p in self.population if p not in person.connections and p.id != person.id]
            random_connections = random.sample(
                potential_connections,
                min(int(avg_connections * 0.3), len(potential_connections))
            )
            person.connections.extend(random_connections)
    
    def run_simulation(self):
        for day in range(self.config["simulation_days"]):
            self.simulate_day()
            self.record_stats()
            print(f"Dzień {day+1} zakończony")
        
        return self.stats_history
    
    def simulate_day(self):
        """Wykonuje symulację jednego dnia według wybranego algorytmu."""
        #Najpierw aktualizacja pozycji osób
        for person in self.population:
            person.move()
        
        #Następnie uruchomienie algorytmu symulacji
        self.simulation_algorithm()
    
    def standard_algorithm(self):
        """Standardowy algorytm symulacji oparty na kontaktach i odległościach."""
        #Najpierw szczepienia, jeśli są włączone
        self._apply_vaccinations()
        
        #Symulacja interakcji między ludźmi
        for person in self.population:
            if person.status == "infected":
                #Zarażona osoba może zarażać innych
                contacts_today = self.config["contacts_per_day"]
                if self.config["social_distancing"]:
                    contacts_today = int(contacts_today * 0.5)  #Redukcja kontaktów
                if self.config.get("quarantine_infected", False):
                    contacts_today = int(contacts_today * 0.2)  #Dalsza redukcja dla kwarantanny
                
                #Kontakt zależy od odległości między osobami
                for other in self.population:
                    if other.status == "susceptible" and other.id != person.id:
                        #Obliczenie odległości między osobami
                        distance = ((person.x - other.x)**2 + (person.y - other.y)**2)**0.5
                        
                        #Prawdopodobieństwo zarażenia maleje z kwadratem odległości
                        infection_chance = self.config["infection_rate"] * (10 / (distance + 1))**2
                        
                        if distance < 5 and random.random() < infection_chance:
                            other.status = "infected"
                
                #Aktualizacja stanu choroby
                person.days_infected += 1
                
                #Możliwość wyzdrowienia lub śmierci
                if random.random() < self.config["mortality_rate"]:
                    person.status = "deceased"
                elif random.random() < self.config["recovery_rate"]:
                    person.status = "recovered"
                    person.immune_days = self.config["immunity_period"]
                    person.days_infected = 0
            
            #Aktualizacja odporności
            elif person.status == "recovered":
                if person.immune_days > 0:
                    person.immune_days -= 1
                else:
                    person.status = "susceptible"  #Utrata odporności
    
    def sir_algorithm(self):
        """Implementacja klasycznego modelu SIR."""
        #Model SIR (Susceptible-Infected-Recovered) opiera się na równaniach różniczkowych
        #Tu implementujemy prostą wersję dyskretną
        
        #Najpierw szczepienia, jeśli są włączone
        self._apply_vaccinations()
        
        #Zmienne pomocnicze
        N = len(self.population)
        susceptible = [p for p in self.population if p.status == "susceptible"]
        infected = [p for p in self.population if p.status == "infected"]
        
        #Parametry modelu
        beta = self.config["infection_rate"] * self.config["contacts_per_day"] / N
        gamma = self.config["recovery_rate"]
        
        #Modyfikatory na podstawie interwencji
        if self.config["social_distancing"]:
            beta *= 0.5
        if self.config.get("quarantine_infected", False):
            beta *= 0.2
        
        #Prawdopodobieństwo zarażenia nowych osób
        new_infected_count = int(beta * len(susceptible) * len(infected))
        if new_infected_count > 0:
            new_infected = random.sample(susceptible, min(new_infected_count, len(susceptible)))
            for person in new_infected:
                person.status = "infected"
        
        #Proces wyzdrowienia lub śmierci
        for person in infected:
            person.days_infected += 1
            if random.random() < self.config["mortality_rate"]:
                person.status = "deceased"
            elif random.random() < gamma:
                person.status = "recovered"
                person.immune_days = self.config["immunity_period"]
                person.days_infected = 0
        
        #Aktualizacja odporności
        for person in self.population:
            if person.status == "recovered" and person.immune_days > 0:
                person.immune_days -= 1
                if person.immune_days == 0:
                    person.status = "susceptible"
    
    def seir_algorithm(self):
        """Implementacja modelu SEIR z dodatkową fazą ekspozycji."""
        #Model SEIR (Susceptible-Exposed-Infected-Recovered) dodaje fazę ekspozycji
        
        #Najpierw szczepienia, jeśli są włączone
        self._apply_vaccinations()
        
        #Zmienne pomocnicze
        N = len(self.population)
        susceptible = [p for p in self.population if p.status == "susceptible"]
        exposed = [p for p in self.population if getattr(p, 'exposed', False) and p.status == "susceptible"]
        infected = [p for p in self.population if p.status == "infected"]
        
        #Parametry modelu
        beta = self.config["infection_rate"] * self.config["contacts_per_day"] / N
        alpha = 0.2  #Współczynnik przejścia z ekspozycji do infekcji (średnio 5 dni inkubacji)
        gamma = self.config["recovery_rate"]
        
        #Modyfikatory na podstawie interwencji
        if self.config["social_distancing"]:
            beta *= 0.5
        if self.config.get("quarantine_infected", False):
            beta *= 0.2
        
        #Ekspozycja nowych osób
        new_exposed_count = int(beta * len(susceptible) * len(infected))
        if new_exposed_count > 0:
            new_exposed = random.sample(
                [p for p in susceptible if not getattr(p, 'exposed', False)],
                min(new_exposed_count, len(susceptible))
            )
            for person in new_exposed:
                person.exposed = True
                person.exposure_days = 0
        
        #Przejście z ekspozycji do infekcji
        for person in exposed:
            person.exposure_days += 1
            if random.random() < alpha:
                person.exposed = False
                person.status = "infected"
        
        #Proces wyzdrowienia lub śmierci
        for person in infected:
            person.days_infected += 1
            if random.random() < self.config["mortality_rate"]:
                person.status = "deceased"
            elif random.random() < gamma:
                person.status = "recovered"
                person.immune_days = self.config["immunity_period"]
                person.days_infected = 0
        
        #Aktualizacja odporności
        for person in self.population:
            if person.status == "recovered" and person.immune_days > 0:
                person.immune_days -= 1
                if person.immune_days == 0:
                    person.status = "susceptible"
    
    def network_algorithm(self):
        """Implementacja modelu opartego na sieci społecznej."""
        #W tym modelu każda osoba ma stałą sieć kontaktów
        
        #Najpierw szczepienia, jeśli są włączone
        self._apply_vaccinations()
        
        #Propagacja infekcji przez sieć kontaktów
        newly_infected = []
        for person in [p for p in self.population if p.status == "infected"]:
            #Modyfikatory kontaktów
            contact_reduction = 1.0
            if self.config["social_distancing"]:
                contact_reduction *= 0.5
            if self.config.get("quarantine_infected", False):
                contact_reduction *= 0.2
            
            #Określenie liczby kontaktów danego dnia
            daily_contacts = int(len(person.connections) * contact_reduction)
            if daily_contacts > 0:
                contacts_today = random.sample(person.connections, daily_contacts)
                
                #Próba zarażenia kontaktów
                for contact in contacts_today:
                    if contact.status == "susceptible":
                        #Uwzględnienie odległości fizycznej
                        distance = ((person.x - contact.x)**2 + (person.y - contact.y)**2)**0.5
                        infection_chance = self.config["infection_rate"] * (10 / (distance + 1))**2
                        
                        if random.random() < infection_chance:
                            newly_infected.append(contact)
            
            #Aktualizacja stanu choroby
            person.days_infected += 1
            if random.random() < self.config["mortality_rate"]:
                person.status = "deceased"
            elif random.random() < self.config["recovery_rate"]:
                person.status = "recovered"
                person.immune_days = self.config["immunity_period"]
                person.days_infected = 0
        
        #Zaraźmy nowo zainfekowane osoby
        for person in newly_infected:
            person.status = "infected"
        
        #Aktualizacja odporności
        for person in self.population:
            if person.status == "recovered" and person.immune_days > 0:
                person.immune_days -= 1
                if person.immune_days == 0:
                    person.status = "susceptible"
    
    def _apply_vaccinations(self):
        """Stosuje szczepienia do podatnej populacji."""
        if self.config["vaccination_rate"] > 0:
            susceptible = [p for p in self.population if p.status == "susceptible"]
            daily_vaccinations = int(self.config["vaccination_rate"] * len(susceptible) / 100)
            
            if daily_vaccinations > 0:
                vaccinated = random.sample(susceptible, min(daily_vaccinations, len(susceptible)))
                for person in vaccinated:
                    #Skuteczność szczepienia
                    if random.random() < self.config["vaccination_effectiveness"]:
                        person.status = "recovered"
                        person.immune_days = 10000  #Długotrwała odporność szczepionkowa
    
    def record_stats(self):
        susceptible = sum(1 for p in self.population if p.status == "susceptible")
        infected = sum(1 for p in self.population if p.status == "infected")
        recovered = sum(1 for p in self.population if p.status == "recovered")
        deceased = sum(1 for p in self.population if p.status == "deceased")
        
        #Dodajmy ekspozycję, jeśli używamy modelu SEIR
        exposed = 0
        if self.config["algorithm"] == "SEIR":
            exposed = sum(1 for p in self.population if p.status == "susceptible" and getattr(p, 'exposed', False))
        
        self.stats_history.append({
            "susceptible": susceptible,
            "infected": infected,
            "recovered": recovered,
            "deceased": deceased,
            "exposed": exposed,
            "day": len(self.stats_history)
        })
