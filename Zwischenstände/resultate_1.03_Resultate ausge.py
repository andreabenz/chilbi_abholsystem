import streamlit as st
import pandas as pd
import os

# Definiere den absoluten Pfad zur CSV-Datei
csv_file_path = r"D:\NAS_Cevi WIE\OKs\Chilbi\2024_Chilbi\Abholsystem\bestellungen.csv"

# Titel der Anwendung
st.title("Bereit zur Abholung:")

# Funktion, um die Bestellungen zu laden
def lade_bestellungen():
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
        return df
    return pd.DataFrame(columns=['Zeitstempel', 'Bestellnummer', 'Status'])

# Anzeigen der Bestellungen aus der CSV-Datei
df = lade_bestellungen()
if not df.empty:
    # Filtern nach Bestellungen mit dem Status "nicht abgeholt"
    nicht_abgeholt_df = df[df['Status'] == "nicht abgeholt"]

    if not nicht_abgeholt_df.empty:
        for index, row in nicht_abgeholt_df.iterrows():
            # Anzeige der Bestellnummer als nicht-interaktive Schaltfläche
            st.text(f"Bestellnummer: {row['Bestellnummer']}")
else:
    st.write("Die Datei 'bestellungen.csv' ist leer oder nicht vorhanden.")