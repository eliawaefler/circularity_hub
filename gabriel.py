import os
from PIL import Image
import streamlit as st
# import pandas as pd
# import pydeck as pdk

import streamlit as st
import os
from PIL import Image

def folien():
    # Hauptüberschrift
    st.title("Präsentation uptownBasel")
    st.write("02. Juli 2024")

    # Toggle-Option für Präsentationsmodus
    mode = st.radio("Präsentationsmodus", ("Slides", "Scrollen"))

    # Verzeichnis der Folien
    folien_dir = "./presi_folien/"

    # Themen und ihre Nummern
    themen = {
        "1": "Einführung",
        "2": "Demo",
        "3": "Scraper",
        "4": "ER / Bauteil",
        "5": "Skalierbarkeit",
        "6": "Handlungsempfehlung"
    }

    # Tabs für jedes Thema erstellen
    tabs = st.tabs(list(themen.values()))

    # Aktuellen Tab-Index in Session State initialisieren
    if 'tab_index' not in st.session_state:
        st.session_state.tab_index = 0

    # Den aktuellen Tab bestimmen
    current_tab = st.session_state.tab_index

    # Durch jedes Thema iterieren und die entsprechenden Folien anzeigen
    for thema_nummer, (thema_name, tab) in enumerate(zip(themen.keys(), tabs)):
        if thema_nummer != current_tab:
            continue
        with tab:
            # Dateien im Verzeichnis durchsuchen und filtern
            folien_files = sorted([f for f in os.listdir(folien_dir) if f.startswith(f"{thema_nummer + 1}_")])

            # Wenn keine Folien vorhanden sind, Nachricht anzeigen
            if not folien_files:
                st.write("Keine Folien verfügbar.")
                continue

            if mode == "Slides":
                # Session State für den Folienindex initialisieren
                if f"folien_index_{thema_nummer}" not in st.session_state:
                    st.session_state[f"folien_index_{thema_nummer}"] = 0

                # Pfeiltasten zur Navigation
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    if st.button("<_", key=f"prev_{thema_nummer}"):
                        if st.session_state[f"folien_index_{thema_nummer}"] > 0:
                            st.session_state[f"folien_index_{thema_nummer}"] -= 1
                with col2:
                    if st.button("_>", key=f"next_{thema_nummer}"):
                        if st.session_state[f"folien_index_{thema_nummer}"] < len(folien_files) - 1:
                            st.session_state[f"folien_index_{thema_nummer}"] += 1

                # Funktion für col3: Anzeige der Foliennummer
                with col3:
                    folien_index = st.session_state[f"folien_index_{thema_nummer}"]
                    st.write(f"Folie {folien_index + 1} von {len(folien_files)}")

                folien_index = st.session_state[f"folien_index_{thema_nummer}"]

                # Ausgewählte Folie
                selected_folie = folien_files[folien_index]
                folien_name = selected_folie.split('_', 1)[1].rsplit('.', 1)[0].replace('_', ' ').title()

                # Folienname und Bild anzeigen
                st.write(f"**{folien_name}**")

                # Bild öffnen, skalieren und anzeigen
                image_path = os.path.join(folien_dir, selected_folie)
                image = Image.open(image_path)
                image = image.resize((2160, int(2160 * image.height / image.width)))  # Skalieren auf feste Breite von 2160px
                st.image(image, caption=selected_folie)

            elif mode == "Scrollen":
                for folien_file in folien_files:
                    folien_name = folien_file.split('_', 1)[1].rsplit('.', 1)[0].replace('_', ' ').title()

                    # Folienname und Bild anzeigen
                    st.write(f"**{folien_name}**")

                    # Bild öffnen, skalieren und anzeigen
                    image_path = os.path.join(folien_dir, folien_file)
                    image = Image.open(image_path)
                    image = image.resize((2160, int(2160 * image.height / image.width)))  # Skalieren auf feste Breite von 2160px
                    st.image(image, caption=folien_file)


            # Handlungsempfehlungen nur im Tab 6 anzeigen
            if thema_nummer == 5:  # Tab 6 hat den Index 5
                st.markdown("## Handlungsempfehlung für uptownBasel")

                # Do
                st.markdown("### Do:")
                st.markdown("<span style='color: green;'>- **Bestehende Anwendungsfälle prüfen**: Stellen Sie sicher, dass alle aktuellen Anwendungsfälle klar verstanden und dokumentiert sind.</span>", unsafe_allow_html=True)
                st.markdown("<span style='color: green;'>- **Geschlossener Austausch**: Nutzen Sie das Areal von uptownBasel für den Austausch über Materialpass, Bestandsinventarisierung und Lean Deconstruction.</span>", unsafe_allow_html=True)
                st.markdown("<span style='color: green;'>- **Modellierungsrichtlinien aufarbeiten**: Definieren Sie klar die Bauteile und Baustoffe in Ihren Modellierungsrichtlinien.</span>", unsafe_allow_html=True)

                # Consider
                st.markdown("### Consider:")
                st.markdown("<span style='color: yellow;'>- **Vorreiterrolle übernehmen**: Nutzen Sie die Gelegenheit, eine führende Position im schweizerischen Rohstoff- und Bauteilhandel einzunehmen.</span>", unsafe_allow_html=True)
                st.markdown("<span style='color: yellow;'>- **Stakeholder einbeziehen**: Arbeiten Sie eng mit Lieferanten und Herstellern zusammen, um erste Anwendungsfälle zu identifizieren.</span>", unsafe_allow_html=True)

                # Don't
                st.markdown("### Don't:")
                st.markdown("<span style='color: red;'>- **Anwendungsfälle ohne klaren Nutzen einkaufen**: Vermeiden Sie den Erwerb von Anwendungsfällen zu Marketingzwecken ohne eine klare Vorstellung, welchen Nutzen sie für das Unternehmen bringen.</span>", unsafe_allow_html=True)



    
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
