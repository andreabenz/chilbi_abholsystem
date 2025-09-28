# Chilbi Abholsystem

Abholsystem für die Chilbi des Cevi Wiesendangen-Elsai-Hegi

Ein einfaches Abholsystem, entwickelt mit [Streamlit](https://streamlit.io/)
Das System ermöglicht es, Bestellungen einzugeben, ihren Status zu verwalten und den Abholprozess übersichtlich darzustellen.

## Installation und Nutzung

1. Repository clonen und in [eingabe.py](eingabe.py), [resultate.py](resultate.py) und [start_abholsystem.py](start_abholsystem.py) die Paths anpassen.


2. bestellungen.csv mit folgenden Spalten erstellen
```csv
Zeitstempel | Bestellnummer | Status
```

3. Dependencies Installieren:
```bash
cd Abholsystem
pip install streamlit pandas
```

4. Danach kann das System ausgeführt werden
```bash
streamlit run start_abholsystem
```