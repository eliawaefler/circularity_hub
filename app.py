import streamlit as st
import pandas as pd
import pydeck as pdk
# im terminal: streamlit run app.py


def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", ("Home", "Map View", "UserSpace","Community"))
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "userpw" not in st.session_state:
        st.session_state.userpw = False

    def set_username():
        st.session_state.userpw = True

    if choice == "Home":
        st.title("Circularity Hub")
        st.write("Die Plattform für zirkuläres Bauen.")
    elif choice == "Map View":
        st.title("Map View")
        st.write("Die besten Materiallager für dein Projekt.")
        show_map()

    elif choice == "UserSpace":

        st.title(f"welcome {st.session_state.username}")
        if st.session_state.userpw:
            st.title("meine Projekte")
            st.write("Upload and download files.")
            file_uploader()
            file_downloader()
        else:
            st.session_state.username = st.text_input("username")
            st.session_state.userpw = st.text_input("password", type="password", on_change=set_username)

    elif choice == "Community":
        community_space()
        new_topic()

def add_tag():
    new_tag = st.session_state.tag_input
    if new_tag:  # Check if the input is not empty
        if 'tags' not in st.session_state:
            st.session_state.tags = [new_tag]
        else:
            st.session_state.tags.append(new_tag)
        st.session_state.tag_input = ''  # Clear the input box after adding

def community_space():

    st.title("Community Space")
    st.write("Share your Ideas with your Community")

    # Erstellen von Spalten für die Einträge
    col1, col2, col3 = st.columns(3)

    # Eintrag in der ersten Spalte
    with col1:
        st.subheader("Community Garden")
        st.write("A community garden with spaces for everyone to plant.")
        st.caption("Tags: #gardening #community #green")

    # Eintrag in der zweiten Spalte
    with col2:
        st.subheader("Sports Day")
        st.write("Weekly community sports day to promote health and wellbeing.")
        st.caption("Tags: #health #sports #weekly")

    # Eintrag in der dritten Spalte
    with col3:
        st.subheader("Book Swap")
        st.write("A monthly book swap event in our local library.")
        st.caption("Tags: #books #library #swap")

def new_topic():
    st.header("Create a new Topic")
    title = st.text_input("Type title, or paste a link here")
    category = st.selectbox("Select a category", ["Category 1", "Category 2", "Category 3"])

    # Tags functionality
    if 'tags' not in st.session_state:
        st.session_state.tags = []  # Initialize tags if not present
    new_tag = st.text_input("Add a tag", key="tag_input")
    if new_tag:
        st.session_state.tags.append(new_tag)  # Add new tag
        st.write(st.session_state.tags)  # Display tags
        st.session_state.tag_input = ''  # Reset input field

    content = st.text_area("Content", height=200)
    if st.button("Create Topic"):
        if title and category and content:
            st.success(f"Topic '{title}' created in '{category}' with tags {st.session_state.tags}.")
            # You might want to reset fields or handle the new topic (e.g., store it somewhere)
        else:
            st.error("Please fill out all fields to create a topic.")

def show_map():
    # Sample data: Latitude and Longitude of some cities
    data = {
        "latitude": [47.559401, 47.55546, 47.519401],
        "longitude": [7.588576, 7.60522, 7.518576],
        "city": ["1", "2", "3"],
        "citydata": ["Industriestrasse 48: Score=0.971", "Althausstrasse 11: Score=0.921", "Kreutzweg 3: Score=0.913"]
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

if __name__ == "__main__":
    main()
