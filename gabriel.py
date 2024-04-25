import streamlit as st
# import pandas as pd
# import pydeck as pdk


def speckle():
    st.title('Webseite Einbetten')
    # Setze die URL, die du einbetten möchtest
    url = 'https://app.speckle.systems/projects/99d586a085'
    # Erstelle einen iframe, um die Webseite einzubetten
    iframe_code = f'<iframe src="{url}" width="150%" height="700" style="border:none;"></iframe>'
    # Zeige den iframe im Streamlit Dashboard an
    st.markdown(iframe_code, unsafe_allow_html=True)
