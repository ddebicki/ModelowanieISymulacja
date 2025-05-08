# Symulacja Rozprzestrzeniania się Chorób

## Opis projektu
Zaawansowany symulator rozprzestrzeniania się chorób z wizualizacją w czasie rzeczywistym i różnymi modelami epidemiologicznymi:

- **Wizualizacja przestrzenna** - pokazuje populację jako kropki poruszające się w przestrzeni 2D
- **Statystyki w czasie rzeczywistym** - wykresy pokazujące rozwój epidemii
- **Interaktywne sterowanie** - możliwość włączania i wyłączania interwencji w trakcie symulacji
- **Różne modele epidemiologiczne** - standardowy, SIR, SEIR, model sieciowy

## Modele epidemiologiczne

1. **Model standardowy** - oparty na interakcjach i odległościach między osobami
2. **Model SIR** - klasyczny model Susceptible-Infected-Recovered
3. **Model SEIR** - rozszerzony model uwzględniający fazę ekspozycji
4. **Model sieciowy** - symulacja rozprzestrzeniania się choroby w sieci społecznej

## Uruchamianie symulacji

### Podstawowe uruchomienie:
```bash
python main.py
```

### Z parametrami:
```bash
python main.py --population 2000 --days 150 --infected 10 --algorithm SEIR --visual
```

### Dostępne parametry:
- `--population` - wielkość populacji
- `--days` - liczba dni symulacji
- `--infected` - początkowa liczba zarażonych
- `--algorithm` - wybór algorytmu (standard, SIR, SEIR, network)
- `--visual` - aktywacja wizualizacji w czasie rzeczywistym
- `--distancing` - aktywacja dystansu społecznego

## Interakcja podczas symulacji
Podczas działania wizualizacji w czasie rzeczywistym można:
- Włączyć/wyłączyć dystans społeczny
- Włączyć/wyłączyć kwarantannę
- Ustawić poziom szczepień

## Wymagania
- Python 3.6+
- matplotlib
- numpy
