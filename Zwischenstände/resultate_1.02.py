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
            col1, col2 = st.columns([3, 1])
            with col1:
                # Anzeige der Bestellnummer in einem Textfeld
                st.text(f"Bestellnummer: {row['Bestellnummer']}")  # Verwendung von st.text für nicht-interaktive Anzeige
            with col2:
                # Hier kannst du die Schaltfläche zum Abholen der Bestellung anzeigen
                st.button(f"Abholen {row['Bestellnummer']}", key=f"abholen_{index}_{row['Bestellnummer']}")
    else:
        st.write("Keine Bestellungen abholbereit.")
else:
    st.write("Die Datei 'bestellungen.csv' ist leer oder nicht vorhanden.")

# Funktion, um den Status einer Bestellung zu aktualisieren
def bestellung_abholen(bestellnummer):
    df = pd.read_csv(csv_file_path)
    df.loc[df['Bestellnummer'] == bestellnummer, 'Status'] = "abgeholt"
    df.to_csv(csv_file_path, index=False)