#Konfiguracja symulacji rozprzestrzeniania się choroby
SIMULATION_CONFIG = {
    #Parametry populacji
    "population_size": 1500,       #Liczba osób w populacji
    "initial_infected": 3,         #Początkowa liczba zarażonych osób
    
    #Parametry choroby
    "infection_rate": 0.03,        #Prawdopodobieństwo zarażenia przy kontakcie (0-1)
    "recovery_rate": 0.03,          #Dzienna szansa na wyzdrowienie (0-1)
    "mortality_rate": 0.0005,        #Śmiertelność choroby (0-1)
    "immunity_period": 28,         #Okres odporności po wyzdrowieniu (dni)
    
    #Parametry interakcji społecznych
    "contacts_per_day": 10,        #Średnia liczba kontaktów dziennie
    "social_distancing": False,    #Czy stosowane jest dystansowanie społeczne
    "quarantine_infected": False,  #Czy zarażeni są kwarantannowani (ograniczenie kontaktów)
    
    #Parametry interwencji
    "vaccination_rate": 0.0,       #Tempo szczepienia populacji (0-1)
    "vaccination_effectiveness": 0.95, #Skuteczność szczepień (0-1)
    
    #Parametry algorytmów
    "algorithm": "SIR",           #Dostępne: "standard", "SIR", "SEIR", "network"
    "lockdown_threshold": 0.1,     #Próg zakażeń dla automatycznej blokady (0-1)
    
    #Parametry symulacji
    "simulation_days": 365,        #Całkowity czas symulacji w dniach
    "plot_results": True,          #Czy wyświetlać wykres
    "save_to_file": False,         #Czy zapisywać wykres do pliku
    "real_time_visualization": True #Czy używać wizualizacji w czasie rzeczywistym
}
