import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Seitenkonfiguration für volle Breite
st.set_page_config(
    page_title="Bestellungen zur Abholung",
    layout="wide"
)

# Definiere den absoluten Pfad zur CSV-Datei und zur Audio-Datei
csv_file_path = r"C:\Users\Flo\NAS Cevi WIE\OK\Chilbi\2024_Chilbi\Abholsystem\bestellungen.csv"
audio_file_path = r"C:\Users\Flo\NAS Cevi WIE\OK\Chilbi\2024_Chilbi\Abholsystem\Glocke.mp3"

# Logo oben links einfügen
logo_path = r"C:\Users\Flo\NAS Cevi WIE\OK\Chilbi\2024_Chilbi\Abholsystem\Logo.png"
st.image(logo_path, width=300)

# Hintergrundfarbe und Schriftgrößen anpassen
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFFFFF;  /* Hintergrundfarbe */
    }
    /* Header ausblenden */
    header {
        visibility: hidden; /* Header unsichtbar machen */
        height: 0; /* Höhe auf 0 setzen */
    }   
    /* Farbe des Eingabefeldes ändern */
    .stTextInput > div > input {
        background-color: #006400;  /* Grün */
        color: black;  /* Textfarbe */
    }
    /* Vergrößere die Bestellnummer */
    .bestellnummer {
        font-size: 50px; 
        font-weight: bold;
        color: #323394;
    }
    /* Anpassung der Button-Stile */
    .stButton>button {
        height: 80px;
        width: 120px;
        border: 2px solid #990000; 
        font-size: 40px;  /* Schriftgröße */
        color: #323394;  /* Schriftfarbe */
        background-color: white;  /* Hintergrundfarbe */
    }
    .stButton>button:hover {
        background-color: #D3D3D3;  /* Hintergrundfarbe beim Hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialisiere die Liste der Bestellungen im Session State
if 'bestellungen' not in st.session_state:
    st.session_state.bestellungen = []

# Initialisiere die Bestellnummer im Session State
if 'neue_bestellnummer' not in st.session_state:
    st.session_state.neue_bestellnummer = ""

# Initialisiere den Audio-Status im Session State
if 'audio_played' not in st.session_state:
    st.session_state.audio_played = False

# Funktion, um eine neue Bestellung hinzuzufügen und in die CSV-Datei zu schreiben
def neue_bestellung(bestellnummer):
    if bestellnummer:
        st.session_state.bestellungen.append(bestellnummer)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        neue_zeile = pd.DataFrame({
            'Zeitstempel': [timestamp],
            'Bestellnummer': [bestellnummer],
            'Status': ["nicht abgeholt"]
        })

        if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
            try:
                df = pd.read_csv(csv_file_path)
                df = pd.concat([neue_zeile, df], ignore_index=True)
            except pd.errors.EmptyDataError:
                df = neue_zeile
        else:
            df = neue_zeile

        df.to_csv(csv_file_path, index=False)

        return True  # Rückgabe für die Audio-Wiedergabe

    return False

# Funktion, um den Status einer Bestellung zu aktualisieren
def bestellung_abholen(bestellnummer):
    df = pd.read_csv(csv_file_path)
    df.loc[df['Bestellnummer'] == bestellnummer, 'Status'] = "abgeholt"
    df.to_csv(csv_file_path, index=False)
    st.rerun()

# Funktion, um den Status einer Bestellung zurückzusetzen
def bestellung_zuruecksetzen(bestellnummer):
    df = pd.read_csv(csv_file_path)
    df.loc[df['Bestellnummer'] == bestellnummer, 'Status'] = "nicht abgeholt"
    df.to_csv(csv_file_path, index=False)
    st.rerun()

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

    col_c, col_zero, col_ok = st.columns([1, 1, 1])
    with col_c:
        if st.button("C", key="loeschen"):
            st.session_state.neue_bestellnummer = ""  # Leere das gesamte Eingabefeld
    with col_zero:
        if st.button("0", key="button_0"):
            st.session_state.neue_bestellnummer += "0"
    with col_ok:
        if st.button("OK", key="eingabe"):
            if neue_bestellung(st.session_state.neue_bestellnummer):
                st.session_state.neue_bestellnummer = ""  # Leere das Eingabefeld nach Bestätigung
                st.session_state.audio_played = True  # Setze Audio-Status auf True

    st.text_input("Eingegebene Bestellnummer:", value=st.session_state.neue_bestellnummer, disabled=True)

    # Audio-Icon unterhalb des Eingabefeldes einfügen
    if st.session_state.audio_played:
        st.audio(audio_file_path, autoplay=True)  # Spiele die Audio-Datei ab und zeige das Audio-Icon an
        st.session_state.audio_played = False  # Setze Audio-Status zurück

with col2:
    st.subheader("Fertige Bestellungen zur Abholung:")  # Titel wieder hinzugefügt
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
        if not df.empty:
            # Erstelle eine Liste für die Buttons für nicht abgeholte Bestellungen
            buttons = []
            for index, row in df.iterrows():
                if row['Status'] == "nicht abgeholt":
                    buttons.append(row['Bestellnummer'])

            # Teile die Buttons in zwei Spalten auf
            cols = st.columns(2)
            for i, button in enumerate(buttons):
                col_index = i % 2
                with cols[col_index]:
                    if st.button(f"Abholen {button}", key=f"abholen_{button}"):
                        bestellung_abholen(button)

            # Füge den horizontalen Strich hinzu
            st.markdown("<hr>", unsafe_allow_html=True)  # Hier wird die Linie hinzugefügt
            
            # Abgeholte Bestellungen auflisten
            st.subheader("Abgeholte Bestellungen:")
            abgeholte_buttons = df[df['Status'] == "abgeholt"]['Bestellnummer'].tolist()

            # Erstelle Buttons für die abgeholten Bestellungen
            if abgeholte_buttons:
                cols_abgeholt = st.columns(2)
                for i, button in enumerate(abgeholte_buttons):
                    col_index = i % 2
                    with cols_abgeholt[col_index]:
                        if st.button(f"Bestellung {button} zurücksetzen", key=f"zuruecksetzen_{button}"):
                            bestellung_zuruecksetzen(button)  # Setze den Status zurück
            else:
                st.write("Keine abgeholten Bestellungen.")
        else:
            st.write("Keine aktuellen Bestellungen.")
    else:
        st.write("Keine aktuellen Bestellungen.")
