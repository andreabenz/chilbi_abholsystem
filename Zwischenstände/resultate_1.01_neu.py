import streamlit as st
import pandas as pd
import os

# Definiere den Pfad zur CSV-Datei
csv_file_path = r"D:\NAS_Cevi WIE\OKs\Chilbi\2024_Chilbi\Abholsystem\bestellungen.csv"

# Titel der Anwendung
st.title("Bestellübersicht")

# Funktion, um die Bestellungen zu laden
def lade_bestellungen():
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
        return df
    return pd.DataFrame(columns=['Zeitstempel', 'Bestellnummer', 'Status'])

# Bestellungen laden
df = lade_bestellungen()

# Überprüfen, ob der DataFrame nicht leer ist
if not df.empty:
    # Filtern nach Bestellungen mit dem Status "nicht abgeholt"
    nicht_abgeholt_df = df[df['Status'] == "nicht abgeholt"]

    if not nicht_abgeholt_df.empty:
        st.subheader("Bestellungen nicht abgeholt:")
        st.write(nicht_abgeholt_df[['Bestellnummer', 'Status']])  # Anzeige nur der Bestellnummern und Status
    else:
        st.write("Keine Bestellungen mit dem Status 'nicht abgeholt' gefunden.")
else:
    st.write("Die Datei 'bestellungen.csv' ist leer oder nicht vorhanden.")