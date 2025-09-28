import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Seitenkonfiguration für volle Breite
st.set_page_config(
    page_title="Bestellungen zur Abholung",
    layout="wide"
)

# Definiere den absoluten Pfad zur CSV-Datei
csv_file_path = r"C:\Users\Flo\NAS Cevi WIE\OK\Chilbi\2024_Chilbi\Abholsystem\bestellungen.csv"

# Logo oben links einfügen
logo_path = r"C:\Users\Flo\NAS Cevi WIE\OK\Chilbi\2024_Chilbi\Abholsystem\Logo.png"  # Pfad zum Logo anpassen
st.image(logo_path, width=300)

# Hintergrundfarbe und Schriftgrößen anpassen
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F0F0F0;  /* Hintergrundfarbe */
    }
    /* Header ausblenden */
    header {
        visibility: hidden; /* Header unsichtbar machen */
        height: 0; /* Höhe auf 0 setzen */
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
        st.session_state.neue_bestellnummer = ""
        st.rerun()

# Funktion, um den Status einer Bestellung zu aktualisieren
def bestellung_abholen(bestellnummer):
    df = pd.read_csv(csv_file_path)
    df.loc[df['Bestellnummer'] == bestellnummer, 'Status'] = "abgeholt"
    df.to_csv(csv_file_path, index=False)
    st.rerun()

# CSS zur Anpassung der Button-Größe
st.markdown("""
    <style>
    .stButton>button {
        height: 80px;
        width: 120px;
        font-size: 70px;
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

    col_c, col_zero, col_ok = st.columns([1, 1, 1])
    with col_c:
        if st.button("C", key="loeschen"):
            st.session_state.neue_bestellnummer = st.session_state.neue_bestellnummer[:-1]
    with col_zero:
        if st.button("0", key="button_0"):
            st.session_state.neue_bestellnummer += "0"
    with col_ok:
        if st.button("OK", key="eingabe"):
            neue_bestellung(st.session_state.neue_bestellnummer)

    st.text_input("Eingegebene Bestellnummer:", value=st.session_state.neue_bestellnummer, disabled=True)

with col2:
    st.subheader("Fertige Bestellungen zur Abholung:")  # Titel wieder hinzugefügt
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
        if not df.empty:
            # Erstelle eine Liste für die Buttons
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
        else:
            st.write("Keine aktuellen Bestellungen.")
    else:
        st.write("Keine aktuellen Bestellungen.")
