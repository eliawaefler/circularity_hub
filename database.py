import streamlit as st
import json
import os
import uuid


def create_project(project_type, project_name, address, speckle_link, plz_ort, uploaded_files, baujahr, renojahr,
                   geb_lang, geb_breit, geb_hoch, mat_wand, mat_fen, mat_tur):
    # Ensure the /images directory exists
    if not os.path.exists('images'):
        os.makedirs('images')

    # Process and save files, storing their GUIDs
    file_guids = {}
    for file in uploaded_files:
        guid = str(uuid.uuid4())
        file_path = os.path.join('images', f'{guid}.jpg')  # Assuming all files are images
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        file_guids[file.name] = guid

    # Create the project data JSON structure
    project_data = {
        "PK": str(uuid.uuid4()),
        "metadata": {
            "authortype": "user",
            "authorname": st.session_state.username,
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
                "last_renovation": renojahr,
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


def main():
    if st.session_state.get("user_space", "new") == "new":
        st.subheader("Neues Projekt")
        project_type = st.radio("Projekttyp", ["Abbruch", "Neubau", "Umbau"])
        project_name = st.text_input("Projektname:")
        address = st.text_input("Strasse, Hausnummer")
        plz_ort = st.text_input("PLZ / Ort: (zwingend mit / trennen)")
        baujahr = st.text_input("Baujahr: [YYYY]")
        renojahr = st.text_input("letzte Renovierung Jahr: [YYYY]")
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
                    create_project(project_type, project_name, address, speckle_link, plz_ort, uploaded_files, baujahr,
                                   renojahr, geb_lang, geb_breit, geb_hoch, mat_wand, mat_fen, mat_tur)
                    st.success("Upload successful")
                else:
                    st.error("Please upload at least one file.")
            st.session_state.user_space = "menu"

        if st.button("Back"):
            st.session_state.user_space = "menu"

if __name__ == "__main__":
    if "username" not in st.session_state:
        st.session_state.username = "Testuser"
    if "user_space" not in st.session_state:
        st.session_state.user_space = "new"
    main()
