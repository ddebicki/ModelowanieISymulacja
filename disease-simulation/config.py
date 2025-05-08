# Konfiguracja symulacji rozprzestrzeniania się choroby
SIMULATION_CONFIG = {
    # Parametry populacji
    "population_size": 1000,       # Liczba osób w populacji
    "initial_infected": 5,         # Początkowa liczba zarażonych osób
    
    # Parametry choroby
    "infection_rate": 0.05,        # Prawdopodobieństwo zarażenia przy kontakcie (0-1)
    "recovery_rate": 0.1,          # Dzienna szansa na wyzdrowienie (0-1)
    "mortality_rate": 0.02,        # Śmiertelność choroby (0-1)
    "immunity_period": 14,         # Okres odporności po wyzdrowieniu (dni)
    
    # Parametry interakcji społecznych
    "contacts_per_day": 10,        # Średnia liczba kontaktów dziennie
    "social_distancing": False,    # Czy stosowane jest dystansowanie społeczne
    
    # Parametry symulacji
    "simulation_days": 100,        # Całkowity czas symulacji w dniach
    "plot_results": True,          # Czy wyświetlać wykres
    "save_to_file": False,         # Czy zapisywać wykres do pliku
    "real_time_visualization": True # Czy używać wizualizacji w czasie rzeczywistym
}
