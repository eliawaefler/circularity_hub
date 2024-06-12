from random import random

import streamlit as st
import pandas as pd
import pydeck as pdk
from PIL import Image
import os
import uuid
import json
import psycopg2
from psycopg2 import sql
import neon




def create_project(project_type, project_name, address, speckle_link, plz_ort, uploaded_files, baujahr, reno_jahr,
                   geb_lang, geb_breit, geb_hoch, mat_wand, mat_fen, mat_tur):
    if not os.path.exists('database/user_images'):
        os.makedirs('database/user_images')

    file_guids = {}
    for file in uploaded_files:
        guid = str(uuid.uuid4())
        file_path = os.path.join('database/user_images', f'{guid}.jpg')
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        file_guids[file.name] = guid

    project_data = {
        "pk": str(uuid.uuid4()),
        "author_type": "user",
        "author_name": st.session_state.username,
        "name": project_name,
        "project_type": project_type,
        "address": address,
        "zip_code": plz_ort.split('/')[0].strip(),
        "city": plz_ort.split('/')[1].strip(),
        "year_built": baujahr,
        "last_renovation": reno_jahr,
        "expected_deconstruction": str(int(baujahr) + 50),
        "volume_m3": str(int(geb_lang) * int(geb_hoch) * int(geb_breit)),
        "length_m": geb_lang,
        "width_m": geb_breit,
        "height_m": geb_hoch,
        "walls_type": mat_wand,
        "windows": mat_fen,
        "doors": mat_tur,
        "speckle_link": speckle_link,
        "files": json.dumps(file_guids)
    }

    #insert_project_data(project_data)

def user_space():
    if st.session_state.user_space in ["menu", "map"]:
        if st.button("neues Projekt"):
            st.session_state.user_space = "new"

        my_projects = neon.read_db(st.secrets["NEON_URL"], "geb",
                                   condition=f"user_name = '{st.session_state.username}'")
        l, r = st.columns(2)
        with l:
            st.subheader("meine Projekte")
            #st.write(my_projects)
            for p in my_projects:
                if st.button(str(p[1])):
                    st.session_state.user_space = "menu"
                    st.subheader(str(p[1]))
                    st.write(f"projektinformationen: Adresse: {p[2]}, Typ: {p[4]}, Baujahr: {p[6]}")
                    all_p = neon.read_db(st.secrets["NEON_URL"], "geb", condition=f"typ <> '{p[7]}'")
                    sorted_p = sorted(all_p, key=lambda x: abs(x[6]-p[6]+50))
                    st.write("")
                    st.write("Hier die besten Matches für Dein Projekt:")
                    for match in sorted_p[:3]:
                        st.write(f"{sorted_p.index(match)+1}. das Projekt **{match[1]}**, *{match[2]}* "
                                 f"ist ein Typ *{match[4]}* mit Baujahr *{match[6]}*.   "
                                 f"Deine Kontaktperson ist **{match[3]}**.")
                    st.session_state.user_space = "map"
                    st.write("")
                    st.write("")
        with r:
            if st.session_state.user_space == "map":
                show_map()


    elif st.session_state.user_space == "new":
        def mock_project():
            # Define the page layout and form elements
            st.title("Data Entry for Building")
            with st.form("building_form"):
                # Fields for user to fill
                baujahr = st.number_input('Baujahr', min_value=1900, max_value=2050, value=1990, step=1)
                nutzung_options = ['Wohnen', 'Gewerbe', 'Industrie', 'Landwirtschaft']
                nutzung = st.selectbox('Nutzung', options=nutzung_options)
                typ_options = ['neu', 'abbruch', 'umbau', 'andere']
                typ = st.selectbox('Typ', options=typ_options)
                name = st.text_input('Name des Gebäudes', max_chars=200)
                adresse = st.text_input('Adresse')
                ort = st.text_input('Ort')
                files = st.file_uploader("Upload Project Files")
                # Submit button
                submitted = st.form_submit_button("Submit")

                if submitted:
                    # Create data object
                    next_id = len(neon.read_db(st.secrets["NEON_URL"], "geb")) + 1
                    data = {
                        # 'id': int(sha256.sha_dez(f"{name}+{time.time()}")),   DAS Wäre für unique id
                        'id': next_id,
                        'baujahr': baujahr,
                        'user_name': st.session_state['username'],
                        'nutzung': nutzung,
                        'datenstufe': '3' if baujahr and nutzung and typ and name and adresse and ort else '2',
                        'autor': 'webscraper',
                        'typ': typ,
                        'name': name,
                        'adresse': f"{adresse} {ort}"
                    }
                    with st.spinner("adding to db"):

                        add_2_db_res = neon.write_to_db(st.secrets["NEON_URL"], "geb", data)
                        if add_2_db_res == "":
                            st.success("entry added to db")
                        else:
                            st.error(add_2_db_res)

        def mock_project_old():
            st.subheader("Neues Projekt")
            project_type = st.radio("Projekttyp", ["Abbruch", "Neubau", "Umbau"])
            project_name = st.text_input("Projektname:")
            address = st.text_input("Strasse, Hausnummer")
            plz_ort = st.text_input("PLZ / Ort: (zwingend mit / trennen)")
            baujahr = st.text_input("Baujahr: [YYYY]")
            reno_jahr = st.text_input("letzte Renovierung Jahr: [YYYY]")
            geb_lang = st.text_input("Gebäudelänge: [m]")
            geb_breit = st.text_input("Gebäudebreite: [m]")
            geb_hoch = st.text_input("Gebäudehöhe: [m]")
            uploaded_files = st.file_uploader("Upload files, IFC, PDF-Pläne, Bilder, usw", accept_multiple_files=True)
            speckle_link = st.text_input("Speckle link: ")
            mat_wand = st.text_input("Material Wände: ")
            mat_fen = st.text_input("Fenster Material (HolzMetall, Holz, ...): ")
            mat_tur = st.text_input("Tür Materialisierung: ")

            if st.button("Process upload"):
                with st.spinner("Processing"):
                    if uploaded_files:
                        create_project(project_type, project_name, address, speckle_link, plz_ort, uploaded_files,
                                       baujahr, reno_jahr, geb_lang, geb_breit, geb_hoch, mat_wand, mat_fen, mat_tur)
                        st.success("Upload successful")
                    else:
                        st.error("Please upload at least one file.")
                st.session_state.user_space = "menu"
        mock_project()
        if st.button("Back"):
            st.session_state.user_space = "menu"



