import random
import matplotlib.pyplot as plt
import numpy as np
from config import SIMULATION_CONFIG
from models.person import Person
from simulation.disease_simulation import DiseaseSimulation
from utils.visualization import plot_simulation_results, create_real_time_visualization

# The Person class is now imported from models.person, no need to define it here

if __name__ == "__main__":
    print("Uruchamianie symulacji rozprzestrzeniania się choroby...")
    simulation = DiseaseSimulation(SIMULATION_CONFIG)
    
    if SIMULATION_CONFIG["real_time_visualization"]:
        print("Uruchamianie wizualizacji w czasie rzeczywistym...")
        animation = create_real_time_visualization(simulation)
    else:
        results = simulation.run_simulation()
        
        final_stats = results[-1]
        print("\nWyniki końcowe:")
        print(f"Podatni: {final_stats['susceptible']} osób")
        print(f"Zarażeni: {final_stats['infected']} osób")
        print(f"Ozdrowieńcy: {final_stats['recovered']} osób")
        print(f"Zmarli: {final_stats['deceased']} osób")
