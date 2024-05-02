import streamlit as st
from texte import *
from PIL import Image
# import pandas as pd
# import pydeck as pdk
# im terminal: streamlit run app.py


def crop_webp_image(input_path, output_path, crop_box):
    # Load the image
    image = Image.open(input_path)

    # Crop the image using the crop_box
    cropped_image = image.crop(crop_box)

    # Save the cropped image
    cropped_image.save(output_path, 'WEBP')


def community_space():
    st.title("Community Space")
    st.write("Share your Ideas with your Community")

    # Define the CSS style for the container
    container_style = """
       <style>
           .styledContainer {
               background-color: #f0f0f0; /* Light grey background */
               border-radius: 10px;      /* Rounded corners */
               padding: 20px;            /* Padding around the content */
               margin: 10px 0;           /* Margin for some space around the container */
           }
       </style>
       """

    # CSS für die individuellen Beitragsboxen
    st.markdown("""
        <style>
        .box, .large {
            background-color: #f0f0f0;  /* Light gray background */
            padding: 20px;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;  /* Content at the top and tags at the bottom */
            margin-bottom: 20px;  /* Space between boxes */
        }
    
        .box {
            height: 250px;  /* Fixed height for smaller boxes */
        }
        </style>
        """, unsafe_allow_html=True)

    # Erstellen von Spalten für die Einträge
    col1, col2, col3 = st.columns(3)

    # Eintrag in der ersten Spalte
    with col1:
        st.markdown("""
            <div class='box'>
                <h4>Speckle</h4>
                <p>Informationen rund um den Workflow mit Speckle.</p>
                <p style='opacity: 0.6;'>#digitalezwillinge #bim #speckleintegration</p>
            </div>
            """, unsafe_allow_html=True)

    # Eintrag in der zweiten Spalte
    with col2:
        st.markdown("""
            <div class='box'>
                <h4>Best Practice</h4>
                <p>Anwendungsfälle der Community.</p>
                <p style='opacity: 0.6;'>#outofthebox #buildingsmart</p>
            </div>
            """, unsafe_allow_html=True)

    # Eintrag in der dritten Spalte
    with col3:
        st.markdown("""
            <div class='box'>
                <h4>Events</h4>
                <p>Seien dabei und lerne vieles Neues dazu!</p>
                <p style='opacity: 0.6;'>#community #learn #havefun #events</p>
            </div>
            """, unsafe_allow_html=True)

    # Eintrag von Planer
    with st.container(border=True):
        st.subheader("Integration von Second Hand Bauteilen in den Planungsprozess")
        col1, col2 = st.columns([1, 6])
        with col1:
            st.image("images/user_planer.webp")
            st.write("Dennis Draft")
            st.write("Planer")
        with col2:
            st.image("images/digital_twin.webp")
            st.write(planer_text)
            text_color = "grey"
            st.markdown(f"<p style='color: {text_color};'>#DigitaleZwillinge #BIM #SpeckleIntegration"
                        f"#automatisiertebauteilsuche</p>",
                        unsafe_allow_html=True)
    # Eintrag von Bauherrn
    with st.container(border=True):
        st.subheader("Strategische Planung für die Wiederverwendung von Bauteilen")
        col1, col2 = st.columns([1, 6])
        with col1:
            st.image("images/user_bauherr.webp")
            st.write("Beni Burkhalter")
            st.write("Bauherr")
        with col2:
            st.image("images/office.webp")
            st.write(bauherr_text)
            text_color = "grey"
            st.markdown(f"<p style='color: {text_color};'>#strategisch #neartoyou #nachhaltig</p>",
                        unsafe_allow_html=True)

    # Eintrag von Handwerker
    with st.container(border=True):
        st.subheader("Effizienzsteigerung durch präzise Bauteil-Identifikation im Handwerk")
        col1, col2 = st.columns([1, 6])
        with col1:
            st.image("images/user_handwerker.webp")
            st.write("Arnold Armstrong")
            with st.container():
                st.markdown('<div class="styledContainer">', unsafe_allow_html=True)
                st.write("Handwerker")
                st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.image("images/gtin.webp")
            st.write(handwerker_text)
            text_color = "grey"
            st.markdown(f"<p style='color: {text_color};'>#GTIN #workflow #zusammenarbeit</p>",
                        unsafe_allow_html=True)

    # Button zum Hinzufügen neuer Beiträge
    if st.button('Add New Post'):
        set_create_new_post()
        new_post()


def new_post():
    st.header("Create a new post")
    title = st.text_input("Type title, or paste a link here")
    category = st.selectbox("Select a category", ["Anwendungsfälle", "Workflow", "News"])
    # Tags functionality
    if 'tags' not in st.session_state:
        st.session_state.tags = []  # Initialize tags if not present
    new_tag = st.text_input("Add a tag", key="tag_input")
    if new_tag:
        st.session_state.tags.append(new_tag)  # Add new tag
        st.write(st.session_state.tags)  # Display tags
        st.session_state.tag_input = ''  # Reset input field

    content = st.text_area("Content", height=200)
    if st.button("Create post"):
        if title and category and content:
            st.success(f"post '{title}' created in '{category}' with tags {st.session_state.tags}.")
            # You might want to reset fields or handle the new topic (e.g., store it somewhere)
        else:
            st.error("Please fill out all fields to create a post.")


def set_create_new_post():
    st.session_state.create_new_post = True


def use_crop_images():
    input_image_path = 'images/avatars.webp'
    output_image_path = 'images/user_bauherr.webp'

    crop_box = (0, 0, 320, 1024)  # Example crop box: (left, upper, right, lower)
    crop_webp_image(input_image_path, output_image_path, crop_box)

    output_image_path = 'images/user_planer.webp'
    crop_box = (330, 0, 680, 1024)  # Example crop box: (left, upper, right, lower)
    crop_webp_image(input_image_path, output_image_path, crop_box)

    output_image_path = 'images/user_handwerker.webp'
    crop_box = (700, 0, 1024, 1024)  # Example crop box: (left, upper, right, lower)
    crop_webp_image(input_image_path, output_image_path, crop_box)