def set_username():
    st.session_state.user_logged_in = True


def add_tag():
    new_tag = st.session_state.tag_input
    if new_tag:  # Check if the input is not empty
        if 'tags' not in st.session_state:
            st.session_state.tags = [new_tag]
        else:
            st.session_state.tags.append(new_tag)
        st.session_state.tag_input = ''  # Clear the input box after adding


def show_map():
    st.subheader("Map View")
    st.write("Die besten Materiallager für dein Projekt.")
    # Sample data: Latitude and Longitude of some cities
    r = random.randint(-9, 9)/100000
    data = {

        "latitude": [47.556401+r, 47.55246+r, 47.51901+r],
        "longitude": [7.584576+r, 7.60572+r, 7.53976+r],
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
        st.session_state.user_space = "menu"
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


"""
def create_project(project_type, project_name, address, speckle_link, plz_ort, uploaded_files, baujahr, reno_jahr,
                   geb_lang, geb_breit, geb_hoch, mat_wand, mat_fen, mat_tur):
    # Ensure the /images directory exists
    if not os.path.exists('database/user_images'):
        os.makedirs('database/user_images')

    # Process and save files, storing their GUIDs
    file_guids = {}
    for file in uploaded_files:
        guid = str(uuid.uuid4())
        file_path = os.path.join('database/user_images', f'{guid}.jpg')  # Assuming all files are images
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        file_guids[file.name] = guid

    # Create the project data JSON structure
    project_data = {
        "PK": str(uuid.uuid4()),
        "metadata": {
            "author_type": "user",
            "author_name": st.session_state.username,
            "name": project_name,
            "projectType": project_type
        },
        "circ_data": {
            "address": {
                "full_address": address,
                "zip_code": plz_ort.split('/')[0].strip(),
                "city": plz_ort.split('/')[1].strip()
            },
            "time": {
                "year_built": baujahr,
                "last_renovation": reno_jahr,
                "expected_deconstruction": str(int(baujahr)+50)
            },
            "size": {
                "volume_m3": str(int(geb_lang)*int(geb_hoch)*int(geb_breit)),
                "length_m": geb_lang,
                "width_m": geb_breit,
                "height_m": geb_hoch
            },
            "materials": {
                "walls_type": mat_wand,
                "windows": mat_fen,
                "doors": mat_tur
            },
            "links": {
                "speckle": speckle_link
            }
        },
        "content": {
            "files": file_guids
        }
    }

    # Save the project data as JSON
    json_path = os.path.join('projects', f'{project_name.replace(" ", "_")}.json')
    if not os.path.exists('projects'):
        os.makedirs('projects')
    with open(json_path, 'w') as f:
        json.dump(project_data, f, indent=4)


def user_space():
    if st.session_state.user_space == "menu":
        st.subheader("meine Projekte")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Neubau EFH Eichenstrasse 45"):
                st.session_state.user_space = "construction"
        with col2:
            if st.button("Abbruch MFH Holzweg 13"):
                st.session_state.user_space = "deconstruction"
        with col3:
            if st.button("neues Projekt"):
                st.session_state.user_space = "new"

    elif st.session_state.user_space == "deconstruction":
        st.subheader("Abbruch MFH Holzweg 13")
        st.image(Image.open("images/abbruch.webp"), caption="Abbruch Mehrfamilienhaus")
        st.button("Informationen erfassen")
        file_downloader()
        if st.button("back"):
            st.session_state.user_space = "menu"

    elif st.session_state.user_space == "construction":
        st.subheader("Neubau EFH Eichenstrasse 45")
        st.image(Image.open("images/efh.webp"), caption="neues Einfamilienhaus rendering")
        st.button("InInformationen erfassen")
        if st.button("geeignete 'Materiallager' auf Karte anzeigen"):
            show_map()
        file_downloader()
        if st.button("back"):
            st.session_state.user_space = "menu"

    elif st.session_state.user_space == "new":
        st.subheader("Neues Projekt")
        project_type = st.radio("Projekttyp", ["Abbruch", "Neubau", "Umbau"])
        project_name = st.text_input("Projektname:")
        address = st.text_input("Strasse, Hausnummer")
        plz_ort = st.text_input("PLZ / Ort: (zwingend mit / trennen)")
        baujahr = st.text_input("Baujahr: [YYYY]")
        reno_jahr = st.text_input("letzte Renovierung Jahr: [YYYY]")
        geb_lang = st.text_input("Gebäudelänge: [m]")
        geb_breit = st.text_input("Gebäudebreite: [m]")
        geb_hoch = st.text_input("Gebäudehöhe: [m]")
        uploaded_files = st.file_uploader("Upload files, IFC, PDF-Pläne, Bilder, usw", accept_multiple_files=True)
        speckle_link = st.text_input("Speckle link: ")
        mat_wand = st.text_input("Material Wände: ")
        mat_fen = st.text_input("Fenster Material (HolzMetall, Holz, ...): ")
        mat_tur = st.text_input("Tür Materialisierung: ")

        if st.button("Process upload"):
            with st.spinner("Processing"):
                if uploaded_files:
                    create_project(project_type, project_name, address, speckle_link, plz_ort, uploaded_files,
                                   baujahr,
                                   reno_jahr, geb_lang, geb_breit, geb_hoch, mat_wand, mat_fen, mat_tur)
                    st.success("Upload successful")
                else:
                    st.error("Please upload at least one file.")
            st.session_state.user_space = "menu"

        if st.button("Back"):
            st.session_state.user_space = "menu"
"""


def mock_project_view_old():
    if st.session_state.user_space == "menu":

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Neubau EFH Eichenstrasse 45"):
                st.session_state.user_space = "construction"
        with col2:
            if st.button("Abbruch MFH Holzweg 13"):
                st.session_state.user_space = "deconstruction"
        with col3:
            if st.button("neues Projekt"):
                st.session_state.user_space = "new"

    elif st.session_state.user_space == "deconstruction":
        st.subheader("Abbruch MFH Holzweg 13")
        st.image(Image.open("images/abbruch.webp"), caption="Abbruch Mehrfamilienhaus")
        st.button("Informationen erfassen")
        file_downloader()
        if st.button("back"):
            st.session_state.user_space = "menu"

    elif st.session_state.user_space == "construction":
        st.subheader("Neubau EFH Eichenstrasse 45")
        st.image(Image.open("images/efh.webp"), caption="neues Einfamilienhaus rendering")
        st.button("InInformationen erfassen")
        if st.button("geeignete 'Materiallager' auf Karte anzeigen"):
            show_map()
        file_downloader()
        if st.button("back"):
            st.session_state.user_space = "menu"



if __name__ == "__main__":
    st.session_state.username = "BeispielBenutzer"  # Beispiel-Username für Demonstrationszwecke
    if 'user_space' not in st.session_state:
        st.session_state.user_space = "menu"
    user_space()
