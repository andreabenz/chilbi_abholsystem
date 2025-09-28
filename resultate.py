import streamlit as st
import pandas as pd
import os
import time

# Seitenkonfiguration für volle Breite
st.set_page_config(
    page_title="Bestellungen zur Abholung",
    layout="wide"
)

# Definiere den absoluten Pfad zur CSV-Datei
csv_file_path = r"C:\Users\Cevi WIE\Abholsystem\bestellungen.csv"

# Logo oben links einfügen
logo_path = r"C:\Users\Cevi WIE\Abholsystem\Logo.png" # Pfad zum Logo anpassen
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
    /* Schriftgröße anpassen */
    .stMarkdown, .stText {
        font-size: 10px;  /* Schriftgröße für den Text */
    }
    /* Vergrößere die Container */
    .container {
        border: 5px solid #990000; 
        border-radius: 15px; 
        padding: 20px; 
        margin: 10px; 
        text-align: center; 
        width: 300px;
        max-height: 180px;
        line-height: 120px;
    }
    /* Vergrößere die Bestellnummer */
    .bestellnummer {
        font-size: 150px; 
        font-weight: bold;
    }
    /* Titelgröße und Schriftart anpassen */
    h1 {
        font-size: 50px;  /* Schriftgröße für den Titel */
        font-weight: bold; /* Optional: Fett */
        font-family: 'Montserrat', sans-serif; /* Schriftart anpassen */
        text-align: center; /* Zentrieren */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Hintergrundfarbe und Schriftgrößen anpassen
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFFFFF;  /* Hintergrundfarbe */
    }
    /* Schriftgröße anpassen */
    .stMarkdown, .stText {
        font-size: 10px;  /* Schriftgröße für den Text */
    }
    /* Vergrößere die Container */
    .container {
        border: 2px solid #C41333; 
        border-radius: 15px; 
        padding: 20px; 
        margin: 10px; 
        text-align: center; 
        width: 100%;  /* Volle Breite nutzen */
    }
    /* Vergrößere die Bestellnummer */
    .bestellnummer {
        font-size: 200px; 
        font-weight: bold;
        color: #323394
    }
    /* Titelgröße und Schriftart anpassen */
    .custom-title {
        font-size: 80px;  /* Schriftgröße für den Titel */
        font-weight: bold; /* Fett */
        font-family: 'Montserrat', sans-serif; /* Schriftart anpassen */
        text-align: center; /* Zentrieren */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Titel der Anwendung in einer Zeile
st.markdown('<h1 class="custom-title">Bereit zur Abholung:</h1>', unsafe_allow_html=True)


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
        cols = st.columns(2)  # Zwei Spalten erstellen
        for index, row in nicht_abgeholt_df.iterrows():
            # Bestellnummer in der ersten Spalte
            with cols[index % 2]:  # Verteile die Bestellnummern auf die Spalten
                st.markdown(
                    f"<div class='container'>"
                    f"<span class='bestellnummer'>{row['Bestellnummer']}</span></div>", 
                    unsafe_allow_html=True
                )
else:
    st.write("Die Datei 'bestellungen.csv' ist leer oder nicht vorhanden.")


time.sleep(1)
st.rerun()