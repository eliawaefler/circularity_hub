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
        st.title("Home Page")
        st.write("Welcome to the example Streamlit application.")
    elif choice == "Map View":
        st.title("Map View")
        st.write("Map displaying highlighted locations.")
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
            st.session_state.userpw = st.text_input("password", on_change=set_username)

    elif choice == "Community":
        st.title("Community Space")
        st.write("Share your Ideas with your Community")


def show_map():
    # Sample data: Latitude and Longitude of some cities
    data = {
        "latitude": [47.559601, 47.55576, 47.519601],
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
