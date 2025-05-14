import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.widgets import Button, Slider, RadioButtons
import matplotlib.patches as patches

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
    """Tworzy ulepszoną wizualizację symulacji w czasie rzeczywistym."""
    #Ustawienie stylów dla lepszej wizualizacji
    plt.style.use('dark_background')
    
    #Stworzenie okna z odpowiednim układem wykresów
    fig = plt.figure(figsize=(18, 10))
    grid = plt.GridSpec(3, 3, figure=fig)
    
    #Główny obszar symulacji
    ax_main = fig.add_subplot(grid[0:2, 0:2])
    #Wykres statystyk w czasie
    ax_stats = fig.add_subplot(grid[0:2, 2])
    #Panel kontrolny
    ax_controls = fig.add_subplot(grid[2, :])
    ax_controls.axis('off')  #Ukrycie osi dla panelu kontrolnego
    
    #Dodanie tytułu i informacji
    fig.suptitle('Symulacja Rozprzestrzeniania się Choroby', fontsize=20, color='white')
    
    # --- DODANE: informacja o limicie populacji ---
    population_limit = 2000
    if simulation.config["population_size"] > population_limit:
        ax_main.text(
            50, 50,
            f"Graficzna wizualizacja dostępna tylko dla populacji do {population_limit} osób.\n"
            f"Aktualna populacja: {simulation.config['population_size']}",
            color="red", fontsize=18, ha='center', va='center', bbox=dict(facecolor='black', alpha=0.7)
        )
        plt.draw()
        plt.pause(5)
        plt.close(fig)
        return None
    elif simulation.config["population_size"] > 0.8 * population_limit:
        ax_main.text(
            50, 5,
            f"Uwaga: graficzna wizualizacja działa optymalnie do {population_limit} osób.",
            color="orange", fontsize=12, ha='center', va='bottom', bbox=dict(facecolor='black', alpha=0.5)
        )
    # --- KONIEC DODANEGO ---
    
    #Kolory dla różnych stanów z gradientem dla zarażonych
    base_colors = {
        'susceptible': '#3498db',  #Niebieski
        'infected': '#e74c3c',     #Czerwony
        'recovered': '#2ecc71',    #Zielony
        'deceased': '#7f8c8d'      #Szary
    }
    
    #Ustawienia głównego obszaru symulacji
    ax_main.set_title('Rozmieszczenie Populacji', fontsize=16, color='white')
    ax_main.set_xlim(0, 100)
    ax_main.set_ylim(0, 100)
    ax_main.set_facecolor('#111111')  #Ciemne tło
    ax_main.grid(True, alpha=0.3)
    
    #Dodanie legendy dla pozycji osób
    legend_elements = [
        patches.Patch(facecolor=base_colors['susceptible'], label='Podatni'),
        patches.Patch(facecolor=base_colors['infected'], label='Zarażeni'),
        patches.Patch(facecolor=base_colors['recovered'], label='Ozdrowieńcy'),
        patches.Patch(facecolor=base_colors['deceased'], label='Zmarli')
    ]
    ax_main.legend(handles=legend_elements, loc='upper right')
    
    #Dodanie informacji tekstowych
    day_text = ax_main.text(5, 95, '', fontsize=12, color='white')
    stats_text = ax_main.text(5, 90, '', fontsize=10, color='white')
    
    #Inicjalizacja wykresu kropek
    scatter = ax_main.scatter([], [], c=[], s=[], alpha=0.7, edgecolors='white')
    
    #Ustawienia wykresu statystyk
    ax_stats.set_title('Przebieg epidemii', fontsize=16, color='white')
    ax_stats.set_xlabel('Dzień', color='white')
    ax_stats.set_ylabel('Liczba osób', color='white')
    ax_stats.set_facecolor('#111111')
    ax_stats.grid(True, alpha=0.3)
    ax_stats.tick_params(axis='x', colors='white')
    ax_stats.tick_params(axis='y', colors='white')
    
    #Inicjalizacja linii na wykresie statystyk
    susceptible_line, = ax_stats.plot([], [], '-', color=base_colors['susceptible'], linewidth=2, label='Podatni')
    infected_line, = ax_stats.plot([], [], '-', color=base_colors['infected'], linewidth=2, label='Zarażeni')
    recovered_line, = ax_stats.plot([], [], '-', color=base_colors['recovered'], linewidth=2, label='Ozdrowieńcy')
    deceased_line, = ax_stats.plot([], [], '-', color=base_colors['deceased'], linewidth=2, label='Zmarli')
    ax_stats.legend()
    
    #Dane dla wykresów
    days_data = []
    susceptible_data = []
    infected_data = []
    recovered_data = []
    deceased_data = []
    
    #Ustawienia limitów osi
    ax_stats.set_xlim(0, simulation.config["simulation_days"])
    ax_stats.set_ylim(0, simulation.config["population_size"])
    
    #Dodanie przycisków kontrolnych
    ax_social_dist = plt.axes([0.2, 0.05, 0.15, 0.07])
    btn_social_dist = Button(ax_social_dist, 'Dystans społeczny: WYŁ', color='darkred')
    
    ax_quarantine = plt.axes([0.4, 0.05, 0.15, 0.07])
    btn_quarantine = Button(ax_quarantine, 'Kwarantanna: WYŁ', color='darkred')
    
    ax_vaccination = plt.axes([0.6, 0.05, 0.15, 0.07])
    slider_vaccination = Slider(ax_vaccination, 'Szczepienia', 0, 1, valinit=0, valstep=0.01)
    
    #Aktualne ustawienia symulacji
    simulation_settings = {
        'social_distancing': False,
        'quarantine': False,
        'vaccination_rate': 0
    }
    
    def update_social_distance(event):
        simulation_settings['social_distancing'] = not simulation_settings['social_distancing']
        simulation.config["social_distancing"] = simulation_settings['social_distancing']
        btn_social_dist.label.set_text(f'Dystans społeczny: {"WŁ" if simulation_settings["social_distancing"] else "WYŁ"}')
        btn_social_dist.color = 'darkgreen' if simulation_settings["social_distancing"] else 'darkred'
        
    def update_quarantine(event):
        simulation_settings['quarantine'] = not simulation_settings['quarantine']
        simulation.config["quarantine_infected"] = simulation_settings['quarantine']
        btn_quarantine.label.set_text(f'Kwarantanna: {"WŁ" if simulation_settings["quarantine"] else "WYŁ"}')
        btn_quarantine.color = 'darkgreen' if simulation_settings["quarantine"] else 'darkred'
    
    def update_vaccination(val):
        simulation_settings['vaccination_rate'] = val
        simulation.config["vaccination_rate"] = val
    
    btn_social_dist.on_clicked(update_social_distance)
    btn_quarantine.on_clicked(update_quarantine)
    slider_vaccination.on_changed(update_vaccination)
    
    def update(frame):
        #Aktualizacja symulacji
        if frame > 0:
            simulation.simulate_day()
            simulation.record_stats()
        
        #Aktualizacja wykresu kropek
        x = [person.x for person in simulation.population]
        y = [person.y for person in simulation.population]
        
        #Kolorowanie osób na podstawie statusu, z gradientem dla zarażonych
        colors = []
        sizes = []
        
        for person in simulation.population:
            if person.status == "infected":
                #Gradient od jasnoczerwonego do ciemnoczerwonego w zależności od czasu infekcji
                infection_progress = min(person.days_infected / 14.0, 1.0)  #Normalizacja do max 14 dni
                r = 0.9 - 0.5 * infection_progress  #Od jasnego do ciemnego czerwonego
                g = 0.2 - 0.2 * infection_progress
                b = 0.2 - 0.2 * infection_progress
                colors.append((r, g, b))
                #Rozmiar rośnie wraz z czasem infekcji
                sizes.append(30 + 40 * infection_progress)
            elif person.status == "susceptible":
                colors.append(base_colors['susceptible'])
                sizes.append(30)
            elif person.status == "recovered":
                colors.append(base_colors['recovered'])
                sizes.append(30)
            else:  #deceased
                colors.append(base_colors['deceased'])
                sizes.append(20)  #Mniejszy rozmiar dla zmarłych
                
        scatter.set_offsets(np.c_[x, y])
        scatter.set_color(colors)
        scatter.set_sizes(sizes)
        
        #Aktualizacja wykresu statystyk
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
        
        #Aktualizacja informacji tekstowych
        day_text.set_text(f'Dzień: {stats["day"]}')
        
        #Dynamiczne statystyki
        stats_info = f'Podatni: {stats["susceptible"]} ({stats["susceptible"]/simulation.config["population_size"]:.1%})\n'
        stats_info += f'Zarażeni: {stats["infected"]} ({stats["infected"]/simulation.config["population_size"]:.1%})\n'
        stats_info += f'Ozdrowieńcy: {stats["recovered"]} ({stats["recovered"]/simulation.config["population_size"]:.1%})\n'
        stats_info += f'Zmarli: {stats["deceased"]} ({stats["deceased"]/simulation.config["population_size"]:.1%})'
        stats_text.set_text(stats_info)
        
        return scatter, susceptible_line, infected_line, recovered_line, deceased_line, day_text, stats_text
    
    ani = animation.FuncAnimation(
        fig, update, frames=simulation.config["simulation_days"]+1,
        interval=35, blit=True, repeat=False  
    )
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, bottom=0.15)
    plt.show()
    
    return ani
