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

        # Neue Zeile zur CSV-Datei mit Zeitstempel, Bestellnummer und Status "nicht abgeholt"
        neue_zeile = pd.DataFrame({
            'Zeitstempel': [timestamp],
            'Bestellnummer': [bestellnummer],
            'Status': ["nicht abgeholt"]
        })

        # Prüfen, ob die Datei existiert und nicht leer ist
        if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
            try:
                # Bestehende Datei laden
                df = pd.read_csv(csv_file_path)
                # Neue Zeile an den DataFrame anhängen
                df = pd.concat([neue_zeile, df], ignore_index=True)  # Neue Bestellungen oben
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

        # Seite neu laden
        st.rerun()

# Funktion, um den Status einer Bestellung zu aktualisieren
def bestellung_abholen(bestellnummer):
    # CSV-Datei laden
    df = pd.read_csv(csv_file_path)

    # Status der Bestellung auf "abgeholt" ändern
    df.loc[df['Bestellnummer'] == bestellnummer, 'Status'] = "abgeholt"

    # Aktualisierten DataFrame in die CSV-Datei speichern
    df.to_csv(csv_file_path, index=False)

    # Seite neu laden
    st.rerun()

# CSS zur Anpassung der Button-Größe
st.markdown("""
    <style>
    .stButton>button {
        height: 60px;
        width: 80px;
        font-size: 36px;
    }
    </style>
    """, unsafe_allow_html=True)

# Layout aufteilen in zwei Spalten
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Gib die abzuholende Bestellnummer ein:")

    # Digitale Zifferntastatur
    buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    cols = st.columns(3)

    # Erstelle die Zifferntastatur
    for i, button in enumerate(buttons):
        if cols[i % 3].button(button, key=f"button_{button}"):
            st.session_state.neue_bestellnummer += button

    # Zeige die 0 unter dem 8er Button, mit C und OK
    col_c, col_zero, col_ok = st.columns([1, 1, 1])  # Neue Zeilen für C, 0 und OK
    with col_c:
        if st.button("C", key="loeschen"):  # Löschen-Button auf "C" abgekürzt
            st.session_state.neue_bestellnummer = st.session_state.neue_bestellnummer[:-1]
    with col_zero:
        if st.button("0", key="button_0"):
            st.session_state.neue_bestellnummer += "0"
    with col_ok:
        if st.button("OK", key="eingabe"):  # Eingabe-Button auf "OK" abgekürzt
            neue_bestellung(st.session_state.neue_bestellnummer)

    # Anzeigen des aktuellen Wertes
    st.text_input("Eingegebene Bestellnummer:", value=st.session_state.neue_bestellnummer, disabled=True)

with col2:
    # Anzeigen der Bestellungen aus der CSV-Datei
    st.subheader("Fertige Bestellungen zur Abholung:")
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
        if not df.empty:
            for index, row in df.iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    # Farbe je nach Status festlegen
                    if row['Status'] == "abgeholt":
                        st.markdown(f"<span style='color: green;'>**Bestellnummer:** {row['Bestellnummer']} - **Status:** {row['Status']}</span>", unsafe_allow_html=True)
                    elif row['Status'] == "nicht abgeholt":
                        st.markdown(f"<span style='color: red;'>**Bestellnummer:** {row['Bestellnummer']} - **Status:** {row['Status']}</span>", unsafe_allow_html=True)
                with col2:
                    if row['Status'] == "nicht abgeholt":
                        if st.button(f"Abholen {row['Bestellnummer']}", key=f"abholen_{index}_{row['Bestellnummer']}"):
                            bestellung_abholen(row['Bestellnummer'])
        else:
            st.write("Keine aktuellen Bestellungen.")
    else:
        st.write("Keine aktuellen Bestellungen.")