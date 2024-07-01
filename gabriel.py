import os
from PIL import Image
import streamlit as st
from io import BytesIO
# import pandas as pd
# import pydeck as pdk

# Cache function to load image bytes
@st.cache_data
def load_image_bytes(file_path):
    try:
        with Image.open(file_path) as img:
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format=img.format)
            img_byte_arr = img_byte_arr.getvalue()
            return img_byte_arr
    except Exception as e:
        return None, str(e)

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
            if f"folien_files_{thema_nummer}" not in st.session_state:
                st.session_state[f"folien_files_{thema_nummer}"] = sorted(
                    [f for f in os.listdir(folien_dir) if f.startswith(f"{thema_nummer}_")]
                )

            folien_files = st.session_state[f"folien_files_{thema_nummer}"]

            # Wenn keine Folien vorhanden sind, Nachricht anzeigen
            if not folien_files:
                st.write("Keine Folien verfügbar.")
                continue

            # Session State für den Folienindex initialisieren
            if f"folien_index_{thema_nummer}" not in st.session_state:
                st.session_state[f"folien_index_{thema_nummer}"] = 0

            folien_index = st.session_state[f"folien_index_{thema_nummer}"]

            # Pfeiltasten zur Navigation und Folien-Count anzeigen
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("<_", key=f"prev_{thema_nummer}"):
                    if st.session_state[f"folien_index_{thema_nummer}"] > 0:
                        st.session_state[f"folien_index_{thema_nummer}"] -= 1
                        folien_index = st.session_state[f"folien_index_{thema_nummer}"]

            with col2:
                if folien_index < len(folien_files) - 1:
                    if st.button("_>", key=f"next_{thema_nummer}"):
                        st.session_state[f"folien_index_{thema_nummer}"] += 1
                        folien_index = st.session_state[f"folien_index_{thema_nummer}"]

            with col3:
                st.write(f"Folie {folien_index + 1} von {len(folien_files)}")

            # Ausgewählte Folie
            selected_folie = folien_files[folien_index]
            folien_name = selected_folie.split('_', 1)[1].rsplit('.', 1)[0].replace('_', ' ').title()

            # Folienname anzeigen
            st.write(f"**{folien_name}**")

            file_path = os.path.join(folien_dir, selected_folie)

            # Bild anzeigen
            img_bytes, error = load_image_bytes(file_path)
            if img_bytes:
                st.image(img_bytes, caption=selected_folie)
            else:
                st.error(f"Fehler beim Laden der Folie {file_path}: {error}")




    
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
