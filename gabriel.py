import streamlit as st
# import pandas as pd
# import pydeck as pdk

def folien():
    #hier code einfügen.
    return 0

    
def speckle():
    st.title('Das Speckle Dashboard')
    
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
