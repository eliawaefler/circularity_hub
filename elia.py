import streamlit as st
import pandas as pd
import pydeck as pdk

def user_space():
    st.subheader("meine Projekte")
    if st.button("Neubau EFH Eichenstrasse 45"):
        show_construction_project()
    if st.button("Abbruch MFH Unterholzweg 13"):
        show_deconstruction_project()
    if st.button("neues Projekt"):
        new_project()

def show_deconstruction_project():
    st.subheader("Abbruch MFH Unterholzweg 13")
    st.button("Informationen erfassen")
    file_downloader()


def show_construction_project():
    st.subheader("Neubau EFH Eichenstrasse 45")
    st.button("InInformationen erfassen")
    if st.button("geeignete 'Materiallager' auf Karte anzeigen"):
        show_map()
    file_downloader()


def new_project():
    st.subheader("neues Projekt")
    st.radio("Projekttyp", ["Abbruch", "Neubau", "Umbau"])
    st.text_input("Projektname:")
    st.text_input("Adresse:")
    st.text_input("PLZ / Ort:")
    st.write("Upload files.")
    file_uploader()
    st.button("Process upload")


def goto_map():
    st.sidebar.radio("Go to Map View")


def set_username():
    st.session_state.user_pw = True


def add_tag():
    new_tag = st.session_state.tag_input
    if new_tag:  # Check if the input is not empty
        if 'tags' not in st.session_state:
            st.session_state.tags = [new_tag]
        else:
            st.session_state.tags.append(new_tag)
        st.session_state.tag_input = ''  # Clear the input box after adding


def show_map():
    st.title("Map View")
    st.write("Die besten Materiallager für dein Projekt.")
    # Sample data: Latitude and Longitude of some cities
    data = {
        "latitude": [47.559401, 47.55546, 47.519401],
        "longitude": [7.588576, 7.60522, 7.518576],
        "city": ["1", "2", "3"],
        "citydata": ["Industriestrasse 48: Score=0.971", "Althausstrasse 11: Score=0.921", "Kreuzweg 3: Score=0.913"]
    }
    df = pd.DataFrame(data)
    # Create a map using the data
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=47.6,
            longitude=7.588576,
            zoom=8.5,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=df,
                get_position='[longitude, latitude]',
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "TextLayer",
                data=df,
                get_position='[longitude, latitude]',
                get_text='city',
                get_size=30,
                elevation_range=[100, 1000],
                get_color=[0, 0, 0],
                get_angle=0,
                # Setting the text anchor and alignment to center
                get_text_anchor="'right'",
                get_alignment_baseline="'top'"
            )
        ],
    ))
    if st.button("back"):
        user_space()


def file_uploader():
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        st.write("Uploaded file is {} bytes long".format(len(bytes_data)))


def file_downloader():
    # Create a simple text file to download
    with open("example_text.txt", "w") as f:
        f.write("Here is some text that will be in the downloadable text file.")

    with open("example_text.txt", "rb") as f:
        st.download_button(
            label="Download Text File",
            data=f,
            file_name="example_text.txt",
            mime="text/plain"
        )

