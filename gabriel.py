import os
from PIL import Image
import streamlit as st
# import pandas as pd
# import pydeck as pdk

def display_presentation(slide_folder):
    themen = {
        "1": "Einführung",
        "2": "Datenbank",
        "3": "Demo",
        "4": "Bauteilerfassung",
        "5": "Skalierbarkeit",
        "6": "Handlungsempfehlung"
    }

    # Create tabs for each topic
    tabs = st.tabs([f"{key}: {value}" for key, value in themen.items()])

    # Iterate through each topic and display slides
    for i, (key, value) in enumerate(themen.items()):
        with tabs[i]:
            slide_files = sorted([f for f in os.listdir(slide_folder) if f.startswith(f"{key}_")])
            for slide in slide_files:
                slide_name = slide.split("_")[2].split(".")[0]
                st.markdown(f"### {slide_name}")
                image_path = os.path.join(slide_folder, slide)
                st.image(image_path, use_column_width=True)
                st.caption(slide)
                
            if i == 5:
                st.markdown("## Handlungsempfehlung für uptownBasel")

                # Do
                st.success("### Do:")
                st.write("**Bestehende Anwendungsfälle prüfen**: Stellen Sie sicher, dass alle aktuellen Anwendungsfälle klar verstanden und dokumentiert sind.")
                st.write("**Geschlossener Austausch**: Nutzen Sie das Areal von uptownBasel für den Austausch über Materialpass, Bestandsinventarisierung und Lean Deconstruction.")
                st.write("**Modellierungsrichtlinien aufarbeiten**: Definieren Sie klar die Bauteile und Baustoffe in Ihren Modellierungsrichtlinien.")

                # Consider
                st.warning("### Consider:")
                st.write("**Vorreiterrolle übernehmen**: Nutzen Sie die Gelegenheit, eine führende Position im schweizerischen Rohstoff- und Bauteilhandel einzunehmen.")
                st.write("**Stakeholder einbeziehen**: Arbeiten Sie eng mit Lieferanten und Herstellern zusammen, um erste Anwendungsfälle zu identifizieren.")

                # Don't
                st.error("### Don't:")
                st.write("**Anwendungsfälle ohne klaren Nutzen einkaufen**: Vermeiden Sie den Erwerb von Anwendungsfällen zu Marketingzwecken ohne eine klare Vorstellung, welchen Nutzen sie für das Unternehmen bringen.")
   
            # Add button to go to the next tab
            if i < len(tabs) - 1:
                if st.button(f"Next: {themen[str(i+2)]}"):
                    st.session_state["tab_index"] = i + 1
                    st.rerun()


def folien():
    # Hauptüberschrift
    st.title("Präsentation UptownBasel")
    st.write("02. Juli 2024")

    # Verzeichnis der Folien
    folien_dir = "./presi_folien/"
    display_presentation(folien_dir)
         
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
