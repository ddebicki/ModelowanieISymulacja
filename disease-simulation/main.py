import random
import matplotlib.pyplot as plt
import numpy as np
import argparse
import time
from config import SIMULATION_CONFIG
from models.person import Person
from simulation.disease_simulation import DiseaseSimulation
from utils.visualization import plot_simulation_results, create_real_time_visualization

def parse_arguments():
    """Parsowanie argumentów linii poleceń dla łatwiejszej konfiguracji."""
    parser = argparse.ArgumentParser(description="Symulacja rozprzestrzeniania się choroby")
    
    parser.add_argument("--population", type=int, help="Wielkość populacji")
    parser.add_argument("--days", type=int, help="Liczba dni symulacji")
    parser.add_argument("--infected", type=int, help="Początkowa liczba zarażonych")
    parser.add_argument("--algorithm", choices=["standard", "SIR", "SEIR", "network"], 
                        help="Algorytm symulacji")
    parser.add_argument("--visual", action="store_true", help="Uruchom wizualizację w czasie rzeczywistym")
    parser.add_argument("--distancing", action="store_true", help="Aktywuj dystans społeczny")
    
    args = parser.parse_args()
    
    #Aktualizacja konfiguracji na podstawie argumentów
    config = SIMULATION_CONFIG.copy()
    if args.population:
        config["population_size"] = args.population
    if args.days:
        config["simulation_days"] = args.days
    if args.infected:
        config["initial_infected"] = args.infected
    if args.algorithm:
        config["algorithm"] = args.algorithm
    if args.visual:
        config["real_time_visualization"] = True
    if args.distancing:
        config["social_distancing"] = True
        
    return config

if __name__ == "__main__":
    #Parsowanie argumentów linii poleceń
    try:
        config = parse_arguments()
    except:
        config = SIMULATION_CONFIG

    # Automatyczne wyłączenie graficznej wizualizacji dla dużych populacji
    if config["population_size"] > 2000:
        if config["real_time_visualization"]:
            print("\n==============================================================")
            print("Graficzna wizualizacja (kropeczki) jest dostępna tylko dla populacji do 2000 osób.")
            print("Dla większych populacji wyświetlany jest tylko wykres liczbowy/statystyki.")
            print("==============================================================\n")
            print("Trwa przetwarzanie...\n")
            time.sleep(5)
        config["real_time_visualization"] = False

    print("Uruchamianie symulacji rozprzestrzeniania się choroby...")
    print(f"- Algorytm: {config['algorithm']}")
    print(f"- Populacja: {config['population_size']} osób")
    print(f"- Początkowe zarażenia: {config['initial_infected']} osób")
    print(f"- Czas symulacji: {config['simulation_days']} dni")
    
    simulation = DiseaseSimulation(config)
    
    if config["real_time_visualization"]:
        print("Uruchamianie wizualizacji w czasie rzeczywistym...")
        animation = create_real_time_visualization(simulation)
    else:
        results = simulation.run_simulation()
        
        final_stats = results[-1]
        print("\nWyniki końcowe:")
        print(f"Podatni: {final_stats['susceptible']} osób ({final_stats['susceptible']/config['population_size']:.1%})")
        print(f"Zarażeni: {final_stats['infected']} osób ({final_stats['infected']/config['population_size']:.1%})")
        print(f"Ozdrowieńcy: {final_stats['recovered']} osób ({final_stats['recovered']/config['population_size']:.1%})")
        print(f"Zmarli: {final_stats['deceased']} osób ({final_stats['deceased']/config['population_size']:.1%})")
        
        #Wyświetlenie wykresu
        plot_simulation_results(results, config)
