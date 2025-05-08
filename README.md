# ModelowanieISymulacja - Symulacja rozprzestrzeniania się chorób

## Opis projektu
Ten projekt implementuje symulację rozprzestrzeniania się chorób w populacji. Model uwzględnia:
- Zarażanie się przez kontakt między osobami
- Różne stany osób (podatne, zarażone, ozdrowieńcy, zmarli)
- Parametry choroby (zaraźliwość, śmiertelność, tempo zdrowienia)
- Interwencje (dystans społeczny)

## Wymagania
- Python 3.6+
- matplotlib
- numpy

## Uruchamianie symulacji

1. Dostosuj parametry symulacji w pliku `disease-simulation/config.py`
2. Uruchom symulację za pomocą:
   ```bash
   python disease-simulation/main.py
   ```
3. Wyniki zostaną wyświetlone w postaci wykresu i podsumowania w konsoli

## Parametry symulacji
- `population_size` - wielkość populacji
- `initial_infected` - początkowa liczba zarażonych
- `infection_rate` - prawdopodobieństwo zarażenia przy kontakcie
- `recovery_rate` - dzienna szansa na wyzdrowienie
- `mortality_rate` - śmiertelność choroby
- `immunity_period` - okres odporności po wyzdrowieniu
- `contacts_per_day` - średnia liczba kontaktów dziennie
- `social_distancing` - czy stosowane jest dystansowanie społeczne
- `simulation_days` - całkowity czas symulacji w dniach