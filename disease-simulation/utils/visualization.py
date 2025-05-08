import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def plot_simulation_results(stats_history, config):
    days = [stat["day"] for stat in stats_history]
    susceptible = [stat["susceptible"] for stat in stats_history]
    infected = [stat["infected"] for stat in stats_history]
    recovered = [stat["recovered"] for stat in stats_history]
    deceased = [stat["deceased"] for stat in stats_history]
    
    plt.figure(figsize=(12, 8))
    plt.plot(days, susceptible, label='Podatni', color='blue')
    plt.plot(days, infected, label='Zarażeni', color='red')
    plt.plot(days, recovered, label='Ozdrowieńcy', color='green')
    plt.plot(days, deceased, label='Zmarli', color='black')
    
    plt.title('Symulacja rozprzestrzeniania się choroby')
    plt.xlabel('Dzień')
    plt.ylabel('Liczba osób')
    plt.legend()
    plt.grid(True)
    
    if config["save_to_file"]:
        plt.savefig('simulation_results.png')
    else:
        plt.show()

def create_real_time_visualization(simulation):
    """Tworzy wizualizację symulacji w czasie rzeczywistym."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('Symulacja rozprzestrzeniania się choroby')
    
    # Kolory dla różnych stanów
    colors = {
        'susceptible': 'blue',
        'infected': 'red',
        'recovered': 'green',
        'deceased': 'black'
    }
    
    # Wykres z kropkami (osobami)
    scatter = ax1.scatter([], [], c=[], s=50, alpha=0.8)
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 100)
    ax1.set_title('Rozmieszczenie populacji')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    
    # Dodanie legendy dla kolorów
    for status, color in colors.items():
        ax1.scatter([], [], c=color, label=status.capitalize())
    ax1.legend()
    
    # Wykres liczby osób w czasie
    days_data = []
    susceptible_data = []
    infected_data = []
    recovered_data = []
    deceased_data = []
    
    susceptible_line, = ax2.plot([], [], 'b-', label='Podatni')
    infected_line, = ax2.plot([], [], 'r-', label='Zarażeni')
    recovered_line, = ax2.plot([], [], 'g-', label='Ozdrowieńcy')
    deceased_line, = ax2.plot([], [], 'k-', label='Zmarli')
    
    ax2.set_xlim(0, simulation.config["simulation_days"])
    ax2.set_ylim(0, simulation.config["population_size"])
    ax2.set_title('Przebieg epidemii w czasie')
    ax2.set_xlabel('Dzień')
    ax2.set_ylabel('Liczba osób')
    ax2.legend()
    ax2.grid(True)
    
    day_text = ax2.text(0.02, 0.95, '', transform=ax2.transAxes)
    
    def update(frame):
        # Aktualizacja symulacji
        if frame > 0:
            simulation.simulate_day()
            simulation.record_stats()
        
        # Aktualizacja danych dla wykresu kropek
        x = [person.x for person in simulation.population]
        y = [person.y for person in simulation.population]
        color_values = [colors[person.status] for person in simulation.population]
        scatter.set_offsets(np.c_[x, y])
        scatter.set_color(color_values)
        
        # Aktualizacja wykresu w czasie
        stats = simulation.stats_history[-1]
        days_data.append(stats["day"])
        susceptible_data.append(stats["susceptible"])
        infected_data.append(stats["infected"])
        recovered_data.append(stats["recovered"])
        deceased_data.append(stats["deceased"])
        
        susceptible_line.set_data(days_data, susceptible_data)
        infected_line.set_data(days_data, infected_data)
        recovered_line.set_data(days_data, recovered_data)
        deceased_line.set_data(days_data, deceased_data)
        
        # Aktualizacja tekstu dnia
        day_text.set_text(f'Dzień: {stats["day"]}')
        
        return scatter, susceptible_line, infected_line, recovered_line, deceased_line, day_text
    
    ani = animation.FuncAnimation(
        fig, update, frames=simulation.config["simulation_days"]+1,
        interval=200, blit=True, repeat=False
    )
    
    plt.tight_layout()
    plt.show()
    
    return ani
