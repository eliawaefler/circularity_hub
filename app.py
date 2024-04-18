import streamlit as st
import pandas as pd
import pydeck as pdk


def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", ("Home", "Map View", "File Upload/Download"))

    if choice == "Home":
        st.title("Home Page")
        st.write("Welcome to the example Streamlit application.")

    elif choice == "Map View":
        st.title("Map View")
        st.write("Map displaying highlighted locations.")
        show_map()

    elif choice == "File Upload/Download":
        st.title("File Upload and Download")
        st.write("Upload and download files.")
        file_uploader()
        file_downloader()


def show_map():
    # Sample data: Latitude and Longitude of some cities
    data = {
        "latitude": [34.0522, 36.1699, 40.7128],
        "longitude": [-118.2437, -115.1398, -74.0060],
        "city": ["Los Angeles", "Las Vegas", "New York"]
    }
    df = pd.DataFrame(data)

    # Create a map using the data
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=3.5,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=df,
                get_position='[longitude, latitude]',
                radius=200000,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
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
