import streamlit as st

# Initialisiere die Liste der Bestellungen im Session State
if 'bestellungen' not in st.session_state:
    st.session_state.bestellungen = []

# Initialisiere die Bestellnummer im Session State
if 'neue_bestellnummer' not in st.session_state:
    st.session_state.neue_bestellnummer = ""

# Funktion, um eine neue Bestellung hinzuzufügen
def neue_bestellung(bestellnummer):
    if bestellnummer:
        st.session_state.bestellungen.append(bestellnummer)
        st.session_state.neue_bestellnummer = ""  # Leeren des Eingabefeldes

# Funktion, um eine Bestellung zu löschen
def bestellung_abholen(bestellnummer):
    st.session_state.bestellungen.remove(bestellnummer)

# Tabs erstellen
eingabe_tab, resultate_tab = st.tabs(["Eingabe", "Resultate"])

# Tab für die Eingabe der Bestellungen
with eingabe_tab:
    st.title("Bestellabholung - Eingabe")

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

# Tab für die Anzeige der Resultate
with resultate_tab:
    st.title("Bestellabholung - Resultate")

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
