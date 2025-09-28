import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Definiere den absoluten Pfad zur CSV-Datei
csv_file_path = r"C:\Users\Flo\NAS Cevi WIE\OK\Chilbi\2024_Chilbi\Abholsystem\bestellungen.csv"

# Initialisiere die Liste der Bestellungen im Session State
if 'bestellungen' not in st.session_state:
    st.session_state.bestellungen = []

# Initialisiere die Bestellnummer im Session State
if 'neue_bestellnummer' not in st.session_state:
    st.session_state.neue_bestellnummer = ""

# Funktion, um eine neue Bestellung hinzuzufügen und in die CSV-Datei zu schreiben
def neue_bestellung(bestellnummer):
    if bestellnummer:
        # Bestellnummer zur Session State Liste hinzufügen
        st.session_state.bestellungen.append(bestellnummer)

        # Zeit- und Datumsstempel generieren
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Neue Zeile zur CSV-Datei mit Zeitstempel, Bestellnummer und Status "nein"
        neue_zeile = pd.DataFrame({
            'Zeitstempel': [timestamp],
            'Bestellnummer': [bestellnummer],
            'Status': ["nein"]  # Status-Spalte mit dem Wert "nein"
        })

        # Prüfen, ob die Datei existiert und nicht leer ist
        if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
            try:
                # Bestehende Datei laden
                df = pd.read_csv(csv_file_path)
                # Neue Zeile an den DataFrame anhängen
                df = pd.concat([df, neue_zeile], ignore_index=True)
            except pd.errors.EmptyDataError:
                # Datei existiert, ist aber leer - neuen DataFrame erstellen
                df = neue_zeile
        else:
            # Datei existiert nicht oder ist leer - neuen DataFrame erstellen
            df = neue_zeile

        # DataFrame in die CSV-Datei speichern
        df.to_csv(csv_file_path, index=False)

        # Leeren des Eingabefeldes
        st.session_state.neue_bestellnummer = ""

# Funktion, um eine Bestellung abzuholen und den Status zu aktualisieren
def bestellung_abholen(bestellnummer):
    # CSV-Datei laden
    df = pd.read_csv(csv_file_path)

    # Status der Bestellung auf "ja" ändern
    df.loc[df['Bestellnummer'] == bestellnummer, 'Status'] = "ja"

    # Aktualisierten DataFrame in die CSV-Datei speichern
    df.to_csv(csv_file_path, index=False)

    # Bestellung aus der Session State Liste entfernen
    st.session_state.bestellungen.remove(bestellnummer)

# Titel der Anwendung
st.title("Bestellabholung")

# Digitale Zifferntastatur
st.subheader("Gib die Bestellnummer ein:")
cols = st.columns(3)
buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Löschen', 'Bestellung hinzufügen']

for i, button in enumerate(buttons):
    if i < 10:  # Zifferntasten
        if cols[i % 3].button(button):
            st.session_state.neue_bestellnummer += button
    elif button == 'Löschen':
        if cols[i % 3].button(button):
            st.session_state.neue_bestellnummer = st.session_state.neue_bestellnummer[:-1]
    elif button == 'Bestellung hinzufügen':
        if cols[i % 3].button(button):
            neue_bestellung(st.session_state.neue_bestellnummer)

# Anzeigen des aktuellen Wertes
st.text_input("Eingegebene Bestellnummer:", value=st.session_state.neue_bestellnummer, disabled=True)

# Anzeige der aktuellen Bestellungen
if st.session_state.bestellungen:
    st.subheader("Fertige Bestellungen zur Abholung:")
    for bestellung in st.session_state.bestellungen:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Bestellnummer:** {bestellung}")
        with col2:
            if st.button(f"Abholen {bestellung}", key=bestellung):
                bestellung_abholen(bestellung)
                st.success(f"Bestellung {bestellung} wurde abgeholt!")
else:
    st.write("Keine aktuellen Bestellungen.")