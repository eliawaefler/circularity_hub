import streamlit as st
import os
# import pandas as pd
# import pydeck as pdk

# Funktion zur Anzeige der Folien
def folien():
    # Hauptüberschrift
    st.title("Präsentation")

    # Verzeichnis der Folien
    folien_dir = "./presi_folien/"

    # Themen und ihre Nummern
    themen = {
        "1": "Einführung",
        "2": "Demo",
        "3": "Scraper",
        "4": "ER / Bauteil",
        "5": "Skalierbarkeit",
        "6": "Potenzial / Abschluss / Handlungsempfehlung"
    }

    # Tabs für jedes Thema erstellen
    tabs = st.tabs(list(themen.values()))

    # Durch jedes Thema iterieren und die entsprechenden Folien anzeigen
    for thema_nummer, (thema_name, tab) in enumerate(zip(themen.keys(), tabs), start=1):
        with tab:
            # Dateien im Verzeichnis durchsuchen und filtern
            folien_files = sorted([f for f in os.listdir(folien_dir) if f.startswith(f"{thema_nummer}_")])

            # Wenn keine Folien vorhanden sind, Nachricht anzeigen
            if not folien_files:
                st.write("Keine Folien verfügbar.")
                continue

            # Slider zur Auswahl der Folie -> evtl. mit Pfeil-slider
            folien_index = st.slider(f"Wähle eine Folie für {thema_name}", 0, len(folien_files)-1, 0)
            
            # Ausgewählte Folie anzeigen (Anzeigen von path für Legende)
            selected_folie = folien_files[folien_index]
            st.image(os.path.join(folien_dir, selected_folie), caption=selected_folie)
    
def speckle():
    st.title('BIM-Hub Dashboard')
    
    # Initialisiere die Session State, falls noch nicht geschehen
    if 'url' not in st.session_state:
        st.session_state['url'] = 'https://app.speckle.systems/projects/99d586a085'

    # URL-Eingabefeld
    user_url = st.text_input('Gib die Speckle URL ein:', st.session_state['url'])

    # Dropdown-Menü für vordefinierte URLs
    predefined_urls = {
        'Tür': 'https://app.speckle.systems/projects/99d586a085/models/405c047b71',
        'Betonmasse': 'https://app.speckle.systems/projects/99d586a085/models/ff98034292',
        'Waschbecken': 'https://app.speckle.systems/projects/99d586a085/models/77a1abfe44',
        'Gesamt': 'https://app.speckle.systems/projects/99d586a085/models/2ffc61a729'
    }
    selected_project = st.selectbox('Wähle ein vordefiniertes Projekt:', [''] + list(predefined_urls.keys()))

    # Update the URL based on the dropdown selection
    if selected_project:
        st.session_state['url'] = predefined_urls[selected_project]
    
    # Verwende entweder die benutzerdefinierte URL oder die vordefinierte URL
    url = st.session_state['url']

    # Erstelle einen iframe, um die Webseite einzubetten
    iframe_code = f'<iframe src="{url}" width="100%" height="800" style="border:none;"></iframe>'
    # Zeige den iframe im Streamlit Dashboard an
    st.markdown(iframe_code, unsafe_allow_html=True)
