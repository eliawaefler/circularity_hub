import streamlit as st
# import pandas as pd
# import pydeck as pdk


def speckle():
    st.title('Das Speckle Dashboard')
    
    # URL-Eingabefeld
    user_url = st.text_input('Gib die Speckle URL ein:', 'https://app.speckle.systems/projects/99d586a085')
    
    # Dropdown-Menü für vordefinierte URLs
    predefined_urls = {
        'Projekt Tür': 'https://app.speckle.systems/projects/99d586a085/models/405c047b71',
        'Projekt Fenster': 'https://app.speckle.systems/projects/99d586a085/models/ff98034292',
        'Projekt Gesamt': 'https://app.speckle.systems/projects/99d586a085/models/2ffc61a729'
    }
    selected_project = st.selectbox('Wähle ein vordefiniertes Projekt:', list(predefined_urls.keys()))
    
    # Verwende entweder die benutzerdefinierte URL oder die vordefinierte URL
    url = user_url if user_url else predefined_urls[selected_project]
    
    # Erstelle einen iframe, um die Webseite einzubetten
    iframe_code = f'<iframe src="{url}" width="150%" height="1000" style="border:none;"></iframe>'
    # Zeige den iframe im Streamlit Dashboard an
    st.markdown(iframe_code, unsafe_allow_html=True)
