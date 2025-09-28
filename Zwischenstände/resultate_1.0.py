import streamlit as st
import pandas as pd

# Funktion, um die CSV-Datei zu lesen
def lade_bestellungen():
    try:
        return pd.read_csv("bestellungen.csv")["Bestellnummer"].tolist()
    except FileNotFoundError:
        return []

# Funktion, um eine Bestellung zu löschen
def bestellung_abholen(bestellnummer):
    bestellungen = lade_bestellungen()
    bestellungen.remove(bestellnummer)
    pd.DataFrame(bestellungen, columns=["Bestellnummer"]).to_csv("bestellungen.csv", index=False)

# Titel der Anwendung
st.title("Bestellabholung - Resultate")

# Anzeige der aktuellen Bestellungen
bestellungen = lade_bestellungen()
if bestellungen:
    st.subheader("Fertige Bestellungen zur Abholung:")
    for bestellung in bestellungen:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Bestellnummer:** {bestellung}")
        with col2:
            if st.button(f"Abholen {bestellung}", key=bestellung):
                bestellung_abholen(bestellung)
                st.success(f"Bestellung {bestellung} wurde abgeholt!")
else:
    st.write("Keine aktuellen Bestellungen.")
